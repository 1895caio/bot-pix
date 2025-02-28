import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Token do seu bot no Telegram
TELEGRAM_TOKEN = os.getenv('HTTP API:7126188971:AAG1btnbPclPYDTCE_riTmsPVP7PjMnX3Zg')

# Dados do PIX (você pode personalizar)
CHAVE_PIX = '30039c5d-c603-472c-82c0-3b956ccc2298'
VALOR_PIX = 'R$ 9.80'  # Valor sugerido

# Comando /start
async def start(update: Update, context: CallbackContext):
    mensagem = f"""
    Olá! Para ter acesso ao melhor grupo do telegram com mais de mil mídias totalmente selecionadas por mim, realize o pagamento via PIX para a chave:
    
    **Chave PIX:** {CHAVE_PIX}
    **Valor:** R$ {VALOR_PIX}
    
    Após o pagamento, envie o comprovante para validar o seu acesso ao grupo.
    """
    await update.message.reply_text(mensagem)

# Função para lidar com mensagens (opcional)
async def handle_message(update: Update, context: CallbackContext):
    await update.message.reply_text("Obrigado pela mensagem! Entrarei em contato assim que confirmar o pagamento.")

# Configuração do bot
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Adiciona os handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main()

