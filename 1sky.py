
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import smtplib
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging

# إعداد تسجيل الأخطاء
logging.basicConfig(level=logging.INFO)

# ضع التوكن الخاص بك هنا
Token = "7555688318:AAFa1-6j1oIaL_4W04DK3viH6s6-sR1nz5U"
bot = telebot.TeleBot(Token, parse_mode="Markdown")

Owner = '6517259054'
BayaTi = set()

user_data = {}
info_updated = {}

start_spam_button = types.InlineKeyboardButton(text="بدء الإرسال", callback_data="start_spam")
stop_spam_button = types.InlineKeyboardButton(text="إيقاف الإرسال", callback_data="stop_spam")
view_accounts_button = types.InlineKeyboardButton(text="عرض حساباتك", callback_data="view_accounts")
set_email_button = types.InlineKeyboardButton(text="تعين حسابك", callback_data="set_email")
set_victim_email_button = types.InlineKeyboardButton(text="تعين بريد الدعم", callback_data="set_victim_email")
set_message_subject_button = types.InlineKeyboardButton(text="تعيين موضوع", callback_data="set_message_subject")
set_message_button = types.InlineKeyboardButton(text="تعيين كليشة", callback_data="set_message")
set_send_count_button = types.InlineKeyboardButton(text="تعيين عدد إرسال", callback_data="set_send_count")
set_image_button = types.InlineKeyboardButton(text="تعيين صورة", callback_data="upload_image")
set_interval_button = types.InlineKeyboardButton(text="تعيين سليب", callback_data="set_interval")
clear_upload_image_button = types.InlineKeyboardButton(text="مسح صورة الرفع", callback_data="clear_upload_image")
view_info_button = types.InlineKeyboardButton(text="عرض معلوماتك", callback_data="view_info")
clear_info_button = types.InlineKeyboardButton(text="مسح معلوماتك", callback_data="clear_info")

telegram_channel_button = types.InlineKeyboardButton(text="قناتي", url="https://t.me/HORNS4")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    if user_id in BayaTi:
        if user_id not in user_data:
            user_data[user_id] = initialize_user_data()
        if user_id not in info_updated:
            info_updated[user_id] = False
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(start_spam_button, stop_spam_button)
        markup.add(view_accounts_button, set_email_button)
        markup.add(set_victim_email_button, set_message_subject_button)
        markup.add(set_message_button, set_send_count_button)
        markup.add(set_image_button, set_interval_button)
        markup.add(view_info_button, clear_upload_image_button)
        markup.add(clear_info_button)
        markup.add(telegram_channel_button)
        bot.reply_to(message, "مرحبًا بك في الروبوت الذي يرسل تقارير إلى Telegram الخاص بـSKY", reply_markup=markup)
    else:
        bot.reply_to(message, "*• • نجب عزيزي ، ارسلت شعار @J7OOO للمالك حتى يوافق عليك ...*")
        request_approval(user_id, message.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("Done_") or call.data.startswith("Reject_"))
