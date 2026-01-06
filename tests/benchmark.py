# src/benchmark.py

import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import tiktoken
from src.handler import DocGenerator

def run_benchmark():
    sample_diff = """
    diff --git a/app.py b/app.py
    index 832a..b212 100644
    --- a/app.py
    +++ b/app.py
    @@ -10,4 +10,5 @@ def hello():
         print("Hello World")
    +    print("New Feature Added")
    """
    
    print("=== 벤치마크 시작 ===")
    
    # 토큰 계산
    enc = tiktoken.encoding_for_model("gpt-4o")
    input_tokens = len(enc.encode(sample_diff))
    print(f"[*] 입력 토큰 수: {input_tokens}")

    # 실행 시간 측정
    start_time = time.time()
    
    generator = DocGenerator()
    result = generator.generate_docs(sample_diff)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    output_tokens = len(enc.encode(result))
    
    print(f"[*] 소요 시간: {elapsed_time:.2f}초")
    print(f"[*] 출력 토큰: {result}")
    print(f"[*] 출력 토큰 수: {output_tokens}")
    print("=== 벤치마크 종료 ===")

if __name__ == "__main__":
    run_benchmark()