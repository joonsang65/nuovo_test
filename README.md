# New Project

This project leverages AI, specifically Google Gemini, to automate the process of updating project documentation and `README.md` files based on recent Git changes. It also incorporates an advanced benchmarking system designed to evaluate the outputs of AI models.

## Features

*   **Automated README Updates**: Automatically analyzes Git diffs and updates the `README.md` file using Gemini, ensuring your project's primary documentation is always current with the latest development.
*   **Semantic Recall Benchmarking System**: An advanced system for evaluating AI model outputs, now featuring:
    *   **Semantic Recall**: A new metric that measures the semantic similarity between model-generated content and ground truth by utilizing word embeddings and cosine similarity.
    *   **Improved Data Management**: Enhanced flexibility to load and manage various dataset files (e.g., `dataset_easy.py`, `dataset_normal.py`) for comprehensive testing.
    *   **Enhanced Logging**: Provides detailed benchmark results, including Semantic Recall scores, execution time, and lists of missing tokens for better insights.
*   **Flexible CI/CD Integration**: The documentation and README update workflow is seamlessly integrated into GitHub Actions, supporting:
    *   Automatic execution upon Pull Request merges to the `main` branch.
    *   Manual triggering via the GitHub Actions tab for on-demand updates whenever necessary.

## Setup

To get started with this project, please follow these setup instructions:

1.  **Python 3.11+**: Ensure you have a compatible Python version installed.
2.  **Install Dependencies**: Install all required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: `numpy` is now a dependency, specifically for the semantic recall feature of the benchmarking system.*
3.  **Gemini API Key**: A Google Gemini API key is required.
    *   **For Local Development**: Create a `.env` file in the project's root directory and add your key:
        ```
        GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```
    *   **For GitHub Actions**: Add `GEMINI_API_KEY` to your repository's secrets.

## Usage

### Updating README & Documentation

The project's `README.md` and documentation are updated automatically through GitHub Actions:

*   **Automatic Updates on PR Merge**: Whenever a Pull Request is merged into the `main` branch, the `auto-docs.yml` workflow will automatically run, analyze the Git diff, and update the `README.md` file accordingly.
*   **Manual Trigger**: You can manually trigger the workflow:
    1.  Navigate to the "Actions" tab in your GitHub repository.
    2.  Select the "Auto Docs" workflow from the left sidebar.
    3.  Click the "Run workflow" button, typically choosing the `main` branch, to initiate an on-demand update.

### Running Benchmarks

While the `src/main.py` script is now primarily focused on `README.md` updates, the benchmark tests themselves are located in `tests/test_docs/benchmark.py`. These can be executed directly for evaluation purposes.

## Project Structure

*   `src/`: Contains the core logic for the project.
    *   `src/handler.py`: Includes `DocGenerator` (for general documentation generation) and the newly added `ReadmeGenerator` class.
    *   `src/main.py`: The main entry point for the application, currently focused on processing Git diffs to update `README.md`.
*   `tests/test_docs/`: This directory now houses the benchmark tests, including the updated `benchmark.py`.

## Recent Updates

*   **Automated README Generation**: A new `ReadmeGenerator` class has been implemented and integrated into `src/main.py` to automatically update `README.md` based on Git diffs.
*   **GitHub Actions Workflow Enhancements**:
    *   The `auto-docs.yml` workflow now explicitly includes logic to add and commit changes to `README.md`.
    *   Added `workflow_dispatch` to `auto-docs.yml`, enabling manual triggering of the workflow directly from the GitHub Actions tab.
    *   Adjusted workflow conditions to run on both Pull Request merges and manual dispatches.
*   **Advanced Benchmarking System**: The `tests/benchmark.py` file has been moved to `tests/test_docs/benchmark.py` and significantly upgraded to include:
    *   **Semantic Recall**: A new, more sophisticated metric for evaluating semantic similarity in model outputs.
    *   Integration of `numpy` as a dependency for advanced scientific computing within benchmarks.
    *   Refined dataset handling to support multiple test dataset files.
*   **Codebase Cleanup**:
    *   The `generated_docs.md` file has been removed, as the direct output of documentation is now primarily integrated into `README.md` updates.
    *   The `.gitignore` file has been updated with more precise patterns for ignoring test-related output and dataset files (`tests/test*/dataset_*.py` and `tests/output*`).