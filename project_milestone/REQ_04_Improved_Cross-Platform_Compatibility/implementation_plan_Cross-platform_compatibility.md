# Improved Cross-Platform Compatibility

This plan aims to ensure the project can be seamlessly cloned and built on Linux, Mac, and Windows.

## Proposed Changes

### Backend

#### [MODIFY] [rag_engine.py](file:///f:/side_projects/RAG_cua_hang_phu_tung/backend/rag_engine.py)
- Remove hardcoded absolute Windows paths for API keys (`F:\side_projects\...`).
- Use relative paths for local key files (e.g., `./keys/...`) if they exist, or rely solely on environment variables from `.env`.
- Ensure all file path operations use `os.path.join` for OS-specific separators.

#### [NEW] [setup.sh](file:///f:/side_projects/RAG_cua_hang_phu_tung/setup.sh)
- Create a bash script equivalent to [install_python.ps1](file:///f:/side_projects/RAG_cua_hang_phu_tung/install_python.ps1) for Linux/Mac to automate the initial environment setup.

### Documentation

#### [MODIFY] [README.md](file:///f:/side_projects/RAG_cua_hang_phu_tung/README.md)
- Update installation instructions to be more balanced between Windows and Linux/Mac.
- Highlight the use of [gradlew](file:///f:/side_projects/RAG_cua_hang_phu_tung/gradlew) (Unix) vs [gradlew.bat](file:///f:/side_projects/RAG_cua_hang_phu_tung/gradlew.bat) (Windows).

#### [MODIFY] [QUICKSTART.md](file:///f:/side_projects/RAG_cua_hang_phu_tung/QUICKSTART.md)
- Add Unix-style commands alongside Windows-style commands (e.g., `venv/bin/python` vs `venv/Scripts/python.exe`).

#### [MODIFY] [Gradle Usage Guide.md](file:///f:/side_projects/RAG_cua_hang_phu_tung/other_information/Gradle Usage Guide.md)
- Update examples to show [./gradlew](file:///f:/side_projects/RAG_cua_hang_phu_tung/gradlew) as the primary command for Unix users.

## Verification Plan

### Automated Tests
- Run `:backend:test` using Gradle on the current machine (Windows) to ensure no regressions.
- Command: `.\gradlew.bat :backend:test`

### Manual Verification
1.  **Windows Verification**:
    - Run `.\gradlew.bat runAll` to ensure the application still starts and functions on Windows.
2.  **Linux/Mac Simulation (Dry Run)**:
    - Review `setup.sh` syntax for correctness.
    - Verify that [rag_engine.py](file:///f:/side_projects/RAG_cua_hang_phu_tung/backend/rag_engine.py) no longer attempts to access `F:\` drive on any OS.
    - Ask the user if they can verify on a Mac or Linux machine if available, or I will use the browser tool to check documentation links.
