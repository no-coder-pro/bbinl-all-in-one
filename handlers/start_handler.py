def register(bot, custom_command_handler, command_prefixes_list): 
    @custom_command_handler("start")
    @custom_command_handler("arise")
    def start_command(message):
        user = message.from_user
        username = f"@{user.username}" if user.username else user.first_name
        welcome_text = (
            f"👋 <b>Welcome {username}!</b>\n\n"
            "🛠 Available Commands:\n"

            f"`{command_prefixes_list[0]}arise` `{command_prefixes_list[1]}arise` `{command_prefixes_list[2]}arise` — Start the bot\n" 
            f"`{command_prefixes_list[0]}gen` `{command_prefixes_list[1]}gen` `{command_prefixes_list[2]}gen` — Generate random cards with BIN info\n" 
            f"`{command_prefixes_list[0]}chk` `{command_prefixes_list[1]}chk` `{command_prefixes_list[2]}chk` — Check a single card's status\n" 
            f"`{command_prefixes_list[0]}mas` `{command_prefixes_list[1]}mas` `{command_prefixes_list[2]}mas` — Check all generated cards at once (reply to a list)\n" 
            f"`{command_prefixes_list[0]}fake` `{command_prefixes_list[1]}fake` `{command_prefixes_list[2]}fake` — get fake address\n" 
            f"`{command_prefixes_list[0]}country` `{command_prefixes_list[1]}country` `{command_prefixes_list[2]}country` — check the available country\n" 
            f"`{command_prefixes_list[0]}imagine` `{command_prefixes_list[1]}imagine` `{command_prefixes_list[2]}imagine` — generate ai images\n" 
            f"`{command_prefixes_list[0]}bgremove` `{command_prefixes_list[1]}bgremove` `{command_prefixes_list[2]}bgremove` — remove image bacground\n" 
            f"`{command_prefixes_list[0]}download` `{command_prefixes_list[1]}download` `{command_prefixes_list[2]}download` — download almost any video of yt fb & insta\n" 
            f"`{command_prefixes_list[0]}gemini` `{command_prefixes_list[1]}gemini` `{command_prefixes_list[2]}gemini` — talk to gemini\n" 
            f"`{command_prefixes_list[0]}gpt` `{command_prefixes_list[1]}gpt` `{command_prefixes_list[2]}gpt` — talk to gpt\n" 
            f"`{command_prefixes_list[0]}say` `{command_prefixes_list[1]}say` `{command_prefixes_list[2]}say` —  text to speech\n" 
            f"`{command_prefixes_list[0]}translate` `{command_prefixes_list[1]}translate` `{command_prefixes_list[2]}translate` — translate texts\n" 
            f"`{command_prefixes_list[0]}info` `{command_prefixes_list[1]}info` `{command_prefixes_list[2]}info` — get telegram user/bot/group/channel info\n"
            f"`{command_prefixes_list[0]}reveal` `{command_prefixes_list[1]}reveal` `{command_prefixes_list[2]}reveal` — Show all the commands\n\n" 
            f"<code>{command_prefixes_list[0]}gen &lt;bin&gt; .cnt &lt;amount&gt;</code> — Control quantity\n\n" 
            "📢 Join our Telegram Channel:\n"
            "<a href='https://t.me/bro_bin_lagbe'>https://t.me/bro_bin_lagbe</a>"
        )
        bot.send_message(message.chat.id, welcome_text, parse_mode="HTML")