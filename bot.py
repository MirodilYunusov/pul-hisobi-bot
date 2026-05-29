import telebot
import json
import os
from datetime import datetime

TOKEN = "7824009799:AAFsXJKrJAilKlK4SwRvcXWbL52VaT86y38"

bot = telebot.TeleBot(TOKEN)

# Ma'lumotlarni saqlash
def malumot_yukla():
    if os.path.exists("pul.json"):
        with open("pul.json", "r") as f:
            return json.load(f)
    return {"kirimlar": [], "chiqimlar": []}

def malumot_saqlа(data):
    with open("pul.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# /start
@bot.message_handler(commands=["start"])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("📥 Kirim", "📤 Chiqim")
    keyboard.row("📊 Hisobot", "🗑 Tozala")
    bot.send_message(message.chat.id,
        "💰 Pul Hisobi Botiga xush kelibsiz!",
        reply_markup=keyboard)
    
    @bot.message_handler(func=lambda m: m.text in ["📥 Kirim", "📤 Chiqim", "📊 Hisobot", "🗑 Tozala"])
def tugma_handler(message):
    if message.text == "📥 Kirim":
        kirim_boshlash(message)
    elif message.text == "📤 Chiqim":
        chiqim_boshlash(message)
    elif message.text == "📊 Hisobot":
        hisobot(message)
    elif message.text == "🗑 Tozala":
        tozala(message)

# /kirim
@bot.message_handler(commands=["kirim"])
def kirim_boshlash(message):
    bot.send_message(message.chat.id, "📥 Qancha pul kirdi? (faqat raqam yoz)\nMasalan: 50000")
    bot.register_next_step_handler(message, kirim_summa)

def kirim_summa(message):
    try:
        summa = float(message.text)
        bot.send_message(message.chat.id, "📝 Qayerdan? (masalan: ishxona, qarz oldi)")
        bot.register_next_step_handler(message, lambda m: kirim_saqlа(m, summa))
    except:
        bot.send_message(message.chat.id, "❌ Faqat raqam yoz! Qaytadan /kirim")

def kirim_saqlа(message, summa):
    data = malumot_yukla()
    data["kirimlar"].append({
        "summa": summa,
        "sabab": message.text,
        "vaqt": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    malumot_saqlа(data)
    bot.send_message(message.chat.id, f"✅ Kirim saqlandi!\n💵 Summa: {summa:,.0f} so'm\n📝 Sabab: {message.text}")

# /chiqim
@bot.message_handler(commands=["chiqim"])
def chiqim_boshlash(message):
    bot.send_message(message.chat.id, "📤 Qancha pul chiqdi? (faqat raqam yoz)\nMasalan: 20000")
    bot.register_next_step_handler(message, chiqim_summa)

def chiqim_summa(message):
    try:
        summa = float(message.text)
        bot.send_message(message.chat.id, "📝 Nimaga? (masalan: ovqat, transport)")
        bot.register_next_step_handler(message, lambda m: chiqim_saqlа(m, summa))
    except:
        bot.send_message(message.chat.id, "❌ Faqat raqam yoz! Qaytadan /chiqim")

def chiqim_saqlа(message, summa):
    data = malumot_yukla()
    data["chiqimlar"].append({
        "summa": summa,
        "sabab": message.text,
        "vaqt": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    malumot_saqlа(data)
    bot.send_message(message.chat.id, f"✅ Chiqim saqlandi!\n💸 Summa: {summa:,.0f} so'm\n📝 Sabab: {message.text}")

# /hisobot
@bot.message_handler(commands=["hisobot"])
def hisobot(message):
    data = malumot_yukla()
    
    jami_kirim = sum(k["summa"] for k in data["kirimlar"])
    jami_chiqim = sum(c["summa"] for c in data["chiqimlar"])
    qoldiq = jami_kirim - jami_chiqim

    matn = f"📊 HISOBOT\n\n"
    matn += f"📥 Jami kirim: {jami_kirim:,.0f} so'm\n"
    matn += f"📤 Jami chiqim: {jami_chiqim:,.0f} so'm\n"
    matn += f"💰 Qoldiq: {qoldiq:,.0f} so'm\n\n"

    if data["kirimlar"]:
        matn += "📥 So'nggi kirimlar:\n"
        for k in data["kirimlar"][-3:]:
            matn += f"  • {k['summa']:,.0f} so'm — {k['sabab']} ({k['vaqt']})\n"

    if data["chiqimlar"]:
        matn += "\n📤 So'nggi chiqimlar:\n"
        for c in data["chiqimlar"][-3:]:
            matn += f"  • {c['summa']:,.0f} so'm — {c['sabab']} ({c['vaqt']})\n"

    bot.send_message(message.chat.id, matn)

# /tozala
@bot.message_handler(commands=["tozala"])
def tozala(message):
    malumot_saqlа({"kirimlar": [], "chiqimlar": []})
    bot.send_message(message.chat.id, "🗑 Barcha ma'lumotlar o'chirildi!")

print("Bot ishga tushdi...")
bot.polling()