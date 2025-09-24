import requests
from telebot.types import Message
from fuzzywuzzy import fuzz
import json

# সকল কান্ট্রি ডেটা, কোড এবং নাম
code_to_name = {
    "AD": "Andorra", "AE": "United Arab Emirates", "AF": "Afghanistan", "AG": "Antigua And Barbuda",
    "AL": "Albania", "AM": "Armenia", "AO": "Angola", "AR": "Argentina",
    "AS": "American Samoa", "AT": "Austria", "AU": "Australia", "AZ": "Azerbaijan",
    "BA": "Bosnia And Herzegovina", "BB": "Barbados", "BD": "Bangladesh", "BE": "Belgium",
    "BF": "Burkina Faso", "BG": "Bulgaria", "BH": "Bahrain", "BI": "Burundi",
    "BJ": "Benin", "BM": "Bermuda", "BN": "Brunei", "BO": "Bolivia",
    "BQ": "Caribbean Netherlands", "BR": "Brazil", "BS": "Bahamas", "BT": "Bhutan",
    "BW": "Botswana", "BY": "Belarus", "BZ": "Belize", "CA": "Canada",
    "CD": "Congo (Drc)", "CF": "Central African Republic", "CG": "Republic Of The Congo",
    "CH": "Switzerland", "CI": "Côte D'Ivoire", "CL": "Chile", "CM": "Cameroon",
    "CN": "China", "CO": "Colombia", "CR": "Costa Rica", "CU": "Cuba",
    "CV": "Cape Verde", "CY": "Cyprus", "CZ": "Czech Republic", "DE": "Germany",
    "DJ": "Djibouti", "DK": "Denmark", "DM": "Dominica", "DO": "Dominican Republic",
    "DZ": "Algeria", "EC": "Ecuador", "EE": "Estonia", "EG": "Egypt",
    "ER": "Eritrea", "ES": "Spain", "ET": "Ethiopia", "FI": "Finland",
    "FJ": "Fiji", "FR": "France", "GA": "Gabon", "GD": "Grenada",
    "GE": "Georgia", "GH": "Ghana", "GL": "Greenland", "GR": "Greece",
    "GT": "Guatemala", "HK": "Hong Kong", "HR": "Croatia", "HU": "Hungary",
    "ID": "Indonesia", "IE": "Ireland", "IL": "Israel", "IN": "India",
    "IQ": "Iraq", "IR": "Iran", "IS": "Iceland", "IT": "Italy",
    "JO": "Jordan", "JP": "Japan", "KE": "Kenya", "KH": "Cambodia",
    "KR": "South Korea", "KZ": "Kazakhstan", "LB": "Lebanon", "LK": "Sri Lanka",
    "LT": "Lithuania", "LV": "Latvia", "MA": "Morocco", "MD": "Moldova",
    "ME": "Montenegro", "MM": "Myanmar", "MR": "Mauritania", "MV": "Maldives",
    "MX": "Mexico", "MY": "Malaysia", "NG": "Nigeria", "NL": "Netherlands",
    "NO": "Norway", "NP": "Nepal", "NZ": "New Zealand", "OM": "Oman",
    "PA": "Panama", "PE": "Peru", "PH": "Philippines", "PK": "Pakistan",
    "PL": "Poland", "PR": "Puerto Rico", "PT": "Portugal", "QA": "Qatar",
    "RO": "Romania", "RS": "Serbia", "RU": "Russia", "SA": "Saudi Arabia",
    "SD": "Sudan", "SE": "Sweden", "SG": "Singapore", "SI": "Slovenia",
    "SK": "Slovakia", "SM": "San Marino", "SV": "El Salvador", "TH": "Thailand",
    "TR": "Turkey", "TW": "Taiwan (China)", "TZ": "Tanzania", "UA": "Ukraine",
    "UG": "Uganda", "UK": "United Kingdom", "US": "United States", "VE": "Venezuela",
    "VN": "Vietnam", "YE": "Yemen", "ZA": "South Africa",
    "GB": "United Kingdom",
    "CD": "Congo (Drc)",
    "KZT": "Kazakhstan" 
}

# সমস্ত ইনপুট (নাম, কোড, বা অতিরিক্ত কোড) কে API-ready কোডে রূপান্তর করার জন্য একটি একক ডিকশনারি
country_lookup = {name.lower(): code for code, name in code_to_name.items()}
country_lookup.update({code.lower(): code for code in code_to_name.keys()})
country_lookup['gb'] = 'UK'
country_lookup['great britain'] = 'UK'
country_lookup['kzt'] = 'KZ'


