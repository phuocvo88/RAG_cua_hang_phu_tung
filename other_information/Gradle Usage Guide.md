# Gradle Usage Guide for RAG_cua_hang_phu_tung

This guide explains how to use Gradle to build, test, and run the RAG project.

## Prerequisites

- **Java 17 or higher** - Required for Gradle
- **Python 3.x** - For backend
- **Node.js 20.x** - For frontend (will be auto-downloaded by Gradle)

## Quick Start

**Linux/Mac:**
```bash
# Make gradlew executable (first time only)
chmod +x gradlew

# List all available tasks
./gradlew tasks
```

**Windows:**
```powershell
# Use the normal wrapper
.\gradlew.bat tasks

# Or use the fixed wrapper (handles JAVA_HOME issues)
.\gradlew-fixed.bat tasks
```

## Important Note: JAVA_HOME

**Windows:** If you encounter errors about invalid JAVA_HOME, use the `gradlew-fixed.bat` wrapper on Windows, which automatically sets the correct Java path.

**Linux/Mac:** Ensure Java 17+ is installed and JAVA_HOME is set:
```bash
# Check Java version
java -version

# Set JAVA_HOME (add to ~/.bashrc or ~/.zshrc for persistence)
export JAVA_HOME=/path/to/jdk-17
```

## Available Tasks

### Application Tasks

Run the entire application:

**Linux/Mac:**
```bash
./gradlew runAll         # Run both backend and frontend
```

**Windows:**
```powershell
.\gradlew.bat runAll     # Or .\gradlew-fixed.bat runAll
```

Run individual components:

**Linux/Mac:**
```bash
./gradlew :backend:run   # Run FastAPI backend only
./gradlew :frontend:dev  # Run Next.js frontend only
./gradlew :frontend:start # Run Next.js in production mode
```

**Windows:**
```powershell
.\gradlew.bat :backend:run
.\gradlew.bat :frontend:dev
.\gradlew.bat :frontend:start
```

### Build Tasks

Build the entire project:

**Linux/Mac:**
```bash
./gradlew buildAll       # Build backend deps + frontend
```

**Windows:**
```powershell
.\gradlew.bat buildAll
```

Build individual components:

**Linux/Mac:**
```bash
./gradlew :backend:installDependencies  # Install Python packages
./gradlew :frontend:buildApp            # Build Next.js for production
```

**Windows:**
```powershell
.\gradlew.bat :backend:installDependencies
.\gradlew.bat :frontend:buildApp
```

### Verification Tasks

Run all tests and linting:

**Linux/Mac:**
```bash
./gradlew testAll        # Run all tests
./gradlew lintAll        # Run all linting
```

**Windows:**
```powershell
.\gradlew.bat testAll
.\gradlew.bat lintAll
```

Run individual verifications:

**Linux/Mac:**
```bash
./gradlew :backend:test  # Run Python tests
./gradlew :backend:lint  # Lint Python code
./gradlew :frontend:lint # Lint Next.js code
```

**Windows:**
```powershell
.\gradlew.bat :backend:test
.\gradlew.bat :backend:lint
.\gradlew.bat :frontend:lint
```

### Cleanup Tasks

Clean build artifacts:

**Linux/Mac:**
```bash
./gradlew clean          # Clean all build artifacts
./gradlew :backend:clean # Clean backend only
./gradlew :frontend:clean # Clean frontend only
```

**Windows:**
```powershell
.\gradlew.bat clean
.\gradlew.bat :backend:clean
.\gradlew.bat :frontend:clean
```

### Python-Specific Tasks

**Linux/Mac:**
```bash
./gradlew :backend:setupVenv           # Create Python virtual environment
./gradlew :backend:listPackages        # List installed Python packages
./gradlew :backend:printPythonPath     # Show Python interpreter path
```

**Windows:**
```powershell
.\gradlew.bat :backend:setupVenv
.\gradlew.bat :backend:listPackages
.\gradlew.bat :backend:printPythonPath
```

### Node-Specific Tasks

**Linux/Mac:**
```bash
./gradlew :frontend:npmInstall  # Install Node packages
./gradlew :frontend:nodeSetup   # Download and install Node.js
```

**Windows:**
```powershell
.\gradlew.bat :frontend:npmInstall
.\gradlew.bat :frontend:nodeSetup
```

## Project Structure

