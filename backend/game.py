try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    
    # Load model once (will cache)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def calculate_similarity(word1, word2):
        """Calculate semantic similarity between two words"""
        try:
            embeddings = model.encode([word1, word2])
            similarity = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )
            return float(similarity)
        except:
            return fallback_similarity(word1, word2)
            
except ImportError:
    def calculate_similarity(word1, word2):
        return fallback_similarity(word1, word2)

def fallback_similarity(word1, word2):
    """Fallback similarity calculation"""
    if word1 == word2:
        return 1.0
    
    set1, set2 = set(word1), set(word2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    if union == 0:
        return 0.0
    
    return intersection / union

def evaluate_guess(guess, target):
    """Evaluate a guess against the target word"""
    if guess == target:
        return "Perfect!", "🔥🔥🔥", 1.0, True, "exact"
    
    similarity = calculate_similarity(guess, target)
    
    if similarity >= 0.8:
        return "On Fire!", "🔥🔥", similarity, False, "hot"
    elif similarity >= 0.6:
        return "Getting Warmer", "🌡️", similarity, False, "warm"
    elif similarity >= 0.4:
        return "Cool", "❄️", similarity, False, "cool"
    else:
        return "Freezing", "🧊", similarity, False, "cold"
