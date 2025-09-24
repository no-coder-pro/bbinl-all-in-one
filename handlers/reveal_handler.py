def register(bot, custom_command_handler, command_prefixes_list):
    @custom_command_handler("reveal")
    @custom_command_handler("help")
    def show_help(message):
        user = message.from_user
        username = f"@{user.username}" if user.username else user.first_name

        help_text = (
            "🛠 <b>Available Commands:</b>\n\n"
            "🔸 <b>AI & Chat</b>\n"
            "<code>/gemini</code> — Chat with Gemini AI\n"
            "<code>/gpt</code> — Chat with GPT AI\n"
            "<code>/grok</code> — Chat with Grok AI\n"
            "<code>/deepseek</code> — Chat with Deepseek AI\n\n"

            "🔸 <b>Media & Image Tools</b>\n"
            "<code>/yt</code> — Search & download YouTube videos\n"
            "<code>/dl</code> — Download videos from YouTube, Facebook & Instagram\n"
            "<code>/imagine</code> — Generate images with AI\n"
            "<code>/gmeg</code> — Generate images with Gemini AI\n"
            "<code>/bgremove</code> — Remove image background\n"
            "<code>/enh</code> — Enhance face in photos\n"
            "<code>/pfp</code> — Download Facebook/Instagram profile pictures\n"
            "<code>/edit</code> — Edit images using a prompt\n\n"

            "🔸 <b>Card & Banking Tools</b>\n"
            "<code>/gen</code> — Generate cards with BIN\n"
            "<code>/chk</code> — Check a single card\n"
            "<code>/mas</code> — Check multiple cards at once\n"
            "<code>/b3</code> — Check cards using B3 gateway\n"
            "<code>/mb3</code> — Check multiple cards using B3 gateway\n"
            "<code>/bin</code> — Get detailed BIN info\n"
            "<code>/iban</code> — Generate IBAN for various countries\n"
            "<code>/ibncntry</code> — See supported IBAN countries\n\n"

            "🔸 <b>Info & Utility</b>\n"
            "<code>/info</code> — Get user, bot, group, or channel info\n"
            "<code>/fake</code> — Generate fake addresses\n"
            "<code>/country</code> — See supported countries for fake addresses\n"
            "<code>/wth</code> — Get weather info\n"
            "<code>/translate</code> — Translate any text\n"
            "<code>/say</code> — Convert text to voice message\n"
            "<code>/bomb</code> — Send SMS spam to a phone number\n"
            "<code>/spam</code> — Send spam text messages\n"
            "<code>/spmtxt</code> — Create a text file for spamming\n\n"

            "🔸 <b>Other</b>\n"
            "<code>/start</code> — See the welcome message\n"
            "<code>/reveal</code> — Show all commands\n"
            "<code>/help</code> — Show all commands\n\n"

            "🔸 <b>বিশেষ দ্রষ্টব্য:</b> আপনি !, #, ', অথবা অন্য যেকোনো চিহ্ন দিয়েও কমান্ড চালাতে পারবেন।\n"
            f"\n👤 <i>Revealed by:</i> {username}"
        )

        bot.reply_to(message, help_text, parse_mode="HTML")
