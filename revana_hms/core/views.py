from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
from django.core.cache import cache
from core.models import SearchKeyword
from hospitals.models import Hospital, Department, Treatment
from doctors.models import Doctor
try:
    from core.semantic_search import SemanticSearchService
except ImportError:
    SemanticSearchService = None

# Static Synonym Dictionary (Strategy 2)
SYNONYM_MAP = {
    "heart attack": "cardiology",
    "sugar": "endocrinology",
    "tooth pain": "dentistry",
    "skin rash": "dermatology",
    "hair fall": "dermatology",
    "bone fracture": "orthopedic",
    "kids": "pediatrics",
}

@api_view(['GET'])
@permission_classes([AllowAny]) # Making it public for mobile search if needed, or stick to IsAuthenticated
def test_auth(request):
    return Response(
        {
            "message": "Token is Valid",
            "user": str(request.user),
            "user_id": request.user.id 
        }
    )

@api_view(['GET'])
@permission_classes([AllowAny])
def universal_search(request):
    """
    Universal Search API for Mobile
    Strategies:
    1. Input Normalization (Synonyms)
    2. Location Filtering (City)
    3. Partial Matching (icontains)
    4. Caching
    """
    query = request.GET.get('query', '').lower().strip()
    city = request.GET.get('city', '').lower().strip()
    
    if not query:
        return Response({"doctors": [], "hospitals": []})

    # Strategy 4: Caching
    cache_key = f"search:{city}:{query}"
    cached_results = cache.get(cache_key)
    if cached_results:
       return Response(cached_results)

    # Strategy 2 & 3: Synonym Mapping
    # First check static dictionary
    normalized_query = SYNONYM_MAP.get(query, query)
    
    # Then check Admin-Editable Synonyms (Strategy 3)
    # If the normalized query is still the original distinct from mapped, check DB
    # Or just check DB for the normalized query if it matches a keyword
    try:
        db_synonym = SearchKeyword.objects.filter(keyword__iexact=normalized_query).first()
        if db_synonym:
            normalized_query = db_synonym.mapped_term.lower()
    except Exception:
        pass # Fallback to ignore DB errors if any

    # Strategy 0: Semantic Search (MiniLM)
    # If pure keyword search might fail, try to find a semantic match
    semantic_match = None
    if SemanticSearchService:
        try:
            service = SemanticSearchService.get_instance()
            # Only use if query is not very short
            if len(query) > 3:
                 semantic_match = service.get_best_match(query)
        except Exception as e:
            print(f"Semantic Search Error: {e}")

    # Strategy 1: Search Logic
    
    # 1. Filter Hospitals by City first (if provided)
    hospital_filter = Q(is_approved=True) # Basic filter
    if city:
        hospital_filter &= Q(city__icontains=city)
        
    matching_hospitals_queryset = Hospital.objects.filter(hospital_filter)
    
    # 2. Search for Hospitals matching query (Department or Name)
    # User said "only shows doctors and hospitals"
    # Logic: Hospital matches if its name matches OR it has a department matching query
    
    hospital_search_results = matching_hospitals_queryset.filter(
        Q(name__icontains=normalized_query) |
        Q(departments__name__icontains=normalized_query) |
        (Q(departments__name__icontains=semantic_match) if semantic_match else Q())
    ).distinct()

    # 3. Search for Doctors
    # Doctors must belong to the hospitals in the filtered city
    # Doctor matches if name matches OR specialization matches OR treatments match
    
    doctors_queryset = Doctor.objects.filter(
        hospital__in=matching_hospitals_queryset,
        is_approved=True 
    ).filter(
        Q(name__icontains=normalized_query) |
        Q(specialization__icontains=normalized_query) |
        Q(treatments__name__icontains=normalized_query) |
         (Q(specialization__icontains=semantic_match) | Q(treatments__name__icontains=semantic_match) if semantic_match else Q())
    ).distinct()

    # Format Results
    hospitals_data = []
    for h in hospital_search_results:
        hospitals_data.append({
            "id": h.id,
            "name": h.name,
            "city": h.city,
            "type": "hospital",
            "action": "Visit"
        })

    doctors_data = []
    for d in doctors_queryset:
        doctors_data.append({
            "id": d.id,
            "name": d.name,
            "specialization": d.specialization,
            "hospital_name": d.hospital.name,
            "type": "doctor",
            "action": "Book"
        })

    results = {
        "doctors": doctors_data,
        "hospitals": hospitals_data
    }

    # Cache results for 5 minutes (300 seconds)
    cache.set(cache_key, results, timeout=300)

    return Response(results)
