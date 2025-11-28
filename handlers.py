# handlers.py
from aiogram import types
from db import cur, conn, init_db, get_setting, set_setting, log_tx
from config import REF_BONUS, MIN_WITHDRAW, PAYMENTS_CHANNEL, FORCE_SUB_CHANNELS
from keyboards import main_menu_kb

async def start_handler(message: types.Message, bot):
    args = message.get_args()
    user = message.from_user
    cur.execute("SELECT user_id FROM users WHERE user_id=?", (user.id,))
    if not cur.fetchone():
        referred_by = None
        if args:
            try:
                referred_by = int(args.split()[0])
            except:
                referred_by = None
        cur.execute("INSERT INTO users (user_id, username, first_name, referred_by) VALUES (?, ?, ?, ?)",
                    (user.id, user.username, user.first_name, referred_by))
        conn.commit()
        if referred_by and referred_by != user.id:
            cur.execute("SELECT user_id FROM users WHERE user_id=?", (referred_by,))
            if cur.fetchone():
                cur.execute("UPDATE users SET balance = balance + ?, ref_bonus_received = 1 WHERE user_id=?", (REF_BONUS, referred_by))
                conn.commit()
                log_tx(referred_by, "referral_gain", REF_BONUS, f"from {user.id}")

    # force subscribe check: simple version (only one channel)
    subscribed = True
    for ch in FORCE_SUB_CHANNELS:
        try:
            member = await bot.get_chat_member(ch, user.id)
            if member.status in ('left','kicked'):
                subscribed = False
                break
        except:
            # if check fails, we won't block
            subscribed = True

    if not subscribed:
        await message.answer("Iltimos majburiy kanallarga obuna bo'ling.", reply_markup=None)
        return

    await message.answer(f"Salom, {user.first_name}! Bu botga xush kelibsiz.", reply_markup=main_menu_kb())

async def balance_handler(message: types.Message):
    uid = message.from_user.id
    cur.execute("SELECT balance, usd_balance, stars FROM users WHERE user_id=?", (uid,))
    r = cur.fetchone()
    if not r:
        await message.reply("Siz /start bilan ro'yxatdan o'ting.")
        return
    bal, usd, stars = r
    await message.reply(f"Balans: {bal} ball\nUSD(virtual): {usd}\nStars: {stars}")
