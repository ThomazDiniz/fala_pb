@echo off
REM ====================================================================
REM  Experimento Final - RODA DO ZERO (--overwrite): recalcula TODOS os
REM  1800 audios, ignorando o que ja existe. Duplo-clique para rodar.
REM  Argumentos extras tambem sao repassados, ex.:
REM     rodar_experimento_OVERWRITE.bat --workers 3
REM ====================================================================
setlocal
cd /d "%~dp0"

REM --- (opcional) ambiente conda. Deixe em branco para usar o python do PATH.
set "CONDA_ENV="

if defined CONDA_ENV (
    set "PYRUN=conda run -n %CONDA_ENV% --no-capture-output python"
) else (
    set "PYRUN=python"
)

echo ============================================================
echo  Experimento Final  (MODO OVERWRITE - refaz tudo)
echo  Pasta : %CD%
echo  Python: %PYRUN%
echo ============================================================

if not exist "experimento_final.py" (
    echo [ERRO] experimento_final.py nao encontrado nesta pasta.
    pause & exit /b 1
)

echo.
echo [1/2] Instalando dependencias (requirements.txt)...
%PYRUN% -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias.
    pause & exit /b 1
)

echo.
echo [2/2] Rodando o experimento com --overwrite ...
%PYRUN% experimento_final.py --overwrite %*
if errorlevel 1 (
    echo.
    echo [ERRO] O experimento falhou. Veja resultados\experimento_final.log
    pause & exit /b 1
)

echo.
echo ============================================================
echo  CONCLUIDO. Resultados em:  resultados\
echo    - csv1_todas_metricas.csv     (1800 linhas)
echo    - csv2_melhor_de_3.csv        (600 linhas)
echo    - plots\*.png
echo    - conclusoes_preliminares.md
echo ============================================================
pause
endlocal
