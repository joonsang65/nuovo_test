# tests/test_docs/benchmark.py

import time
import os
import sys
import re
import numpy as np
from datetime import datetime
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src.handler import DocGenerator
import dataset_easy_docs as dataset_easy_docs
import dataset_normal_docs as dataset_normal_docs
load_dotenv()

# 불필요하게 acc 하락 방지용 stop word 설정
STOP_WORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
    'of', 'with', 'by', 'as', 'it', 'this', 'that', '은', '는', '이', '가', '을', '를', '의', '에', '와', '과', '한', '하다'
}

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
            print(f"Warning: Failed to embed word '{word}': {e}")
            embeddings[word] = np.zeros(768) # 에러 시 0 벡터 처리
            
    return embeddings

def compute_max_similarity(target_vec, comparison_vectors):
    if not comparison_vectors:
        return 0.0
    comp_matrix = np.array(comparison_vectors)
    dot_products = np.dot(comp_matrix, target_vec)
    norms = np.linalg.norm(comp_matrix, axis=1) * np.linalg.norm(target_vec)
    
    # ZeroDivisionError 방지를 위함
    similarities = np.divide(dot_products, norms, out=np.zeros_like(dot_products), where=norms!=0)
    
    return np.max(similarities)

def calculate_semantic_recall(client, ground_truth, model_output, threshold=0.85):
    gt_tokens = tokenize(ground_truth)
    out_tokens = tokenize(model_output)
    
    if not gt_tokens:
        return 0.0, []
        
    if not out_tokens:
        return 0.0, list(gt_tokens)

    # 일치 단어 먼저 제거 - 완전 일치하는 단어는 제외하는 게 token 사용량 절약 가능함
    exact_matches = gt_tokens.intersection(out_tokens)
    remaining_gt_tokens = gt_tokens - exact_matches

    # 전부 똑같을 경우 -> recall = 1.0    
    if not remaining_gt_tokens:
        print('all same')
        return 1.0, []

    # 임베딩 기반 의미 비교 수행 - Ground Truth의 남은 단어 임베딩
    gt_embeddings = get_word_embeddings(client, list(remaining_gt_tokens))
    
    out_embeddings = get_word_embeddings(client, list(out_tokens))
    out_vectors = list(out_embeddings.values())
    
    semantic_matches = set()
    missing_tokens = set()

    # 유사도 판단 - 0.85 이상일 경우에만 추가
    for gt_word in remaining_gt_tokens:
        gt_vec = gt_embeddings.get(gt_word)
        max_sim = compute_max_similarity(gt_vec, out_vectors)
        
        if max_sim >= threshold:
            semantic_matches.add(gt_word)
        else:
            missing_tokens.add(gt_word)
            
    # 일치 단어 + 의미 유사 단어 합치기
    total_matches = len(exact_matches) + len(semantic_matches)
    score = total_matches / len(gt_tokens)
    
    return score, list(missing_tokens)

def run_benchmark(test_dataset):
    print("=== 벤치마크 시작 ===")
    
    try:
        generator = DocGenerator()
        client = generator.client
    except Exception as e:
        print(f"Generator 초기화 실패: {e}")
        return

    output_dir = os.path.join(os.path.dirname(__file__), 'output_docs')
    os.makedirs(output_dir, exist_ok=True)

    total_time = 0.0
    total_score = 0.0
    total_output_tokens = 0
    total_api_tokens = 0
    
    test_count = len(test_dataset)
    details_log = []

    for data in test_dataset:
        case_id = data['id']
        sample_diff = data['diff']
        ground_truth = data['ground_truth']
        
        # 문서 생성
        start_time = time.time()        
        result = generator.generate_docs(sample_diff)
        elapsed_time = time.time() - start_time
        
        model_output = result["text"]
        usage = result["usage"]
        
        # Semantic Recall 평가
        score, missing = calculate_semantic_recall(client, ground_truth, model_output)
        
        total_time += elapsed_time
        total_score += score
        total_output_tokens += usage.get("output_tokens", 0)
        total_api_tokens += usage.get("total_tokens", 0)

        missing_str = ", ".join(missing) if missing else "Perfect Coverage"
        
        log_entry = (
            f"[{case_id}] Recall Score: {score:.4f} / Time: {elapsed_time:.2f}s\n"
            f"[Missings]: {missing_str}\n"
            f"[Model Output]\n{model_output}\n\n"
            f"[Ground Truth]\n{ground_truth}\n"
            f"{'-' * 40}"
        )
        
        details_log.append(log_entry)        
        print(f"[{case_id}] Score: {score:.4f} / Time: {elapsed_time:.2f}s")

    # Summary
    if test_count > 0:
        avg_score = total_score / test_count
        avg_time = total_time / test_count
        avg_output_tokens = total_output_tokens / test_count
        avg_total_tokens = total_api_tokens / test_count
    else:
        avg_score = avg_time = avg_output_tokens = avg_total_tokens = 0

    summary_text = (
        "====== Summary ======\n"
        f"Total Samples     : {test_count}\n"
        f"Avg Semantic Recall: {avg_score:.4f} (Target: 1.0)\n"
        f"Avg Time          : {avg_time:.2f}s\n"
        f"Avg Output Tokens : {avg_output_tokens:.1f}\n"
        f"Avg Total Tokens  : {avg_total_tokens:.1f}\n\n"
        "===== Details =====\n"
    )

    current_time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{current_time_str}.txt"
    file_path = os.path.join(output_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(summary_text)
        f.write("\n".join(details_log))

    print(f"[Avg Recall]: {avg_score:.4f}")
    print("=== 벤치마크 종료 ===")

if __name__ == "__main__":
    DATASET_MAP = {
    "easy": dataset_easy_docs.TEST_DATASET,
    "normal": dataset_normal_docs.TEST_DATASET
    }
    while True:
        mode = input("Choose mode [ easy / normal ] : ").lower()
        if mode in DATASET_MAP:
            test_dataset = DATASET_MAP[mode]
            break
        print("Wrong input")

    start_time = time.time()
    run_benchmark(test_dataset)

    print(f'Total benchmark test time : {time.time() - start_time:.2f}')