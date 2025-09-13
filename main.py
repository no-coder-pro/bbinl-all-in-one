import telebot
import os
from flask import Flask
from threading import Thread
import cleanup
import string
import logging

# Handlers import
from handlers import (
    start_handler,
    bgremove_handler,
    gen_handler,
    chk_handler,
    bin_handler,
    reveal_handler,
    gemini_handler,
    gmeg_handler,
    imagine_handler,
    say_handler,
    translate_handler,
    download_handler,
    gpt_handler,
    fakeAddress_handler,
    fakeAddress2_handler,
    fakeAddress3_handler,
    userinfo_handler,
    yt_handler,
    spam_handler,
    iban_handler,
    wth_handler
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ Error: BOT_TOKEN environment variable is not set!")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

COMMAND_PREFIXES = list(string.punctuation)

def custom_command_handler(command_name):
    def decorator(handler_func):
        @bot.message_handler(func=lambda message: message.text and any(
            message.text.lower().startswith(f"{prefix}{command_name}") for prefix in COMMAND_PREFIXES
        ))
        def wrapper(message):
            return handler_func(message)
        return wrapper
    return decorator

app = Flask('')

# Custom logging filter to suppress health check spam
class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        # Suppress logs for /api health check requests
        if hasattr(record, 'getMessage'):
            message = record.getMessage()
            if 'HEAD /api' in message and '404' in message:
                return False
        return True

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 5000))
    # Apply the filter to suppress health check spam
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.addFilter(HealthCheckFilter())
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

def register_handler(handler_module, handler_name):
    try:
        handler_module.register(bot, custom_command_handler, COMMAND_PREFIXES)
        print(f"✅ {handler_name} handler loaded successfully")
    except Exception as e:
        print(f"❌ {handler_name} handler failed to load: {str(e)}")

print("\n🔄 Loading command handlers...")
print("-" * 40)

# Register all handlers
register_handler(start_handler, "Start")
register_handler(gen_handler, "Gen")
register_handler(chk_handler, "Check")
register_handler(bin_handler, "BIN")
register_handler(reveal_handler, "Reveal")
register_handler(gemini_handler, "Gemini")
register_handler(gmeg_handler, "gmeg")
register_handler(imagine_handler, "Imagine")
register_handler(say_handler, "Say")
register_handler(translate_handler, "Translate")
register_handler(download_handler, "Download")
register_handler(bgremove_handler, "BG Remove")
register_handler(gpt_handler, "GPT")
register_handler(fakeAddress_handler, "Fake Address")
register_handler(fakeAddress2_handler, "Fake Address2")
register_handler(fakeAddress3_handler, "Fake Address3")
register_handler(userinfo_handler, "User Info")
register_handler(yt_handler, "yt")
register_handler(spam_handler, "spam")
register_handler(iban_handler, "iban")
register_handler(wth_handler, "weather")


print("-" * 40)
print("✨ Handler registration completed!\n")

cleanup.cleanup_project()

if __name__ == '__main__':
    print("🤖 Bot is running...")
    bot.infinity_polling()
