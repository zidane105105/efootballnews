import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# ==================== تنظیمات ====================
TOKEN = "8579243065:AAENt7FKnuaOdqzJYHA_vNXPVWzlN2J-GWk"  # توکن جدید
ADMIN_ID = 7302403677  # آیدی عددی شما (برای دسترسی به آمار)
ADMIN_USERNAME = "@ZIZO_AT"  # یوزرنیم جهت نمایش در راهنما
MAIN_PHOTO = "https://i.postimg.cc/zvNMtyC4/file-000000008e90724389c31b9919183328.png"
USERS_FILE = "users.json"

# ==================== دیتابیس متون دو زبانه (کامل) ====================
TEXTS = {
    # ===== انتخاب زبان =====
    "language_selection": {
        "fa": "🌐 لطفاً زبان مورد نظر خود را انتخاب کنید:",
        "en": "🌐 Please select your preferred language:"
    },
    "language_persian": {
        "fa": "فارسی 🇮🇷",
        "en": "Persian 🇮🇷"
    },
    "language_english": {
        "fa": "انگلیسی 🇬🇧",
        "en": "English 🇬🇧"
    },
    "language_set_fa": {
        "fa": "✅ زبان فارسی با موفقیت انتخاب شد.",
        "en": "✅ Persian language selected successfully."
    },
    "language_set_en": {
        "fa": "✅ زبان انگلیسی با موفقیت انتخاب شد.",
        "en": "✅ English language selected successfully."
    },

    # ===== صفحه اصلی =====
    "welcome_main": {
        "fa": "༺༽ به ربات راهنمای ای‌فوتبال خوش آمدید ༼༻\n\n"
              "✨ این ربات چه کاری انجام می‌ده؟\n"
              "📌 هر چیزی که درباره ای‌فوتبال نیاز داشته باشید، به صورت خلاصه و مفید توضیح می‌دیم تا مشکل و خواسته شما برطرف بشه 👈🏻⚡\n\n"
              "🔻 همه اطلاعات ای‌فوتبال رو به صورت گزینه‌ای در اختیارتون می‌ذارم. هر کدوم رو خواستید انتخاب کنید تا اطلاعات مربوط به اون گزینه براتون نمایش داده بشه ✔️",
        "en": "༺༽ Welcome to eFootball Guide Bot ༼༻\n\n"
              "✨ What does this bot do?\n"
              "📌 Whatever you need to know about eFootball, we'll explain briefly and usefully to solve your problem 👈🏻⚡\n\n"
              "🔻 I'll provide all eFootball information as options below. Choose whatever you want to see the related information ✔️"
    },

    # ===== دکمه‌های صفحه اصلی =====
    "main_buttons": {
        "special_skills": {
            "fa": "▪️ اطلاعات مربوط به اسکیل‌های مخصوص",
            "en": "▪️ Special Skills"
        },
        "playing_style": {
            "fa": "▪️ همه چیز مربوط به Playing Style",
            "en": "▪️ Playing Styles"
        },
        "boosters": {
            "fa": "▪️ همه چیز در مورد بوسترها",
            "en": "▪️ About Boosters"
        },
        "linkup": {
            "fa": "▪️ لینک آپ مربی",
            "en": "▪️ Link Up Play"
        },
        "points": {
            "fa": "▪️ همه چیز در مورد پوینت ای‌فوتبال",
            "en": "▪️ Shop Point"
        },
        "player_style": {
            "fa": "▪️ همه چیز در مورد Player Playing Style",
            "en": "▪️ Player Playing Style"
        },
        "instructions": {
            "fa": "▪️ همه چیز در مورد Individual Instructions",
            "en": "▪️ Individual Instructions"
        }
    },

    # ===== دکمه برگشت =====
    "back_button": {
        "fa": "🔙 برگشت به صفحه اصلی",
        "en": "🔙 Back to Main Menu"
    },

    # ===== بخش پوینت =====
    "points_section": {
        "title": {
            "fa": "⚡️ **Efootball Points** ✔️",
            "en": "⚡️ **Efootball Points** ✔️"
        },
        "content": {
            "fa": "────────────────────────────\n"
                  "✅ شما با پوینت‌هایی که از ایونت‌ها و جشنواره‌ها می‌گیرید می‌تونید کارهای زیادی کنید.\n\n"
                  "🔹 **شوتایم و هایلایت** : با پرداخت بین ۵۰۰۰ تا ۱۵۰۰۰ پوینت می‌تونید بگیرید (مقدار پوینت فعلاً همین قدر هست!) 👈\n\n"
                  "🔹 **۲۵ کوین رایگان** : اگر ریجن شما ژاپن باشه می‌تونید توی بخش پوینت هفته به هفته یا چند روزی یک بار ۲۵ کوین رایگان بگیرید که کمک نسبتاً خوبیه براتون.\n\n"
                  "▪️ **روش گرفتن ۲۵ سکه (برای ریجن ژاپن) در بخش پوینت:**\n"
                  "روی ۲۵ تا کلیک کنید و به سایت کونامی میرید (فیلترشکن حتماً خاموش باشه). نیاز به جیمیل و رمز اکانتتون دارید تا بتونید ثبتش کنید و بعدش پایین سایت گزینه تأیید بزنید و برگردید به اکانت و تمام ✅\n"
                  "────────────────────────────",
            "en": "────────────────────────────\n"
                  "✅ You can do many things with the points you get from events and festivals.\n\n"
                  "🔹 **Showtime & Highlight** : You can get them by paying between 5000 to 15000 points (the point amount is currently this much!) 👈\n\n"
                  "🔹 **25 free coins** : If your region is Japan, you can get 25 free coins weekly or every few days in the points section, which is a relatively good help.\n\n"
                  "▪️ **How to get 25 coins (for Japan region) in the points section:**\n"
                  "Click on the 25 coins and go to Konami site (VPN must be off). You need your email and account password to register it, then click confirm at the bottom of the site and return to your account ✅\n"
                  "────────────────────────────"
        }
    },

    # ===== بخش اسکیل‌ها =====
    "skills_menu": {
        "title": {
            "fa": "🔰 مربوط به کدام بخش می‌خوای در مورد اسکیل‌های مخصوص بدونی؟",
            "en": "🔰 Which section's special skills would you like to know about?"
        },
        "dribblers": {
            "fa": "▪️ مخصوص بازیکن‌های دریبلر",
            "en": "▪️ Dribblers"
        },
        "forwards": {
            "fa": "▪️ مهاجمین",
            "en": "▪️ Forwards"
        },
        "defenders": {
            "fa": "▪️ مدافع",
            "en": "▪️ Defenders"
        },
        "goalkeepers": {
            "fa": "▪️ گلرها",
            "en": "▪️ Goalkeepers"
        },
        "midfielders": {
            "fa": "▪️ هافبک و بازیساز",
            "en": "▪️ Midfielders & Playmakers"
        }
    },

    # ===== اسکیل مهاجمین =====
    "fw_skills": {
        "fa": "────────────────────────────\n"
              "🔰 **Bullet Header**\n"
              "Enables the player to head the ball sharply towards goal, shooting with power and accuracy even from awkward positions or when off balance.\n\n"
              "🇮🇷 فارسی: بازیکن را قادر می‌سازد تا توپ را با سر به شدت به سمت دروازه بفرستد و حتی از موقعیت‌های نامناسب یا در صورت عدم تعادل، با قدرت و دقت شوت کند.\n\n"
              "🔰 **Blitz Curler**\n"
              "Performs a Controlled Shot with heavy topspin while the Power Gauge is at least 50% full.\n\n"
              "🇮🇷 فارسی: یک شوت کنترل‌شده با تاپ‌اسپین سنگین انجام می‌دهد در حالی که نشانگر قدرت حداقل ۵۰٪ پر است. (یعنی شوتی می‌زنه که ۵۰ درصد قدرت نشون میده یا کات ولی بیشتر از حد عمل می‌کنه)\n\n"
              "🔰 **Low Screamer**\n"
              "Performing a Stunning Shot while the Power Gauge is under 50% full will increase the speed of the shot. A Dipping Shot will not occur.\n\n"
              "🇮🇷 فارسی: انجام یک شوت خیره‌کننده در حالی که نشانگر قدرت کمتر از ۵۰٪ پر است، سرعت شوت را افزایش می‌دهد. شوت غوطه‌ور اتفاق نمی‌افتد.\n\n"
              "🔰 **Phenomenal Finishing**\n"
              "Increases the power and accuracy of finishing shots attempted from unorthodox body positions.\n\n"
              "🇮🇷 فارسی: قدرت و دقت ضربات تمام‌کننده از موقعیت‌های بدنی غیرمعمول را افزایش می‌دهد.\n\n"
              "🔰 **Willpower**\n"
              "Improves player's shooting abilities whenever they take a shot, up to a maximum of 8 times.\n\n"
              "🇮🇷 فارسی: توانایی‌های شوت‌زنی بازیکن را هر زمان که شوت می‌زند، حداکثر تا ۸ بار، بهبود می‌بخشد. (۸ تا شوت که بزنی قدرت زیاد میشه، همون تمام‌کنندگی)\n"
              "────────────────────────────",
        "en": "────────────────────────────\n"
              "🔰 **Bullet Header**\n"
              "Enables the player to head the ball sharply towards goal, shooting with power and accuracy even from awkward positions or when off balance.\n\n"
              "🔰 **Blitz Curler**\n"
              "Performs a Controlled Shot with heavy topspin while the Power Gauge is at least 50% full.\n\n"
              "🔰 **Low Screamer**\n"
              "Performing a Stunning Shot while the Power Gauge is under 50% full will increase the speed of the shot. A Dipping Shot will not occur.\n\n"
              "🔰 **Phenomenal Finishing**\n"
              "Increases the power and accuracy of finishing shots attempted from unorthodox body positions.\n\n"
              "🔰 **Willpower**\n"
              "Improves player's shooting abilities whenever they take a shot, up to a maximum of 8 times.\n"
              "────────────────────────────"
    },

    # ===== اسکیل دریبلرها =====
    "dribble_skills": {
        "fa": "────────────────────────────\n"
              "🔰 **Momentum Dribbling**\n"
              "Improves player's dribbling abilities in the attacking third (deep in opposition territory).\n\n"
              "🇮🇷 فارسی: توانایی دریبل بازیکن را در یک سوم تهاجمی (در عمق زمین حریف) بهبود می‌بخشد.\n\n"
              "🔰 **Acceleration Burst**\n"
              "Enables the player to perform a quick Sharp Touch while stationary or moving slowly. Special Sharp Touch motions may also be triggered.\n\n"
              "🇮🇷 فارسی: بازیکن را قادر می‌سازد تا در حالت سکون یا حرکت آهسته، یک ضربه سریع و دقیق (Sharp Touch) انجام دهد. حرکات ویژه ضربه سریع (Sharp Touch) نیز ممکن است فعال شوند.\n\n"
              "🔰 **Magnetic Feet**\n"
              "When in possession of the ball, increases the player's ability to keep it based on the number of opponents within 5 metres (4 opponents max).\n\n"
              "🇮🇷 فارسی: هنگام مالکیت توپ، توانایی بازیکن برای حفظ آن را بر اساس تعداد حریفان در فاصله ۵ متری (حداکثر ۴ حریف) افزایش می‌دهد.\n"
              "────────────────────────────",
        "en": "────────────────────────────\n"
              "🔰 **Momentum Dribbling**\n"
              "Improves player's dribbling abilities in the attacking third (deep in opposition territory).\n\n"
              "🔰 **Acceleration Burst**\n"
              "Enables the player to perform a quick Sharp Touch while stationary or moving slowly. Special Sharp Touch motions may also be triggered.\n\n"
              "🔰 **Magnetic Feet**\n"
              "When in possession of the ball, increases the player's ability to keep it based on the number of opponents within 5 metres (4 opponents max).\n"
              "────────────────────────────"
    },

    # ===== اسکیل مدافعین =====
    "defender_skills": {
        "fa": "────────────────────────────\n"
              "🔰 **Long-reach Tackle**\n"
              "Increases the frequency of standing tackles, even against far away opponents, while stationary or moving slowly.\n\n"
              "🇮🇷 فارسی: تعداد تکل‌های ایستاده را حتی در مقابل حریفان دور، در حالت سکون یا حرکت آهسته افزایش می‌دهد.\n\n"
              "🔰 **Fortress**\n"
              "Improves player's defensive abilities after the second half mark, as long as the team has a goal advantage.\n\n"
              "🇮🇷 فارسی: توانایی‌های دفاعی بازیکن را پس از نیمه دوم بهبود می‌بخشد، مادامی که تیم از برتری گل برخوردار باشد.\n\n"
              "🔰 **Aerial Fort**\n"
              "Improves player's abilities regarding aerial duels when positioned inside his own penalty box.\n\n"
              "🇮🇷 فارسی: توانایی‌های بازیکن را در دوئل‌های هوایی، هنگامی که در محوطه جریمه خودی قرار دارد، بهبود می‌بخشد.\n"
              "────────────────────────────",
        "en": "────────────────────────────\n"
              "🔰 **Long-reach Tackle**\n"
              "Increases the frequency of standing tackles, even against far away opponents, while stationary or moving slowly.\n\n"
              "🔰 **Fortress**\n"
              "Improves player's defensive abilities after the second half mark, as long as the team has a goal advantage.\n\n"
              "🔰 **Aerial Fort**\n"
              "Improves player's abilities regarding aerial duels when positioned inside his own penalty box.\n"
              "────────────────────────────"
    },

    # ===== اسکیل هافبکها =====
    "mf_skills": {
        "fa": "────────────────────────────\n"
              "🔰 **Edged Crossing**\n"
              "Enables the player to put in vertically rotating crosses that fall sharply.\n\n"
              "🇮🇷 فارسی: بازیکن را قادر می‌سازد تا پاس‌های چرخشی عمودی را که به شدت فرود می‌آیند، وارد دروازه کند. (همون دیوید بکامی 😂)\n\n"
              "🔰 **Game-changing Pass**\n"
              "Improves player's passing abilities after the second half kick-off, under the circumstances that the team is either drawing or losing.\n\n"
              "🇮🇷 فارسی: توانایی‌های پاس‌دهی بازیکن را پس از شروع نیمه دوم، تحت شرایطی که تیم یا مساوی می‌کند یا می‌بازد، بهبود می‌بخشد. (عوض‌کننده جریان بازی)\n\n"
              "🔰 **Visionary Pass**\n"
              "Increases the accuracy of one-touch passes, first-time shots and traps performed by players who receive passes from the holder of this Player Skill.\n\n"
              "🇮🇷 فارسی: دقت پاس‌های تک‌ضرب، شوت‌های اول و تله‌های انجام‌شده توسط بازیکنانی را که از دارنده این مهارت بازیکن پاس دریافت می‌کنند، افزایش می‌دهد.\n\n"
              "🔰 **Phenomenal Pass**\n"
              "Increases the power and accuracy of passes attempted from unorthodox body positions.\n\n"
              "🇮🇷 فارسی: قدرت و دقت پاس‌های انجام‌شده از موقعیت‌های بدنی غیرمعمول را افزایش می‌دهد.\n\n"
              "🔰 **Attack Trigger**\n"
              "Increases all teammates' Attacking Awareness when this player has control of the ball.\n\n"
              "🇮🇷 فارسی: وقتی این بازیکن کنترل توپ را در اختیار دارد، آگاهی تهاجمی همه هم‌تیمی‌ها را افزایش می‌دهد.\n"
              "────────────────────────────",
        "en": "────────────────────────────\n"
              "🔰 **Edged Crossing**\n"
              "Enables the player to put in vertically rotating crosses that fall sharply.\n\n"
              "🔰 **Game-changing Pass**\n"
              "Improves player's passing abilities after the second half kick-off, under the circumstances that the team is either drawing or losing.\n\n"
              "🔰 **Visionary Pass**\n"
              "Increases the accuracy of one-touch passes, first-time shots and traps performed by players who receive passes from the holder of this Player Skill.\n\n"
              "🔰 **Phenomenal Pass**\n"
              "Increases the power and accuracy of passes attempted from unorthodox body positions.\n\n"
              "🔰 **Attack Trigger**\n"
              "Increases all teammates' Attacking Awareness when this player has control of the ball.\n"
              "────────────────────────────"
    },

    # ===== اسکیل گلرها =====
    "gk_skills": {
        "fa": "────────────────────────────\n"
              "🔰 **GK Spirit Roar**\n"
              "Goalkeeper Skill that improves the physical abilities of your DF players when leading after half-time.\n\n"
              "🇮🇷 فارسی: مهارت دروازه‌بانی که توانایی‌های فیزیکی بازیکنان خط دفاعی شما را هنگام پیشروی پس از نیمه اول بهبود می‌بخشد.\n\n"
              "🔰 **GK Directing Defence**\n"
              "Goalkeeper Skill that improves the defensive abilities of your DF players positioned deep in your own territory.\n\n"
              "🇮🇷 فارسی: مهارت دروازه‌بانی که توانایی‌های دفاعی بازیکنان خط دفاعی شما را که در عمق زمین خودی قرار دارند، بهبود می‌بخشد.\n"
              "────────────────────────────",
        "en": "────────────────────────────\n"
              "🔰 **GK Spirit Roar**\n"
              "Goalkeeper Skill that improves the physical abilities of your DF players when leading after half-time.\n\n"
              "🔰 **GK Directing Defence**\n"
              "Goalkeeper Skill that improves the defensive abilities of your DF players positioned deep in your own territory.\n"
              "────────────────────────────"
    },

    # ===== لینک آپ =====
    "linkup": {
        "fa": "────────────────────────────\n"
              "⚡️ **Link Up Play** ✅\n\n"
              "☆ کل این جریان به مربی شما بستگی داره و هر مربی یه لینک آپ خاصی داره.\n\n"
              "☆ برای مثال لینک آپ کاپلو (مربی که قبلاً با ۷۵۰ میشد گرفتش و حتماً خیلی‌هاتون گرفتینش) اینجوری بود که DMF رو به CF با یه پاس بلند وصل می‌کرد و این یه جورایی استراتژی و تکنیک برای بازیه و هر کسی که این رو داشته باشه می‌تونه راحت‌تر گل بزنه.\n\n"
              "📌 **نکته مهم:** لینک آپ‌ها خیلی مهم هستن و حتماً سعی کنید توی انتخاب و گرفتن مربی به لینک آپش دقت کنید. ⚡\n"
              "────────────────────────────",
        "en": "────────────────────────────\n"
              "⚡️ **Link Up Play** ✅\n\n"
              "☆ This whole concept depends on your manager and each manager has a specific link up.\n\n"
              "☆ For example, Capello's link up (the manager who could be obtained with 750 previously and many of you probably got him) connected DMF to CF with a long pass, and this is a strategy and technique for the game. Anyone who has this can score more easily.\n\n"
              "📌 **Important:** Link ups are very important, so make sure to pay attention to the manager's link up when choosing and acquiring them. ⚡\n"
              "────────────────────────────"
    },

    # ===== بوسترها =====
    "boosters": {
        "fa": "📸 توی عکس بالا همه قابلیت‌های بوستر داده شدن و کامل بهتون نشون میده چه بوستری چه آماری رو اضافه می‌کنه! ⚡ 👈🏻",
        "en": "📸 The image above shows all booster capabilities and fully demonstrates which booster adds which stats! ⚡ 👈🏻"
    },

    # ===== پلینگ استایل =====
    "playing_styles": {
        "fa": "────────────────────────────\n"
              "**🔰 1. Quick Counter**\n"
              "✓ حمله سریع بعد از توپ‌گیری\n"
              "✓ پاس عمقی، دویدن پشت دفاع\n"
              "✓ مناسب بازی تهاجمی و فشار بالا\n"
              "✅ خوب برای: وینگر سریع، مهاجم فرارکن\n"
              "❌ بد برای: دفاع کُند، پاس‌کاری اضافه\n"
              "👉 اگر کند بازی کنی، این سبک به کارت نمیاد. تمام.\n\n"
              "**🔰 2. Long Ball Counter**\n"
              "✓ دفاع عقب + توپ بلند\n"
              "✓ ضدحمله مستقیم\n"
              "✓ ریسک کم، صبر زیاد\n"
              "✅ خوب برای: مهاجم قدبلند یا سرعتی، تیم دفاعی\n"
              "❌ بد برای: مالکیت توپ، پاس کوتاه\n\n"
              "**🔰 3. Possession Game**\n"
              "✓ مالکیت توپ، پاس کوتاه\n"
              "✓ حوصله، کنترل بازی\n"
              "✓ کم‌ریسک ولی کند\n"
              "✅ خوب برای: هافبک تکنیکی، پاس دقیق\n"
              "❌ بد برای: ضدحمله سریع\n"
              "👉 اگه صبر نداری، این سبک برات زهره.\n\n"
              "**🔰 4. Out Wide**\n"
              "✓ بازی از کناره‌ها\n"
              "✓ سانتر زیاد\n"
              "✓ فشار روی فول‌بک‌ها\n"
              "✅ خوب برای: وینگر سریع، مهاجم سرزن\n"
              "❌ بد برای: بازی مرکزی\n"
              "👉 بدون مهاجم سرزن = سبک بی‌معنی.\n\n"
              "**🔰 5. Long Ball**\n"
              "✓ توپ بلند بدون ضدحمله خاص\n"
              "✓ فشار کمتر از Long Ball Counter\n"
              "✅ خوب برای: بازی فیزیکی\n"
              "❌ بد برای: سرعت و تکنیک\n"
              "👉 نسخه ضعیف‌تر و بی‌روح Long Ball Counter.\n"
              "────────────────────────────",
        "en": "────────────────────────────\n"
              "**🔰 1. Quick Counter**\n"
              "✓ Quick attack after winning the ball\n"
              "✓ Through passes, running behind defense\n"
              "✓ Suitable for offensive play and high pressure\n"
              "✅ Good for: Fast wingers, poachers\n"
              "❌ Bad for: Slow defense, excessive passing\n"
              "👉 If you play slow, this style won't suit you. Period.\n\n"
              "**🔰 2. Long Ball Counter**\n"
              "✓ Deep defense + long balls\n"
              "✓ Direct counter-attack\n"
              "✓ Low risk, high patience\n"
              "✅ Good for: Tall or fast strikers, defensive teams\n"
              "❌ Bad for: Possession play, short passes\n\n"
              "**🔰 3. Possession Game**\n"
              "✓ Ball possession, short passes\n"
              "✓ Patience, game control\n"
              "✓ Low risk but slow\n"
              "✅ Good for: Technical midfielders, precise passes\n"
              "❌ Bad for: Fast counter-attacks\n"
              "👉 If you lack patience, this style is poison for you.\n\n"
              "**🔰 4. Out Wide**\n"
              "✓ Play from the flanks\n"
              "✓ Lots of crosses\n"
              "✓ Pressure on fullbacks\n"
              "✅ Good for: Fast wingers, target men\n"
              "❌ Bad for: Central play\n"
              "👉 Without a target man = meaningless style.\n\n"
              "**🔰 5. Long Ball**\n"
              "✓ Long balls without specific counter-attack\n"
              "✓ Less pressure than Long Ball Counter\n"
              "✅ Good for: Physical play\n"
              "❌ Bad for: Speed and technique\n"
              "👉 Weaker, soulless version of Long Ball Counter.\n"
              "────────────────────────────"
    },

    # ===== پلیر پلینگ استایل =====
    "player_playing_style": {
        "fa": "────────────────────────────\n"
              "**🧤 دروازه‌بان**\n"
              "🔹 **Offensive Goalkeeper**\n"
              "✓ میاد جلو، توپ‌های پشت دفاع رو جمع می‌کنه.\n"
              "👉 سرعت واکنش مهمه\n"
              "🔹 **Defensive Goalkeeper**\n"
              "✓ می‌چسبه به دروازه، امن.\n"
              "👉 ضدحمله حریف اذیتت می‌کنه\n\n"
              "**🔷 دفاع وسط (CB)**\n"
              "🔹 **Extra Frontman**\n"
              "✓ دفاعی که یهو حمله می‌کنه.\n"
              "👉 ریسک بالا، مخصوص پلیر حرفه‌ای\n"
              "🔹 **The Destroyer**\n"
              "✓ قطع‌کن حمله، خشن، پرس بالا.\n"
              "👉 جای‌گیری بد = خطا و کارت\n"
              "🔹 **Build Up**\n"
              "✓ میاد عقب توپ می‌گیره، بازی رو می‌سازه.\n"
              "👉 فشار شدید؟ نابود می‌شه\n\n"
              "**🔶 دفاع کناری (RB / LB)**\n"
              "🔹 **Offensive Full-back**\n"
              "✓ حمله می‌کنه، اضافه می‌شه.\n"
              "👉 پشتش خالی می‌مونه\n"
              "🔹 **Defensive Full-back**\n"
              "✓ می‌مونه عقب، امن.\n"
              "👉 تو حمله انتظار نداشته باش\n"
              "🔹 **Full-back Finisher**\n"
              "✓ می‌ره داخل محوطه، شوت می‌زنه.\n\n"
              "**🟢 هافبک‌های هجومی (AMF / CMF)**\n"
              "🔹 **Creative Playmaker**\n"
              "✓ مغز تیم، پاس کلیدی.\n"
              "👉 فشار بخوره، خاموش می‌شه\n"
              "🔹 **Classic No.10**\n"
              "✓ ثابت، تکنیکی، بازی قدیمی.\n"
              "👉 دفاع نمی‌کنه، توقع نداشته باش\n"
              "🔹 **Hole Player**\n"
              "✓ یهو می‌زنه تو محوطه، خطرناک.\n"
              "👉 بدون پوشش دفاعی ریسکه\n\n"
              "**🟡 هافبک‌های میانی و دفاعی (CMF / DMF)**\n"
              "🔹 **Box-to-Box**\n"
              "✓ همه‌جا هست، پرانرژی.\n"
              "👉 اگر استقامت پایین باشه، افتضاح\n"
              "🔹 **Orchestrator**\n"
              "✓ ریتم بازی دستشه، پاس‌ساز عمیق.\n"
              "👉 کند بازی می‌کنه، عجله نکن\n"
              "🔹 **Anchor Man**\n"
              "✓ میخ وسط زمین، نمی‌ره جلو.\n"
              "👉 کسل‌کننده ولی حیاتی\n\n"
              "**🔵 وینگرها / کناره‌ها (LWF / RWF / RMF / LMF)**\n"
              "🔹 **Prolific Winger**\n"
              "✓ چسبیده به خط، دریبل و سانتر.\n"
              "👉 ضدحمله دوست‌داشتنی\n"
              "🔹 **Roaming Flank**\n"
              "✓ می‌زنه داخل، آزاد بازی می‌کنه.\n"
              "👉 شلوغی وسط رو زیاد می‌کنه\n"
              "🔹 **Cross Specialist**\n"
              "✓ فقط سانتر دقیق.\n"
              "👉 مهاجم سرزن نداشته باشی = آشغال\n\n"
              "**🔴 مهاجم‌ها (CF / SS)**\n"
              "🔹 **Goal Poacher**\n"
              "✓ همیشه پشت دفاعه، فرار می‌کنه، تموم‌کننده.\n"
              "👉 بدون پاس عمقی = بی‌فایده\n"
              "🔹 **Dummy Runner**\n"
              "✓ مدافع رو می‌کشه بیرون، فضا می‌سازه.\n"
              "👉 خودش گل‌زن نیست، مکمل بقیه‌ست\n"
              "🔹 **Fox in the Box**\n"
              "✓ داخل محوطه کمین می‌کنه، شکارچی واقعی.\n"
              "👉 بیرون باهاش کار نکن، اونجا می‌میره\n"
              "🔹 **Target Man**\n"
              "✓ توپ نگه می‌داره، بدن می‌ذاره، پاس می‌ده.\n"
              "👉 بدون وینگر = نصفه‌کاره\n"
              "🔹 **Deep-Lying Forward**\n"
              "✓ میاد عقب، بازی‌سازی می‌کنه.\n"
              "👉 اگه تنها مهاجمه، تیمت بی‌دندونه.\n"
              "────────────────────────────",
        "en": "────────────────────────────\n"
              "**🧤 Goalkeeper**\n"
              "🔹 **Offensive Goalkeeper**\n"
              "✓ Comes forward, collects balls behind the defense.\n"
              "👉 Reaction speed matters\n"
              "🔹 **Defensive Goalkeeper**\n"
              "✓ Stays close to goal, safe.\n"
              "👉 Opponent's counter-attack will trouble you\n\n"
              "**🔷 Center Back (CB)**\n"
              "🔹 **Extra Frontman**\n"
              "✓ A defender who suddenly attacks.\n"
              "👉 High risk, for professional players\n"
              "🔹 **The Destroyer**\n"
              "✓ Attack interceptor, aggressive, high press.\n"
              "👉 Bad positioning = fouls and cards\n"
              "🔹 **Build Up**\n"
              "✓ Comes back to receive ball, builds play.\n"
              "👉 Intense pressure? Gets destroyed\n\n"
              "**🔶 Full Back (RB / LB)**\n"
              "🔹 **Offensive Full-back**\n"
              "✓ Attacks, overlaps.\n"
              "👉 Leaves space behind\n"
              "🔹 **Defensive Full-back**\n"
              "✓ Stays back, safe.\n"
              "👉 Don't expect attacking contribution\n"
              "🔹 **Full-back Finisher**\n"
              "✓ Goes inside the box, shoots.\n\n"
              "**🟢 Attacking Midfielders (AMF / CMF)**\n"
              "🔹 **Creative Playmaker**\n"
              "✓ Team's brain, key passes.\n"
              "👉 Under pressure, gets neutralized\n"
              "🔹 **Classic No.10**\n"
              "✓ Static, technical, old-school play.\n"
              "👉 Doesn't defend, don't expect it\n"
              "🔹 **Hole Player**\n"
              "✓ Suddenly enters the box, dangerous.\n"
              "👉 Without defensive cover = risky\n\n"
              "**🟡 Central & Defensive Midfielders (CMF / DMF)**\n"
              "🔹 **Box-to-Box**\n"
              "✓ Everywhere, energetic.\n"
              "👉 If stamina is low, disastrous\n"
              "🔹 **Orchestrator**\n"
              "✓ Controls game tempo, deep playmaker.\n"
              "👉 Plays slow, don't rush\n"
              "🔹 **Anchor Man**\n"
              "✓ Stays in midfield center, doesn't go forward.\n"
              "👉 Boring but vital\n\n"
              "**🔵 Wingers / Flanks (LWF / RWF / RMF / LMF)**\n"
              "🔹 **Prolific Winger**\n"
              "✓ Sticks to the line, dribbles and crosses.\n"
              "👉 Lovely for counter-attacks\n"
              "🔹 **Roaming Flank**\n"
              "✓ Moves inside, plays freely.\n"
              "👉 Increases central congestion\n"
              "🔹 **Cross Specialist**\n"
              "✓ Only accurate crosses.\n"
              "👉 No target man = useless\n\n"
              "**🔴 Forwards (CF / SS)**\n"
              "🔹 **Goal Poacher**\n"
              "✓ Always behind defense, runs, finisher.\n"
              "👉 No through passes = useless\n"
              "🔹 **Dummy Runner**\n"
              "✓ Pulls defenders out, creates space.\n"
              "👉 Not a scorer, complements others\n"
              "🔹 **Fox in the Box**\n"
              "✓ Lurks in the box, true hunter.\n"
              "👉 Don't use outside the box, dies there\n"
              "🔹 **Target Man**\n"
              "✓ Holds ball, uses body, passes.\n"
              "👉 No wingers = half-functional\n"
              "🔹 **Deep-Lying Forward**\n"
              "✓ Drops deep, playmakes.\n"
              "👉 If sole striker, your team is toothless.\n"
              "────────────────────────────"
    },

    # ===== اینستراکشن =====
    "instructions": {
        "fa": "────────────────────────────\n"
              "⚙️ **Individual Instructions (دستور فردی بازیکن)**\n\n"
              "🔹 **Anchoring**\n"
              "✓ بازیکن به موقعیت خودش می‌چسبه و ولش نمی‌کنه.\n"
              "👉 برای DMF یا CB عالیه\n"
              "❌ برای AMF = حماقت\n\n"
              "🔹 **Defensive**\n"
              "✓ کمتر جلو می‌ره، اول دفاع.\n"
              "👉 فول‌بک‌ها و هافبک دفاعی\n"
              "❌ روی بازیکن خلاق = خفه‌ش می‌کنی\n\n"
              "🔹 **Attacking**\n"
              "✓ آزادتر جلو می‌ره، ریسک بالا.\n"
              "👉 وینگر، فول‌بک هجومی\n"
              "❌ بدون پوشش دفاعی = خودکشی\n\n"
              "🔹 **Counter Target**\n"
              "✓ تو دفاع برنمی‌گرده، جلو می‌مونه.\n"
              "👉 مهاجم سرعتی برای ضدحمله\n"
              "❌ اگه توپ نگه نمی‌داره، به درد نمی‌خوره\n\n"
              "🔹 **Tight Marking**\n"
              "✓ بچسب به یه بازیکن خاص.\n"
              "👉 مهار ستاره حریف\n"
              "❌ اشتباه بزنی، کل دفاع می‌ریزه\n\n"
              "🔹 **Man Marking**\n"
              "✓ مارک مستقیم بازیکن به بازیکن.\n"
              "👉 حریف تک‌ستاره\n"
              "❌ حریف پاس‌کاری؟ بدبخت می‌شی\n\n"
              "🔹 **Deep Line**\n"
              "✓ خط دفاع عقب‌تر می‌ایسته.\n"
              "👉 جلوی پاس عمقی\n"
              "❌ فشار بالا؟ نابود می‌شه\n"
              "────────────────────────────",
        "en": "────────────────────────────\n"
              "⚙️ **Individual Instructions**\n\n"
              "🔹 **Anchoring**\n"
              "✓ Player sticks to position and doesn't leave it.\n"
              "👉 Great for DMF or CB\n"
              "❌ For AMF = stupidity\n\n"
              "🔹 **Defensive**\n"
              "✓ Goes forward less, prioritizes defense.\n"
              "👉 Fullbacks and defensive midfielders\n"
              "❌ On creative player = suffocates them\n\n"
              "🔹 **Attacking**\n"
              "✓ Goes forward more freely, high risk.\n"
              "👉 Wingers, attacking fullbacks\n"
              "❌ Without defensive cover = suicide\n\n"
              "🔹 **Counter Target**\n"
              "✓ Doesn't track back in defense, stays forward.\n"
              "👉 Fast striker for counter-attacks\n"
              "❌ If can't hold ball, useless\n\n"
              "🔹 **Tight Marking**\n"
              "✓ Stick to a specific player.\n"
              "👉 Marking opponent's star\n"
              "❌ If you mess up, entire defense collapses\n\n"
              "🔹 **Man Marking**\n"
              "✓ Direct player-to-player marking.\n"
              "👉 Single-star opponent\n"
              "❌ Against passing teams? You're doomed\n\n"
              "🔹 **Deep Line**\n"
              "✓ Defense line sits deeper.\n"
              "👉 Prevents through passes\n"
              "❌ High pressure? Gets destroyed\n"
              "────────────────────────────"
    },

    # ===== راهنما =====
    "help": {
        "fa": "🆘 در صورت داشتن مشکل به مدیریت مراجعه کنید:\n{admin}",
        "en": "🆘 If you have any problems, contact the admin:\n{admin}"
    }
}

