# src/main.py

import argparse
from handler import get_git_diff, DocGenerator

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="HEAD^", help="Base commit SHA")
    parser.add_argument("--head", default="HEAD", help="Head commit SHA")
    args = parser.parse_args()

    print(f"[*] Diff 추출 중... ({args.base} ... {args.head})")
    diff_content = get_git_diff(args.base, args.head)
    
    if len(diff_content) > 10000:
        print("[!] Diff가 너무 깁니다. 앞부분만 사용합니다.")
        diff_content = diff_content[:10000]

    print("[*] 문서 생성 중 (GEMINI)...")
    generator = DocGenerator()
    result = generator.generate_docs(diff_content)
    docs_text = result["text"]
    usage = result["usage"]

    output_path = "generated_docs.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(docs_text)
    
    print(f"[SUCCESS] 문서가 생성되었습니다: {output_path}")
    
    if usage:
        print(f"[*] 토큰 사용량: 입력 {usage.get('prompt_tokens')} / 출력 {usage.get('output_tokens')} / 합계 {usage.get('total_tokens')}")
    
    print("-" * 20)
    print(docs_text)

if __name__ == "__main__":
    main()