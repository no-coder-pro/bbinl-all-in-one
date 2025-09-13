import os
import re
import requests
import subprocess
from telebot import TeleBot
from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
import threading
import json
import time
from typing import Optional

# === APIs ===
SEARCH_API = "https://smartytdl.vercel.app/search?q="
DOWNLOAD_API = "https://smartytdl.vercel.app/dl?url="

# === Store user-specific data ===
user_search_results = {}
user_sent_messages = {}

# === Helper Functions ===
def download_file(url, filename, bot=None, chat_id=None):
    try:
        with requests.get(url, stream=True, timeout=15) as r:
            r.raise_for_status()
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        if bot and chat_id:
                            try:
                                bot.send_chat_action(chat_id, 'upload_document')
                            except Exception:
                                pass
        return True
    except Exception as e:
        print(f"[!] Direct download failed: {e}")
        return False

def fallback_ytdlp(link, filename, audio=False):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        format_str = 'bestaudio[ext=m4a]' if audio else '18'
        cmd = [
            "yt-dlp",
            "-f", format_str,
            "-o", filename,
            link
        ]
        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print(f"[!] yt-dlp fallback failed: {e}")
        return False

def register(bot: TeleBot, custom_command_handler, command_prefixes_list):

    # Define the regex pattern for sanitizing filenames outside the f-string
    FILENAME_SANITIZE_PATTERN = r'[\\/:*?"<>|]'

    @custom_command_handler("yt")
    def yt_command(message: Message):
        if not message.text:
            bot.reply_to(message, f"দয়া করে ইউটিউব সার্চ করার জন্য কিছু লিখুন।\nUsage: `{command_prefixes_list[0]}yt <search query>` অথবা `{command_prefixes_list[1]}yt <YouTube link>`", parse_mode="Markdown")
            return
        
        command_text_full = message.text.split(" ", 1)[0].lower()
        actual_command_len = 0
        for prefix in command_prefixes_list:
            if command_text_full.startswith(f"{prefix}yt"):
                actual_command_len = len(f"{prefix}yt")
                break

        query_raw = message.text[actual_command_len:].strip()

        if not query_raw:
            bot.reply_to(message, f"দয়া করে ইউটিউব সার্চ করার জন্য কিছু লিখুন।\nUsage: `{command_prefixes_list[0]}yt <search query>` অথবা `{command_prefixes_list[1]}yt <YouTube link>`", parse_mode="Markdown")
            return

        query = query_raw

        if "youtu" in query:
            try:
                res = requests.get(DOWNLOAD_API + query)
                res.raise_for_status()
                data = res.json()

                if not data.get("success") or not data.get("title"):
                    bot.reply_to(message, "❌ ভিডিও ডেটা আনতে সমস্যা হয়েছে।")
                    return

                title = re.sub(FILENAME_SANITIZE_PATTERN, '', data["title"])
                thumb = data.get("thumbnail")
                duration = data.get("duration", "Unknown")
                caption = f"🕒 {duration}\n{title}"

                user_search_results[message.chat.id] = [{
                    "title": title,
                    "imageUrl": thumb,
                    "duration": duration,
                    "link": query
                }]

                markup = InlineKeyboardMarkup()
                markup.add(
                    InlineKeyboardButton("🎵 অডিও", callback_data=f"download_{0}_audio"),
                    InlineKeyboardButton("🎬 ভিডিও", callback_data=f"download_{0}_video")
                )

                sent_msg = bot.send_photo(message.chat.id, photo=thumb, caption=caption, reply_markup=markup)
                user_sent_messages[message.chat.id] = [sent_msg.message_id]

            except Exception as e:
                print(f"[YT LINK ERROR] {e}")
                bot.reply_to(message, "❌ ভিডিও প্রসেস করতে সমস্যা হয়েছে।")
            return

        try:
            resp = requests.get(SEARCH_API + query)
            resp.raise_for_status()
            data = resp.json()

            if "result" not in data or not data["result"]:
                bot.reply_to(message, "❌ কোনো রেজাল্ট পাওয়া যায়নি।")
                return

            results = data["result"][:10]
            user_search_results[message.chat.id] = results

            msg_text = "🔍 সার্চ রেজাল্ট:\n\n"
            for i, video in enumerate(results):
                title = re.sub(FILENAME_SANITIZE_PATTERN, '', video["title"])
                duration = video.get("duration", "Unknown")
                msg_text += f"[{i+1}] 🕒 {duration} | 🎵 {title}\n"

            markup = InlineKeyboardMarkup(row_width=5)
            buttons = [InlineKeyboardButton(str(i+1), callback_data=f"select_{i}") for i in range(len(results))]
            markup.add(*buttons)
            bot.send_message(message.chat.id, msg_text, reply_markup=markup)

        except Exception as e:
            print(f"[SEARCH ERROR] {e}")
            bot.reply_to(message, "❌ সার্চ করতে সমস্যা হয়েছে।")


    @bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("select_"))
    def handle_select(call: CallbackQuery):
        if not call.data:
            bot.answer_callback_query(call.id, "Invalid request")
            return
        
        idx = int(call.data.split("_")[1])
        chat_id = call.message.chat.id

        if chat_id not in user_search_results:
            bot.answer_callback_query(call.id, "সেশন শেষ হয়ে গেছে। দয়া করে আবার সার্চ করুন।")
            return

        video = user_search_results[chat_id][idx]
        title = re.sub(FILENAME_SANITIZE_PATTERN, '', video["title"])
        duration = video.get("duration", "Unknown")
        thumb_url = video.get("imageUrl")
        link = video["link"]

        caption = f"🕒 {duration}\n{title}"
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🎵 অডিও", callback_data=f"download_{idx}_audio"),
            InlineKeyboardButton("🎬 ভিডিও", callback_data=f"download_{idx}_video")
        )

        sent_msg = bot.send_photo(chat_id, photo=thumb_url, caption=caption, reply_markup=markup)

        if chat_id not in user_sent_messages:
            user_sent_messages[chat_id] = []
        user_sent_messages[chat_id].append(sent_msg.message_id)

        bot.answer_callback_query(call.id)

    def process_download(bot, chat_id, idx, choice):
        # Initialize variables to prevent unbound variable errors
        wait_msg = None
        filename = None
        title = "Downloaded File"
        
        try:
            wait_msg = bot.send_message(chat_id, f"📥 ডাউনলোড হচ্ছে... অপেক্ষা করুন")

            video = user_search_results.get(chat_id, [])[idx]
            link = video["link"]

            res = requests.get(DOWNLOAD_API + link)
            res.raise_for_status()
            ddata = res.json()

            if ddata.get("success"):
                medias = ddata.get("medias", [])
                media_url = None

                if choice == "audio":
                    for media in medias:
                        if media.get("type") == "audio":
                            media_url = media.get("url")
                            break
                else:
                    for media in medias:
                        if (
                            media.get("type") == "video"
                            and media.get("has_audio") == True
                            and media.get("extension") == "mp4"
                        ):
                            media_url = media.get("url")
                            break
                    if not media_url:
                        for media in medias:
                            if media.get("type") == "video" and media.get("has_audio")== True:
                                media_url = media.get("url")
                                break

                if media_url:
                    title = "Downloaded File"
                    try:
                        title = ddata.get("title", "Downloaded File")
                    except:
                        pass

                    filename = f"downloads/{re.sub(FILENAME_SANITIZE_PATTERN, '', title)}.mp4" if choice == "video" else f"downloads/{re.sub(FILENAME_SANITIZE_PATTERN, '', title)}.m4a"

                    success = download_file(media_url, filename, bot, chat_id)
                    if not success:
                        raise Exception("Direct download failed")
                else:
                    raise Exception("No valid media URL found")
            else:
                raise Exception("API failed")

            try:
                bot.send_message(chat_id, f"✅ সফলভাবে ডাউনলোড হয়েছে!")
                with open(filename, "rb") as f:
                    if choice == "audio":
                        bot.send_audio(chat_id, f, caption=f"🎵 {title}")
                    else:
                        bot.send_video(chat_id, f, caption=f"🎬 {title}")
                bot.delete_message(chat_id, wait_msg.message_id)
            except Exception as e:
                bot.send_message(chat_id, f"❌ ফাইল পাঠাতে সমস্যা হয়েছে:\n{str(e)}")
            finally:
                if filename and os.path.exists(filename):
                    os.remove(filename)

        except Exception as e:
            print(f"[x] Direct method failed: {e}")
            if wait_msg:
                try:
                    bot.edit_message_text(f"❌ ডাউনলোড করতে সমস্যা হয়েছে: {str(e)}\nবিকল্প পদ্ধতি ব্যবহার করা হচ্ছে...", chat_id=chat_id, message_id=wait_msg.message_id)
                except:
                    bot.send_message(chat_id, f"❌ ডাউনলোড করতে সমস্যা হয়েছে: {str(e)}\nবিকল্প পদ্ধতি ব্যবহার করা হচ্ছে...")

            try:
                video = user_search_results.get(chat_id, [])[idx]
                link = video["link"]
                title = video.get("title", "Downloaded File")
                filename = f"downloads/{re.sub(FILENAME_SANITIZE_PATTERN, '', title)}.mp4" if choice == "video" else f"downloads/{re.sub(FILENAME_SANITIZE_PATTERN, '', title)}.m4a"
                fallback_success = fallback_ytdlp(link, filename, audio=(choice == "audio"))
                if not fallback_success:
                    bot.send_message(chat_id, f"❌ বিকল্প পদ্ধতিতেও ডাউনলোড ব্যর্থ হয়েছে।")
                    if filename and os.path.exists(filename): 
                        os.remove(filename)
                    return

                with open(filename, "rb") as f:
                    if choice == "audio":
                        bot.send_audio(chat_id, f, caption=f"🎵 {title}")
                    else:
                        bot.send_video(chat_id, f, caption=f"🎬 {title}")
                if wait_msg:
                    bot.delete_message(chat_id, wait_msg.message_id)
            except Exception as e:
                bot.send_message(chat_id, f"❌ বিকল্প পদ্ধতিতে ফাইল পাঠাতে সমস্যা হয়েছে:\n{str(e)}")
            finally:
                if filename and os.path.exists(filename):
                    os.remove(filename)


    @bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("download_"))
    def handle_download(call: CallbackQuery):
        if not call.data:
            bot.answer_callback_query(call.id, "Invalid request")
            return
        
        parts = call.data.split("_")
        idx_or_link = parts[1]
        choice = parts[2]
        chat_id = call.message.chat.id

        if chat_id not in user_search_results:
            bot.answer_callback_query(call.id, "সেশন শেষ হয়ে গেছে। দয়া করে আবার সার্চ করুন।")
            return

        if "http" in idx_or_link:
            # Direct link - this shouldn't happen in normal operation since we use indices
            # But handle it gracefully by sending error message
            bot.send_message(chat_id, "❌ Direct link processing is not supported in this callback. Please use the search function.")
        else:
            idx = int(idx_or_link)
            # The download function needs the index, not the link itself
            threading.Thread(target=process_download, args=(bot, chat_id, idx, choice)).start()

        bot.answer_callback_query(call.id)
