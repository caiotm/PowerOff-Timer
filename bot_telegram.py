import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import tkinter as tk
import os
import sys

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot de desligamento online. Envie /desligar_em 30 ou /cancelar.")

async def desligar_em(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        minutos = int(context.args[0])
        # Escreve em um arquivo temporário para comunicar com o processo principal
        with open("comando_bot.txt", "w") as f:
            f.write(f"START {minutos}")
        await update.message.reply_text(f"Desligamento agendado para {minutos} minutos.")
    except:
        await update.message.reply_text("Erro: use /desligar_em <minutos>")

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("comando_bot.txt", "w") as f:
        f.write("CANCEL")
    await update.message.reply_text("Desligamento cancelado.")

async def main():
    app = ApplicationBuilder().token("6475033114:AAHXcfd2sgf5-NsP5smlSjgtEpJ7PZ1JW_g").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("desligar_em", desligar_em))
    app.add_handler(CommandHandler("cancelar", cancelar))
    print("Bot do Telegram rodando...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
