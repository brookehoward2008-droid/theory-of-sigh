@echo off
setlocal
title Visceral Theory of Sight - Publication Engine
cd /d "%~dp0"

echo ============================================================
echo   Visceral Theory of Sight - local publication engine
echo   Working folder: %CD%
echo ============================================================
echo.

echo [1/4] Updating to the engine branch...
git fetch origin claude/gallant-ptolemy-k0zpgr
git checkout claude/gallant-ptolemy-k0zpgr
git pull origin claude/gallant-ptolemy-k0zpgr
echo.

set "VTS_OUTPUT_DIR=C:\VTS-output"
echo [2/4] Outputs will be written to: %VTS_OUTPUT_DIR%
echo.

echo [3/4] Installing dependencies (token-free, local)...
python scripts\build.py --setup
echo.

echo [4/4] Environment check...
python scripts\build.py --check
echo.

set "IDMLPATH=%~1"
if "%IDMLPATH%"=="" set /p IDMLPATH="Enter full path to an .idml to refine (or press Enter to skip): "
if not "%IDMLPATH%"=="" python scripts\build.py --refine-idml --idml "%IDMLPATH%"
echo.

echo ============================================================
echo   Done.  Any outputs are in %VTS_OUTPUT_DIR%
echo   Tip: you can drag an .idml file onto run.bat to refine it.
echo ============================================================
pause
endlocal
