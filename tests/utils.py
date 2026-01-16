# tests/utils.py

import re
import numpy as np

# -------------------------
#   CONFIG
# -------------------------

THRESHOLD = 0.85

STOP_WORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
    'of', 'with', 'by', 'as', 'it', 'this', 'that', '은', '는', '이', '가', '을', '를', '의', '에', '와', '과', '한', '하다'
}

# -------------------------
#   CALC FUNC
# -------------------------

def tokenize(text):
    if not text:
        return set()
    words = re.findall(r'[a-zA-Z0-9가-힣]{2,}', text.lower())
    return set(w for w in words if w not in STOP_WORDS)

def get_word_embeddings(client, words, model="models/text-embedding-004"):
    if not words:
        return {}
    
    embeddings = {}
    for word in words:
        try:
            result = client.models.embed_content(
                model=model,
                contents=word
            )
            embeddings[word] = np.array(result.embeddings[0].values)
        except Exception as e:
            embeddings[word] = np.zeros(768)
            
    return embeddings

def compute_max_similarity(target_vec, comparison_vectors):
    if not comparison_vectors:
        return 0.0
    comp_matrix = np.array(comparison_vectors)
    dot_products = np.dot(comp_matrix, target_vec)
    norms = np.linalg.norm(comp_matrix, axis=1) * np.linalg.norm(target_vec)
    
    similarities = np.divide(dot_products, norms, out=np.zeros_like(dot_products), where=norms!=0)
    return np.max(similarities)

def calculate_semantic_recall(client, ground_truth, model_output, threshold=THRESHOLD):
    """
    Ground Truth(핵심 내용)가 Model Output에 포함되었는지 검사
    """
    gt_tokens = tokenize(ground_truth)
    out_tokens = tokenize(model_output)
    
    if not gt_tokens:
        return 0.0, []
    if not out_tokens:
        return 0.0, list(gt_tokens)

    exact_matches = gt_tokens.intersection(out_tokens)
    remaining_gt_tokens = gt_tokens - exact_matches

    if not remaining_gt_tokens:
        return 1.0, []

    # 임베딩 비교
    gt_embeddings = get_word_embeddings(client, list(remaining_gt_tokens))
    out_embeddings = get_word_embeddings(client, list(out_tokens))
    out_vectors = list(out_embeddings.values())
    
    semantic_matches = set()
    missing_tokens = set()

    for gt_word in remaining_gt_tokens:
        gt_vec = gt_embeddings.get(gt_word)
        max_sim = compute_max_similarity(gt_vec, out_vectors)
        
        if max_sim >= threshold:
            semantic_matches.add(gt_word)
        else:
            missing_tokens.add(gt_word)
            
    total_matches = len(exact_matches) + len(semantic_matches)
    score = total_matches / len(gt_tokens)
    
    return score, list(missing_tokens)