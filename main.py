from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+
# ---------- CONFIG ----------
API_ID = 38016148            # my.telegram.org မှ
API_HASH = "2239cc376facdb84cb5b7f2f1d7bf002"

BOT_TOKEN = "8431786252:AAFFLfJiExGfB7FRulS_Pl83XUO_PXME6cQ"

# Provided employee list
EMPLOYEES = [
    "SHANE ARKAR", "SAN SAN HLAING", "SAI WIN MYINT", "PAN WINT HLWAR", "NWAY NWAY OO",
    "ZIN KO KHANT", "WAH WAH HLAING", "WUTT YI", "NAN EI SWE", "NAY MYO AUNG",
    "THAE EI PHYO", "THAN THAN HTAY", "MAW MAW", "SEINT SEINT THU", "NANG PHYU WIN MO",
    "EI THANDAR AUNG", "PHOO MYAT THWE", "KHAM MYAT", "CHERRY SAN", "KYI WAI YAN",
    "SU PAN HTWAR", "THU ZAR LWIN", "EI YADANAR PHYO", "KHAING ZAW WAI", "WAI ZIN OO",
    "SANDAR MOE", "YOON SHWE YI OO", "AUNG SAY", "HTET HTET HLAING", "TIN ZAR",
    "MYO THU SHEIN", "KHIN SWE WIN", "SU YADANAR", "ZAW THU LWIN", "YE LIN TUN",
    "PAYE PAYE", "NANG KYI PHWE", "ARKAR MIN HTET", "EI SHWE ZIN", "AUNG MIN KHANT",
    "KHAING HNIN WAI", "SAI LYNN MAUNG", "MAN CHUU", "NYEIN CHAN", "YOON NADI PHYO",
    "KHIN THET WAI", "THURA AUNG", "NAN EI EI WINE", "NYI HTET NAING", "AUNG PAING",
    "HLAING ZAW HTET", "SHAIN KO NAING", "CHIT KO OO", "WANA AUNG", "NYI NYI ZAW",
    "SAI AUNG AUNG", "SWEL THET WAI KYAW", "THI THI SWE", "YAN NAING SOE", "NANG EAINDRAY THU",
    "SHWE ZIN WIN", "KHAING THAZIN", "ZAY YAR MYINT HTUN ZAW", "MIN MYAT SOE", "HLAING WAI AUNG",
    "MYO MIN KHANT", "THET NAING OO", "PHYU ZIN OO", "EI EI WIN", "KYAW MYO HTET",
    "KYAW ZIN WIN", "HTAY WAI AUNG", "THAW WAI YAN ZAW", "THANT ZIN OO", "WANA TUN",
    "PONT PONT AYE", "HTEIN LIN AUNG", "AUNG KO KO", "YAN NAING TUN", "THAN THAN AYE",
    "HSU MON AUNG", "NAN WUTT YI", "PHYO ZIN LIN", "SAI KHAN MOON", "LIN HTET KYAW",
    "THIKE SOE OO", "WAI ZIN KHAING", "ZAR NI PHYO", "HTUN NAY LIN", "MYINT MYAT THAW",
    "NAN CHAW SU KYAW", "SHOON LAE MAY AUNG", "SANOE", "NAN SU PONE CHIT", "KAUNG MYAT OO",
    "PHYO LAPYAE", "HLA MYO THU", "NAY TOE AUNG", "THIHA ZAW", "AYE MYAT SOE",
    "YE KYAW HTWE", "HTET HTET", "AYE MYAT NOE", "SAN MIN HTWE", "NYI NYI ZAW",
    "TIN TIN MYO", "HTET LIN AUNG", "BA SOE", "HSU KABYAR", "MYA THWAY CHAL",
    "LAMIN THIDAR HTWE"
]

# fill up to 200
while len(EMPLOYEES) < 200:
    EMPLOYEES.append(f"Employee{len(EMPLOYEES)+1}")

COLOR_SEQUENCE = ["🟢","🟢","🟡","🟡","🔴","🔴"]

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open("start.jpg", "rb"),
        caption="Welcome To Office Secret Auto Bot  👋"
    )

# ---------------- PROCESS NUMBER ----------------
async def process_star(number_key: str, update_obj, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data.setdefault("clicks", {})

    my_timezone = ZoneInfo("Asia/Yangon")  # Yangon time zone

    if number_key not in user_data:
        now = datetime.now(my_timezone)
        user_data[number_key] = {
            "count": 1,
            "last_time": now,
            "employee": EMPLOYEES[int(number_key[3:]) - 1]
        }
        color = COLOR_SEQUENCE[0]
        start_time = now.strftime("%H:%M")
        await update_obj.reply_text(f"{color} {user_data[number_key]['employee']} {start_time}")
        return

    info = user_data[number_key]
    now = datetime.now(my_timezone)
    prev_time = info["last_time"]
    info["last_time"] = now
    info["count"] += 1

    color = COLOR_SEQUENCE[(info["count"] - 1) % len(COLOR_SEQUENCE)]

    if info["count"] % 2 == 1:
        await update_obj.reply_text(f"{color} {info['employee']} {now.strftime('%H:%M')}")
    else:
        delta_min = int((now - prev_time).total_seconds() / 60)
        await update_obj.reply_text(f"{color} {info['employee']} {delta_min} မိနစ်ကြာမြင့်သည်")

# ---------------- BUTTON HANDLER ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("ID နံပါတ် 1 မှ 111 ထိနှစ်သက်ရာနံပါတ်ကိုရေးပို့ပါ")

# ---------------- MESSAGE HANDLER ----------------
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.isdigit():
        num = int(text)
        if 1 <= num <= 200:
            await process_star(f"num{num}", update.message, context)

# ---------------- APP ----------------
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

print("Bot is running...")
app.run_polling()

