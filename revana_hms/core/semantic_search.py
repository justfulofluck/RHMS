from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.conf import settings
from hospitals.models import Department, Treatment

class SemanticSearchService:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def __init__(self):
        # Load lightweight model optimized for speed
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.specializations = []
        self.embeddings = None
        self.refresh_embeddings()
        
    def refresh_embeddings(self):
        """
        Loads all Departments and Treatments from DB and precomputes embeddings.
        Call this on startup or periodically.
        """
        # Fetch dynamic list from DB
        departments = list(Department.objects.values_list('name', flat=True).distinct())
        treatments = list(Treatment.objects.values_list('name', flat=True).distinct())
        
        # Combine unique terms
        self.specializations = list(set(departments + treatments))
        
        # Add some manual medical mappings if needed
        # self.specializations.extend(["General Physician", "Pediatrics"])
        
        if self.specializations:
            self.embeddings = self.model.encode(self.specializations)
        else:
            self.embeddings = None
        
    def get_best_match(self, query, threshold=0.6):
        """
        Returns the best matching specialization/treatment for a natural language query.
        """
        if not self.embeddings is not None and len(self.specializations) > 0:
            return None
            
        query_vec = self.model.encode([query])
        scores = cosine_similarity(query_vec, self.embeddings)[0]
        best_idx = np.argmax(scores)
        
        if scores[best_idx] > threshold:
            return self.specializations[best_idx]
        return None