def handle_approval(call):
    user_id = int(call.data.split('_')[1])
    if call.data.startswith('Done_'):
        BayaTi.add(user_id)
        bot.send_message(user_id, "*تم وافقت عليه*")
        bot.send_message(Owner, "*• وافقت عليه ياروعه ...*")
    elif call.data.startswith("Reject_"):
        bot.send_message(user_id, "*• ما وافقت عليك ياروعه هههههههه...*")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.message.chat.id
    if user_id not in BayaTi:
        bot.send_message(user_id, "لم يتم الموافقة عليك بعد.")
        return

    if call.data == "set_email":
        bot.send_message(user_id, "أرسل الايميل:رمز تطبيقات")
        bot.register_next_step_handler(call.message, set_email, user_id)

    elif call.data == "set_victim_email":
        bot.send_message(user_id, "أرسل إيميلات الضحايا مفصولة بفواصل")
        bot.register_next_step_handler(call.message, set_victim_email, user_id)

    elif call.data == "set_message_subject":
        bot.send_message(user_id, "أرسل موضوع الرسالة")
        bot.register_next_step_handler(call.message, set_message_subject, user_id)

    elif call.data == "set_message":
        bot.send_message(user_id, "أرسل الكليشة ")
        bot.register_next_step_handler(call.message, set_message, user_id)

    elif call.data == "set_send_count":
        bot.send_message(user_id, "أرسل عدد الرسائل ")
        bot.register_next_step_handler(call.message, set_send_count, user_id)

    elif call.data == "set_interval":
        bot.send_message(user_id, "ارسل الوقت بين رسالة ورسالة بثواني")
        bot.register_next_step_handler(call.message, set_interval, user_id)

    elif call.data == "start_spam":
        user_data[user_id]['is_spamming'] = True
        start_spam(user_id)

    elif call.data == "stop_spam":
        user_data[user_id]['is_spamming'] = False
        bot.send_message(user_id, "تم إيقاف الإرسال.")

    elif call.data == "view_info":
        if info_updated.get(user_id, False):
            bot.send_message(user_id, "تم تحديث المعلومات.")
            info_updated[user_id] = False
        info_text = (f"البريد الإلكتروني: {', '.join([account['email'] for account in user_data[user_id]['accounts']])}\n"
                     f"رمز التطبيقات: {', '.join([account['password'] for account in user_data[user_id]['accounts']])}\n"
                     f"موضوع الرسالة: {user_data[user_id]['subject']}\n"
                     f"الرسالة: {user_data[user_id]['message_body']}\n"
                     f"سليب الرسائل: {user_data[user_id]['interval']} ثانية\n"
                     f"عدد الرسائل: {user_data[user_id]['number']}\n"
                     f"مسار الصورة: {'تم رفع الصورة' if user_data[user_id]['image_data'] else 'لم يتم تعيين صورة'}")
        bot.send_message(user_id, info_text)

    elif call.data == "clear_info":
        clear_info(user_id)
        info_updated[user_id] = True
        bot.send_message(user_id, "تم مسح جميع المعلومات.")

    elif call.data == "clear_upload_image":
        clear_uploaded_image(user_id)
        info_updated[user_id] = True
        bot.send_message(user_id, "تم مسح صورة الرفع.")

    elif call.data == "upload_image":
        bot.send_message(user_id, "ارسل الصورة")
        bot.register_next_step_handler(call.message, upload_image, user_id)

    elif call.data == "view_accounts":
        if user_data[user_id]['accounts']:
            accounts_text = "\n".join([f"{account['email']} : {account['password']}" for account in user_data[user_id]['accounts']])
            bot.send_message(user_id, f"الحسابات الموجودة:\n{accounts_text}")
            bot.send_message(user_id, "لحذف حساب، أرسل /cler ايميل:باسورد")
        else:
            bot.send_message(user_id, "لا توجد حسابات مضافة حتى الآن.")

@bot.message_handler(commands=['cler'])
def delete_account(message):
    user_id = message.from_user.id
    if message.text.startswith('/cler '):
        email_password = message.text.split('/cler ')[1].split(':')
        if len(email_password) == 2:
            email = email_password[0].strip()
            password = email_password[1].strip()
            user_data[user_id]['accounts'] = [acc for acc in user_data[user_id]['accounts'] if not (acc['email'] == email and acc['password'] == password)]
            bot.reply_to(message, f"تم حذف الحساب بنجاح: {email}:{password}")
        else:
            bot.reply_to(message, "الرجاء إدخال الأمر بالصيغة الصحيحة: /cler ايميل:باسورد")

def set_email(message, user_id):
    email_password = message.text.split(":")
    if len(email_password) != 2:
        bot.send_message(user_id, "الرجاء إدخال البريد الإلكتروني وكلمة المرور للتطبيقات بالصيغة الصحيحة (البريد:كلمة المرور).")
        return
    email = email_password[0].strip()
    password = email_password[1].strip()
    user_data[user_id]['accounts'].append({'email': email, 'password': password})
    info_updated[user_id] = True
    bot.send_message(user_id, f"تم تعيين الحساب بنجاح: {email}:{password}")

def set_victim_email(message, user_id):
    victim_emails = message.text.split(',')
    user_data[user_id]['victim_emails'] = [email.strip() for email in victim_emails]
    info_updated[user_id] = True
    bot.send_message(user_id, "تم تعيين إيميلات الضحايا بنجاح.")

