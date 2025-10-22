@echo off
echo # teste_simples.py > teste_simples.py
echo print('🧪 TESTE SIMPLES DO SELENIUM') >> teste_simples.py
echo. >> teste_simples.py
echo try: >> teste_simples.py
echo     from selenium import webdriver >> teste_simples.py
echo     from selenium.webdriver.chrome.service import Service >> teste_simples.py
echo     from selenium.webdriver.chrome.options import Options >> teste_simples.py
echo     from webdriver_manager.chrome import ChromeDriverManager >> teste_simples.py
echo. >> teste_simples.py
echo     print('✅ Selenium importado com sucesso!') >> teste_simples.py
echo. >> teste_simples.py
echo     # Teste básico do Chrome >> teste_simples.py
echo     chrome_options = Options() >> teste_simples.py
echo     chrome_options.add_argument('--no-sandbox') >> teste_simples.py
echo     chrome_options.add_argument('--disable-dev-shm-usage') >> teste_simples.py
echo. >> teste_simples.py
echo     print('🚀 Iniciando Chrome...') >> teste_simples.py
echo     driver = webdriver.Chrome( >> teste_simples.py
echo         service=Service(ChromeDriverManager().install()), >> teste_simples.py
echo         options=chrome_options >> teste_simples.py
echo     ) >> teste_simples.py
echo. >> teste_simples.py
echo     print('✅ Chrome iniciado!') >> teste_simples.py
echo     print('🌐 Abrindo Google...') >> teste_simples.py
echo     driver.get('https://www.google.com') >> teste_simples.py
echo     print('✅ Google carregado!') >> teste_simples.py
echo     print(f'📄 Título: {driver.title}') >> teste_simples.py
echo. >> teste_simples.py
echo     driver.quit() >> teste_simples.py
echo     print('🎉 TESTE CONCLUÍDO COM SUCESSO!') >> teste_simples.py
echo. >> teste_simples.py
echo except Exception as e: >> teste_simples.py
echo     print(f'❌ ERRO: {e}') >> teste_simples.py
echo     print('💡 Possíveis soluções:') >> teste_simples.py
echo     print('1. Verifique se o Chrome está instalado') >> teste_simples.py
echo     print('2. Execute: pip install selenium webdriver-manager') >> teste_simples.py
echo     print('3. Execute como administrador') >> teste_simples.py