def find_country(input_text: str):
    """
    ইউজার ইনপুট থেকে কান্ট্রি কোড অথবা নাম খুঁজে বের করে।
    যদি সরাসরি না পায়, তবে সাজেশন দেয়।
    """
    input_lower = input_text.strip().lower()

    if input_lower in country_lookup:
        code = country_lookup[input_lower]
        name = code_to_name.get(code)
        return code, name

    suggestions = []
    for name_lower, code in country_lookup.items():
        ratio = fuzz.ratio(input_lower, name_lower)
        partial_ratio = fuzz.partial_ratio(input_lower, name_lower)

        if ratio >= 70 or (len(input_lower) > 2 and partial_ratio >= 80):
            suggestions.append(f"{code_to_name.get(code)} ({code})")

    suggestions = sorted(list(set(suggestions)))

    if suggestions:
        return None, suggestions
    else:
        return None, None


def register(bot, custom_command_handler, command_prefixes_list):

    @custom_command_handler("fake")
    def handle_fake(message: Message):
        command_text = message.text.split(" ", 1)[0].lower()
        actual_command_len = 0
        for prefix in command_prefixes_list:
            if command_text.startswith(f"{prefix}fake"):
                actual_command_len = len(f"{prefix}fake")
                break

        user_input = message.text[actual_command_len:].strip()

        if not user_input:
            bot.reply_to(message, f"❌ Country name or code missing.\n\nউদাহরণ:\n`{command_prefixes_list[0]}fake US`\n`{command_prefixes_list[1]}fake bangladesh`", parse_mode="HTML")
            return

        try:
            target_country_code, local_suggestions = find_country(user_input)

            if target_country_code:
                api_url = f"https://fakexy-api-sage.vercel.app/api/address?code={target_country_code}"
                response = requests.get(api_url)
                response.raise_for_status()
                address = response.json()
                username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

                caption_text = (
                    f"<b>{address.get('Flag_Emoji', '')} Address for {address.get('Country', 'Unknown')}</b> (<code>{address.get('Country_Code', '').upper()}</code>)\n"
                    f"•{'━'*10}•\n"
                    f"𝗡𝗮𝗺𝗲: <code>{address.get('Full Name', 'N/A')}</code>\n"
                    f"𝗚𝗲𝗻𝗱𝗲𝗿: <code>{address.get('Gender', 'N/A')}</code>\n"
                    f"𝗣𝗵𝗼𝗻𝗲: <code>{address.get('Phone Number', 'N/A')}</code>\n"
                    f"•{'━'*5} 𝗔𝗱𝗱𝗿𝗲𝘀𝘀 {'━'*5}•\n"
                    f"𝗦𝘁𝗿𝗲𝗲𝘁: <code>{address.get('Street', 'N/A')}</code>\n"
                    f"𝗖𝗶𝘁𝘆: <code>{address.get('City/Town', 'N/A')}</code>\n"
                    f"𝗦𝘁𝗮𝘁𝗲: <code>{address.get('State/Province/Region', 'N/A')}</code>\n"
                    f"𝗣𝗼𝘀𝘁𝗮𝗹 𝗖𝗼𝗱𝗲: <code>{address.get('Zip/Postal Code', 'N/A')}</code>\n"
                    f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆: <code>{address.get('Country', 'N/A')}</code>\n"
                    f"•{'━'*5} 𝗔𝗱𝗱𝗶𝘁𝗶𝗼𝗻𝗮𝗹 𝗜𝗻𝗳𝗼 {'━'*5}•\n"
                    f"𝗖𝘂𝗿𝗿𝗲𝗻𝗰𝘆: <code>{address.get('currency', 'N/A')}</code>\n"
                    f"𝗧𝗶𝗺𝗲𝘇𝗼𝗻𝗲: <code>{address.get('Time Zone', 'N/A')}</code>\n"
                    f"•{'━'*10}•\n"
                    f"👤 𝗥𝗲𝗤𝘂𝗲𝘀𝘁 𝗯𝘆: {username}"
                )

                if 'Country_Flag' in address and address['Country_Flag']:
                    bot.send_photo(message.chat.id, address['Country_Flag'], caption=caption_text, parse_mode="HTML")
                else:
                    bot.send_message(message.chat.id, caption_text, parse_mode="HTML")

            elif local_suggestions:
                suggestion_text = "\n".join([f"`{s}`" for s in local_suggestions])
                bot.send_message(message.chat.id, f"❌ Country not found. Did you mean one of these?\n{suggestion_text}", parse_mode="HTML")

            else:
                api_url = f"https://fakexy-api-sage.vercel.app/api/address?code={user_input.upper()}"
                response = requests.get(api_url)
                response.raise_for_status()

                address = response.json()
                username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
                caption_text = (
                    f"<b>{address.get('Flag_Emoji', '')} Address for {address.get('Country', 'Unknown')}</b> (<code>{address.get('Country_Code', '').upper()}</code>)\n"
                    f"•{'━'*10}•\n"
                    f"𝗡𝗮𝗺𝗲: <code>{address.get('Full Name', 'N/A')}</code>\n"
                    f"𝗚𝗲𝗻𝗱𝗲𝗿: <code>{address.get('Gender', 'N/A')}</code>\n"
                    f"𝗣𝗵𝗼𝗻𝗲: <code>{address.get('Phone Number', 'N/A')}</code>\n"
                    f"•{'━'*5} 𝗔𝗱𝗱𝗿𝗲𝘀𝘀 {'━'*5}•\n"
                    f"𝗦𝘁𝗿𝗲𝗲𝘁: <code>{address.get('Street', 'N/A')}</code>\n"
                    f"𝗖𝗶𝘁𝘆: <code>{address.get('City/Town', 'N/A')}</code>\n"
                    f"𝗦𝘁𝗮𝘁𝗲: <code>{address.get('State/Province/Region', 'N/A')}</code>\n"
                    f"𝗣𝗼𝘀𝘁𝗮𝗹 𝗖𝗼𝗱𝗲: <code>{address.get('Zip/Postal Code', 'N/A')}</code>\n"
                    f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆: <code>{address.get('Country', 'N/A')}</code>\n"
                    f"•{'━'*5} 𝗔𝗱𝗱𝗶𝘁𝗶𝗼𝗻𝗮𝗹 𝗜𝗻𝗳𝗼 {'━'*5}•\n"
                    f"𝗖𝘂𝗿𝗿𝗲𝗻𝗰𝘆: <code>{address.get('currency', 'N/A')}</code>\n"
                    f"𝗧𝗶𝗺𝗲𝘇𝗼𝗻𝗲: <code>{address.get('Time Zone', 'N/A')}</code>\n"
                    f"•{'━'*10}•\n"
                    f"👤 𝗥𝗲𝗤𝘂𝗲𝘀𝘁 𝗯𝘆: {username} | 𝗝𝗼𝗶𝗻: @bro_bin_lagbe"
                )

                if 'Country_Flag' in address and address['Country_Flag']:
                    bot.send_photo(message.chat.id, address['Country_Flag'], caption=caption_text, parse_mode="HTML")
                else:
                    bot.send_message(message.chat.id, caption_text, parse_mode="HTML")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                try:
                    error_response = e.response.json()
                    api_suggestions = error_response.get("suggestions", [])
                    if api_suggestions:
                        suggestion_lines = [f"`{s['name']} ({s['code']})`" for s in api_suggestions]
                        suggestion_text = "\n".join(suggestion_lines)
                        bot.send_message(message.chat.id, f"❌ Country not found. Did you mean one of these?\n{suggestion_text}", parse_mode="HTML")
                    else:
                        bot.send_message(message.chat.id, f"❌ Country not found. No similar names or codes were found.", parse_mode="HTML")
                except (json.JSONDecodeError, AttributeError):
                    bot.send_message(message.chat.id, f"❌ An error occurred while processing the API response: {str(e)}")
            else:
                bot.send_message(message.chat.id, f"❌ An error occurred: {str(e)}")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ An unexpected error occurred: {str(e)}")

    @custom_command_handler("country")
    def handle_countries(message: Message):
        try:
            if not code_to_name:
                bot.send_message(message.chat.id, "⚠️ No countries available at the moment.")
                return

            country_lines = []
            for code, name in code_to_name.items():
                country_lines.append(f"• {name} (<code>{code.upper()}</code>)")

            msg = (
                f"<b>🌐 Supported Countries (Total: {len(code_to_name)})</b>\n"
                f"{'━'*34}\n"
                f"{chr(10).join(country_lines)}\n"
                f"{'━'*34}\n"
                "✅ You can use full country names or country codes.\n"
                f"উদাহরণ: <code>{command_prefixes_list[0]}fake US</code> or <code>{command_prefixes_list[1]}fake bangladesh</code>"
            )

            bot.send_message(message.chat.id, msg, parse_mode="HTML")

        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Failed to load country list.\nError: {str(e)}")
