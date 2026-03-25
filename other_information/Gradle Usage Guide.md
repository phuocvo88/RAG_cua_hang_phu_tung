# Gradle Usage Guide for RAG_cua_hang_phu_tung

This guide explains how to use Gradle to build, test, and run the RAG project.

## Prerequisites

- **Java 17 or higher** - Required for Gradle
- **Python 3.x** - For backend
- **Node.js 20.x** - For frontend (will be auto-downloaded by Gradle)

## Quick Start

### Windows
```bash
# Use the fixed wrapper (handles JAVA_HOME issues)
.\gradlew-fixed.bat tasks

# Or set JAVA_HOME first, then use normal wrapper
set JAVA_HOME=C:\Program Files\Java\jdk-17
.\gradlew tasks
```

### Linux/Mac
```bash
./gradlew tasks
```

## Important Note: JAVA_HOME

If you encounter errors about invalid JAVA_HOME, use the `gradlew-fixed.bat` wrapper on Windows, which automatically sets the correct Java path.

## Available Tasks

### Application Tasks

Run the entire application:
```bash
.\gradlew-fixed.bat runAll         # Run both backend and frontend
```

Run individual components:
```bash
.\gradlew-fixed.bat :backend:run   # Run FastAPI backend only
.\gradlew-fixed.bat :frontend:dev  # Run Next.js frontend only
.\gradlew-fixed.bat :frontend:start # Run Next.js in production mode
```

### Build Tasks

Build the entire project:
```bash
.\gradlew-fixed.bat buildAll       # Build backend deps + frontend
```

Build individual components:
```bash
.\gradlew-fixed.bat :backend:installDependencies  # Install Python packages
.\gradlew-fixed.bat :frontend:buildApp            # Build Next.js for production
```

### Verification Tasks

Run all tests and linting:
```bash
.\gradlew-fixed.bat testAll        # Run all tests
.\gradlew-fixed.bat lintAll        # Run all linting
```

Run individual verifications:
```bash
.\gradlew-fixed.bat :backend:test  # Run Python tests
.\gradlew-fixed.bat :backend:lint  # Lint Python code
.\gradlew-fixed.bat :frontend:lint # Lint Next.js code
```

### Cleanup Tasks

Clean build artifacts:
```bash
.\gradlew-fixed.bat clean          # Clean all build artifacts
.\gradlew-fixed.bat :backend:clean # Clean backend only
.\gradlew-fixed.bat :frontend:clean # Clean frontend only
```

### Python-Specific Tasks

```bash
.\gradlew-fixed.bat :backend:setupVenv           # Create Python virtual environment
.\gradlew-fixed.bat :backend:listPackages        # List installed Python packages
.\gradlew-fixed.bat :backend:printPythonPath     # Show Python interpreter path
```

### Node-Specific Tasks

```bash
.\gradlew-fixed.bat :frontend:npmInstall  # Install Node packages
.\gradlew-fixed.bat :frontend:nodeSetup   # Download and install Node.js
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
```bash
.\gradlew-fixed.bat :backend:setupVenv
```

### Node Modules Not Installed
**Problem:** Frontend tasks fail

**Solution:**
```bash
.\gradlew-fixed.bat :frontend:npmInstall
```

## Common Workflows

### First Time Setup
```bash
# 1. Setup backend
.\gradlew-fixed.bat :backend:setupVenv
.\gradlew-fixed.bat :backend:installDependencies

# 2. Setup frontend
.\gradlew-fixed.bat :frontend:npmInstall

# 3. Run everything
.\gradlew-fixed.bat runAll
```

### Daily Development
```bash
# Clean and rebuild
.\gradlew-fixed.bat clean buildAll

# Run tests and lint
.\gradlew-fixed.bat testAll lintAll

# Start development servers
.\gradlew-fixed.bat runAll
```

### Production Build
```bash
# Build everything for production
.\gradlew-fixed.bat buildAll

# Run in production mode
.\gradlew-fixed.bat :frontend:start
```

## Tips

1. **Parallel Execution:** Add `--parallel` to run independent tasks concurrently
   ```bash
   .\gradlew-fixed.bat buildAll --parallel
   ```

2. **Skip Tests:** Use `-x test` to skip tests during build
   ```bash
   .\gradlew-fixed.bat buildAll -x test
   ```

3. **Verbose Output:** Use `--info` or `--debug` for detailed logs
   ```bash
   .\gradlew-fixed.bat run --info
   ```

4. **Continuous Build:** Use `--continuous` to automatically rebuild on file changes
   ```bash
   .\gradlew-fixed.bat buildAll --continuous
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
