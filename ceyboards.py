# keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("🔸 Balans", callback_data="bal"),
           InlineKeyboardButton("🔁 Transfer", callback_data="transfer"),
           InlineKeyboardButton("⭐ Buy/Sell Stars", callback_data="stars"),
           InlineKeyboardButton("💵 Buy/Sell USD", callback_data="usd"),
           InlineKeyboardButton("🎮 Mini-oʻyinlar", callback_data="games"),
           InlineKeyboardButton("❓ Support", callback_data="support"))
    return kb

def admin_menu_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("📊 Dashboard", callback_data="admin_stats"),
           InlineKeyboardButton("🧾 Withdraws", callback_data="admin_withdraws"),
           InlineKeyboardButton("💱 Sell Requests", callback_data="admin_sells"),
           InlineKeyboardButton("📣 Broadcast", callback_data="admin_broadcast"),
           InlineKeyboardButton("⚙️ Settings", callback_data="admin_settings"),
           InlineKeyboardButton("🔒 Logout", callback_data="admin_logout"))
    return kb
