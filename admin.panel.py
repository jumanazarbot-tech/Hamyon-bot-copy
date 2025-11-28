# admin_panel.py
from aiogram import types
from db import cur, conn, log_tx
from config import ADMIN_IDS, PAYMENTS_CHANNEL

async def admin_dashboard(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("Faqat adminlar uchun.")
        return
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]
    cur.execute("SELECT SUM(balance) FROM users")
    total_balance = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM withdraws WHERE status='pending'")
    pending_withdraws = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM sell_requests WHERE status='pending'")
    pending_sells = cur.fetchone()[0]

    text = (
        f"📊 Dashboard\n\nUsers: {total_users}\n"
        f"Total balance: {total_balance}\n"
        f"Pending withdraws: {pending_withdraws}\n"
        f"Pending sells: {pending_sells}\n"
    )
    await message.reply(text)
