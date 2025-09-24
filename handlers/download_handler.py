
import os
import re
import json
import yt_dlp
import requests
from telebot import TeleBot
from telebot.types import Message

# ---------------------- Config ----------------------

# URLs খোঁজার রেজেক্স
URL_RE = re.compile(r'(https?://[^\s]+)')

# কুকিজ ফোল্ডারের পথ (এই ফাইলের এক লেভেল উপরে cookies/)
COOKIES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cookies')

# ডোমেইন → কুকিজ ফাইল ম্যাপ
PLATFORM_COOKIES = {
    "facebook.com": "facebook.txt",
    "fb.watch": "facebook.txt",
    "instagram.com": "instagram.txt",
    "instagr.am": "instagram.txt",
}

# টেলিগ্রামের ভিডিও আপলোড সীমা ~2GB
TELEGRAM_2GB = 2 * 1024 * 1024 * 1024

# YouTube API endpoint (আপনি যেই API ব্যবহার করতে চান)
YOUTUBE_API_ENDPOINT = "https://yt-api-flax.vercel.app/dl?url="

# ---------------------- Utils ----------------------

def _detect_domain(url: str) -> str:
    """URL থেকে ডোমেইন সনাক্ত করে।"""
    try:
        m = re.match(r'https?://(?:www\.)?([^/]+)', url)
        return m.group(1).lower() if m else ""
    except Exception:
        return ""

def _cookie_path_for(domain: str) -> str | None:
    """ডোমেইনের জন্য কুকিজ ফাইলের পথ প্রদান করে।"""
    for k, v in PLATFORM_COOKIES.items():
        if k in domain:
            return os.path.join(COOKIES_FOLDER, v)
    return None

def _is_youtube_domain(domain: str) -> bool:
    """ডোমেইনটি YouTube-এর কিনা তা পরীক্ষা করে।"""
    return "youtube.com" in domain or "youtu.be" in domain

def _choose_best_muxed_format(info: dict) -> str | None:
    """info থেকে সেরা muxed ফরম্যাট আইডি বেছে নেয়।"""
    fmts = info.get("formats") or []
    muxed = []
    for f in fmts:
        ac = (f.get("acodec") or "none").lower()
        vc = (f.get("vcodec") or "none").lower()
        if ac != "none" and vc != "none":
            muxed.append(f)
    if not muxed:
        return None
    
    # mp4 প্রাধান্য
    mp4_muxed = [f for f in muxed if (f.get("ext") or "").lower() == "mp4"]
    if mp4_muxed:
        mp4_muxed.sort(key=lambda f: (f.get("height") or 0, f.get("tbr") or 0), reverse=True)
        return str(mp4_muxed[0].get("format_id"))

    # অন্য যেকোনো muxed
    muxed.sort(key=lambda f: (f.get("height") or 0, f.get("tbr") or 0), reverse=True)
    return str(muxed[0].get("format_id"))

# ---------------------- Download Core (yt-dlp) ----------------------

def download_video_yt_dlp(url: str, download_dir: str, cookies_path: str | None) -> str:
    """yt-dlp ব্যবহার করে ভিডিও ডাউনলোড করে।"""
    os.makedirs(download_dir, exist_ok=True)
    opts = {
        "quiet": True,
        "noplaylist": True,
        "retries": 3,
        "ignoreerrors": False,
        "geo_bypass": True,
        "outtmpl": os.path.join(download_dir, "%(title).150s-%(id)s.%(ext)s"),
    }
    if cookies_path and os.path.exists(cookies_path):
        opts["cookiefile"] = cookies_path
    
    # FB/IG এর জন্য ফরম্যাট পছন্দ
    opts["format"] = "b[ext=mp4][acodec!=none][vcodec!=none]/b"
    
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        path = info.get("requested_downloads", [{}])[0].get("filepath")
        if not path or not os.path.exists(path):
            # ফলব্যাক
            path = ydl.prepare_filename(info)
        if not path or not os.path.exists(path):
            raise RuntimeError("ডাউনলোড করা ফাইলটি পাওয়া যায় না।")
        return path

# ---------------------- Telegram Handler ----------------------

