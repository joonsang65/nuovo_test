# src/benchmark.py

import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    from src.handler import DocGenerator
except ImportError:
    print("모듈을 찾을 수 없습니다. 경로를 확인하세요.")
    sys.exit(1)
from dataset import TEST_DATASET

def count_tokens_safe(generator, text):
    """
    Generator에 count_tokens가 있으면 쓰고, 없으면 길이로 대략 추산합니다.
    """
    if hasattr(generator, 'count_tokens'):
        return generator.count_tokens(text)
    else:
        return len(text) // 3

def run_benchmark():
    print("=== 벤치마크 시작 ===")
    print("-" * 80)
    print(f"{'ID':<4} | {'소요시간':<8} | {'토큰수':<6} | {'실제 답변 (Ground Truth)':<30} | {'모델 답변 (Model Output)'}")
    print("-" * 80)

    try:
        generator = DocGenerator()
    except Exception as e:
        print(f"Generator 초기화 실패: {e}")
        return

    for data in TEST_DATASET:
        sample_diff = data['diff']
        ground_truth = data['ground_truth']
        
        # 실행 시간
        start_time = time.time()
        
        try:
            model_output = generator.generate_docs(sample_diff)
        except Exception as e:
            model_output = f"Error: {e}"

        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # 토큰 수 계산
        output_tokens = count_tokens_safe(generator, model_output)
        
        clean_output = model_output.replace('\n', ' ').strip()[:50] + "..." # 너무 길면 자름
        
        print(f"[{data['id']}] {elapsed_time:.2f}s / {output_tokens} tokens")
        print(f" ㄴ 모델: {clean_output}")
        print(f" ㄴ 정답: {ground_truth}")
        print("-" * 40)

    print("=== 벤치마크 종료 ===")

if __name__ == "__main__":
    if TEST_DATASET[0] == ...:
        print("스크립트 내에 TEST_DATASET을 채워주세요!")
    else:
        run_benchmark()