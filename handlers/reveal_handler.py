def register(bot, custom_command_handler, command_prefixes_list): 
    @custom_command_handler("reveal")
    @custom_command_handler("help")
    def show_help(message):
        user = message.from_user
        username = f"@{user.username}" if user.username else user.first_name
        help_text = (
            "🛠 Available Commands:\n\n"
            "`/arise` `.arise` `,arise` — Start the bot\n"
            "`/gen` `.gen` `,gen` — Generate random cards with BIN info\n"
            "`/chk` `.chk` `,chk` — Check a single card's status\n"
            "`/mas` `.mas` `,mas` — Check all generated cards at once (reply to a list)\n"
            "`/fake` `.fake` `,fake` — get fake address\n"
            "`/country` `.country` `,country` — check the available country\n"
            "`/imagine` `.imagine` `,imagine` — generate ai images\n"
            "`/bgremove` `.bgremove` `,bgremove` — remove image bacground\n"
            "`/download` `.download` `,download` — download almost any video of yt fb & insta\n"
            "`/gemini` `.gemini` `,gemini` — talk to gemini\n"
            "`/gpt` `.gpt` `,gpt` — talk to gpt\n"
            "`/say` `.say` `,say` —  text to speech\n"
            "`/translate` `.translate` `,translate` — translate texts\n"
            "`/info` `.info` `,info` — get telegram user/bot/group/channel info\n"
            "`/reveal` `.reveal` `,reveal` — Show all the commands\n\n"
            "<code>/gen &lt;bin&gt; .cnt &lt;amount&gt;</code> — Control quantity\n"
            f"\n👤 Revealed by: {username}"
        )
        bot.reply_to(message, help_text, parse_mode="HTML")