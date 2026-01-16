# tests/test_docs/benchmark.py

import time
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.handler import DocGenerator
from src.config import Config
from utils import calculate_semantic_recall
import dataset_easy_docs
import dataset_normal_docs

load_dotenv()

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
        
        # docs 생성
        start_time = time.time()        
        result = generator.generate_docs(sample_diff)
        elapsed_time = time.time() - start_time
        
        model_output = result["text"]
        usage = result["usage"]
        
        # 평가
        score, missing = calculate_semantic_recall(
            client, 
            ground_truth, 
            model_output, 
            threshold=Config.SEMANTIC_RECALL_THRESHOLD
        )
        
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