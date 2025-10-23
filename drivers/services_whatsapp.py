# drivers/services_whatsapp.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import os


def enviar_whatsapp_real(nome_motorista):
    """
    Envia mensagem REAL para seu WhatsApp - VERSAO CORRIGIDA
    """
    driver = None
    try:
        print("")
        print("📱 INICIANDO ENVIO WHATSAPP REAL...")
        print("=" * 60)

        # ✅ CONFIGURAR CHROME - VERSAO SIMPLIFICADA
        chrome_options = Options()

        # NOVO: Re-introduzir modo headless para rodar em servidores (sem GUI)
        chrome_options.add_argument("--headless") # ← RE-INSERIDO

        # Configurações básicas
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1200,800")

        # Diretório para salvar sessão (evita scan repetido)
        session_dir = os.path.join(os.getcwd(), 'whatsapp_session')
        os.makedirs(session_dir, exist_ok=True)
        chrome_options.add_argument(f"--user-data-dir={session_dir}")
        chrome_options.add_argument("--profile-directory=Default")

        print("🚀 Iniciando Chrome...")

        # ✅ INICIAR CHROME - VERSAO SIMPLES
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        print("✅ Chrome iniciado com sucesso!")
        print("🌐 Abrindo WhatsApp Web...")

        # ✅ ABRIR WHATSAPP WEB
        driver.get("https://web.whatsapp.com")

        # Aguardar carregamento
        wait = WebDriverWait(driver, 60)  # 60 segundos para QR Code

        print("⏳ Aguardando autenticação...")
        print("")
        print("📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱")
        print("🚨 IMPORTANTE: ESCANEIE O QR CODE NO NAVEGADOR!")
        print("📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱 📱")
        print("")
        print("💡 Dica: Marque 'Manter conectado' para evitar scans futuros")
        print("⏰ Você tem 60 segundos para escanear...")

        # ✅ AGUARDAR ATÉ ESTAR LOGADO
        try:
            search_box = wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            print("")
            print("✅ ✅ ✅ WhatsApp Web logado com sucesso! ✅ ✅ ✅")

        except Exception as e:
            print("")
            print("❌ ❌ ❌ Timeout - QR Code não escaneado em 60 segundos ❌ ❌ ❌")
            print("💡 Dica: Execute novamente e escaneie mais rápido")
            driver.quit()
            return False

        # ✅ BUSCAR CONVERSA
        print("🔍 Buscando conversa 'Eu'...")
        search_box.clear()
        search_box.send_keys("Eu")

        time.sleep(3)

        # ✅ CLICAR NA CONVERSA
        try:
            chat = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//span[@title="Eu"]'))
            )
            chat.click()
            print("✅ Conversa 'Eu' selecionada!")

        except Exception as e:
            print("❌ Conversa 'Eu' não encontrada")
            print("💡 Verifique se tem uma conversa com você mesmo")
            driver.quit()
            return False

        time.sleep(2)

        # ✅ ENCONTRAR CAIXA DE MENSAGEM
        print("⌨️  Procurando caixa de mensagem...")
        try:
            message_box = wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            print("✅ Caixa de mensagem encontrada!")

        except Exception as e:
            print("❌ Caixa de mensagem não encontrada")
            driver.quit()
            return False

        # ✅ MENSAGEM FORMATADA
        mensagem = (
            f"🚗 *NOVO MOTORISTA CADASTRADO!*\n\n"
            f"👤 *Nome:* {nome_motorista}\n"
            f"📅 *Data:* {datetime.now().strftime('%d/%m/%Y')}\n"
            f"⏰ *Hora:* {datetime.now().strftime('%H:%M:%S')}\n\n"
            f"🔔 *Sistema:* MotoristaPower\n"
            f"_Cadastro automático_"
        )

        print("💬 Digitando mensagem...")
        message_box.send_keys(mensagem)
        time.sleep(2)

        # ✅ ENVIAR MENSAGEM
        print("📤 Enviando mensagem...")
        try:
            send_button = driver.find_element(By.XPATH, '//button[@data-tab="11"]')
            send_button.click()
            print("✅ Mensagem enviada com sucesso!")

        except Exception as e:
            print("❌ Botão enviar não encontrado, tentando com ENTER...")
            from selenium.webdriver.common.keys import Keys
            message_box.send_keys(Keys.ENTER)
            print("✅ Mensagem enviada com ENTER!")

        # ✅ CONFIRMAR ENVIO
        time.sleep(5)

        # ✅ FECHAR NAVEGADOR
        print("🔒 Fechando navegador...")
        driver.quit()

        print("")
        print("🎉 🎉 🎉 WHATSAPP ENVIADO COM SUCESSO! 🎉 🎉 🎉")
        print("=" * 60)
        print("")

        return True

    except Exception as e:
        print(f"❌ ERRO: {e}")

        if driver:
            try:
                driver.quit()
            except:
                pass

        return False


def testar_whatsapp():
    """
    Teste manual do WhatsApp
    """
    print("🧪 TESTE MANUAL DO WHATSAPP")
    print("=" * 60)
    resultado = enviar_whatsapp_real("TESTE MANUAL - Motorista")

    if resultado:
        print("🎉 SUCESSO! WhatsApp funcionando!")
    else:
        print("💥 FALHA! Verifique as mensagens acima.")

    return resultado


if __name__ == "__main__":
    testar_whatsapp()