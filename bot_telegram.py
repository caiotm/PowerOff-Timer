import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

nest_asyncio.apply()  # Permite reentrância do loop de eventos

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Comando /start recebido!")
    await update.message.reply_text("Bot de desligamento online. Envie /desligar_em 30 ou /cancelar.")

async def desligar_em(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        minutos = int(context.args[0])
        with open("comando_bot.txt", "w") as f:
            f.write(f"START {minutos}")
        await update.message.reply_text(f"Desligamento agendado para {minutos} minutos.")
    except Exception as e:
        print(f"Erro no comando desligar_em: {e}")
        await update.message.reply_text("Erro: use /desligar_em <minutos>")

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("comando_bot.txt", "w") as f:
        f.write("CANCEL")
    await update.message.reply_text("Desligamento cancelado.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Erro: {context.error}")

async def main():
    app = ApplicationBuilder().token("SEU_TOKEN_AQUI").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("desligar_em", desligar_em))
    app.add_handler(CommandHandler("cancelar", cancelar))
    app.add_error_handler(error_handler)
    print("Bot do Telegram rodando...")
    await app.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
