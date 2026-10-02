# PharmEasy Regional Pulse - Review Quality Gate

def review_gate(review_text: str, rating: int, language: str = "en"):
    """
    Filters low quality / fake reviews
    """
    if not review_text or len(review_text.strip()) < 5:
        return False, "Too short"
    
    # Block spam words
    spam_words = ["fake", "free money", "click here", "buy now"]
    if any(word in review_text.lower() for word in spam_words):
        return False, "Spam detected"
    
    # Rating vs text check
    if rating <= 2 and len(review_text) < 10:
        return False, "Low effort negative review"
    
    return True, "Approved"

# Test
if __name__ == "__main__":
    print(review_gate("Very good service, fast delivery", 5))
    print(review_gate("ok", 1))
