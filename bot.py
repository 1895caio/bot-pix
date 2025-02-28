import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Token do seu bot no Telegram (lido da variável de ambiente)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Seu chat ID (obtido do @userinfobot)
ADMIN_CHAT_ID = '1861247735'  # Substitua pelo seu chat ID

# Dados do PIX
CHAVE_PIX = '30039c5d-c603-472c-82c0-3b956ccc2298'
VALOR_PIX = 'R$ 9.80'  # Valor sugerido

# Link do grupo privado
GRUPO_PRIVADO_LINK = "https://t.me/+9ZVZAUWj90diNjUx"  # Substitua pelo link real do seu grupo

# Dicionário para armazenar usuários que enviaram comprovantes
pendentes = {}

# Comando /start
async def start(update: Update, context: CallbackContext):
    mensagem = f"""
    Olá! Para ter acesso ao melhor grupo do Telegram, realize o pagamento via PIX:

    **Chave PIX:** {CHAVE_PIX}
    **Valor:** {VALOR_PIX}

    Após o pagamento, envie o comprovante aqui para validar seu acesso ao grupo.
    """
    await update.message.reply_text(mensagem)

# Função para lidar com mensagens e comprovantes
async def handle_message(update: Update, context: CallbackContext):
    user_chat_id = update.message.chat_id
    user_name = update.message.from_user.full_name

    # Armazena o usuário na lista de pendentes
    pendentes[user_chat_id] = user_name

    # Notifica o administrador
    mensagem_admin = f"Novo comprovante recebido!\n\nNome: {user_name}\nID do usuário: {user_chat_id}\n\nPara confirmar o pagamento, envie o comando:\n\n`/aprovar {user_chat_id}`"
    
    if update.message.photo:
        # Se for uma imagem, pega a maior resolução disponível
        file_id = update.message.photo[-1].file_id
        await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=file_id, caption=mensagem_admin, parse_mode="Markdown")
    else:
        # Se for um texto
        mensagem_admin += f"\n\nMensagem: {update.message.text}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensagem_admin, parse_mode="Markdown")

    # Responde ao usuário
    await update.message.reply_text("Seu comprovante foi enviado para análise. Aguarde a confirmação do pagamento.")

# Função para aprovar pagamento e enviar link
async def aprovar(update: Update, context: CallbackContext):
    # Verifica se o administrador enviou o comando corretamente
    if len(context.args) != 1:
        await update.message.reply_text("Uso correto: /aprovar <ID do usuário>")
        return

    user_chat_id = int(context.args[0])

    # Verifica se o usuário está na lista de pendentes
    if user_chat_id in pendentes:
        # Envia o link do grupo para o usuário
        await context.bot.send_message(chat_id=user_chat_id, text=f"✅ Pagamento confirmado! Aqui está seu acesso ao grupo:\n{GRUPO_PRIVADO_LINK}")

        # Remove o usuário da lista de pendentes
        del pendentes[user_chat_id]

        # Confirmação para o administrador
        await update.message.reply_text(f"Usuário {user_chat_id} aprovado com sucesso!")
    else:
        await update.message.reply_text("Usuário não encontrado na lista de pendentes.")

# Configuração do bot
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Adiciona os handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
    application.add_handler(CommandHandler("aprovar", aprovar))

    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main()
