import pyrogram
import time
import pyromod
from pyromod import *
from pyromod import ask
from pyrogram import *
from pyrogram.types import *
from pyrogram import enums
from pyrogram.errors import PhoneNumberInvalid, PhoneNumberFlood, PhoneNumberBanned, PhoneCodeInvalid, UserDeactivatedBan, SessionPasswordNeeded
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import utils.db
from utils.db import *
from utils.msg import *

API_ID = 1 # YOUR API ID
API_HASH = "1" # YOUR API HASH
BOT_TOKEN = "1" # YOUR BOT_TOKEN
BOT_SESSION_NAME = "bot_session" 
UBOT_SESSION_NAME = "ubot_session"
USE_PROXIES = False # DEFAULT False, TO USE PROXIES, LOAD PROXIES IN "proxies.txt"

#GENERIC DB AND NON VARIABLES
global CLN, STOPPED, RUNNING  # DONT CHANGE
ADMINS = get_admins() # DONT CHANGE
STOPPED = True # DONT CHANGE
RUNNING = False # DONT CHANGE

# INLINE KEYBOARD MARKUP
START_MESSAGE_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton("✅ SPAM", "spam")],[InlineKeyboardButton("➕ ADD VOIP", "add"),InlineKeyboardButton("➖ REMOVE VOIP","remove")],[InlineKeyboardButton("⚙️ SETTINGS", "settings")],[InlineKeyboardButton("OPEN SOURCE", url="https://t.me/OpenSourceFFA")]])
STOP_START_MESSAGE_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton("❌ STOP SPAM", "spam")],[InlineKeyboardButton("➕ ADD VOIP", "add"),InlineKeyboardButton("➖ REMOVE VOIP","remove")],[InlineKeyboardButton("⚙️ SETTINGS", "settings")],[InlineKeyboardButton("OPEN SOURCE", url="https://t.me/OpenSourceFFA")]])
BACK_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", "back")]])
SETTINGS_MESSAGE_MARKUP = InlineKeyboardMarkup([[InlineKeyboardButton("⏰ SPAM TIME","spamtime"),InlineKeyboardButton("💬 SET MESSAGE","setmessage")],[InlineKeyboardButton("➕ ADD ADMIN", "addadmin"),InlineKeyboardButton("➖ REMOVE ADMIN","removeadmin")],[InlineKeyboardButton("➕ ADD GROUP", "addgroup"),InlineKeyboardButton("➖ REMOVE GROUP","removegroup")],[InlineKeyboardButton("🔙 BACK", "back")]])

#BOT 
app = Client(BOT_SESSION_NAME,API_ID,API_HASH,bot_token=BOT_TOKEN)

#USERBOT SPAMMER 
if USE_PROXIES == False:
    ubot = Client(UBOT_SESSION_NAME,api_id=API_ID,api_hash=API_HASH, device_model="iPhone 13", system_version="15.1.1", app_version="8.1.2")
else:
    proxy = get_random_proxy()
    ip, port = proxy.split(":")
    ubot = Client(UBOT_SESSION_NAME,api_id=API_ID,api_hash=API_HASH, device_model="iPhone 13", system_version="15.1.1", app_version="8.1.2",proxy=dict(hostname=ip,port=int(port),username=None,password=None))

# SPAM FUNCTION
def start_spamming(userbot):
        print("spam")
        for x in get_groups():
            try:
                userbot.send_message(x, get_message())
            except Exception:
                pass