```
RAG_cua_hang_phu_tung/
├── settings.gradle              # Multi-project configuration
├── build.gradle                 # Root project tasks
├── gradle.properties            # Gradle properties (Java home)
├── gradlew / gradlew.bat       # Gradle wrapper scripts
├── gradlew-fixed.bat           # Fixed wrapper for Windows JAVA_HOME issues
├── backend/
│   ├── build.gradle            # Backend Python tasks
│   ├── requirements.txt        # Python dependencies
│   └── venv/                   # Python virtual environment (auto-created)
└── frontend/
    ├── build.gradle            # Frontend Node.js tasks
    ├── package.json            # Node.js dependencies
    └── node_modules/           # Node packages (auto-installed)
```

## Task Dependencies

Gradle automatically manages task dependencies:

- `run` depends on `installDependencies`
- `installDependencies` depends on `setupVenv`
- `buildApp` depends on `npmInstall`
- `start` depends on `buildApp`
- `lint` depends on `installDependencies`/`npmInstall`

## Configuration Files

### gradle.properties
Sets the Java home directory and Gradle console mode:
```properties
org.gradle.java.home=C:\\Program Files\\Java\\jdk-17
org.gradle.console=verbose
```

### settings.gradle
Defines the multi-project structure:
```groovy
rootProject.name = 'RAG_cua_hang_phu_tung'
include 'backend'
include 'frontend'
```

## Troubleshooting

### JAVA_HOME Error
**Problem:** `ERROR: JAVA_HOME is set to an invalid directory`

**Solution:**
1. Use `gradlew-fixed.bat` instead of `gradlew.bat`
2. Or update your system JAVA_HOME environment variable to point to Java 17

### Python Virtual Environment Not Found
**Problem:** Task fails because venv doesn't exist

**Solution:**

**Linux/Mac:**
```bash
./gradlew :backend:setupVenv
```

**Windows:**
```powershell
.\gradlew.bat :backend:setupVenv
```

### Node Modules Not Installed
**Problem:** Frontend tasks fail

**Solution:**

**Linux/Mac:**
```bash
./gradlew :frontend:npmInstall
```

**Windows:**
```powershell
.\gradlew.bat :frontend:npmInstall
```

## Common Workflows

### First Time Setup

**Linux/Mac:**
```bash
# 1. Setup backend
./gradlew :backend:setupVenv
./gradlew :backend:installDependencies

# 2. Setup frontend
./gradlew :frontend:npmInstall

# 3. Run everything
./gradlew runAll
```

**Windows:**
```powershell
# 1. Setup backend
.\gradlew.bat :backend:setupVenv
.\gradlew.bat :backend:installDependencies

# 2. Setup frontend
.\gradlew.bat :frontend:npmInstall

# 3. Run everything
.\gradlew.bat runAll
```

### Daily Development

**Linux/Mac:**
```bash
# Clean and rebuild
./gradlew clean buildAll

# Run tests and lint
./gradlew testAll lintAll

# Start development servers
./gradlew runAll
```

**Windows:**
```powershell
# Clean and rebuild
.\gradlew.bat clean buildAll

# Run tests and lint
.\gradlew.bat testAll lintAll

# Start development servers
.\gradlew.bat runAll
```

### Production Build

**Linux/Mac:**
```bash
# Build everything for production
./gradlew buildAll

# Run in production mode
./gradlew :frontend:start
```

**Windows:**
```powershell
# Build everything for production
.\gradlew.bat buildAll

# Run in production mode
.\gradlew.bat :frontend:start
```

## Tips

1. **Parallel Execution:** Add `--parallel` to run independent tasks concurrently

   **Linux/Mac:**
   ```bash
   ./gradlew buildAll --parallel
   ```

   **Windows:**
   ```powershell
   .\gradlew.bat buildAll --parallel
   ```

2. **Skip Tests:** Use `-x test` to skip tests during build

   **Linux/Mac:**
   ```bash
   ./gradlew buildAll -x test
   ```

   **Windows:**
   ```powershell
   .\gradlew.bat buildAll -x test
   ```

3. **Verbose Output:** Use `--info` or `--debug` for detailed logs

   **Linux/Mac:**
   ```bash
   ./gradlew run --info
   ```

   **Windows:**
   ```powershell
   .\gradlew.bat run --info
   ```

4. **Continuous Build:** Use `--continuous` to automatically rebuild on file changes

   **Linux/Mac:**
   ```bash
   ./gradlew buildAll --continuous
   ```

   **Windows:**
   ```powershell
   .\gradlew.bat buildAll --continuous
   ```

## IDE Integration

Most IDEs (IntelliJ IDEA, VS Code with Gradle extension) can automatically detect and integrate with Gradle:

1. Open the project root folder
2. The IDE should auto-detect `build.gradle`
3. Gradle tasks will appear in the IDE's Gradle tool window
4. You can run tasks directly from the IDE

---

*Created: 2026-03-25*
*For more information, see [Planning Gradle Integration.md](Planning%20Gradle%20Integration.md)*
