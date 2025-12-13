import os
import uuid
from pyrogram import Client, filters

# ---------- CONFIG ----------
API_ID = 38016148            # my.telegram.org မှ
API_HASH = "2239cc376facdb84cb5b7f2f1d7bf002"
BOT_TOKEN = "8460883145:AAGkADxVKTX3INg6qrvKhJo768448JvYhrs"
# ----------------------------

app = Client(
    "webm_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "🎬 WebM Bot Ready!\n\n"
        "MP4 / Video ပို့လိုက်ရင် WebM ပြန်ပြောင်းပေးမယ်"
    )

@app.on_message(filters.video)
async def convert(client, message):
    input_file = await message.download()
    output_file = f"{uuid.uuid4()}.webm"

    os.system(
        f'ffmpeg -i "{input_file}" '
        f'-c:v libvpx-vp9 -b:v 1M '
        f'-c:a libopus "{output_file}"'
    )

    await message.reply_document(
        output_file,
        caption="✅ Converted to WebM"
    )

    os.remove(input_file)
    os.remove(output_file)

print("Bot is running...")
app.run()