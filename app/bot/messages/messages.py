import os
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.oprations import admin
from app.version import __version__


class _MessageSetings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
        case_sensitive=True,
        extra="ignore",
    )

    START_MAIN_ADMIN: dict = {
        "en": (
            "Welcome!\n"
            "━━━━━━━━━━━━━━━━━\n"
            f"🛡️ version: {__version__}\n"
            "👨‍💻 devlop by: @primez_dev\n"
            "🏢 Sponsor: @Magic_Mizban"
        ),
        "fa": (
            "خوش آمدید!\n"
            "━━━━━━━━━━━━━━━━━\n"
            f"🛡️ version: {__version__}\n"
            "👨‍💻 devlop by: @primez_dev\n"
            "🏢 Sponsor: @Magic_Mizban"
        ),
    }
    START_DEALER: dict = {
        "en": ("👋 Hi, you can use the buttons"),
        "fa": ("👋 درود، میتونی از دکمه های زیر استفادی کنی"),
    }
    START_MESSAGE: dict = {
        "en": ("👋 Welcome, if you want to use this bot you need to register"),
        "fa": ("👋 خوش آمدید، اگر می‌خواهید از سرویس ما استفاده کنید باید ثبت نام کنید"),
    }

    DEALERS_STATUS: dict = {
        "en": (
            "<pre>👤 Username: {username}</pre>\n"
            "⌛ Days remaining: {days_remaining} D\n"
            "📊 Traffic: {traffic} GB\n"
            "💻 Panel in use: {panel}\n"
            "ℹ️ Status: {status}\n"
            "➖➖➖➖➖➖➖➖➖➖\n"
        ),
        "fa": (
            "<pre>👤 نام کاربری: {username}</pre>\n"
            "⌛ روزهای باقی‌مانده: {days_remaining} روز\n"
            "📊 ترافیک: {traffic} گیگابایت\n"
            "💻 پنل درحال استفاده: {panel}\n"
            "ℹ️ وضعیت: {status}\n"
            "➖➖➖➖➖➖➖➖➖➖\n"
        ),
    }
    PANELS_STATUS: dict = {
        "en": (
            "<pre>🌐 Panel name: {name}</pre>\n"
            "⚙️ <b>CPU Usage:</b> {cpu_usage}%\n"
            "💾 <b>Memory Usage:</b> {ram_usage}%\n"
            "🛡️ <b>Xray Status:</b> {xray_status}\n"
            "📝 <b>Xray Version:</b> {xray_version}\n"
            "⏱️ <b>Uptime:</b> {uptime} hours\n"
            "➖➖➖➖➖➖➖➖➖➖\n"
        ),
        "fa": (
            "<pre>🌐 نام پنل: {name}</pre>\n"
            "⚙️ <b>استفاده پردازنده:</b> %{cpu_usage}\n"
            "💾 <b>استفاده رم:</b> %{ram_usage}\n"
            "🛡️ <b>وضعیت ایکسری:</b> {xray_status}\n"
            "📝 <b>نسخه ایکسری:</b> {xray_version}\n"
            "⏱️ <b>مدت روشن بودن:</b> {uptime} ساعت\n"
            "➖➖➖➖➖➖➖➖➖➖\n"
        ),
    }
    LOG_MESSAGE: dict = {
        "en": ("📝 Last 10 log entries:"),
        "fa": ("📝 10 لاگ اخر:"),
    }
    BACKING_UP: dict = {
        "en": ("Backing up database..."),
        "fa": ("پشتیبان گیری از دیتابیس..."),
    }
    HELP_TEXT: dict = {
        "en": (
            "<b>📄 Current help text:</b>\n\n"
            "- {help_text}"
            "━━━━━━━━━━━━━━━━━\n"
            "Please send the new help text:"
        ),
        "fa": (
            "<b>📄 متن راهنمای فعلی:</b>\n\n"
            "- {help_text}\n"
            "━━━━━━━━━━━━━━━━━\n"
            "لطفا متن راهنمای جدید رو بفرستید:"
        ),
    }
    CANCEL_OPERATION: dict = {
        "en": ("🔸 Operation canceled."),
        "fa": ("🔸 عملیات لغو شد."),
    }
    HELP_TEXT_CHANGED: dict = {
        "en": ("✅ Help text changed successfully."),
        "fa": ("✅ متن راهنمای تغییر کرد."),
    }
    ERROR: dict = {
        "en": ("Error: {e}"),
        "fa": ("خطا: {e}"),
    }
    REGISTRATION_TEXT: dict = {
        "en": (
            "<b>⚪ Current registration text:</b>\n\n"
            "- {registration_text}\n"
            "━━━━━━━━━━━━━━━━━\n"
            "Please send the new registration text:"
        ),
        "fa": (
            "<b>⚪ متن ثبت‌نام فعلی:</b>\n\n"
            "- {registration_text}\n"
            "━━━━━━━━━━━━━━━━━\n"
            "لطفا متن ثبت‌نام جدید را بفرستید:"
        ),
    }
    REGISTRATION_TEXT_CHANGED: dict = {
        "en": ("✅ Registration text changed successfully."),
        "fa": ("✅ متن ثبت‌نام تغییر کرد."),
    }
    NOTIF_STATUS: dict = {
        "en": (
            "<b>📳 Current notification status:</b>\n\n"
            "- Start the bot = {start_status}\n"
            "- Create a new client = {create_status}\n"
            "- Delete a client = {delete_status}\n"
        ),
        "fa": (
            "<b>📳 وضعیت اعلان های فعلی:</b>\n\n"
            "- استارت ربات = {start_status}\n"
            "- ساخت یک کاربر توسط نماینده = {create_status}\n"
            "- حذف یک کاربر توسط نماینده = {delete_status}\n"
        ),
    }
    START_NOTIF: dict = {
        "en": (
            "<b>📳 Oh, someone starred the bot:</b>\n\n"
            "<b>👤 Full name:</b> {name}\n"
            "<b>🆔 Username:</b> @{user_id}\n"
            "<b>🪪 Chat ID:</b> {chat_id}\n"
            "<a href='tg://openmessage?user_id={chat_id}'>💬<b> Open chat</b></a>"
        ),
        "fa": (
            "<b>📳 اوه، ربات استارت شد توسط:</b>\n\n"
            "<b>👤 نـام:</b> {name}\n"
            "<b>🆔 نام کاربری:</b> @{user_id}\n"
            "<b>🪪 چت ایدی:</b> {chat_id}\n"
            "<a href='tg://openmessage?user_id={chat_id}'>💬<b> بازکردن چـــت </b></a>"
        ),
    }
    PLAN_IS_NOT_EXIST: dict = {
        "en": ("⚠️ Plan not found!"),
        "fa": ("⚠️ پلن یافت نشد!"),
    }
    SHOW_PLANS: dict = {
        "en": (
            "🆔 ID: {id}\n"
            "📊 Traffic: {traffic} G\n"
            "⌛ Deadline: {deadline} days\n"
            "💸 Price: {price} $\n"
            "━━━━━━━━━━━━━━━━━\n"
        ),
        "fa": (
            "🆔 ایدی پلن: {id}\n"
            "📊 ترافیک: {traffic} گیگ\n"
            "⌛ تاریخ انقضا: {deadline} روز\n"
            "💸 قیمت: {price} تومان\n"
            "━━━━━━━━━━━━━━━━━\n"
        ),
    }
    WAITING_FOR_PLAN_TRAFFIC: dict = {
        "en": ("1- plase enter a traffic(GB) for this plan:"),
        "fa": ("1- لطفا ترافیک(گیگ) برای این پلن را وارد کنید:"),
    }
    WAITING_FOR_PLAN_DEADLINE: dict = {
        "en": ("2- plase enter a deadline(days) for this plan:"),
        "fa": ("2- لطفا تاریخ انقضا(روز) برای این پلن را وارد کنید:"),
    }
    WAITING_FOR_PLAN_PRICE: dict = {
        "en": ("3- plase enter a price($) for this plan:"),
        "fa": ("3- لطفا قیمت(تومان) برای این پلن را وارد کنید:"),
    }
    WAITING_FOR_PLAN_ID: dict = {
        "en": ("0- plase enter a plan id:"),
        "fa": ("0- لطفا ایدی پلن را وارد کنید:"),
    }
    PLAN_NOT_EXIST: dict = {
        "en": ("⚠️ Plan not found!"),
        "fa": ("⚠️ پلن یافت نشد!"),
    }
    PLAN_ADDED: dict = {
        "en": ("✅ Plan added successfully!\n"),
        "fa": ("✅ پلن با موفقیت اضافه شد!\n"),
    }
    INVALID_VALUE: dict = {
        "en": ("⚠️ Invalid value!"),
        "fa": ("⚠️ ورودی نا معتبر است!"),
    }
    PLAN_UPDATED: dict = {
        "en": ("✅ Plan updated successfully!\n"),
        "fa": ("✅ پلن با موفقیت بروز رسانی شد!\n"),
    }
    CONFIRM_PLAN_DELETE: dict = {
        "en": ("⚠️ Are you sure you want to delete this plan?"),
        "fa": ("⚠️ از حذف این پلن اطمینان دارید؟"),
    }
    PLAN_DELETED: dict = {
        "en": ("✅ Plan deleted successfully!\n"),
        "fa": ("✅ پلن با موفقیت حذف شد!\n"),
    }
    WAITING_FOR_CONFIRM_SIGNUP_ADMIN: dict = {
        "en": (
            "ℹ️ Your registration request has been sent to the administrator Please wait..."
        ),
        "fa": ("ℹ️ درخواست شما برای مدیر ارسال شد لطفا صبر کنید..."),
    }
    YOUR_REGISTERITION_REQUEST_REJECTED: dict = {
        "en": ("⚠️ Your request has been rejected."),
        "fa": ("⚠️ درخواست شما رد شد."),
    }
    A_NEW_SIGNUP_REQUEST: dict = {
        "en": (
            "📳 New registration request by:\n\n"
            "👤 Full name: {name}\n"
            "<b>🆔 Username:</b> @{user_id}\n"
            "<b>🪪 Chat ID:</b> {chat_id}\n"
            "<a href='tg://openmessage?user_id={chat_id}'>💬<b> Open chat</b></a>"
        ),
        "fa": (
            "📳 درخواست ایجاد حساب جدید از:\n\n"
            "<b>👤 نـام:</b> {name}\n"
            "<b>🆔 نام کاربری:</b> @{user_id}\n"
            "<b>🪪 چت ایدی:</b> {chat_id}\n"
            "<a href='tg://openmessage?user_id={chat_id}'>💬<b> بازکردن چـــت </b></a>"
        ),
    }
    WAITING_FOR_CONFIRM_SIGNUP_SUCCESS: dict = {
        "en": ("✅ Your request has been accepted\nYour plan has been added"),
        "fa": ("✅ درخواست شما پذیرش شد\nپلن شما با موفقیت اضافه شد"),
    }
    REJECT_REGISTERATION_RULES: dict = {
        "en": (
            "⚠️ Rejection of registration rules by:\n\n"
            "👤 Full name: {name}\n"
            "<b>🆔 Username:</b> @{user_id}\n"
            "<b>🪪 Chat ID:</b> {chat_id}\n"
            "<a href='tg://openmessage?user_id={chat_id}'>💬<b> Open chat</b></a>"
        ),
        "fa": (
            "📳 یک رد قوانین ثبت نام جدید توسط:\n\n"
            "<b>👤 نـام:</b> {name}\n"
            "<b>🆔 نام کاربری:</b> @{user_id}\n"
            "<b>🪪 چت ایدی:</b> {chat_id}\n"
            "<a href='tg://openmessage?user_id={chat_id}'>💬<b> بازکردن چـــت </b></a>"
        ),
    }
    CHOOSE_A_USERNAME_FOR_THE_REQUESTER: dict = {
        "en": ("1- Registration request approved. Please enter a Username:"),
        "fa": ("1- درخواست ثبت‌نام تایید شد. لطفاً یک یوزرنیم وارد کنید:"),
    }
    CHOOSE_A_PASSWORD_FOR_THE_REQUESTER: dict = {
        "en": ("2- Please enter a Password:"),
        "fa": ("2- لطفا یک پسورد وارد کنید:"),
    }
    CHOOSE_A_PANEL_FOR_THE_REQUESTER: dict = {
        "en": ("3- Please enter a panel 🆔 for this dealer:"),
        "fa": ("3- لطفا یک پنل 🆔 برای این نماینده وارد کنید:"),
    }
    PANEL_NOT_EXIST: dict = {
        "en": ("⚠️ Panel not found!"),
        "fa": ("⚠️ پنل یافت نشد!"),
    }
    CHOOSE_A_INBOUND_FOR_THE_REQUESTER: dict = {
        "en": ("4- Please enter a inbound id for this dealer:"),
        "fa": ("4- لطفا یک اینباند ایدی برای این نماینده وارد کنید:"),
    }
    REGISTERITION_REQUEST_APPROVED: dict = {
        "en": (
            "✅ Registration request approved and panel access sent to dealer/admin"
        ),
        "fa": ("✅ درخواست ثبت نام تایید شد و دسترسی پنل به نماینده ارسال شد"),
    }
    YOUR_REGISTERITION_REQUEST_HAS_BEEN_CONFIRMED: dict = {
        "en": (
            "<b>🎉 Your registration has been confirmed.</b>\n\n"
            "Username: {username}\n"
            "Password: {password}\n"
        ),
        "fa": (
            "<b>🎉 درخواست ثبت نام شما تایید شد.</b>\n\n"
            "یوزرنیم: {username}\n"
            "پسورد: {password}\n"
        ),
    }
    LOGIN_STEP1: dict = {
        "en": ("1- Please enter your username:"),
        "fa": ("1- لطفا یوزرنیم خودتون رو وارد کنید:"),
    }
    LOGIN_STEP2: dict = {
        "en": ("2- Please enter your password:"),
        "fa": ("2- لطفا پسورد خودتون رو وارد کنید:"),
    }
    LOGIN_STEP3: dict = {
        "en": ("3- Please solve this captcha:\n{question} = ?"),
        "fa": ("3- لطفا این کپچا رو حل کنید:\n{question} = ?"),
    }
    CAPTCHA_WRONG: dict = {
        "en": ("❌ Wrong answer! Please try again:"),
        "fa": ("❌ پاسخ اشتباه! لطفا دوباره تلاش کنید:"),
    }
    LOGIN_SUCCESS: dict = {
        "en": ("✅ Login successful! Welcome back."),
        "fa": ("✅ ورود موفقیت آمیز! خوش آمدید."),
    }
    LOGIN_FAILED: dict = {
        "en": ("❌ Login failed! Invalid username or password."),
        "fa": ("❌ ورود ناموفق! نام کاربری یا رمز عبور اشتباه است."),
    }
    MY_ACCOUNT: dict = {
        "en": (
            "👤 Username: {username}\n"
            "🔐 Password: {password}\n"
            "📊 Traffic: {traffic}\n"
            "⌛ Expiry time: {expiry_time}D"
        ),
        "fa": (
            ".\n"
            "👤 نام کاربری: {username}\n"
            "🔐 رمزعبور: {password}\n"
            "📊 ترافیک: {traffic} گیگ\n"
            "⌛ انقضا: {expiry_time}روز"
        ),
    }
    SHOW_PLANS_FOR_DEALER: dict = {
        "en": ("🛍️ Available  plans:"),
        "fa": ("🛍️ پلن های موجود برای شارژ اشتراک شما:"),
    }
    SELECTED_PLAN: dict = {
        "en": (
            "<b> Selected plan:</b>\n\n"
            "📊 Traffic: {traffic} GB\n"
            "⌛ Expiry time: {expiry_time}D\n"
            "💸 Price: {price} $"
        ),
        "fa": (
            "<b>پلن انتخابی شما برای خرید:</b>\n\n"
            "📊 ترافیک: {traffic} گیگ\n"
            "⌛ تاریخ انقضا: {expiry_time}روز\n"
            "💸 قیمت: {price} تومان"
        ),
    }

    PAYMENT_WITH_CARD: dict = {"en": "💳 Card Payment", "fa": "💳 کارت به کارت"}

    CANCEL: dict = {"en": "❌ Cancel", "fa": "❌ انصراف"}

    SEND_PAYMENT_METHODS: dict = {
        "en": "Please click the confirm button to proceed with card payment.",
        "fa": "لطفا برای ادامه خرید یکی از روش های موجود را انتخاب کنید.",
    }

    SEND_CARD_PAYMENT_PHOTO: dict = {
        "en": "ℹ️ Please send a photo of your card payment receipt\n\n💸Amount: {price}\n💳Card number: {card_num}",
        "fa": "ℹ️ لطفا عکس رسید پرداخت کارت به کارت را ارسال کنید\n\n💸مبلغ: {price}\n💳شماره کارت: {card_num}",
    }

    PAYMENT_SENT_FOR_APPROVAL: dict = {
        "en": "Your payment has been sent for approval. We will notify you once it's approved.",
        "fa": "پرداخت شما برای تایید ارسال شد. پس از تایید به شما اطلاع داده خواهد شد.",
    }

    PAYMENT_CONFIRMATION_REQUEST: dict = {
        "en": (
            "📳 Payment confirmation request\n\n"
            "👤 From: {username}\n"
            "📊 Traffic: {traffic} GB\n"
            "⌛ Days: {days}\n"
            "💸 Price: {price} $"
        ),
        "fa": (
            "📳 درخواست تایید پرداخت\n\n"
            "👤 از: {username}\n"
            "📊 ترافیک: {traffic} گیگابایت\n"
            "⌛ انقضا: {days} روز\n"
            "💸 قیمت: {price} تومان"
        ),
    }

    APPROVE_PAYMENT: dict = {"en": "✅ Approve", "fa": "✅ تایید"}

    REJECT_PAYMENT: dict = {"en": "❌ Reject", "fa": "❌ رد"}

    PAYMENT_APPROVED: dict = {
        "en": "✅ Your payment has been approved! Your plan has been activated.",
        "fa": "✅ پرداخت شما تایید شد! پلن شما فعال شد.",
    }

    PAYMENT_REJECTED: dict = {
        "en": "❌ Your payment has been rejected. Please contact support if you believe this is a mistake.",
        "fa": "❌ پرداخت شما رد شد. اگر فکر می‌کنید اشتباهی رخ داده، لطفا با پشتیبانی تماس بگیرید.",
    }

    PAYMENT_APPROVED_BY_ADMIN: dict = {
        "en": "✅ Payment approved by admin",
        "fa": "✅ پرداخت توسط ادمین تایید شد",
    }

    PAYMENT_REJECTED_BY_ADMIN: dict = {
        "en": "❌ Payment rejected by admin",
        "fa": "❌ پرداخت توسط ادمین رد شد",
    }

    PAYMENT_CANCELLED: dict = {
        "en": "Payment process has been cancelled.",
        "fa": "فرآیند پرداخت لغو شد.",
    }

    CARD_PAYMENT_DISABLED: dict = {
        "en": "Card payment is currently disabled. Please try again later.",
        "fa": "پرداخت کارت به کارت در حال حاضر غیرفعال است. لطفا بعداً تلاش کنید.",
    }
    LOGOUT: dict = {
        "en": "You have been logged out of your panel‼️",
        "fa": "شما از پنل خود خارج شدید‼️",
    }

    CARD_METHOD_SETTINGS: dict = {
        "en": (
            "💳 <b>Card Payment Settings</b>\n\n"
            "🔄 Status: {status}\n"
            "💳 Card Number: {card_num}\n"
        ),
        "fa": (
            "💳 <b>تنظیمات پرداخت کارت به کارت</b>\n\n"
            "🔄 وضعیت: {status}\n"
            "💳 شماره کارت: {card_num}\n"
        ),
    }

    CHANGE_CARD_METHOD_STATUS: dict = {"en": "🔄 Change Status", "fa": "🔄 تغییر وضعیت"}

    CHANGE_CARD_NUMBER: dict = {
        "en": "💳 Change Card Number",
        "fa": "💳 تغییر شماره کارت",
    }

    ENTER_NEW_CARD_NUMBER: dict = {
        "en": "Please enter the new card number:",
        "fa": "لطفا شماره کارت جدید را وارد کنید:",
    }

    CARD_NUMBER_UPDATED: dict = {
        "en": "✅ Card number has been updated successfully!",
        "fa": "✅ شماره کارت با موفقیت بروزرسانی شد!",
    }


BOT_MESSAGE = _MessageSetings()