def set_message_subject(message, user_id):
    user_data[user_id]['subject'] = message.text.strip()
    info_updated[user_id] = True
    bot.send_message(user_id, "تم تعيين موضوع الرسالة.")

def set_message(message, user_id):
    user_data[user_id]['message_body'] = message.text.strip()
    info_updated[user_id] = True
    bot.send_message(user_id, "تم تعيين كليشة الرسالة.")

def set_send_count(message, user_id):
    try:
        count = int(message.text.strip())
        user_data[user_id]['number'] = count
        info_updated[user_id] = True
        bot.send_message(user_id, "تم تعيين عدد الرسائل.")
    except ValueError:
        bot.send_message(user_id, "الرجاء إدخال عدد صحيح.")

def set_interval(message, user_id):
    try:
        interval = float(message.text.strip())
        user_data[user_id]['interval'] = interval
        info_updated[user_id] = True
        bot.send_message(user_id, "تم تعيين الوقت بين الرسائل.")
    except ValueError:
        bot.send_message(user_id, "الرجاء إدخال عدد صحيح.")

def upload_image(message, user_id):
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        user_data[user_id]['image_data'] = downloaded_file
        info_updated[user_id] = True
        bot.send_message(user_id, "تم رفع الصورة بنجاح.")
    else:
        bot.send_message(user_id, "الرجاء إرسال صورة.")

def clear_info(user_id):
    user_data[user_id] = initialize_user_data()
    info_updated[user_id] = True

def clear_uploaded_image(user_id):
    user_data[user_id]['image_data'] = None
    info_updated[user_id] = True

def initialize_user_data():
    return {
        'accounts': [],
        'victim_emails': [],
        'subject': '',
        'message_body': '',
        'number': 0,
        'interval': 0.0,
        'image_data': None,
        'is_spamming': False
    }

def start_spam(user_id):
    if not user_data[user_id]['accounts']:
        bot.send_message(user_id, "لم تقم بتعيين أي حسابات للإرسال.")
        return
    if not user_data[user_id]['victim_emails']:
        bot.send_message(user_id, "لم تقم بتعيين أي إيميلات للضحايا.")
        return
    if not user_data[user_id]['subject'] or not user_data[user_id]['message_body']:
        bot.send_message(user_id, "لم تقم بتعيين موضوع الرسالة أو كليشة الرسالة.")
        return
    if user_data[user_id]['number'] <= 0:
        bot.send_message(user_id, "عدد الرسائل يجب أن يكون أكبر من صفر.")
        return

    bot.send_message(user_id, "بدء الإرسال...")

    for account in user_data[user_id]['accounts']:
        email = account['email']
        password = account['password']

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)

            for victim_email in user_data[user_id]['victim_emails']:
                for _ in range(user_data[user_id]['number']):
                    if not user_data[user_id]['is_spamming']:
                        break

                    msg = MIMEMultipart()
                    msg['From'] = email
                    msg['To'] = victim_email
                    msg['Subject'] = user_data[user_id]['subject']
                    msg.attach(MIMEText(user_data[user_id]['message_body'], 'plain'))

                    if user_data[user_id]['image_data']:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(user_data[user_id]['image_data'])
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', "attachment; filename= image.png")
                        msg.attach(part)

                    server.sendmail(email, victim_email, msg.as_string())
                    bot.send_message(user_id, f"تم إرسال الرسالة إلى {victim_email}")
                    sleep(user_data[user_id]['interval'])

            server.quit()
        except Exception as e:
            bot.send_message(user_id, f"حدث خطأ أثناء الإرسال من {email}: {str(e)}")

    bot.send_message(user_id, "انتهى الإرسال.")

def request_approval(user_id, username):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="الموافقة", callback_data=f"Done_{user_id}"),
        InlineKeyboardButton(text="الرفض", callback_data=f"Reject_{user_id}")
    )
    bot.send_message(Owner, f"طلب جديد من المستخدم: [{username}](tg://user?id={user_id})", reply_markup=markup)

try:
    bot.polling(none_stop=True)
except Exception as e:
    logging.error(f"خطأ: {str(e)}")