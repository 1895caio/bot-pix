import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Token do seu bot no Telegram
TELEGRAM_TOKEN = 'HTTP API:7126188971:AAG1btnbPclPYDTCE_riTmsPVP7PjMnX3Zg'

# Dados do PIX (você pode personalizar)
CHAVE_PIX = '30039c5d-c603-472c-82c0-3b956ccc2298'
VALOR_PIX = 'R$9.90'  # Valor sugerido

# Comando /start
def start(update: Update, context: CallbackContext):
    mensagem = f"""
    Olá! Para acessar o melhor grupo privado, com mais de 1000 mídias selecionadas realize o pagamento via PIX para a chave:
    
    **Chave PIX:** {CHAVE_PIX}
    **Valor:** R$ {VALOR_PIX}
    
    Após o pagamento, enviar o comprovante para ter acesso ao melhor grupo do telegram.
    """
    update.message.reply_text(mensagem)

# Função para lidar com mensagens (opcional)
def handle_message(update: Update, context: CallbackContext):
    update.message.reply_text("Obrigado pela mensagem! Entrarei em contato assim que confirmar o pagamento.")

# Configuração do bot
def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Adiciona os handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Inicia o bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
