# src/handler.py

import subprocess
import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

def get_git_diff(base_ref: str = "HEAD^", head_ref: str = "HEAD") -> str:
    """
    두 커밋(또는 Ref) 사이의 차이점을 추출합니다.
    """
    try:
        files_cmd = ["git", "diff", "--name-only", base_ref, head_ref]
        changed_files = subprocess.check_output(files_cmd).decode("utf-8").strip().split('\n')
        print(f'변경 파일 : {changed_files}')
        diff_cmd = ["git", "diff", base_ref, head_ref]
        diff_output = subprocess.check_output(diff_cmd).decode("utf-8")
        
        if not diff_output:
            return "변경 사항이 없습니다."
            
        return diff_output

    except subprocess.CalledProcessError as e:
        print(f"Git Error: {e}")
        sys.exit(1)

class DocGenerator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")
        
        self.client = OpenAI(api_key=self.api_key)

    def generate_docs(self, diff_content: str, model: str = "gpt-4o") -> str:
        """
        Diff 내용을 바탕으로 문서를 생성합니다.
        """
        system_prompt = """
        당신은 수석 테크니컬 라이터입니다. 
        제공된 Git Diff를 분석하여 다음 형식의 Markdown 문서를 작성하세요:
        1. **변경 요약**: 무엇이 바뀌었는지 한 문장 요약.
        2. **상세 내용**: 주요 변경 사항을 불렛 포인트로 설명.
        3. **기술적 영향**: 코드 구조나 성능에 미칠 영향.
        """

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"다음 변경 사항을 문서화해줘:\n\n{diff_content}"}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content