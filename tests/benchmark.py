# src/benchmark.py

import time
import os
import sys
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.handler import DocGenerator
from dataset import TEST_DATASET

def count_tokens_safe(generator, text):
    return generator.count_tokens(text)

def run_benchmark():
    print("=== 벤치마크 시작 ===")
    try:
        generator = DocGenerator()
    except Exception as e:
        print(f"Generator 초기화 실패: {e}")
        return

    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    total_time = 0.0
    total_tokens = 0
    test_count = len(TEST_DATASET)
    details_log = []

    for data in TEST_DATASET:
        sample_diff = data['diff']
        ground_truth = data['ground_truth']
        case_id = data['id']
        
        # 실행 시간 측정
        start_time = time.time()
        
        try:
            model_output = generator.generate_docs(sample_diff)
        except Exception as e:
            model_output = f"Error: {e}"

        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # 토큰 수 계산
        output_tokens = count_tokens_safe(generator, model_output)
        
        # 통계 누적
        total_time += elapsed_time
        total_tokens += output_tokens

        log_entry = (
            f"[{case_id}] time : {elapsed_time:.2f}s / token : {output_tokens}\n"
            f"[model]\n{model_output}\n\n"
            f"[ground truth]\n{ground_truth}\n"
            f"{'-' * 40}"
        )
        
        details_log.append(log_entry)
        print(f"[{case_id}] time : {elapsed_time:.2f}s / token : {output_tokens}\n")

    # Summary
    avg_time = total_time / test_count if test_count > 0 else 0
    avg_tokens = total_tokens / test_count if test_count > 0 else 0

    summary_text = (
        "====== summary =====\n"
        f"total time : {total_time:.2f}s / avg time : {avg_time:.2f}s\n"
        f"total token : {total_tokens} / avg token : {avg_tokens:.1f}\n\n"
        "===== details =====\n"
    )

    current_time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{current_time_str}.txt"
    file_path = os.path.join(output_dir, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(summary_text)
        f.write("\n".join(details_log))

    print(f"\n[ result path ]: {file_path}")
    print("=== 벤치마크 종료 ===")

if __name__ == "__main__":
    run_benchmark()