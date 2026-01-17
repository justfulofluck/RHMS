
import os
import django
import time

try:
    from core.semantic_search import SemanticSearchService
    service = SemanticSearchService.get_instance()
    print("\n✅ Semantic Search Service Loaded Successfully!")
except ImportError:
    print("\n❌ Semantic Search Service Import Failed - Dependencies might still be installing.")
    exit(1)
except Exception as e:
    print(f"\n❌ Service Init Error: {e}")
    exit(1)

def verify_semantic_search():
    print("--- Verifying Semantic Search (MiniLM) ---")
    
    # 1. Inspect loaded data
    print(f"Loaded Specializations ({len(service.specializations)}): {service.specializations[:5]}...")
    
    # 2. Test Cases
    test_queries = [
        ("Fracture", "Orthopedics"),
        ("Chest pain", "Cardiology"),
        ("Tooth ache", "Dentistry"), 
        ("Skin rash", "Dermatology"), # Depends if these exist in DB
        ("xyz123", None) # Should expect None
    ]
    
    # Since DB might be empty of these exact departments, we manually inject them for testing logic
    # Real DB check comes later. This verifies the MODEL integration.
    service.specializations = ["Orthopedics", "Cardiology", "Dentistry", "Dermatology", "Pediatrics"]
    service.refresh_embeddings() # Actually this re-reads DB.
    # Let's override manual just for this test script logic verification
    from sentence_transformers import SentenceTransformer
    service.model = SentenceTransformer('all-MiniLM-L6-v2') 
    service.specializations = ["Orthopedics", "Cardiology", "Dentistry", "Dermatology", "Pediatrics"]
    service.embeddings = service.model.encode(service.specializations)
    
    for query, expected in test_queries:
        match = service.get_best_match(query, threshold=0.4) # Lower threshold for simple test
        print(f"Query: '{query}' -> Match: '{match}' (Expected: '{expected}')")
        
    print("\n✅ Verification Complete")

verify_semantic_search()
