def register(bot, custom_command_handler, command_prefixes_list):
    @custom_command_handler("reveal")
    @custom_command_handler("help")
    def show_help(message):
        user = message.from_user
        username = f"@{user.username}" if user.username else user.first_name

        help_text = (
            "🛠 <b>Available Commands:</b>\n\n"
            "🔸 <b>AI & Chat</b>\n"
            "<code>/gemini</code> — Chat with Gemini AI. Example: <code>/gemini What is AI?</code>\n"
            "<code>/gpt</code> — Chat with GPT AI. Example: <code>/gpt How does a car work?</code>\n"
            "<code>/grok</code> — Chat with Grok AI. Example: <code>/grok What is a computer?</code>\n"
            "<code>/deepseek</code> — Chat with Deepseek AI. Example: <code>/deepseek Tell me a story.</code>\n"
            "<code>/ongem</code>, <code>/offgem</code> — Toggle Gemini auto-reply. (Admins only)\n"
            "<code>/ongpt</code>, <code>/offgpt</code> — Toggle GPT auto-reply. (Admins only)\n"
            "<code>/ongrok</code>, <code>/offgrok</code> — Toggle Grok auto-reply. (Admins only)\n"
            "<code>/ondeepseek</code>, <code>/offdeepseek</code> — Toggle Deepseek auto-reply. (Admins only)\n"
            "<code>/reset_gpt</code> — Reset GPT chat history.\n"
            "<code>/reset_grok</code> — Reset Grok chat history.\n"
            "<code>/reset_deepseek</code> — Reset Deepseek chat history.\n\n"

            "🔸 <b>Media & Image Tools</b>\n"
            "<code>/yt</code> — Search & download YouTube videos. Example: <code>/yt funny cat videos</code> or <code>/yt https://youtu.be/id</code>\n"
            "<code>/dl</code> — Download videos from YT, FB & Insta. Example: <code>/dl https://youtu.be/id</code>\n"
            "<code>/imagine</code> — Generate images with AI. Example: <code>/imagine a red dragon flying</code>\n"
            "<code>/gmeg</code> — Generate images with Gemini AI. Example: <code>/gmeg a cat sitting on a moon</code>\n"
            "<code>/bgremove</code> — Remove image background. (Reply to a photo)\n"
            "<code>/enh</code> — Enhance face in photos. (Reply to a photo)\n"
            "<code>/pfp</code> — Download FB/Insta profile pictures. Example: <code>/pfp https://www.facebook.com/...</code>\n"
            "<code>/edit</code> — Edit images using a prompt. (Reply to a photo with prompt) Example: <code>/edit add a hat</code>\n\n"
            
            "🔸 <b>Card & Banking Tools</b>\n"
            "<code>/gen</code> — Generate cards with BIN. Example: <code>/gen 515462xxxxxx|02|28|573 5</code>\n"
            "<code>/chk</code> — Check a single card. Example: <code>/chk 4000123456789012|12|25|123</code>\n"
            "<code>/mas</code> — Mass check cards. (Reply to a list)\n"
            "<code>/b3</code> — Check cards using B3 gateway. Example: <code>/b3 4000123456789012|12|25|123</code>\n"
            "<code>/mb3</code> — Mass check cards with B3. (Reply to a list)\n"
            "<code>/bin</code> — Get detailed BIN info. Example: <code>/bin 426633</code>\n"
            "<code>/iban</code> — Generate IBAN for countries. Example: <code>/iban DE</code>\n"
            "<code>/ibncntry</code> — See supported IBAN countries.\n\n"

            "🔸 <b>Info & Utility</b>\n"
            "<code>/info</code> — Get user/bot/group/channel info. Example: <code>/info @username</code>\n"
            "<code>/usr</code> — Get user info. Example: <code>/usr @username</code> or reply to a message.\n"
            "<code>/bot</code> — Get bot info. Example: <code>/bot @botusername</code>\n"
            "<code>/grp</code> — Get group info. Example: <code>/grp @groupusername</code> or use in a group.\n"
            "<code>/cnnl</code> — Get channel info. Example: <code>/cnnl @channelusername</code>\n"
            "<code>/fake</code> — Generate fake addresses. Example: <code>/fake US</code>\n"
            "<code>/country</code> — See supported countries for fake addresses.\n"
            "<code>/wth</code> — Get weather info. Example: <code>/wth Faridpur</code>\n"
            "<code>/translate</code> — Translate any text. Example: <code>/translate fr Hello</code> or reply to a message.\n"
            "<code>/say</code> — Convert text to voice message. Example: <code>/say Hello everyone!</code>\n"
            "<code>/bomb</code> — Send SMS spam. Example: <code>/bomb 01712345678</code>\n"
            "<code>/spam</code> — Send spam texts. Example: <code>/spam Hello</code>\n"
            "<code>/spmtxt</code> — Create a spam file. Example: <code>/spmtxt 100 Hello</code>\n\n"
            
            "🔸 <b>Other</b>\n"
            "<code>/start</code>, <code>/arise</code> — See the welcome message.\n"
            "<code>/reveal</code>, <code>/help</code> — Show all commands.\n\n"

            "🔸 <b>বিশেষ দ্রষ্টব্য:</b> আপনি !, #, ', অথবা অন্য যেকোনো চিহ্ন দিয়েও কমান্ড চালাতে পারবেন।\n"
            f"\n👤 <i>Revealed by:</i> {username}"
        )

        bot.reply_to(message, help_text, parse_mode="HTML")
