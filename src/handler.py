# src/handler.py

import subprocess
import sys
import os
from google import genai
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
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key and os.getenv("MOCK_MODE") != "true":
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)

    def generate_docs(self, diff_content: str, model: str = "gemini-2.5-flash") -> str:
        
        if os.getenv("MOCK_MODE") == "true":
            return '[MOCK] 자동 생성된 문서 예시 (Gemini)'

        """
        Diff 내용을 바탕으로 문서를 생성합니다.
        """
        try:
            system_prompt = """
            당신은 수석 테크니컬 라이터입니다. 
            제공된 Git Diff를 분석하여 다음 형식의 Markdown 문서를 작성하세요:
            1. **변경 요약**: 무엇이 바뀌었는지 한 문장 요약.
            2. **상세 내용**: 주요 변경 사항을 불렛 포인트로 설명.
            3. **기술적 영향**: 코드 구조나 성능에 미칠 영향.
            """

            # [변경] Gemini 모델 초기화 (시스템 프롬프트 설정)
            generative_model = genai.GenerativeModel(
                model_name=model,
                system_instruction=system_prompt
            )

            # [변경] 콘텐츠 생성 호출
            response = generative_model.generate_content(
                f"다음 변경 사항을 문서화해줘:\n\n{diff_content}"
            )
            
            # [변경] 응답 텍스트 추출 방식 변경
            return response.text
            
        except Exception as e:
            return f"API 호출 중 에러 발생 \n{str(e)}"