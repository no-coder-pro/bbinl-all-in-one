# 🤖 Multi-Feature Telegram Bot

A powerful Telegram bot with multiple utilities including card generation, translation, AI chat, image processing, and more!

---

## 🌟 Features Overview

### 💳 Card Generation & Checking
- **Generate Cards** — Create test cards from BIN numbers.
- **Single Card Check** — Validate an individual card.
- **Mass Check** — Bulk validation of card lists.
- **BIN Information** — Get detailed bank and country info.

### 🤖 AI & Chat Features
- **Gemini AI** — Chat with Google's Gemini AI.
- **GPT Integration** — Optional ChatGPT integration.
- **Grok & Deepseek** — Advanced AI chat models.
- **Auto-Reply** — Enable/disable AI auto-responses.

### 🌐 Translation & Communication
- **Multi-Language Translation** — Translate text to any language.
- **Text-to-Speech** — Convert text to audio.
- **Say Command** — Generate speech from text.

### 🎨 Image & Media Processing
- **Background Removal** — Remove backgrounds from images.
- **Image Generation** — Create AI-generated images.
- **Image Editing** — Edit images using prompts.
- **Media Download** — Download content from various platforms.

### 📊 Information & User Features
- **User Information** — Get detailed info about Telegram users, bots, groups, and channels.
- **Advanced User Lookup** — Multiple methods to fetch user data including usernames and IDs.
- **Group Analysis** — Detailed group and channel information retrieval.

### 🛠️ Utility Features
- **Fake Address Generators** — Generate test addresses for various countries.
- **IBAN Generation** — Create valid IBAN numbers for various countries.
- **Spam Generation** — Text spam and file generation tools (use responsibly).
- **Weather Information** — Real-time weather, forecasts, and air quality data.
- **File Management** — Download and process files.

---

## 📋 Command Reference (for BotFather)

### 🔹 AI & Chat Commands
- `/arise` — Start the bot.
- `/start` — Start the bot.
- `/gemini` — Chat with Gemini AI. Example: `/gemini r u gemini?`.
- `/gpt` — Chat with ChatGPT. Example: `/gpt r u chatgpt?`.
- `/grok` — Chat with Grok AI.
- `/deepseek` — Chat with Deepseek AI.

### 🔹 Media & Image Commands
- `/yt` — Search and download YouTube videos. Example: `/yt Sajjad Ali` or `/yt https://youtu.be/video_id`.
- `/dl` — Download videos from YouTube, Facebook & Instagram. Example: `/dl https://youtu.be/video_id`.
- `/imagine` — Generate images with AI. Example: `/imagine a cat with sunglasses`.
- `/gmeg` — Generate images with Gemini AI. Example: `/gmeg a cat sitting on a moon`.
- `/bgremove` — Remove background from a photo (reply to a photo).
- `/enh` — Enhance face in a photo (reply to a photo).
- `/pfp` — Download Facebook/Instagram profile pictures. Example: `/pfp https://www.facebook.com/...`.
- `/edit` — Edit an image using a prompt (reply to a photo). Example: `/edit a cat with sunglasses`.

### 🔹 Card & Banking Commands
- `/gen` — Generate cards with BIN. Example: `/gen 515462xxxxxx|02|28|573 5`.
- `/chk` — Check a single card. Example: `/chk 4000123456789012|12|25|123`.
- `/mas` — Check multiple cards at once (reply to a list of cards).
- `/b3` — Check card using B3 gateway. Example: `/b3 4000123456789012|12|25|123`.
- `/mb3` — Check multiple cards using B3 gateway.
- `/bin` — Get detailed BIN information. Example: `/bin 426633`.
- `/iban` — Generate IBAN for various countries. Example: `/iban DE`.
- `/ibncntry` — See list of supported IBAN countries.

### 🔹 Info & Utility Commands
- `/info` — Get user, bot, group, or channel info. Example: `/info @username`.
- `/fake` — Generate fake address. Example: `/fake US`.
- `/country` — See list of supported countries for fake address.
- `/wth` — Get weather information. Example: `/wth Faridpur`.
- `/translate` — Translate any text. Example: `/translate fr Hello World`.
- `/say` — Convert text to voice message. Example: `/say Hello World`.
- `/bomb` — Send SMS spam to a phone number. Example: `/bomb 01712345678`.
- `/spam` — Send spam text messages. Example: `/spam Hello World`.
- `/spmtxt` — Create a text file for spamming. Example: `/spmtxt 100 Hello World`.
- `/reveal` — Show a list of all commands.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- Required API keys for various services