# Pyrogram Monkey Patcher (ignore)
def get_peer_type(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"

@app.on_message(filters.command("start") & filters.private)
async def start(cl,msg):
    if is_admin(msg.from_user.id):
        if STOPPED == True:
            await msg.reply(START_MESSAGE.format(msg.from_user.mention), reply_markup=START_MESSAGE_MARKUP)
        else:
            await msg.reply(START_MESSAGE.format(msg.from_user.mention), reply_markup=STOP_START_MESSAGE_MARKUP)
    else:
        for i in ADMINS:
            await app.send_message(i, UNWANTED_START.format(msg.from_user.mention))

@app.on_callback_query()
async def cb_answer(cl,cb):
    global STOPPED
    await cb.answer("✅")
    if cb.data == "back":
        if STOPPED == True:
            await cb.message.edit(START_MESSAGE.format(cb.from_user.mention), reply_markup=START_MESSAGE_MARKUP)
        else:
            await cb.message.edit(START_MESSAGE.format(cb.from_user.mention), reply_markup=STOP_START_MESSAGE_MARKUP)
    if cb.data == "add":
        if is_voip_added() == False:
            phone_number_raw = await cl.ask(cb.from_user.id, PROVIDE_NUMBER)
            phone_number = phone_number_raw.text
            await ubot.connect()
            try:
                sent = await ubot.send_code(phone_number)
                try:
                    code = await cl.ask(cb.from_user.id, IS_NUMBER_VALID, timeout=10)
                except TimeoutError:
                    await cb.message.reply(TIMEOUT_REPLY)
                try:
                    await ubot.sign_in(phone_number, sent.phone_code_hash, code.text)
                    ss = await ubot.export_session_string()
                    add_voip(phone_number, ss)
                    await cb.message.reply(ACCOUNT_LOGGED_IN)
                    try: await ubot.disconnect() 
                    except Exception as e: print(e)
                except SessionPasswordNeeded:
                    await ubot.check_password((await client.ask(cb.from_user.id, ASK_2FA)).text)
                    ss = await ubot.export_session_string()
                    add_voip(phone_number, ss)
                    await cb.message.reply(ACCOUNT_LOGGED_IN)
                    try: await ubot.disconnect() 
                    except Exception as e: print(e)
                except PhoneCodeInvalid:
                    await cb.message.reply(INCORRECT_CODE,  reply_markup = BACK_MARKUP)
                except Exception as e: 
                    await cb.message.reply(ERROR_MSG)
                    print(e)
            except PhoneNumberInvalid:
                await cb.message.reply(INVALID_NUMBER, reply_markup = BACK_MARKUP)
                try: await ubot.disconnect() 
                except Exception as e: print(e)
            except PhoneNumberFlood:
                await cb.message.reply(NUMBER_IN_FLOOD,  reply_markup = BACK_MARKUP)
                try: await ubot.disconnect() 
                except Exception as e: print(e)
            except PhoneNumberBanned:
                await cb.message.reply(NUMBER_BANNED,  reply_markup = BACK_MARKUP)
                try: await ubot.disconnect() 
                except Exception as e: print(e)
            except Exception as e: 
                await cb.message.reply(ERROR_MSG, reply_markup = BACK_MARKUP)
                try: await ubot.disconnect() 
                except Exception as e: print(e)
                print(e)
        else:
            await cb.message.edit(VOIP_ALREADY_ADDED, reply_markup=BACK_MARKUP)
    if cb.data == "addadmin":
        new_admin_raw = await cl.ask(cb.from_user.id, PROVIDE_NEW_ADMIN_ID)
        new_admin = new_admin_raw.text
        if is_admin(int(new_admin)):
            await cb.message.reply(USER_ALREADY_ADMIN)
        else:
            admin(int(new_admin))
            await cb.message.reply_text(USER_NEW_ADMIN)
    if cb.data == "removeadmin":
        rem_admin_raw = await cl.ask(cb.from_user.id, PROVIDE_REMOVE_ADMIN_ID)
        rem_admin = rem_admin_raw.text
        if is_admin(int(rem_admin)):
            unadmin(int(rem_admin))
            await cb.message.reply_text(USER_REMOVED_ADMIN)
        else:
            await cb.message.reply(USER_NOT_ADMIN)
    if cb.data == "settings":
        await cb.message.edit(SETTINGS_MESSAGE, reply_markup=SETTINGS_MESSAGE_MARKUP)
    if cb.data == "setmessage":
        await cl.send_message(cb.from_user.id, f"{get_message()}", parse_mode=enums.ParseMode.MARKDOWN)
        new_msg_raw = await cl.ask(cb.from_user.id, ASK_NEW_MESSAGE)
        new_msg = new_msg_raw.text
        if new_msg == "cancel":
            pass
        else:
            try:
                set_message(new_msg)
                await cb.message.reply(NEW_MESSAGE_SET)
            except Exception as e:
                await cb.message.reply(ERROR_MSG)
                print(e)
    if cb.data == "spamtime":
        await cl.send_message(cb.from_user.id, CURRENT_SPAN_TIME.format(get_time()))
        new_msg_raw = await cl.ask(cb.from_user.id, ASK_NEW_TIME)
        new_msg = new_msg_raw.text
        if new_msg == "cancel":
            pass
        else:
            try:
                set_time(new_msg)
                await cb.message.reply(NEW_SPAM_TIME_SET)
            except Exception as e:
                await cb.message.reply(ERROR_MSG)
                print(e)
    if cb.data == "spam":
        if STOPPED == True:
            if is_voip_added() == True:
                print("voip added")
                if groups_added() == True:
                    print("group added")
                    if STOPPED == True:
                        try:
                            CLN = Client("temp", session_string=get_session_string(get_phone_num()), in_memory=True)
                            await CLN.start()
                            scheduler.add_job(start_spamming, "interval", args=[CLN], seconds=int(get_time()))
                            STOPPED = False
                            RUNNING = True
                            await cb.message.edit(SPAM_STARTED_MSG,reply_markup=BACK_MARKUP)
                        except UserDeactivatedBan:
                            await cb.message.reply(VOIP_BANNED)
                            remove_voip()
        else:
            scheduler.remove_all_jobs()
            STOPPED = True
            RUNNING = False
            await cb.message.edit(SPAM_STOPPED_MSG,reply_markup=BACK_MARKUP)
    if cb.data == "remove":
        if is_voip_added() == True:
            remove_voip()
            await cb.message.edit(VOIP_REMOVED, reply_markup=BACK_MARKUP)
            print("removed")
        else:
            await cb.message.edit(NO_VOIP_AVAILABLE, reply_markup=BACK_MARKUP)
    if cb.data == "addgroup":
        new_group_raw = await cl.ask(cb.from_user.id, PROVIDE_NEW_GROUP_ID)
        new_group = new_group_raw.text
        try:
            if group_exist(int(new_group)):
                await cb.message.reply(GROUP_ADDED_ALREADY)
            else:
                add_group(int(new_group))
                await cb.message.reply_text(NEW_GROUP_ADDED)
        except Exception as e:
            print(e)
            pass
    if cb.data == "removegroup":
        REM_group_raw = await cl.ask(cb.from_user.id, PROVIDE_REM_GROUP_ID)
        REM_group = REM_group_raw.text
        try:
            if group_exist(int(REM_group)):
                remove_group(int(REM_group))
                await cb.message.reply_text(REM_GROUP_ADDED)
            else:
                await cb.message.reply(GROUP_REM_ALREADY)
        except Exception as e:
            print(e)
            pass 
                

scheduler = AsyncIOScheduler()
scheduler.start()
app.run()
idle()
