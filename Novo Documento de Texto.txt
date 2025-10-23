@echo off
REM Ativar venv automaticamente
call venv\Scripts\activate
title 🚀 Deploy Automático - MotoristaPower
color 0A

echo.
echo ========================================
echo    🚀 DEPLOY AUTOMÁTICO - MOTORISTAPOWER
echo ========================================
echo.

REM ➡️ Configurações
set PROJECT_NAME=MotoristaPower
set RAILWAY_URL=https://web-production-336e0.up.railway.app
set GITHUB_URL=https://github.com/EXXXPERIENTE/motoristapower

REM ➡️ Verificar se está no ambiente virtual
echo 🔍 Verificando ambiente virtual...
python -c "import sys; print('✅ Python: ' + sys.version)" >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado ou venv não ativado!
    echo 💡 Execute: venv\Scripts\activate
    pause
    exit /b 1
)

REM ➡️ Verificar se é pasta git
if not exist ".git" (
    echo ❌ ERRO: Não é uma pasta Git!
    echo 💡 Certifique-se de estar na pasta do projeto
    pause
    exit /b 1
)

REM ➡️ Verificar mudanças
echo 📊 Verificando mudanças...
git status --porcelain >nul 2>&1
if errorlevel 1 (
    echo ℹ️  Nenhuma mudança para commitar.
    set /p deploy_anyway="💡 Deseja fazer deploy mesmo assim? (s/n): "
    if /i not "%deploy_anyway%"=="s" (
        echo ❌ Deploy cancelado.
        pause
        exit /b 0
    )
)

REM ➡️ Mensagem do commit
echo.
set /p commit_msg="💬 Mensagem do commit: "
if "%commit_msg%"=="" (
    echo ❌ Mensagem do commit é obrigatória!
    pause
    exit /b 1
)

REM ➡️ Opção de teste local
echo.
set /p test_local="🧪 Testar localmente antes do deploy? (s/n): "
if /i "%test_local%"=="s" (
    echo 🔄 Iniciando servidor local...
    echo 💡 Pressione CTRL+C para parar o servidor e continuar o deploy
    timeout /t 3 >nul
    python manage.py runserver
    echo.
    set /p continuar="✅ Continuar com deploy? (s/n): "
    if /i not "%continuar%"=="s" (
        echo ❌ Deploy cancelado pelo usuário.
        pause
        exit /b 0
    )
)

REM ➡️ Executar deploy
echo.
echo 🚀 INICIANDO DEPLOY...
echo 📤 Adicionando arquivos...
git add .

echo 💾 Criando commit...
git commit -m "%commit_msg%"

echo 📡 Fazendo push...
git push

REM ➡️ Resultado
echo.
echo ========================================
echo           ✅ DEPLOY INICIADO!
echo ========================================
echo.
echo 📋 INFORMAÇÕES:
echo    📝 Commit: %commit_msg%
echo    🌐 Site: %RAILWAY_URL%
echo    📊 Monitor: https://railway.app
echo    🐙 Repo: %GITHUB_URL%
echo.
echo ⏰ O deploy automático levará 2-3 minutos
echo 🔍 Acesse Railway → Deployments para ver o progresso
echo.

REM ➡️ Abrir links no navegador (opcional)
set /p abrir_links="🌐 Abrir links no navegador? (s/n): "
if /i "%abrir_links%"=="s" (
    start "" "%RAILWAY_URL%"
    start "" "https://railway.app"
)

echo.
echo 🎯 Pressione qualquer tecla para fechar...
pause >nul