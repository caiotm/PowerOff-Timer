import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

nest_asyncio.apply()  # Permite reentrância do loop de eventos

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Comando /start recebido!")
    await update.message.reply_text(
        "👋 Olá! Eu sou o Bot Desligador — pronto para ajudar você a controlar o desligamento do seu PC remotamente.\n\n"
        "Aqui estão meus comandos:\n\n"
        "🕒 /desligar_em <minutos>\n"
        "Agende o desligamento do computador. Ex: /desligar_em 30\n\n"
        "⚡ /desligar\n"
        "Desliga o computador em 10 segundos.\n\n"
        "❌ /cancelar\n"
        "Cancele o desligamento agendado."
    )

async def desligar_em(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        minutos = int(context.args[0])
        with open("comando_bot.txt", "w") as f:
            f.write(f"START {minutos}")
        await update.message.reply_text(f"Desligamento agendado para {minutos} minutos.")
    except Exception as e:
        print(f"Erro no comando desligar_em: {e}")
        await update.message.reply_text("Erro: use /desligar_em <minutos>")

async def desligar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("comando_bot.txt", "w") as f:
            f.write("START 0.166")  # ~10 segundos
        await update.message.reply_text("⚠️ O computador será desligado em 10 segundos. Use /cancelar para impedir.")
    except Exception as e:
        print(f"Erro no comando desligar: {e}")
        await update.message.reply_text("Erro ao tentar desligar o computador.")

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("comando_bot.txt", "w") as f:
        f.write("CANCEL")
    await update.message.reply_text("❌ Desligamento cancelado.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Erro: {context.error}")

async def main():
    app = ApplicationBuilder().token("7958716518:AAG6MJMiMDGb_s2QghcsmDQwlXEQKBAR0HE").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("desligar_em", desligar_em))
    app.add_handler(CommandHandler("desligar", desligar))
    app.add_handler(CommandHandler("cancelar", cancelar))
    app.add_error_handler(error_handler)
    print("Bot do Telegram rodando...")
    await app.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
