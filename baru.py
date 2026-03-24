from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from fansx import OWNER_ID, bot, ubot, get_expired_date


class MSG:     
    @staticmethod
    def EXP_MSG_UBOT(X):
        return f"""
<blockquote><b>❏ ᴘᴇᴍʙᴇʀɪᴛᴀʜᴜᴀɴ ᴜsᴇʀʙᴏᴛ</b>
<b>├ ᴀᴄᴄᴏᴜɴ</b> : <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>├ ᴜsᴇʀ ɪᴅ</b> : <code>{X.me.id}</code>
<b>├ ꜱᴛᴀᴛᴜꜱ</b> : ᴇxᴘɪʀᴇᴅ
<b>├ ᴋᴇᴛ</b> : ᴍᴀꜱᴀ ᴀᴋᴛɪꜰ ᴜsᴇʀʙᴏᴛ ᴛᴇʟᴀʜ ʙᴇʀᴀᴋʜɪʀ
<b>├ ᴀᴋꜱᴇꜱ</b> : ᴅɪʜᴇɴᴛɪᴋᴀɴ ꜱᴇᴍᴇɴᴛᴀʀᴀ
<b>╰ ᴀᴋꜱɪ</b> : ꜱɪʟᴀʜᴋᴀɴ ᴘᴇʀᴘᴀɴᴊᴀɴɢ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴋᴛɪꜰᴋᴀɴ ᴋᴇᴍʙᴀʟɪ</blockquote>
"""

    @staticmethod
    def START(message):
        return f"""
<blockquote><b>👋🏻 ʜᴀʟᴏ <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>!

<b> 📚💎@{bot.me.username} ᴀᴅᴀʟᴀʜ ʙᴏᴛ ʏᴀɴɢ ᴅᴀᴘᴀᴛ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ᴅᴇɴɢᴀɴ ᴍᴜᴅᴀʜ</b>

📌ᴀᴘᴀ ɪᴛᴜ ᴜsᴇʀʙᴏᴛ?
ᴜsᴇʀʙᴏᴛ ᴀᴅᴀʟᴀʜ ᴀᴋᴜɴ ᴛᴇʟᴇɢʀᴀᴍ ʙɪᴀꜱᴀ ʏᴀɴɢ ᴅɪᴊᴀʟᴀɴᴋᴀɴ ꜱᴇᴄᴀʀᴀ ᴏᴛᴏᴍᴀᴛɪꜱ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ꜱɪꜱᴛᴇᴍ ʙᴏᴛ.  
ᴅᴇɴɢᴀɴ ᴜsᴇʀʙᴏᴛ, ᴀᴋᴜɴ ᴋᴀᴍᴜ ʙɪꜱᴀ ʙᴇʀᴊᴀʟᴀɴ ꜱᴇᴄᴀʀᴀ ᴀᴜᴛᴏᴍᴀᴛɪꜱ ᴛᴀɴᴘᴀ ʜᴀʀᴜꜱ ᴏɴʟɪɴᴇ ᴛᴇʀᴜꜱ ᴍᴇɴᴇʀᴜꜱ.

📌ᴀᴘᴀ ꜱᴀᴊᴀ ʏᴀɴɢ ʙɪꜱᴀ ᴅɪʟᴀᴋᴜᴋᴀɴ?
- ᴏᴛᴏ ʀᴇꜱᴘᴏɴ ᴄʜᴀᴛ (ʙᴀʟᴀꜱ ᴏᴛᴏᴍᴀᴛɪꜱ)
- ᴍᴀɴᴀᴊᴇᴍᴇɴ ɢʀᴏᴜᴘ / ᴄʜᴀɴɴᴇʟ
- ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴘᴇꜱᴀɴ / ᴘʀᴏᴍᴏꜱɪ
- ᴀᴜᴛᴏ ꜱᴇɴᴅ / ᴀᴜᴛᴏ ᴘᴏꜱᴛ
- ʙɪꜱᴀ ᴅɪɢᴜɴᴀᴋᴀɴ ᴜɴᴛᴜᴋ ᴊᴜᴀʟᴀɴ / ʙɪꜱɴɪꜱ

📌ᴋᴇᴜɴᴛᴜɴɢᴀɴ:
- ᴀᴋᴜɴ ᴀᴋᴛɪꜰ 24 ᴊᴀᴍ
- ʜᴇᴍᴀᴛ ᴡᴀᴋᴛᴜ & ᴇꜰɪꜱɪᴇɴ
- ʙɪꜱᴀ ᴜɴᴛᴜᴋ ʙɪꜱɴɪꜱ / ᴊᴜᴀʟᴀɴ
- ᴍᴜᴅᴀʜ ᴅɪɢᴜɴᴀᴋᴀɴ

🚀ʙᴏᴛ ɪɴɪ ᴅɪᴋᴇᴍʙᴀɴɢᴋᴀɴ ᴏʟᴇʜ <a href=tg://openmessage?user_id={OWNER_ID}>@akuzyura</a>  
ᴊɪᴋᴀ ᴀᴅᴀ ᴋᴇsᴀʟᴀʜᴀɴ ᴀᴛᴀᴜ ᴇʀʀᴏʀ ʙɪꜱᴀ ᴅᴍ ᴏᴡɴᴇʀ.


𝙲𝙰𝚁𝙰 𝚂𝙴𝚆𝙰 𝚄𝚂𝙴𝚁𝙱𝙾𝚃:
1. ᴄʜᴀᴛ ᴏᴡɴᴇʀ ᴜɴᴛᴜᴋ ᴘᴇᴍʙᴇʟɪᴀɴ  
2. ᴋᴏɴꜰɪʀᴍᴀꜱɪ ʜᴀʀɢᴀ & ᴘᴀᴋᴇᴛ  
3. ʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ  
4. ᴋɪʀɪᴍ ᴀᴋᴜɴ / ɴᴏᴍᴏʀ ᴛᴇʟᴇɢʀᴀᴍ  
5. ᴜsᴇʀʙᴏᴛ ᴅɪꜱᴇᴛᴜᴘ & ꜱɪᴀᴘ ᴅɪɢᴜɴᴀᴋᴀɴ

⚠️ɴᴏᴛᴇ:
- ᴜsᴇʀʙᴏᴛ ᴍᴀꜱɪʜ ᴅᴀʟᴀᴍ ᴘᴇɴɢᴇᴍʙᴀɴɢᴀɴ  

ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪʙᴀᴡᴀʜ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b></blockquote>
"""

    @staticmethod
    def TEXT_PAYMENT(harga, total, bulan):
        return f"""
<blockquote><b>💬 sɪʟᴀʜᴋᴀɴ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ</b>

<b>🎟️ ʜᴀʀɢᴀ ᴘᴇʀʙᴜʟᴀɴ: {harga}.000</b>
<b>🗓️ ᴅᴜʀᴀꜱɪ: {bulan} ʙᴜʟᴀɴ</b>
<b>🔖 ᴛᴏᴛᴀʟ ʜᴀʀɢᴀ: ʀᴘ {total}.000</b>

<b>💳 ᴍᴇᴛᴏᴅᴇ ᴘᴇᴍʙᴀʏᴀʀᴀɴ:</b>
<b>├ Qʀɪꜱ (ᴀʟʟ ᴘᴀʏᴍᴇɴᴛ)</b>

📌ᴘᴇᴛᴜɴᴊᴜᴋ:
- ʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ꜱᴇꜱᴜᴀɪ ᴛᴏᴛᴀʟ ᴅɪᴀᴛᴀꜱ  
- ꜱɪᴍᴘᴀɴ ʙᴜᴋᴛɪ ᴘᴇᴍʙᴀʏᴀʀᴀɴ  
- ᴊᴀɴɢᴀɴ ꜱᴀʟᴀʜ ɴᴏᴍɪɴᴀʟ ᴀɢᴀʀ ᴘʀᴏꜱᴇꜱ ᴄᴇᴘᴀᴛ

OWNER BOT : <a href=tg://openmessage?user_id={OWNER_ID}>@akuzyura</a> 

<b>🛍 ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴋᴏɴꜰɪʀᴍᴀꜱɪ ᴜɴᴛᴜᴋ ᴋɪʀɪᴍ ʙᴜᴋᴛɪ ᴘᴇᴍʙᴀʏᴀʀᴀɴ</b></blockquote>
"""

    @staticmethod
    async def UBOT(count):
        return f"""
<blockquote><b>╭〢ᴜʙᴏᴛ ᴘʀᴇᴍɪᴜᴍ ᴢʏᴜʀᴀ</b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>
<b>├〢 ᴀᴄᴄᴏᴜɴᴛ</b> <a href=tg://user?id={ubot._ubot[int(count)].me.id}>{ubot._ubot[int(count)].me.first_name} {ubot._ubot[int(count)].me.last_name or ''}</a>
<b>├〢 ᴜsᴇʀ ɪᴅ</b> <code>{ubot._ubot[int(count)].me.id}</code>
<b>├〢 ꜱᴛᴀᴛᴜꜱ</b> ᴀᴋᴛɪꜰ & ᴏɴʟɪɴᴇ
<b>├〢 ᴍᴏᴅᴇ</b> ᴘʀᴇᴍɪᴜᴍ
<b>├〢 ʀᴜɴᴛɪᴍᴇ</b> 24 ᴊᴀᴍ (ᴠᴘꜱ)
<b>├〢 ꜰɪᴛᴜʀ</b> ᴏᴛᴏ ʀᴇꜱᴘᴏɴ, ʙʀᴏᴀᴅᴄᴀꜱᴛ, ᴍᴀɴᴀᴊᴇᴍᴇɴ
<b>├〢 ꜱᴛᴀᴛᴇ</b> ꜱɪᴀᴘ ᴅɪɢᴜɴᴀᴋᴀɴ
<b>╰〢 ɴᴏᴛᴇ</b> ᴊᴀɢᴀ ᴀᴋᴜɴ ᴀɢᴀʀ ᴛɪᴅᴀᴋ ᴛᴇʀʙᴀᴛᴀꜱ / ᴋᴇɴᴀ ʟɪᴍɪᴛ</blockquote>
"""

    @staticmethod
    def POLICY():
        return f""" <blockquote><b>ᴊɪᴋᴀ ᴀᴅᴀ ᴋᴇɴᴅᴀʟᴀ sɪʟᴀʜᴋᴀɴ ʜᴜʙᴜɴɢɪ  <a href=tg://openmessage?user_id={OWNER_ID}>@akuzyura</a></b></blockquote>
"""
