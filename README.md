안녕하세요! docs.AI 프로젝트에 관심을 가져주셔서 정말 감사해요. 😊
최근 업데이트된 내용을 반영해서 README.md 파일을 새롭게 단장해 보았습니다.

---

# docs.AI

이 프로젝트는 AI, 특히 Google Gemini를 활용하여 최근 Git 변경사항을 기반으로 프로젝트 문서와 `README.md` 파일을 자동으로 업데이트해요. 또한 AI 모델의 출력 결과를 평가하기 위한 고급 벤치마킹 시스템도 포함하고 있답니다. 정말 똑똑하죠? ✨

## 주요 기능 (Features)

*   **자동 README 업데이트**: Git Diff를 자동으로 분석하고 Gemini를 활용해서 `README.md` 파일을 최신 개발 내용에 맞춰 업데이트해 드려요. 덕분에 프로젝트 문서가 항상 최신 상태를 유지할 수 있답니다. 번거로운 수동 작업은 이제 그만! 🙅‍♀️
*   **의미론적 리콜 벤치마킹 시스템 (업데이트)**: AI 모델의 결과물을 평가하기 위한 고급 시스템으로, 이제 두 가지 유형의 벤치마크를 제공해요:
    *   **문서 생성 벤치마크 (`tests/test_docs/benchmark_docs.py`)**: 일반 문서(`DocGenerator`)의 의미론적 리콜을 측정합니다. 모델이 생성한 내용과 실제 정답(ground truth) 간의 의미적 유사도를 측정하는 평가 지표를 사용하며, 이제 **임계값이 0.85로 상향 조정**되어 더 정밀한 평가가 가능해졌어요. 🔍
    *   **README 업데이트 벤치마크 (`tests/test_readme/benchmark_readme.py`)**: `README.md` 파일 업데이트(`ReadmeGenerator`) 전용 벤치마크가 새로 추가되었어요! 🚀 이 시스템은 제공된 Git Diff의 핵심 내용이 업데이트된 README에 잘 반영되었는지 확인하고, 문서의 초기 상태(`current_readme`)를 고려하여 더욱 현실적인 평가를 수행합니다.
    *   **향상된 데이터 관리**: 다양한 데이터셋 파일(예: `dataset_easy_docs.py`, `dataset_normal_docs.py`, `dataset_readme.py`)을 더 유연하게 로드하고 관리할 수 있어 포괄적인 테스트가 가능해졌어요. 📊
    *   **상세 로깅**: 의미론적 리콜 점수, 실행 시간, 누락된 토큰 목록 등 상세한 벤치마크 결과를 제공하여 더 깊이 있는 분석을 돕습니다. 💡
*   **유연한 CI/CD 통합**: 문서 및 README 업데이트 워크플로우는 GitHub Actions에 완벽하게 통합되어 다음을 지원합니다:
    *   `main` 브랜치로 Pull Request가 병합될 때마다 자동으로 실행돼요. 🔄
    *   필요할 때마다 GitHub Actions 탭에서 수동으로 워크플로우를 실행할 수도 있습니다. 편리하죠? 🙌

## 설치 방법 및 사용법 (Setup & Usage)

프로젝트를 시작하려면 다음 설치 지침을 따라주세요. 아주 간단하답니다! 😉

### 설치 방법 (Setup)

1.  **Python 3.11+**: 호환 가능한 Python 버전이 설치되어 있는지 확인해 주세요. 🐍
2.  **의존성 설치**: 필요한 모든 Python 패키지를 설치합니다:
    ```bash
    pip install -r requirements.txt
    ```
    *참고: `numpy`는 벤치마킹 시스템의 의미론적 리콜(Semantic Recall) 기능에 필요한 새로운 의존성입니다.*
3.  **Gemini API 키**: Google Gemini API 키가 필요합니다. 🔑
    *   **로컬 개발용**: 프로젝트 루트 디렉토리에 `.env` 파일을 만들고 키를 추가하세요:
        ```
        GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```
    *   **GitHub Actions용**: 저장소의 Secrets에 `GEMINI_API_KEY`를 추가해 주세요.

### 사용 방법 (Usage)

#### README 및 문서 업데이트

프로젝트의 `README.md`와 문서는 GitHub Actions를 통해 자동으로 업데이트됩니다.

*   **PR 병합 시 자동 업데이트**: Pull Request가 `main` 브랜치로 병합될 때마다 `auto-docs.yml` 워크플로우가 자동으로 실행되어 Git Diff를 분석하고 `README.md` 파일을 업데이트합니다. 🚀
*   **수동 실행**: 다음 단계를 통해 워크플로우를 수동으로 실행할 수 있습니다:
    1.  GitHub 저장소의 "Actions" 탭으로 이동합니다.
    2.  왼쪽 사이드바에서 "Auto Docs" 워크플로우를 선택합니다.
    3.  일반적으로 `main` 브랜치를 선택한 후 "Run workflow" 버튼을 클릭하여 즉시 업데이트를 시작합니다. 👆

#### 벤치마크 실행 🚀

