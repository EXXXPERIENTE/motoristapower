# enviar_pendentes.py
import json
import os
from datetime import datetime


def enviar_pendentes_com_internet():
    """
    Envia todas as notificações pendentes quando tiver internet
    """
    print("📱 ENVIANDO NOTIFICAÇÕES PENDENTES")
    print("=" * 50)

    notificacoes_file = "notificacoes_pendentes.json"

    if not os.path.exists(notificacoes_file):
        print("❌ Nenhuma notificação pendente encontrada")
        return

    with open(notificacoes_file, "r", encoding="utf-8") as f:
        notificacoes = json.load(f)

    pendentes = [n for n in notificacoes if not n.get("enviada", False)]

    if not pendentes:
        print("✅ Todas as notificações já foram enviadas")
        return

    print(f"📊 Encontrando {len(pendentes)} notificação(ões) pendente(s)")
    print("")

    for i, notificacao in enumerate(pendentes, 1):
        print(f"📨 ENVIANDO {i}/{len(pendentes)}:")
        print(f"👤 Motorista: {notificacao['motorista']}")
        print(f"📅 Data: {notificacao['data_hora']}")
        print("💬 Mensagem:")
        print(notificacao['mensagem'])
        print("-" * 40)

        # ✅ AQUI VOCÊ PODE ADICIONAR O CÓDIGO DO WHATSAPP REAL
        # quando tiver internet funcionando
        try:
            # Simular envio (substitua por código real quando tiver internet)
            print("✅ SIMULAÇÃO: Mensagem seria enviada agora")

            # Marcar como enviada
            for n in notificacoes:
                if (n['motorista'] == notificacao['motorista'] and
                        n['data_hora'] == notificacao['data_hora']):
                    n['enviada'] = True
                    n['data_envio'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        except Exception as e:
            print(f"❌ Erro ao enviar: {e}")

    # Salvar atualizações
    with open(notificacoes_file, "w", encoding="utf-8") as f:
        json.dump(notificacoes, f, ensure_ascii=False, indent=2)

    print("")
    print("🎉 PROCESSO CONCLUÍDO!")
    print(f"✅ {len(pendentes)} notificação(ões) processada(s)")
    print("=" * 50)


if __name__ == "__main__":
    enviar_pendentes_com_internet()