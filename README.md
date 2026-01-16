# New Project

이 프로젝트는 AI, 특히 Google Gemini를 활용하여 최근 Git 변경사항을 기반으로 프로젝트 문서와 `README.md` 파일을 자동으로 업데이트합니다. 또한 AI 모델의 출력 결과를 평가하기 위한 고급 벤치마킹 시스템도 포함하고 있어요.

## 주요 기능 (Features)

*   **자동 README 업데이트**: Git Diff를 자동으로 분석하고 Gemini를 활용하여 `README.md` 파일을 최신 개발 내용에 맞춰 업데이트해 줍니다. 덕분에 프로젝트 문서가 항상 최신 상태를 유지할 수 있어요.
*   **의미론적 리콜 벤치마킹 시스템**: AI 모델의 결과물을 평가하기 위한 고급 시스템으로, 다음 기능들을 포함하고 있습니다:
    *   **의미론적 리콜 (Semantic Recall)**: 단어 임베딩(word embeddings)과 코사인 유사도(cosine similarity)를 활용하여 모델이 생성한 내용과 실제 정답(ground truth) 간의 의미적 유사도를 측정하는 새로운 평가 지표입니다.
    *   **향상된 데이터 관리**: 다양한 데이터셋 파일(예: `dataset_easy.py`, `dataset_normal.py`)을 더 유연하게 로드하고 관리할 수 있어 포괄적인 테스트가 가능해졌어요.
    *   **상세 로깅**: 의미론적 리콜 점수, 실행 시간, 누락된 토큰 목록 등 상세한 벤치마크 결과를 제공하여 더 깊이 있는 분석을 돕습니다.
*   **유연한 CI/CD 통합**: 문서 및 README 업데이트 워크플로우는 GitHub Actions에 완벽하게 통합되어 다음을 지원합니다:
    *   `main` 브랜치로 Pull Request가 병합될 때마다 자동으로 실행돼요.
    *   필요할 때마다 GitHub Actions 탭에서 수동으로 워크플로우를 실행할 수도 있습니다.

## 설치 방법 (Setup)

프로젝트를 시작하려면 다음 설치 지침을 따라주세요.

1.  **Python 3.11+**: 호환 가능한 Python 버전이 설치되어 있는지 확인해 주세요.
2.  **의존성 설치**: 필요한 모든 Python 패키지를 설치합니다:
    ```bash
    pip install -r requirements.txt
    ```
    *참고: `numpy`는 벤치마킹 시스템의 의미론적 리콜(Semantic Recall) 기능에 필요한 새로운 의존성입니다.*
3.  **Gemini API 키**: Google Gemini API 키가 필요합니다.
    *   **로컬 개발용**: 프로젝트 루트 디렉토리에 `.env` 파일을 만들고 키를 추가하세요:
        ```
        GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```
    *   **GitHub Actions용**: 저장소의 Secrets에 `GEMINI_API_KEY`를 추가해 주세요.

## 사용 방법 (Usage)

### README 및 문서 업데이트

프로젝트의 `README.md`와 문서는 GitHub Actions를 통해 자동으로 업데이트됩니다.

*   **PR 병합 시 자동 업데이트**: Pull Request가 `main` 브랜치로 병합될 때마다 `auto-docs.yml` 워크플로우가 자동으로 실행되어 Git Diff를 분석하고 `README.md` 파일을 업데이트합니다.
*   **수동 실행**: 다음 단계를 통해 워크플로우를 수동으로 실행할 수 있습니다:
    1.  GitHub 저장소의 "Actions" 탭으로 이동합니다.
    2.  왼쪽 사이드바에서 "Auto Docs" 워크플로우를 선택합니다.
    3.  일반적으로 `main` 브랜치를 선택한 후 "Run workflow" 버튼을 클릭하여 즉시 업데이트를 시작합니다.

### 벤치마크 실행

`src/main.py` 스크립트는 이제 주로 `README.md` 업데이트에 초점을 맞추고 있지만, 벤치마크 테스트 자체는 `tests/test_docs/benchmark.py`에 있습니다. 평가 목적으로 이 파일을 직접 실행할 수 있어요.

## 프로젝트 구조 (Project Structure)

*   `src/`: 프로젝트의 핵심 로직을 담고 있습니다.
    *   `src/handler.py`: `DocGenerator`(일반 문서 생성을 위한 클래스)와 새로 추가된 `ReadmeGenerator` 클래스를 포함합니다.
    *   `src/main.py`: 애플리케이션의 주요 진입점으로, 현재 Git Diff를 처리하여 `README.md`를 업데이트하는 데 중점을 둡니다.
*   `tests/test_docs/`: 이제 벤치마크 테스트들이 이 디렉토리에 있으며, 업데이트된 `benchmark.py`가 포함되어 있습니다.

## 최근 업데이트 (ChangeLog)

*   **README 자동 업데이트 기능 강화**: 새로운 `ReadmeGenerator` 클래스가 도입되어 `src/main.py`에 통합되었으며, `DocGenerator`의 시스템 프롬프트가 한글 출력을 명시하도록 업데이트되었습니다.
*   **GitHub Actions 워크플로우 개선**: `auto-docs.yml` 워크플로우가 `README.md` 변경 사항을 자동으로 추가 및 커밋하도록 로직이 강화되었으며, `workflow_dispatch`가 추가되어 GitHub Actions 탭에서 수동 실행이 가능해졌습니다.
*   **고급 벤치마킹 시스템 도입**: `tests/benchmark.py`가 `tests/test_docs/benchmark.py`로 이동했으며, '의미론적 리콜(Semantic Recall)'이라는 새로운 평가 지표와 `numpy` 의존성이 추가되었습니다. 여러 데이터셋 파일(`dataset_easy.py`, `dataset_normal.py`)을 지원하도록 데이터 처리 방식도 개선되었어요.
*   **코드베이스 정리**: `generated_docs.md` 파일이 삭제되었고, `.gitignore` 파일도 테스트 관련 출력 및 데이터셋 파일을 더 정확하게 무시하도록 업데이트되었습니다.