이제 두 가지 유형의 벤치마크를 실행할 수 있습니다. 여러분의 AI 모델 성능을 직접 확인해 보세요!

*   **문서 생성 벤치마크 (일반 문서)**: `DocGenerator`의 성능을 평가합니다.
    ```bash
    python tests/test_docs/benchmark_docs.py
    ```
    실행 시 'easy' 또는 'normal' 모드를 선택하여 해당 데이터셋(`dataset_easy_docs.py`, `dataset_normal_docs.py`)으로 테스트를 진행할 수 있습니다.
*   **README 업데이트 벤치마크**: `ReadmeGenerator`의 성능을 평가합니다.
    ```bash
    python tests/test_readme/benchmark_readme.py
    ```
    이 벤치마크는 `tests/test_readme/dataset_readme.py`에 정의된 데이터셋을 사용합니다.

각 벤치마크 실행 후 결과는 해당 테스트 디렉토리 내의 `output_docs/` 또는 `output_readme/` 폴더에 상세 로그 파일로 저장됩니다. 📂

## 프로젝트 구조 (Project Structure)

프로젝트의 주요 구성 요소는 다음과 같아요:

```
📂 .github/
└── 📂 workflows/
    └── 📄 auto-docs.yml (자동 문서 업데이트 워크플로우)
📂 src/
├── 📄 handler.py (DocGenerator와 ReadmeGenerator 클래스 포함)
└── 📄 main.py (애플리케이션의 주요 진입점)
📂 tests/
├── 📂 test_docs/ (일반 문서 생성 벤치마크 관련 파일)
│   ├── 📄 benchmark_docs.py (문서 생성 AI 성능 평가 스크립트)
│   ├── 📄 dataset_easy_docs.py (문서 생성 벤치마크용 쉬운 데이터셋)
│   └── 📄 dataset_normal_docs.py (문서 생성 벤치마크용 일반 데이터셋)
└── 📂 test_readme/ (README 업데이트 벤치마크 관련 파일)
    ├── 📄 benchmark_readme.py (README 업데이트 AI 성능 평가 스크립트)
    └── 📄 dataset_readme.py (README 업데이트 벤치마크용 데이터셋)
📄 .env.example (환경 변수 예시)
📄 .gitignore (Git 무시 파일 설정)
📄 README.md (현재 문서)
📄 requirements.txt (Python 의존성 목록)
```

## 최근 업데이트 (ChangeLog)

*   **README 자동 업데이트 기능 강화**: 기존 `ReadmeGenerator` 클래스와 `src/main.py` 통합은 동일하며, `DocGenerator` 및 `ReadmeGenerator`의 시스템 프롬프트가 **한글 출력 및 이모지 사용을 명시적으로 권장**하도록 업데이트되었습니다. 🎨
*   **GitHub Actions 워크플로우 개선**: `auto-docs.yml` 워크플로우가 `README.md` 변경 사항을 자동으로 추가 및 커밋하도록 로직이 강화되었으며, `workflow_dispatch`가 추가되어 GitHub Actions 탭에서 수동 실행이 가능해졌습니다. ⚙️
*   **고급 벤치마킹 시스템 대폭 개선**: 이제 두 가지 유형의 벤치마크를 제공해요! 📊
    *   **기존 문서 생성 벤치마크 리팩토링**: `tests/benchmark.py`가 `tests/test_docs/benchmark_docs.py`로 이름이 변경되었고, '의미론적 리콜(Semantic Recall)'의 **평가 임계값이 0.75에서 0.85로 상향 조정**되어 더욱 엄격한 평가가 가능해졌습니다. `dataset` 파일들도 `dataset_easy_docs.py`, `dataset_normal_docs.py`로 명확하게 이름이 변경되었습니다.
    *   **새로운 README 업데이트 전용 벤치마크 도입**: `tests/test_readme/` 디렉토리 아래에 `benchmark_readme.py`와 `dataset_readme.py`가 추가되어 `ReadmeGenerator`의 성능을 독립적으로 평가할 수 있게 되었습니다.
    *   **벤치마크 로깅 개선**: `README.md` 업데이트 벤치마크(`tests/test_readme/benchmark_readme.py`)에서 생성된 README의 **전체 내용을 로그에 기록**하도록 변경되어, 모델의 출력 결과를 더욱 상세하게 검토하고 디버깅할 수 있게 되었어요. 📝
    *   `numpy` 의존성은 기존과 동일하게 유지됩니다.
*   **프로젝트 구조 및 코드베이스 정리**:
    *   `src/handler.py` 내 `ReadmeUpdater` 클래스가 `ReadmeGenerator`로 이름이 변경되어, 코드베이스의 일관성과 명확성이 향상되었습니다. ✨
    *   더 이상 사용되지 않는 `run.py` 파일과 `generated_docs.md` 파일이 삭제되었습니다. 🗑️
    *   `.gitignore` 파일도 `tests/test*/output*`과 같이 테스트 관련 출력 파일을 더 정확하게 무시하도록 업데이트되었습니다.