### Installation on Replit
1. **Fork this Repl** or create a new Python Repl.
2. **Install Dependencies**: Dependencies will be automatically installed from `requirements.txt`.
3. **Set Environment Variables**: Use Replit Secrets to configure:

```
BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

4. **Run the Bot**: Click the Run button or use `python main.py`.

### Configuration
Add these secrets in your Replit environment as shown above.

---

## 📁 Project Structure

```
├── handlers/                     # Command handlers
│   ├── gen_handler.py            # Card generation
│   ├── chk_handler.py            # Card checking and mass validation
│   ├── bin_handler.py            # BIN information lookup
│   ├── translate_handler.py      # Multi-language translation
│   ├── gemini_handler.py         # Google Gemini AI chat
│   ├── gpt_handler.py            # GPT AI integration
│   ├── say_handler.py            # Text-to-speech conversion
│   ├── bgremove_handler.py       # Background removal from images
│   ├── imagine_handler.py        # AI image generation
│   ├── gart_handler.py           # AI artwork generation
│   ├── userinfo_handler.py       # User/bot/group/channel info
│   ├── fakeAddress_handler.py    # Fake address generation (FakeXYZ)
│   ├── fakeAddress2_handler.py   # Alternative fake addresses
│   ├── fakeAddress3_handler.py   # Third fake address source
│   ├── iban_handler.py           # IBAN generation
│   ├── spam_handler.py           # Spam generation tools
│   ├── wth_handler.py            # Weather information
│   ├── yt_handler.py             # YouTube operations
│   ├── download_handler.py       # Media download
│   ├── start_handler.py          # Welcome messages
│   └── reveal_handler.py         # Command list display
├── main.py                       # Main bot file with Flask server
├── cleanup.py                    # Cleanup utilities
├── flag_data.py                  # Country flags data
├── requirements.txt              # Python dependencies (including FakeXYZ)
└── README.md                     # Documentation
```

---

## ⚠️ Important Notes

### Card Generation Limits
- ✅ Only **Visa (4xxx)** and **MasterCard (5xxx)** BINs supported.
- ⛔ American Express, Discover not supported.
- 🔢 Maximum 30 cards per request.
- ⚠️ Cards are for **testing purposes only**.

### API Rate Limits
- Some features may have rate limits depending on external APIs.
- The bot includes fallback mechanisms for reliability.

### Privacy & Security
- Chat histories are stored locally for AI continuity.
- No sensitive data is permanently stored.
- Use responsibly and follow Telegram's ToS.

---

## 🛠️ Development

### Adding New Features
1. Create a new handler file in `handlers/`.
2. Import and register it in `handlers/__init__.py`.
3. Add registration call in `main.py`.

### Contributing
1. Fork the project.
2. Create a feature branch.
3. Make your changes.
4. Test thoroughly.
5. Submit a pull request.

---

## 📞 Support & Links
- **Telegram**: @no_coder_pro
- **Channel**: https://t.me/bro_bin_lagbe
- **Issues**: Report bugs and request features via the Telegram contact above.
- **Documentation**: See this README file.

---

## 🙏 Credits & Acknowledgments
This bot utilizes several external libraries and services:

- **FakeXYZ Library**: Custom Python library for generating realistic fake address data used in the `/fake` commands.
- **Google Gemini AI**: Advanced AI chat capabilities.
- **OpenAI GPT**: Alternative AI integration.
- **pyTelegramBotAPI**: Core Telegram bot framework.
- **Various APIs**: Weather, BIN lookup, and media download services.

Special thanks to all the open-source libraries and API providers that make this bot possible.

---

## 📄 License
This project is for educational purposes only. Use responsibly and in accordance with all applicable laws and terms of service.

---

## 🔄 Recent Updates
- ✅ Enhanced card generation with multiple fallback APIs.
- ✅ Improved BIN information accuracy.
- ✅ Added translation capabilities.
- ✅ Integrated AI chat features.
- ✅ Background removal functionality.
- ✅ Added comprehensive user information commands.
- ✅ Multiple fake address generators.
- ✅ Weather and YouTube integration.
- ✅ IBAN and spam generation tools.

---

**Happy Botting!** 🤖

*Built with ❤️ for the Telegram community*

