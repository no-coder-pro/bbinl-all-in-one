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
            "<code>/gemini</code> — জেমিনি এআই এর সাথে কথা বলুন\n"
            "<code>/gpt</code> — জিপিটি এআই এর সাথে কথা বলুন\n"
            "<code>/grok</code> — গ্রোক এআই এর সাথে কথা বলুন\n"
            "<code>/deepseek</code> — ডিপসিক এআই এর সাথে কথা বলুন\n\n"

            "🔸 <b>মিডিয়া ও ইমেজ টুলস</b>\n"
            "<code>/yt</code> — ইউটিউব ভিডিও সার্চ ও ডাউনলোড করুন\n"
            "<code>/dl</code> — ইউটিউব, ফেসবুক ও ইনস্টাগ্রাম থেকে ভিডিও ডাউনলোড করুন\n"
            "<code>/imagine</code> — এআই দিয়ে ছবি তৈরি করুন\n"
            "<code>/gmeg</code> — জেমিনি এআই দিয়ে ছবি তৈরি করুন\n"
            "<code>/bgremove</code> — ছবির ব্যাকগ্রাউন্ড সরান\n"
            "<code>/enh</code> — ছবির ফেস এনহ্যান্স করুন\n"
            "<code>/pfp</code> — ফেসবুক/ইনস্টাগ্রাম প্রোফাইল ছবি ডাউনলোড করুন\n"
            "<code>/edit</code> — ছবিতে প্রম্পট ব্যবহার করে এডিট করুন\n\n"

            "🔸 <b>কার্ড ও ব্যাংকিং টুলস</b>\n"
            "<code>/gen</code> — BIN দিয়ে কার্ড জেনারেট করুন\n"
            "<code>/chk</code> — একটি কার্ড চেক করুন\n"
            "<code>/mas</code> — একাধিক কার্ড একসাথে চেক করুন\n"
            "<code>/b3</code> — B3 চেক গেটওয়ে ব্যবহার করে কার্ড চেক করুন\n"
            "<code>/mb3</code> — B3 গেটওয়ে দিয়ে একাধিক কার্ড চেক করুন\n"
            "<code>/bin</code> — BIN-এর বিস্তারিত তথ্য দেখুন\n"
            "<code>/iban</code> — বিভিন্ন দেশের IBAN জেনারেট করুন\n"
            "<code>/ibncntry</code> — IBAN জেনারেশনের জন্য সমর্থিত দেশগুলোর তালিকা দেখুন\n\n"

            "🔸 <b>তথ্য ও ইউটিলিটি</b>\n"
            "<code>/info</code> — ইউজার, বট, গ্রুপ বা চ্যানেলের তথ্য দেখুন\n"
            "<code>/fake</code> — ফেইক অ্যাড্রেস জেনারেট করুন\n"
            "<code>/country</code> — ফেইক অ্যাড্রেসের জন্য সমর্থিত দেশগুলোর তালিকা দেখুন\n"
            "<code>/wth</code> — আবহাওয়ার তথ্য দেখুন\n"
            "<code>/translate</code> — যেকোনো টেক্সট অনুবাদ করুন\n"
            "<code>/say</code> — টেক্সটকে ভয়েস মেসেজে রূপান্তর করুন\n"
            "<code>/bomb</code> — ফোন নম্বরে এসএমএস স্প্যাম করুন\n"
            "<code>/spam</code> — স্প্যাম টেক্সট মেসেজ পাঠান\n"
            "<code>/spmtxt</code> — স্প্যাম করার জন্য টেক্সট ফাইল তৈরি করুন\n\n"

            "🔸 <b>অন্যান্য</b>\n"
            "<code>/start</code> — এই মেসেজটি আবার দেখুন\n"
            "<code>/reveal</code> — সমস্ত কমান্ডের তালিকা দেখুন\n"
            "<code>/help</code> — সমস্ত কমান্ডের তালিকা দেখুন\n\n"

            "📢 <b>আমাদের টেলিগ্রাম চ্যানেলে যোগ দিন:</b>\n"
            "<a href='https://t.me/bro_bin_lagbe'>https://t.me/bro_bin_lagbe</a>"
        )

        bot.send_message(message.chat.id, welcome_text, parse_mode="HTML")
