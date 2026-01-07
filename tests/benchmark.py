# src/benchmark.py

import time
import os
import sys
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.handler import DocGenerator
from dataset import TEST_DATASET

def run_benchmark():
    print("=== 벤치마크 시작 ===")
    try:
        generator = DocGenerator()
    except Exception as e:
        print(f"Generator 초기화 실패: {e}")
        return

    # output 폴더 없을 경우 대비
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)

    total_time = 0.0
    total_output_tokens = 0
    total_api_tokens = 0
    
    test_count = len(TEST_DATASET)
    details_log = []

    for data in TEST_DATASET:
        sample_diff = data['diff']
        ground_truth = data['ground_truth']
        case_id = data['id']
        
        # 실행 시간 측정
        start_time = time.time()        
        result = generator.generate_docs(sample_diff)
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        model_output = result["text"]
        usage = result["usage"]        
        output_tokens = usage["output_tokens"]
        total_tokens = usage["total_tokens"]
        
        # 통계 누적
        total_time += elapsed_time
        total_output_tokens += output_tokens
        total_api_tokens += total_tokens

        log_entry = (
            f"[{case_id}] time : {elapsed_time:.2f}s "
            f"/ output token : {output_tokens} (total charged: {total_tokens})\n"
            f"[model]\n{model_output}\n\n"
            f"[ground truth]\n{ground_truth}\n"
            f"{'-' * 40}"
        )
        
        details_log.append(log_entry)        
        print(f"[{case_id}] time : {elapsed_time:.2f}s / output token : {output_tokens}")

    # Summary
    avg_time = total_time / test_count if test_count > 0 else 0
    avg_output_tokens = total_output_tokens / test_count if test_count > 0 else 0
    avg_total_tokens = total_api_tokens / test_count if test_count > 0 else 0

    summary_text = (
        "====== summary =====\n"
        f"total time : {total_time:.2f}s / avg time : {avg_time:.2f}s\n"
        f"avg output token : {avg_output_tokens:.1f} (answer length)\n"
        f"avg total token  : {avg_total_tokens:.1f} (billed amount)\n\n"
        "===== details =====\n"
    )

    # 파일 저장
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