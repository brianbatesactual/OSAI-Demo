from sentence_transformers import SentenceTransformer, util

# Load SBERT once
_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_similarity_score(sentence1, sentence2):
    embeddings = _model.encode([sentence1, sentence2], convert_to_tensor=True)
    score = util.cos_sim(embeddings[0], embeddings[1])
    return round(score.item(), 4)
