# src/handler.py

import subprocess
import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

def get_git_diff(base_ref: str = "HEAD^", head_ref: str = "HEAD") -> str:
    try:
        files_cmd = ["git", "diff", "--name-only", base_ref, head_ref]
        changed_files = subprocess.check_output(files_cmd).decode("utf-8").strip().split('\n')
        print(f'변경 파일 : {changed_files}')
        
        diff_cmd = ["git", "diff", base_ref, head_ref]
        diff_output = subprocess.check_output(diff_cmd).decode("utf-8")
        
        if not diff_output:
            return "변경 사항 없음"
            
        return diff_output

    except subprocess.CalledProcessError as e:
        print(f"Git Error: {e}")
        sys.exit(1)

class DocGenerator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY 미설정")
        
        self.client = genai.Client(api_key=self.api_key)

    def generate_docs(self, diff_content: str, model: str = "gemini-2.5-flash") -> dict:
        if not self.client:
            raise ValueError("API 클라이언트가 초기화 실패")

        try:
            system_prompt = """
            당신은 수석 테크니컬 라이터입니다. 
            제공된 Git Diff를 분석하여 다음 형식의 Markdown 문서를 한글로 작성하세요:
            1. **변경 요약**: 무엇이 바뀌었는지 한 문장 요약.
            2. **상세 내용**: 주요 변경 사항을 불렛 포인트로 설명.
            3. **기술적 영향**: 코드 구조나 성능에 미칠 영향.
            """

            response = self.client.models.generate_content(
                model=model,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt
                ),
                contents=f"다음 변경 사항을 문서화해줘:\n\n{diff_content}"
            )
        
            usage = response.usage_metadata
            
            return {
                "text": response.text,
                "usage": {
                    "prompt_tokens": usage.prompt_token_count if usage else 0,
                    "output_tokens": usage.candidates_token_count if usage else 0,
                    "total_tokens": usage.total_token_count if usage else 0
                },
            }
            
        except Exception as e:
            return {
                "text": f"API 호출 중 에러 발생 \n{str(e)}",
                "usage": {"prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0},
            }

class ReadmeGenerator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY 미설정")
        
        self.client = genai.Client(api_key=self.api_key)

    def update_readme(self, diff_content: str, current_readme: str, model: str = "gemini-2.5-flash") -> dict:
        """
        Git Diff와 기존 README를 기반으로 최신화된 README 내용을 생성합니다.
        """
        if not self.client:
            raise ValueError("API 클라이언트 초기화 실패")

        try:
            system_prompt = """
            당신은 오픈소스 프로젝트의 숙련된 메인테이너입니다.
            제공된 '기존 README'와 'Git Diff(변경사항)'를 분석하여 README.md를 최신 상태로 업데이트하세요.

            [지침]
            1. **구조 유지**: 기존 README의 헤더, 목차, 스타일을 최대한 유지하세요.
            2. **내용 반영**: Git Diff에서 확인된 새로운 기능, 변경된 설정, 혹은 삭제된 로직을 적절한 섹션(예: Features, Installation, Usage)에 반영하세요.
            3. **Changelog**: 만약 'Changelog' 섹션이 있다면 최신 변경 내역을 추가하고, 없다면 파일 끝에 '## Recent Updates' 섹션을 만들어 요약하세요.
            4. **무결성**: 변경되지 않은 내용은 절대 생략하거나 임의로 수정하지 마세요.
            """

            user_content = f"""
            [기존 README 내용]
            {current_readme}

            [Git Diff 변경사항]
            {diff_content}
            
            위 정보를 바탕으로 업데이트된 README.md 전체 내용을 마크다운 형식으로 출력해줘.
            코드 블록(```markdown ... ```) 없이 내용만 출력해.
            """

            response = self.client.models.generate_content(
                model=model,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt
                ),
                contents=user_content
            )
        
            usage = response.usage_metadata
            
            return {
                "text": response.text,
                "usage": {
                    "prompt_tokens": usage.prompt_token_count if usage else 0,
                    "output_tokens": usage.candidates_token_count if usage else 0,
                    "total_tokens": usage.total_token_count if usage else 0
                },
            }
            
        except Exception as e:
            return {
                "text": current_readme, # 에러 발생 시 기존 내용을 그대로 반환
                "error": str(e),
                "usage": {"prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0},
            }