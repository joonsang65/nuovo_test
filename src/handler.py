# src/handler.py

import subprocess
import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from config import Config

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

    def generate_docs(self, diff_content: str) -> dict:
        if not self.client:
            raise ValueError("API 클라이언트 초기화 실패")

        try:
            response = self.client.models.generate_content(
                model=Config.GENERATION_MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=Config.PROMPT_DOCS_SYSTEM,
                    temperature=Config.TEMPERATURE_DOCS
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

class ReadmeUpdater:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY 미설정")
        self.client = genai.Client(api_key=self.api_key)

    def update_readme(self, diff_content: str, current_readme: str) -> dict:
        if not self.client:
            raise ValueError("API 클라이언트 초기화 실패")

        try:
            user_content = f"""
            [기존 README 내용]
            {current_readme}

            [Git Diff 변경사항]
            {diff_content}
            
            위 내용을 바탕으로 업데이트된 README.md 전체 코드를 생성해줘.
            """

            response = self.client.models.generate_content(
                model=Config.GENERATION_MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=Config.PROMPT_README_SYSTEM,
                    temperature=Config.TEMPERATURE_README
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
                "text": current_readme,
                "error": str(e),
                "usage": {}
            }