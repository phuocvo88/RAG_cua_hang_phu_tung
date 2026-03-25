@echo off
REM Wrapper script to fix JAVA_HOME for Gradle
set "JAVA_HOME=C:\Program Files\Java\jdk-17"
call "%~dp0gradlew.bat" %*
