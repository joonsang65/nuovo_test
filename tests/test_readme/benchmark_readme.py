# tests/test_readme/benchmark_readme.py

import time
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from src.handler import ReadmeUpdater
from src.config import Config
from utils import calculate_semantic_recall
import dataset_readme

load_dotenv()

def run_readme_benchmark(test_dataset):
    print("=== README 벤치마크 시작 ===")
    
    try:
        updater = ReadmeUpdater()
        client = updater.client
    except Exception as e:
        print(f"Updater 초기화 실패: {e}")
        return

    output_dir = os.path.join(os.path.dirname(__file__), 'output_readme')
    os.makedirs(output_dir, exist_ok=True)

    total_time = 0.0
    total_score = 0.0
    total_output_tokens = 0
    
    test_count = len(test_dataset)
    details_log = []

    for data in test_dataset:
        case_id = data['id']
        sample_diff = data['diff']
        current_readme = data.get('current_readme', "# Default Project Title")
        ground_truth = data['ground_truth']
        
        # ReadmeUpdater 호출
        start_time = time.time()
        result = updater.update_readme(sample_diff, current_readme)
        elapsed_time = time.time() - start_time
        
        model_output = result.get("text", "")
        usage = result.get("usage", {})
        
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

        missing_str = ", ".join(missing) if missing else "Perfect Coverage"
        
        log_entry = (
            f"[{case_id}] Recall Score: {score:.4f} / Time: {elapsed_time:.2f}s\n"
            f"[Missings]: {missing_str}\n"
            f"[Ground Truth]: {ground_truth}\n"
            f"{'-' * 40}\n"
            f"[Updated README Head]\n{model_output[:300]}...\n"
            f"{'=' * 40}"
        )
        
        details_log.append(log_entry)        
        print(f"[{case_id}] Score: {score:.4f} / Time: {elapsed_time:.2f}s")

    # summary
    if test_count > 0:
        avg_score = total_score / test_count
        avg_time = total_time / test_count
        avg_output_tokens = total_output_tokens / test_count
    else:
        avg_score = avg_time = avg_output_tokens = 0

    summary_text = (
        "====== Summary ======\n"
        f"Total Samples     : {test_count}\n"
        f"Avg Semantic Recall: {avg_score:.4f} (Target: 1.0)\n"
        f"Avg Time          : {avg_time:.2f}s\n"
        f"Avg Output Tokens : {avg_output_tokens:.1f}\n\n"
        "===== Details =====\n"
    )

    current_time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{current_time_str}.txt"
    file_path = os.path.join(output_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(summary_text)
        f.write("\n".join(details_log))

    print(f"[Avg Recall]: {avg_score:.4f}")
    print(f"[Result Saved]: {file_path}")
    print("=== 벤치마크 종료 ===")

if __name__ == "__main__":
    test_dataset = dataset_readme.TEST_DATASET
    
    start_time = time.time()
    run_readme_benchmark(test_dataset)
    print(f'Total benchmark test time : {time.time() - start_time:.2f}')