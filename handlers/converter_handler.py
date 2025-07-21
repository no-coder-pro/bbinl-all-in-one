import os
import requests
from moviepy.editor import VideoFileClip

VIDEO_PATH = "temp_video.mp4"
RESIZED_VIDEO_PATH = "temp_video_resized.mp4"
AUDIO_PATH = "output_audio.mp3"

MAX_FILE_SIZE_MB = 50
MAX_DURATION = 60  # seconds

def cleanup_files():
    for file in [VIDEO_PATH, RESIZED_VIDEO_PATH, AUDIO_PATH]:
        if os.path.exists(file):
            os.remove(file)

def register(bot, custom_command_handler, command_prefixes_list): 
    @custom_command_handler("convert")
    def convert_handler(message):
        try:
            file_url = None

            command_text_full = message.text.split(" ", 1)[0].lower()
            actual_command_len = 0
            for prefix in command_prefixes_list: 
                if command_text_full.startswith(f"{prefix}convert"):
                    actual_command_len = len(f"{prefix}convert")
                    break

            args_after_command = message.text[actual_command_len:].strip()

            if message.reply_to_message and message.reply_to_message.video:
                file_id = message.reply_to_message.video.file_id
                file_info = bot.get_file(file_id)
                file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
            elif args_after_command:
                file_url = args_after_command
            else:

                bot.reply_to(message, f"ভিডিও ফাইল রিপ্লাই করো অথবা `{command_prefixes_list[0]}convert [ভিডিও URL]` লিখে পাঠাও।\nউদাহরণ: `{command_prefixes_list[0]}convert https://example.com/video.mp4`", parse_mode="Markdown") 
                return

            if not file_url:
                bot.reply_to(message, "ভিডিও URL পাওয়া যায়নি।")
                return

            bot.reply_to(message, "ভিডিও ডাউনলোড করা হচ্ছে, অপেক্ষা করুন...")

            # ভিডিও ডাউনলোড
            r = requests.get(file_url, stream=True)
            r.raise_for_status()
            with open(VIDEO_PATH, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)

            clip = VideoFileClip(VIDEO_PATH)

            # ডিউরেশন চেক, প্রয়োজনে কাটা
            if clip.duration > MAX_DURATION:
                original_duration = clip.duration
                clip = clip.subclip(0, MAX_DURATION)
                bot.send_message(message.chat.id, f"⚠️ ভিডিওর দৈর্ঘ্য {original_duration:.2f} সেকেন্ড, যা {MAX_DURATION} সেকেন্ডের বেশি। ভিডিওটি প্রথম {MAX_DURATION} সেকেন্ডে কাটা হয়েছে।")

            clip = clip.resize(height=480)

            # ভিডিও রিসাইজ ফাইল সেভ করা
            bot.send_message(message.chat.id, "ভিডিও প্রসেস করা হচ্ছে...")
            clip.write_videofile(RESIZED_VIDEO_PATH, codec='libx264', audio_codec='aac', verbose=False, logger=None)

            # নতুন ভিডিও থেকে অডিও বের করা
            bot.send_message(message.chat.id, "অডিও এক্সট্র্যাক্ট করা হচ্ছে...")
            clip_resized = VideoFileClip(RESIZED_VIDEO_PATH)
            clip_resized.audio.write_audiofile(AUDIO_PATH, bitrate="64k", verbose=False, logger=None)

            audio_size_mb = os.path.getsize(AUDIO_PATH) / (1024 * 1024)
            if audio_size_mb > MAX_FILE_SIZE_MB:
                bot.reply_to(message, f"ফাইল সাইজ {audio_size_mb:.2f}MB, যা অনুমোদিত সাইজ ({MAX_FILE_SIZE_MB}MB) এর বেশি। ছোট ভিডিও ব্যবহার করুন।")
                cleanup_files()
                return

            with open(AUDIO_PATH, "rb") as audio_file:
                bot.send_audio(message.chat.id, audio_file, caption="🎵 ভিডিও থেকে কনভার্ট করা অডিও।")

            cleanup_files()

        except Exception as e:
            bot.reply_to(message, f"❌ এরর হয়েছে: {str(e)}")
            print(f"Converter Error: {e}")
            cleanup_files()