import express from "express";
import TelegramBot from "node-telegram-bot-api";
import fetch from "node-fetch";

const BOT_TOKEN = "7514736786:AAGmonV4hG06vnkmwPC-gZFIFrCKrF5CX5k";
const bot = new TelegramBot(BOT_TOKEN);
const app = express();

app.use(express.json());

bot.setWebHook(`${process.env.BASE_URL}/webhook`);

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id,
    "👋✨ *Welcome to the Ultimate Message Copier Bot!* ✨\n\n" +
    "🚀 Use /copy `<source_id>` `<destination_id>` to start copying messages!\n" +
    "💡 Make sure the bot is *admin* in both channels!",
    { parse_mode: "Markdown", reply_to_message_id: msg.message_id }
  );
});

bot.onText(/\/copy (.+)/, async (msg, match) => {
  const chatId = msg.chat.id;
  const args = match[1].split(" ");
  if (args.length !== 2) {
    return bot.sendMessage(chatId, "⚠️ Usage: `/copy <source_id> <destination_id>`", {
      parse_mode: "Markdown",
      reply_to_message_id: msg.message_id
    });
  }

  const [source, dest] = args;
  let messageId = 1;
  let empty = 0;
  const maxEmpty = 15;

  bot.sendMessage(chatId, "🔄 Copying started... Sit tight! ⏳", {
    reply_to_message_id: msg.message_id
  });

  while (empty < maxEmpty) {
    try {
      await bot.copyMessage(dest, source, messageId);
      messageId++;
      empty = 0;
    } catch (e) {
      messageId++;
      empty++;
    }
    await new Promise((r) => setTimeout(r, 300));
  }

  bot.sendMessage(chatId, "✅ Copying finished successfully! 🎉", {
    reply_to_message_id: msg.message_id
  });
});

app.post("/webhook", (req, res) => {
  bot.processUpdate(req.body);
  res.sendStatus(200);
});

app.get("/webhook", async (req, res) => {
  const url = `${req.protocol}://${req.get("host")}/webhook`;
  const response = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/setWebhook?url=${url}`);
  const data = await response.json();
  if (data.ok) res.send("✅ Webhook set successfully.");
  else res.send("❌ Failed to set webhook.");
});

export default app;
