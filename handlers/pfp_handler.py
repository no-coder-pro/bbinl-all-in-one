import os
import asyncio
import aiohttp
import telebot
import logging
from typing import Dict, Any
from urllib.parse import urlparse
import tempfile
import html

# Configure logging
logger = logging.getLogger(__name__)

# New API endpoints
FB_PFP_API = "https://fb-unlock-plum.vercel.app/api/fb?url={url}"
INSTA_PFP_API = "https://fb-unlock-plum.vercel.app/api/ig?url={url}"


async def get_profile_picture(url: str) -> Dict[str, Any]:
    """
    Downloads profile pictures from a given URL using the new API.
    Handles both direct image downloads (Instagram) and JSON responses (Facebook).
    """
    try:
        parsed_url = urlparse(url)
        image_paths = []

        if "instagram.com" in parsed_url.netloc:
            api_url = INSTA_PFP_API.format(url=url)
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as res:
                    if res.status == 404:
                        return {"status": "error", "error": "❌ ইনস্টাগ্রাম প্রোফাইলটি খুঁজে পাওয়া যায়নি অথবা ইউজারনেম ভুল।"}
                    res.raise_for_status()
                    image_bytes = await res.read()

                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                        tmp.write(image_bytes)
                        image_paths.append(tmp.name)
                    return {"status": "success", "image_paths": image_paths, "message": "✅ সফল! এখানে আপনার প্রোফাইল ছবিটি আছে।"}

        elif "facebook.com" in parsed_url.netloc:
            api_url = FB_PFP_API.format(url=url)
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as res:
                    res.raise_for_status()
                    data = await res.json()

                    if data.get("profile_status") == "public":
                        return {"status": "error", "error": "⚠️ This is a Public Profile. আপনি নিজেই প্রোফাইলে গিয়ে ছবিগুলো নিতে পারেন।"}

                    if data.get("status") == "success":
                        image_urls = []
                        if "profile_picture" in data and data["profile_picture"] and len(data["profile_picture"]) > 0:
                            image_urls.append(data["profile_picture"][0])
                        if "cover_photo" in data and data["cover_photo"].get("url"):
                            image_urls.append(data["cover_photo"]["url"])

                        downloaded_count = 0
                        for img_url in image_urls:
                            try:
                                async with session.get(img_url) as img_res:
                                    img_res.raise_for_status()
                                    image_bytes = await img_res.read()
                                    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                                        tmp.write(image_bytes)
                                        image_paths.append(tmp.name)
                                        downloaded_count += 1
                            except aiohttp.ClientResponseError:
                                continue

                        if downloaded_count == 2:
                            message = "✅ সফল! এখানে আপনার প্রোফাইল এবং কভার ছবি আছে।"
                        elif downloaded_count == 1:
                            message = "✅ সফল! তবে শুধুমাত্র একটি ছবি পাওয়া গেছে।"
                        else:
                            return {"status": "error", "error": "❌ প্রোফাইল লকড হওয়া সত্ত্বেও কোনো ছবি পাওয়া যায়নি। হয়তো ছবিগুলো নেই অথবা API থেকে কোনো রেসপন্স আসেনি। অনুগ্রহ করে এডমিনের সাথে যোগাযোগ করুন: @no_coder_pro"}

                        return {"status": "success", "image_paths": image_paths, "message": message}
                    else:
                        error_message = data.get("error", "❌ API থেকে কোনো তথ্য পাওয়া যায়নি।")
                        return {"status": "error", "error": error_message}
        else:
            return {"status": "error", "error": "❌ শুধুমাত্র ফেসবুক বা ইনস্টাগ্রাম প্রোফাইলের URL দিন।"}

    except Exception as e:
        return {"status": "error", "error": f"❌ একটি অপ্রত্যাশিত ত্রুটি হয়েছে: {str(e)}। অনুগ্রহ করে আবার চেষ্টা করুন।"}


def register(bot: telebot.TeleBot, custom_command_handler, command_prefixes_list):

    @custom_command_handler("pfp", "pp")
    def handle_pfp_command(message):
        command_text = message.text.split(" ", 1)[0].lower()
        actual_command_len = 0
        for prefix in command_prefixes_list:
            if command_text.startswith(f"{prefix}pfp") or command_text.startswith(f"{prefix}pp"): 
                actual_command_len = len(command_text)
                break

        url = message.text[actual_command_len:].strip()

        if not url:
            bot.reply_to(
                message,
                "❌ অনুগ্রহ করে একটি ফেসবুক বা ইনস্টাগ্রাম প্রোফাইল URL দিন। যেমন: `/pfp https://www.facebook.com/...`",
                parse_mode="Markdown")
            return

        thinking_message = bot.reply_to(message, "⏳ প্রোফাইল ছবিটি ডাউনলোড করা হচ্ছে...")

        image_paths = []
        try:
            result = asyncio.run(get_profile_picture(url))

            if result['status'] == 'success':
                image_paths = result['image_paths']

                if len(image_paths) > 1:
                    media_group = [telebot.types.InputMediaPhoto(open(path, 'rb')) for path in image_paths]
                    media_group[0].caption = result['message']
                    bot.send_media_group(
                        message.chat.id,
                        media_group,
                        reply_to_message_id=message.message_id
                    )
                else:
                    with open(image_paths[0], 'rb') as f:
                        bot.send_photo(
                            message.chat.id,
                            f,
                            caption=result['message'],
                            reply_to_message_id=message.message_id
                        )

                bot.delete_message(thinking_message.chat.id, thinking_message.message_id)
            else:
                bot.edit_message_text(chat_id=thinking_message.chat.id, message_id=thinking_message.message_id, text=result['error'])
        except Exception as e:
            bot.edit_message_text(chat_id=thinking_message.chat.id, message_id=thinking_message.message_id, text=f"❌ একটি অপ্রত্যাশিত ত্রুটি হয়েছে: {str(e)}। অনুগ্রহ করে আবার চেষ্টা করুন।")
        finally:
            for path in image_paths:
                if os.path.exists(path):
                    os.remove(path)
