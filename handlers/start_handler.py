def register(bot, custom_command_handler, command_prefixes_list): 
    @custom_command_handler("start")
    @custom_command_handler("arise")
    def start_command(message):
        user = message.from_user
        username = f"@{user.username}" if user.username else user.first_name

        welcome_text = (
            f"👋 <b>স্বাগতম {username}!</b>\n\n"
            "🛠 <b>উপলব্ধ কমান্ডসমূহ:</b>\n\n"
            "🔸 <b>এআই ও চ্যাট</b>\n"
            "<code>/gemini</code> — চ্যাট করুন। উদাহরণ: <code>/gemini কেমন আছো?</code>\n"
            "<code>/gpt</code> — চ্যাট করুন। উদাহরণ: <code>/gpt কেমন আছো?</code>\n"
            "<code>/grok</code> — চ্যাট করুন। উদাহরণ: <code>/grok কেমন আছো?</code>\n"
            "<code>/deepseek</code> — চ্যাট করুন। উদাহরণ: <code>/deepseek কেমন আছো?</code>\n\n"

            "🔸 <b>মিডিয়া ও ইমেজ টুলস</b>\n"
            "<code>/yt</code> — ভিডিও ডাউনলোড। উদাহরণ: <code>/yt https://youtu.be/id</code>\n"
            "<code>/dl</code> — ডাউনলোড। উদাহরণ: <code>/dl https://youtu.be/id</code>\n"
            "<code>/imagine</code> — ছবি তৈরি। উদাহরণ: <code>/imagine cat with sunglasses</code>\n"
            "<code>/gmeg</code> — ছবি তৈরি। উদাহরণ: <code>/gmeg a cat sitting on a moon</code>\n"
            "<code>/bgremove</code> — ব্যাকগ্রাউন্ড সরান। (ছবিতে রিপ্লাই)\n"
            "<code>/enh</code> — ফেস এনহ্যান্স। (ছবিতে রিপ্লাই)\n"
            "<code>/pfp</code> — প্রোফাইল ছবি। উদাহরণ: <code>/pfp https://fb.com/...</code>\n"
            "<code>/edit</code> — ছবি এডিট। (ছবিতে রিপ্লাই)\n\n"

            "🔸 <b>কার্ড ও ব্যাংকিং টুলস</b>\n"
            "<code>/gen</code> — কার্ড জেনারেট। উদাহরণ: <code>/gen 515462xxxxxx|02|28|573 5</code>\n"
            "<code>/chk</code> — কার্ড চেক। উদাহরণ: <code>/chk 4000...|12|25|123</code>\n"
            "<code>/mas</code> — একাধিক কার্ড চেক। (কার্ডের লিস্টে রিপ্লাই)\n"
            "<code>/b3</code> — B3 দিয়ে চেক। উদাহরণ: <code>/b3 4000...|12|25|123</code>\n"
            "<code>/mb3</code> — B3 দিয়ে একাধিক কার্ড চেক।\n"
            "<code>/bin</code> — BIN তথ্য। উদাহরণ: <code>/bin 426633</code>\n"
            "<code>/iban</code> — IBAN জেনারেট। উদাহরণ: <code>/iban DE</code>\n"
            "<code>/ibncntry</code> — IBAN দেশের তালিকা।\n\n"

            "🔸 <b>তথ্য ও ইউটিলিটি</b>\n"
            "<code>/info</code> — তথ্য দেখুন। উদাহরণ: <code>/info @username</code>\n"
            "<code>/fake</code> — ফেইক অ্যাড্রেস। উদাহরণ: <code>/fake US</code>\n"
            "<code>/country</code> — দেশের তালিকা।\n"
            "<code>/wth</code> — আবহাওয়ার তথ্য। উদাহরণ: <code>/wth Faridpur</code>\n"
            "<code>/translate</code> — অনুবাদ। উদাহরণ: <code>/translate fr hello</code>\n"
            "<code>/say</code> — টেক্সট-টু-ভয়েস। উদাহরণ: <code>/say হ্যালো</code>\n"
            "<code>/bomb</code> — SMS স্প্যাম। উদাহরণ: <code>/bomb 01712345678</code>\n"
            "<code>/spam</code> — টেক্সট স্প্যাম। উদাহরণ: <code>/spam Hello</code>\n"
            "<code>/spmtxt</code> — স্প্যাম ফাইল। উদাহরণ: <code>/spmtxt 100 Hello</code>\n\n"

            "🔸 <b>অন্যান্য</b>\n"
            "<code>/start</code>, <code>/arise</code> — এই মেসেজটি আবার দেখুন।\n"
            "<code>/reveal</code>, <code>/help</code> — সব কমান্ডের তালিকা দেখুন।\n\n"

            "📢 <b>আমাদের টেলিগ্রাম চ্যানেলে যোগ দিন:</b>\n"
            "<a href='https://t.me/bro_bin_lagbe'>https://t.me/bro_bin_lagbe</a>"
        )

        bot.send_message(message.chat.id, welcome_text, parse_mode="HTML")