# ==================== توابع کمکی ====================
def get_text(key, lang, **kwargs):
    """دریافت متن با کلید و زبان (پشتیبانی از کلیدهای نقطه‌دار)"""
    keys = key.split('.')
    d = TEXTS
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, {})
        else:
            return ""
    if isinstance(d, dict):
        text = d.get(lang, d.get("fa", ""))
    else:
        text = d
    if kwargs and text:
        text = text.format(**kwargs)
    return text

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

# ==================== هندلرها ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)

    if "lang" not in context.user_data:
        keyboard = [
            [InlineKeyboardButton(get_text("language_persian", "fa"), callback_data="lang_fa")],
            [InlineKeyboardButton(get_text("language_english", "en"), callback_data="lang_en")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🌐 Choose your language!\n🌐 زبان مورد نظر را انتخاب کنید!",
            reply_markup=reply_markup
        )
        return

    await show_main_menu(update, context)

async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "lang_fa":
        context.user_data["lang"] = "fa"
        await query.edit_message_text(get_text("language_set_fa", "fa"))
    elif query.data == "lang_en":
        context.user_data["lang"] = "en"
        await query.edit_message_text(get_text("language_set_en", "en"))

    await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id=None):
    lang = context.user_data.get("lang", "fa")
    buttons = TEXTS["main_buttons"]
    keyboard = [
        [InlineKeyboardButton(buttons["special_skills"][lang], callback_data="m_skills")],
        [InlineKeyboardButton(buttons["playing_style"][lang], callback_data="m_styles")],
        [InlineKeyboardButton(buttons["boosters"][lang], callback_data="m_boosters")],
        [InlineKeyboardButton(buttons["linkup"][lang], callback_data="m_linkup")],
        [InlineKeyboardButton(buttons["points"][lang], callback_data="m_points")],
        [InlineKeyboardButton(buttons["player_style"][lang], callback_data="m_pstyle")],
        [InlineKeyboardButton(buttons["instructions"][lang], callback_data="m_instr")]
    ]

    if chat_id is None:
        if update.callback_query:
            try:
                await update.callback_query.message.delete()
            except Exception as e:
                logging.warning(f"خطا در حذف پیام: {e}")
            chat_id = update.callback_query.message.chat_id
        else:
            chat_id = update.effective_chat.id

    try:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=MAIN_PHOTO,
            caption=get_text("welcome_main", lang),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logging.error(f"خطا در ارسال عکس اصلی: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text=get_text("welcome_main", lang),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def service_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = context.user_data.get("lang", "fa")

    back_button = [[InlineKeyboardButton(get_text("back_button", lang), callback_data="back_to_main")]]

    if data == "back_to_main":
        await show_main_menu(update, context)
        return

    # ===== بخش پوینت =====
    if data == "m_points":
        try:
            text = get_text("points_section.content", lang)
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=text,
                reply_markup=InlineKeyboardMarkup(back_button)
            )
        except Exception as e:
            logging.error(f"خطا در ارسال متن پوینت: {e}")
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="❌ متأسفانه متن مورد نظر قابل ارسال نیست. لطفاً بعداً تلاش کنید."
            )
        return

    # ===== بخش اسکیل‌ها =====
    if data == "m_skills":
        skills_menu = TEXTS["skills_menu"]
        keyboard = [
            [InlineKeyboardButton(skills_menu["dribblers"][lang], callback_data="s_drib")],
            [InlineKeyboardButton(skills_menu["forwards"][lang], callback_data="s_fw")],
            [InlineKeyboardButton(skills_menu["defenders"][lang], callback_data="s_def"),
             InlineKeyboardButton(skills_menu["goalkeepers"][lang], callback_data="s_gk")],
            [InlineKeyboardButton(skills_menu["midfielders"][lang], callback_data="s_mf")],
            [InlineKeyboardButton(get_text("back_button", lang), callback_data="back_to_main")]
        ]
        try:
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo="https://i.postimg.cc/Dwp9vyhW/Picsart-26-02-19-15-46-52-587.png",
                caption=skills_menu["title"][lang],
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            logging.error(f"خطا در ارسال عکس skills: {e}")
            await query.message.reply_text(
                skills_menu["title"][lang],
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        return

    # زیرمجموعه‌های اسکیل
    if data == "s_fw":
        await query.message.reply_text(
            TEXTS["fw_skills"][lang],
            reply_markup=InlineKeyboardMarkup(back_button)
        )
        return
    if data == "s_drib":
        await query.message.reply_text(
            TEXTS["dribble_skills"][lang],
            reply_markup=InlineKeyboardMarkup(back_button)
        )
        return
    if data == "s_def":
        await query.message.reply_text(
            TEXTS["defender_skills"][lang],
            reply_markup=InlineKeyboardMarkup(back_button)
        )
        return
    if data == "s_mf":
        await query.message.reply_text(
            TEXTS["mf_skills"][lang],
            reply_markup=InlineKeyboardMarkup(back_button)
        )
        return
    if data == "s_gk":
        await query.message.reply_text(
            TEXTS["gk_skills"][lang],
            reply_markup=InlineKeyboardMarkup(back_button)
        )
        return

    # ===== لینک آپ =====
    if data == "m_linkup":
        try:
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo="https://i.postimg.cc/QxJs33VP/c6ea96bb-faf8-4405-9ca1-b28156c253bf.jpg",
                caption=TEXTS["linkup"][lang],
                reply_markup=InlineKeyboardMarkup(back_button)
            )
        except Exception as e:
            logging.error(f"خطا در ارسال عکس linkup: {e}")
            await query.message.reply_text(
                TEXTS["linkup"][lang],
                reply_markup=InlineKeyboardMarkup(back_button)
            )
        return

    # ===== بوسترها =====
    if data == "m_boosters":
        try:
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo="https://i.postimg.cc/FHP4YVy0/IMG-20260220-140309-189.jpg",
                caption=TEXTS["boosters"][lang],
                reply_markup=InlineKeyboardMarkup(back_button)
            )
        except Exception as e:
            logging.error(f"خطا در ارسال عکس boosters: {e}")
            await query.message.reply_text(
                TEXTS["boosters"][lang],
                reply_markup=InlineKeyboardMarkup(back_button)
            )
        return

    # ===== پلینگ استایل =====
    if data == "m_styles":
        await query.message.reply_text(
            TEXTS["playing_styles"][lang],
            reply_markup=InlineKeyboardMarkup(back_button)
        )
        return

    # ===== پلیر پلینگ استایل =====
    if data == "m_pstyle":
        try:
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo="https://i.postimg.cc/L4zFtptW/Picsart-26-02-19-15-45-58-632.jpg",
                caption=TEXTS["player_playing_style"][lang],
                reply_markup=InlineKeyboardMarkup(back_button)
            )
        except Exception as e:
            logging.error(f"خطا در ارسال عکس player style: {e}")
            await query.message.reply_text(
                TEXTS["player_playing_style"][lang],
                reply_markup=InlineKeyboardMarkup(back_button)
            )
        return

    # ===== اینستراکشن =====
    if data == "m_instr":
        try:
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo="https://i.postimg.cc/52rrc75R/Picsart-26-02-18-17-01-11-847.jpg",
                caption=TEXTS["instructions"][lang],
                reply_markup=InlineKeyboardMarkup(back_button)
            )
        except Exception as e:
            logging.error(f"خطا در ارسال عکس instructions: {e}")
            await query.message.reply_text(
                TEXTS["instructions"][lang],
                reply_markup=InlineKeyboardMarkup(back_button)
            )
        return

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "fa")
    # استفاده از ADMIN_USERNAME به جای ADMIN_ID
    await update.message.reply_text(get_text("help", lang, admin=ADMIN_USERNAME))

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ شما اجازه دسترسی به این دستور را ندارید.")
        return

    users = load_users()
    count = len(users)
    if count > 0:
        sample = users[:10]
        text = f"📊 **آمار کاربران**\n\nتعداد کل کاربران: {count}\n\nنمونه (حداکثر ۱۰):\n" + "\n".join([f"• `{uid}`" for uid in sample])
    else:
        text = "📊 هیچ کاربری ثبت نشده است."
    await update.message.reply_text(text, parse_mode="Markdown")

# ==================== اجرای اصلی ====================
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CallbackQueryHandler(language_handler, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(service_handler, pattern="^(m_|s_|back_to_main)"))

    logging.info("✅ ربات با موفقیت راه‌اندازی شد...")
    app.run_polling()