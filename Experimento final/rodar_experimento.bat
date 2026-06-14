@echo off
REM ====================================================================
REM  Experimento Final - roda tudo (STT + Levenshtein + MOS -> CSV1/CSV2
REM  + graficos + conclusoes). Basta dar duplo-clique ou rodar no cmd.
REM
REM  Argumentos extras sao repassados ao script. Exemplos:
REM     rodar_experimento.bat --limit 30
REM     rodar_experimento.bat --overwrite
REM     rodar_experimento.bat --only-agg
REM ====================================================================
setlocal
cd /d "%~dp0"

REM --- (opcional) ambiente conda. Deixe em branco para usar o python do PATH.
REM     Ex.: set CONDA_ENV=coqui-xtts
set "CONDA_ENV="

if defined CONDA_ENV (
    set "PYRUN=conda run -n %CONDA_ENV% --no-capture-output python"
) else (
    set "PYRUN=python"
)

echo ============================================================
echo  Experimento Final
echo  Pasta : %CD%
echo  Python: %PYRUN%
echo ============================================================

REM --- valida arquivos essenciais
if not exist "experimento_final.py" (
    echo [ERRO] experimento_final.py nao encontrado nesta pasta.
    pause & exit /b 1
)

REM --- instala dependencias (idempotente)
echo.
echo [1/2] Instalando dependencias (requirements.txt)...
%PYRUN% -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias. Verifique o python/conda.
    pause & exit /b 1
)

REM --- roda o pipeline (repassa argumentos: %*)
echo.
echo [2/2] Rodando o experimento...
%PYRUN% experimento_final.py %*
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
