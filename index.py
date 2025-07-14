from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

BOT_TOKEN = "7861791032:AAEzLb7ezn65pXKydI_D_yYWX6oCiR004WU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👋✨ *Welcome to the Ultimate Message Copier Bot!* ✨\n\n"
             "🚀 Use /copy `<source_id>` `<destination_id>` to start copying messages!\n"
             "💡 Make sure the bot is *admin* in both channels!",
        parse_mode="Markdown",
        reply_to_message_id=update.message.message_id
    )

async def start_copy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Usage: `/copy <source_id> <destination_id>`",
            parse_mode="Markdown",
            reply_to_message_id=update.message.message_id
        )
        return

    source_channel = context.args[0]
    destination_channel = context.args[1]

    try:
        source_admin = await context.bot.get_chat_member(source_channel, context.bot.id)
        dest_admin = await context.bot.get_chat_member(destination_channel, context.bot.id)
        if source_admin.status not in ['administrator', 'creator'] or dest_admin.status not in ['administrator', 'creator']:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ The bot must be *admin* in both channels!\n\n🛠️ Please promote the bot and try again.",
                parse_mode="Markdown",
                reply_to_message_id=update.message.message_id
            )
            return
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Unable to access one of the channels. Make sure the bot is added and promoted!",
            reply_to_message_id=update.message.message_id
        )
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🔄 Copying started... Sit tight! ⏳",
        reply_to_message_id=update.message.message_id
    )

    message_id = 1
    empty_count = 0
    max_empty = 15

    while empty_count < max_empty:
        try:
            await context.bot.copy_message(
                chat_id=destination_channel,
                from_chat_id=source_channel,
                message_id=message_id
            )
            message_id += 1
            empty_count = 0
            await asyncio.sleep(0.3)
        except:
            message_id += 1
            empty_count += 1

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="✅ Copying finished successfully! 🎉",
        reply_to_message_id=update.message.message_id
    )

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("copy", start_copy))
print("Bot is running...")
app.run_polling()
