import requests
from telebot.types import Message

# Country mapping: name -> ISO code + aliases
COUNTRY_MAP = {
    "algeria": "dz", "argentina": "ar", "armenia": "am", "australia": "au",
    "austria": "at", "azerbaijan": "az", "bangladesh": "bd", "belgium": "be",
    "brazil": "br", "bulgaria": "bg", "canada": "ca", "china": "cn",
    "colombia": "co", "croatia": "hr", "cyprus": "cy", "czech republic": "cz",
    "denmark": "dk", "egypt": "eg", "estonia": "ee", "finland": "fi",
    "france": "fr", "georgia": "ge", "germany": "de", "greece": "gr",
    "hong kong": "hk", "hungary": "hu", "iceland": "is", "india": "in",
    "indonesia": "id", "iran": "ir", "iraq": "iq", "ireland": "ie",
    "israel": "il", "italy": "it", "japan": "jp", "jordan": "jo",
    "kazakhstan": "kz", "kz": "kz", "kzt": "kz", "latvia": "lv",
    "lithuania": "lt", "malaysia": "my", "moldova": "md", "mongolia": "mn",
    "montenegro": "me", "morocco": "ma", "nepal": "np", "netherlands": "nl",
    "new zealand": "nz", "nigeria": "ng", "norway": "no", "pakistan": "pk",
    "panama": "pa", "peru": "pe", "philippines": "ph", "poland": "pl",
    "portugal": "pt", "qatar": "qa", "romania": "ro", "russia": "ru",
    "saudi arabia": "sa", "serbia": "rs", "slovakia": "sk", "slovenia": "si",
    "south africa": "za", "south korea": "kr", "spain": "es", "sweden": "se",
    "switzerland": "ch", "taiwan": "tw", "thailand": "th", "turkey": "tr",
    "turkiye": "tr", "uganda": "ug", "uk": "gb", "united kingdom": "gb",
    "united states": "us", "usa": "us", "us": "us", "ukraine": "ua",
    "venezuela": "ve", "vietnam": "vn",
}


API_URL = "https://fakerapi.it/api/v2/addresses?_quantity=1&_locale=en&_country_code="

# register function now accepts command_prefixes_list
def register(bot, custom_command_handler, command_prefixes_list): # <-- MODIFIED LINE (added command_prefixes_list)
    @custom_command_handler("fake2")
    def handle_fake(message: Message):
        # Get the full command text and calculate actual command length
        command_text = message.text.split(" ", 1)[0].lower()
        actual_command_len = 0
        # Use command_prefixes_list here
        for prefix in command_prefixes_list: # <-- MODIFIED LINE (using command_prefixes_list)
            if command_text.startswith(f"{prefix}fake2"):
                actual_command_len = len(f"{prefix}fake2")
                break

        user_input_raw = message.text[actual_command_len:].strip()
        args = user_input_raw.split(" ", 1) # এবার সঠিক আর্গুমেন্ট পার্সিং

        if not user_input_raw: # যদি শুধু কমান্ড থাকে, কোনো আর্গুমেন্ট না থাকে
            # Update example message with dynamic prefixes
            bot.reply_to(message, f"❌ Country name missing. উদাহরণ: <code>{command_prefixes_list[0]}fake2 US</code>, <code>{command_prefixes_list[1]}fake2 kazakhstan</code>, <code>{command_prefixes_list[2]}fake2 kzt</code>", parse_mode="HTML") # <-- MODIFIED LINE (updated example)
            return

        user_input = args[0].strip().lower()

        country_code = COUNTRY_MAP.get(user_input)
        if not country_code:
            bot.reply_to(message, "❌ Country not found or unsupported.", parse_mode="HTML")
            return

        try:
            response = requests.get(f"{API_URL}{country_code}")
            if response.status_code != 200:
                bot.send_message(message.chat.id, "❌ Failed to fetch fake address.")
                return

            data = response.json().get("data", [])[0]
            country = data.get("country", "N/A")
            username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

            msg = (
                f"<b>Address for {country_code.upper()}</b>\n"
                f"•{'━'*10}•\n"
                f"𝗦𝘁𝗿𝗲𝗲𝘁 𝗔𝗱𝗱𝗿𝗲𝘀𝘀: <code>{data.get('street', 'N/A')}</code>\n"
                f"𝗦𝘁𝗿𝗲𝗲𝘁 𝗡𝗮𝗺𝗲: <code>{data.get('streetName', 'N/A')}</code>\n"
                f"𝗕𝘂𝗶𝗹𝗱𝗶𝗻𝗴 𝗡𝘂𝗺𝗯𝗲𝗿: <code>{data.get('buildingNumber', 'N/A')}</code>\n"
                f"𝗖𝗶𝘁𝘆: <code>{data.get('city', 'N/A')}</code>\n"
                f"𝗦𝘁𝗮𝘁𝗲: <code>{data.get('state', 'N/A')}</code>\n"
                f"𝗣𝗼𝘀𝘁𝗮𝗹 𝗖𝗼𝗱𝗲: <code>{data.get('zipcode', 'N/A')}</code>\n"
                f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆: <code>{data.get('country', 'N/A')}</code> | "
                f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆 𝗖𝗼𝗱𝗲: <code>{data.get('country_code', country_code.upper())}</code>\n"
                f"•{'━'*10}•\n"
                f"Requested by: {username}  |  𝗝𝗼𝗶𝗻: @bro_bin_lagbe"
            )

            bot.send_message(message.chat.id, msg, parse_mode="HTML")

        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Error: {str(e)}")