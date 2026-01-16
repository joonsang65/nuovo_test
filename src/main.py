# src/main.py

import argparse
import os
from handler import get_git_diff, DocGenerator, ReadmeGenerator 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="HEAD^", help="Base commit SHA")
    parser.add_argument("--head", default="HEAD", help="Head commit SHA")
    args = parser.parse_args()

    print(f"[*] Diff 추출 중... ({args.base} ... {args.head})")
    diff_content = get_git_diff(args.base, args.head)

    print("[*] README 업데이트 중 (GEMINI)...")
    
    readme_path = "README.md"
    current_readme = ""
    
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            current_readme = f.read()
    else:
        print("[!] README.md가 없어 새로 생성합니다.")
        current_readme = "# New Project"

    updater = ReadmeGenerator()
    result = updater.update_readme(diff_content, current_readme)
    
    if "error" not in result:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        print(f"[SUCCESS] {readme_path} 업데이트 완료")
        
        usage = result.get("usage")
        if usage:
             print(f"[*] 토큰 사용량: 합계 {usage.get('total_tokens')}")
    else:
        print(f"[ERROR] README 업데이트 실패: {result['error']}")


    ### docs generator는 일단 주석 처리 해둠
    """
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
    """

if __name__ == "__main__":
    main()