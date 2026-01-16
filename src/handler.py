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
            제공된 Git Diff를 분석하여 다음 형식의 Markdown 문서를 작성하세요:
            1. **변경 요약**: 무엇이 바뀌었는지 한 문장 요약.
            2. **상세 내용**: 주요 변경 사항을 불렛 포인트로 설명.
            3. **기술적 영향**: 코드 구조나 성능에 미칠 영향.

            [제약사항]
            * 반드시 '한국어'로 작성하세요.
            * 전문 용어는 영어로 표기하되, 설명은 한국어로 하세요.
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
            제공된 '기존 README'와 'Git Diff(변경사항)'를 분석하여 README.md를 한글로 최신 상태로 업데이트하세요.

            [핵심 지침]
            1. **언어**: **반드시 모든 설명은 '한국어(Korean)'로 작성하세요.** (제목은 영어로 작성하되 설명은 한글로)
            2. **톤앤매너**: 한국 대학생 개발자가 읽기 편하도록 친근하고 명확하게 작성하고, 필요에 따라 이모지를 적극적으로 사용하세요.
            3. **내용 반영**: 변경 사항(기능 추가, 버그 수정 등)을 적절한 섹션에 자연스럽게 녹여내세요.
            4. **형식 유지**: 기존 마크다운 구조를 깨지 마세요.
            5. **제목 설정**: readme의 제목은 항상 'docs.AI'라고 작성하세요.
            
            [섹션 업데이트 가이드]
            - 기능이 추가되었다면 '주요 기능' 또는 'Features' 섹션에 한글로 설명을 추가하세요.
            - 설치 방법이 바뀌었다면 '설치 방법' 섹션을 수정하세요.
            - 변경 사항이 많다면 파일 끝에 '## 최근 업데이트 (ChangeLog)' 섹션을 만들고 날짜와 함께 한글로 요약해 주세요.            
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