def register(bot: TeleBot, custom_command_handler, command_prefixes_list):

    @custom_command_handler("dl")
    def handle_download(message: Message):
        """
        ব্যবহার:
          <prefix>dl <url>
        """
        text = message.text or ""
        tokens = text.split(maxsplit=1) 
        
        if len(tokens) < 2: 
            bot.reply_to(
                message,
                f"⚠️ ভিডিওর লিঙ্ক দিন। উদাহরণ: `{command_prefixes_list[0]}dl https://www.youtube.com/watch?v=xxxxxxxx}}`", # এখানে পরিবর্তন করা হয়েছে
                parse_mode="Markdown"
            )
            return
        
        args = tokens[1].strip() 
        urls = URL_RE.findall(args)
        if not urls:
            bot.reply_to(
                message,
                f"⚠️ ভিডিওর লিঙ্ক দিন। উদাহরণ: `{command_prefixes_list[0]}dl https://www.youtube.com/watch?v=xxxxxxxx}}`", # এখানে পরিবর্তন করা হয়েছে
                parse_mode="Markdown"
            )
            return
        
        url = urls[0].strip()
        domain = _detect_domain(url)
        
        waiting = bot.reply_to(message, "📥 ডাউনলোড হচ্ছে...")
        file_path = None

        try:
            if _is_youtube_domain(domain):
                # YouTube-এর জন্য API ব্যবহার
                api_url = f"{YOUTUBE_API_ENDPOINT}{url}"
                response = requests.get(api_url)
                if response.status_code != 200:
                    raise Exception(f"API থেকে স্ট্যাটাস কোড {response.status_code} পাওয়া গেছে।")
                
                info = response.json()
                if not info.get("success"):
                    raise Exception(f"API এরর: {info.get('error')}")

                # 360p mp4 ফরম্যাট খুঁজে বের করা
                download_link = None
                for media in info.get("medias", []):
                    if media.get("formatId") == 18 and media.get("ext") == "mp4":
                        download_link = media.get("url")
                        break
                
                if download_link:
                    bot.send_message(
                        message.chat.id,
                        f"✅ আপনার 360p ভিডিও এখানে: [**ডাউনলোড করতে ক্লিক করুন**]({download_link})",
                        parse_mode="Markdown"
                    )
                else:
                    bot.send_message(
                        message.chat.id,
                        f"❌ 360p MP4 ফরম্যাট পাওয়া যায়নি। [ভিডিওটি দেখতে এখানে ক্লিক করুন]({url})",
                        parse_mode="Markdown"
                    )

            else:
                # Facebook, Instagram এবং অন্যান্য প্ল্যাটফর্মের জন্য yt-dlp এবং কুকিজ ব্যবহার
                cookie_file = _cookie_path_for(domain)
                if cookie_file and not os.path.exists(cookie_file):
                    bot.reply_to(
                        message,
                        f"❌ `{domain}` এর কুকিজ ফাইল পাওয়া যায়নি: `{os.path.basename(cookie_file)}`",
                        parse_mode="Markdown"
                    )
                    return
                
                file_path = download_video_yt_dlp(url, "downloads", cookie_file)
                
                size = os.path.getsize(file_path) if os.path.exists(file_path) else 0

                with open(file_path, "rb") as vf:
                    if size and size <= TELEGRAM_2GB and (file_path.lower().endswith(".mp4")):
                        bot.send_video(message.chat.id, vf, caption="✅ ডাউনলোড সফল")
                    else:
                        vf.seek(0)
                        bot.send_document(message.chat.id, vf, caption="✅ ডাউনলোড সফল (ডকুমেন্ট)")
            
        except Exception as e:
            hint = ""
            s = str(e).lower()
            if "requested format is not available" in s or "no such format" in s:
                hint = "\n🔎 এই ভিডিওতে mp4 muxed নাও থাকতে পারে।"
            if "age" in s or "sign in" in s or "login" in s or "premium" in s:
                hint += "\n🔒 লগইন/এজ-রেস্ট্রিক্টেড কন্টেন্ট—সঠিক কুকিজ দিন।"

            bot.reply_to(
                message,
                f"❌ ডাউনলোডে সমস্যা হয়েছে:\n`{str(e)}`{hint}",
                parse_mode="Markdown"
            )
        finally:
            if waiting and waiting.message_id:
                try:
                    bot.delete_message(message.chat.id, waiting.message_id)
                except Exception:
                    pass
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as ce:
                    print(f"Cleanup error: {ce}")
