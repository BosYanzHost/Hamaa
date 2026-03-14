from fansx import *
import requests
import random
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

__MODULE__ = "ᴡᴀ ꜱᴛᴀʟᴋᴇʀ"
__HELP__ = """
<blockquote><b>『 WHATSAPP STALKER 』</b>

<b>⌲ Perintah:</b>
ᚗ <code>{0}wa [nomor]</code> 
⊶ Melihat informasi detail nomor WhatsApp

ᚗ <code>{0}waphoto [nomor]</code>
⊶ Mengambil foto profil WhatsApp

<b>⌲ Contoh:</b>
<code>.wa 628383838383</code>
<code>.waphoto 628383838383</code>
<code>.wa +628383838383</code></blockquote>
"""

# ============================================
# DAFTAR API KEYS (ISI SENDIRI)
#LOGIN AJA DI pitucode.com nanti ada disitu apikey taro aja ini bisa di isi bayak apikey ok
# ============================================
API_KEYS = [
    "7C0dE93af98",  # Key dari contoh
    # "key2",  # Tambahin key lain di sini
    # "key3",
    # "key4",
    # "key5",
]

# Base URL API
BASE_URL = "https://api.pitucode.com/whatsapp-checker-stalker"

def get_random_apikey():
    """Mengambil API key secara random dari daftar"""
    return random.choice(API_KEYS)

def format_phone_number(number):
    """Membersihkan dan memformat nomor telepon"""
    # Hapus semua karakter non-digit
    cleaned = ''.join(filter(str.isdigit, number))
    
    # Jika diawali 0, ganti dengan 62
    if cleaned.startswith('0'):
        cleaned = '62' + cleaned[1:]
    
    # Jika tidak diawali 62, tambahkan 62
    if not cleaned.startswith('62'):
        cleaned = '62' + cleaned
    
    return cleaned

@PY.UBOT("wa")
async def wa_stalker(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        # Cek format
        args = message.text.split()
        if len(args) < 2:
            await message.reply_text(
                f"<blockquote><b>❌ FORMAT SALAH</b>\n\n"
                f"<b>Contoh:</b>\n"
                f"<code>.wa 628383838384</code>\n"
                f"<code>.wa +628383838383</code>\n"
                f"<code>.wa 08383838383</code></blockquote>"
            )
            return
        
        # Bersihkan nomor
        raw_number = args[1]
        phone_number = format_phone_number(raw_number)
        
        # Kirim pesan processing
        processing = await message.reply_text(
            f"{prs} <b>Mencari informasi untuk nomor {phone_number}...</b>"
        )
        
        # Ambil API key random
        apikey = get_random_apikey()
        
        # Request ke API
        params = {"number": f"+{phone_number}"}
        headers = {"x-api-key": apikey}
        
        response = requests.get(
            BASE_URL, 
            params=params, 
            headers=headers, 
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and data.get("result"):
                result = data["result"]
                
                # Ambil data
                country = result.get("country", "Tidak diketahui")
                name = result.get("name", phone_number)
                wa_link = result.get("wa_link", f"https://wa.me/{phone_number}")
                status = result.get("status", "-")
                status_date = result.get("status_date", "-")
                profile_pic = result.get("profile_pic")
                is_business = result.get("is_business", False)
                business_info = result.get("business_info")
                
                # Format status
                status_text = status if status and status != "-" else "Tidak ada status"
                status_date_text = status_date if status_date and status_date != "-" else ""
                
                # Buat caption
                caption = f"""
<blockquote><b>📱 WHATSAPP STALKER</b>

<b>🌍 Negara:</b> {country}
<b>📞 Nomor:</b> <code>{name}</code>
<b>💼 Bisnis:</b> {'✅ Ya' if is_business else '❌ Tidak'}
<b>🔗 Link WA:</b> <a href='{wa_link}'>Klik untuk chat</a>

<b>📝 Status:</b> {status_text} {status_date_text}
"""
                
                # Tambah info bisnis kalo ada
                if is_business and business_info:
                    caption += f"\n<b>🏢 Info Bisnis:</b> {business_info}"
                
                caption += f"\n\n🔑 <b>Key:</b> <code>{apikey[:8]}...</code></blockquote>"
                
                await processing.delete()
                
                # Kalo ada foto profil, kirim foto
                if profile_pic:
                    try:
                        # Download foto profil
                        img_response = requests.get(profile_pic, timeout=10)
                        if img_response.status_code == 200:
                            photo_path = f"wa_profile_{phone_number}.jpg"
                            with open(photo_path, "wb") as f:
                                f.write(img_response.content)
                            
                            await client.send_photo(
                                chat_id=message.chat.id,
                                photo=photo_path,
                                caption=caption
                            )
                            
                            # Hapus file
                            import os
                            if os.path.exists(photo_path):
                                os.remove(photo_path)
                        else:
                            await message.reply_text(caption)
                    except:
                        await message.reply_text(caption)
                else:
                    await message.reply_text(caption)
                    
            else:
                await processing.edit_text(
                    f"{ggl} <b>Gagal mendapatkan informasi untuk nomor {phone_number}</b>"
                )
        else:
            await processing.edit_text(
                f"{ggl} <b>Gagal terhubung ke API! HTTP {response.status_code}</b>"
            )
            
    except requests.exceptions.Timeout:
        await message.reply_text(f"{ggl} <b>Timeout! Server sedang sibuk.</b>")
    except requests.exceptions.ConnectionError:
        await message.reply_text(f"{ggl} <b>Gagal terhubung ke server!</b>")
    except Exception as e:
        await message.reply_text(f"{ggl} <b>Error: {str(e)[:100]}</b>")

@PY.UBOT("waphoto")
async def wa_photo(client, message):
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        # Cek format
        args = message.text.split()
        if len(args) < 2:
            await message.reply_text(
                f"<blockquote><b>❌ FORMAT SALAH</b>\n\n"
                f"<b>Contoh:</b>\n"
                f"<code>.waphoto 628383838383</code>\n"
                f"<code>.waphoto +628383838383</code></blockquote>"
            )
            return
        
        # Bersihkan nomor
        raw_number = args[1]
        phone_number = format_phone_number(raw_number)
        
        # Kirim pesan processing
        processing = await message.reply_text(
            f"{prs} <b>Mencari foto profil untuk nomor {phone_number}...</b>"
        )
        
        # Ambil API key random
        apikey = get_random_apikey()
        
        # Request ke API
        params = {"number": f"+{phone_number}"}
        headers = {"x-api-key": apikey}
        
        response = requests.get(
            BASE_URL, 
            params=params, 
            headers=headers, 
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and data.get("result"):
                result = data["result"]
                profile_pic = result.get("profile_pic")
                
                if profile_pic:
                    try:
                        # Download foto profil
                        img_response = requests.get(profile_pic, timeout=10)
                        if img_response.status_code == 200:
                            photo_path = f"wa_profile_{phone_number}.jpg"
                            with open(photo_path, "wb") as f:
                                f.write(img_response.content)
                            
                            await processing.delete()
                            
                            await client.send_photo(
                                chat_id=message.chat.id,
                                photo=photo_path,
                                caption=f"<blockquote><b>📸 FOTO PROFIL WA</b>\n\n📞 <b>Nomor:</b> <code>{result.get('name', phone_number)}</code>\n🔑 <b>Key:</b> <code>{apikey[:8]}...</code></blockquote>"
                            )
                            
                            # Hapus file
                            import os
                            if os.path.exists(photo_path):
                                os.remove(photo_path)
                        else:
                            await processing.edit_text(f"{ggl} <b>Gagal mendownload foto profil!</b>")
                    except Exception as e:
                        await processing.edit_text(f"{ggl} <b>Error: {str(e)[:100]}</b>")
                else:
                    await processing.edit_text(f"{ggl} <b>Nomor {phone_number} tidak memiliki foto profil!</b>")
            else:
                await processing.edit_text(
                    f"{ggl} <b>Gagal mendapatkan informasi untuk nomor {phone_number}</b>"
                )
        else:
            await processing.edit_text(
                f"{ggl} <b>Gagal terhubung ke API! HTTP {response.status_code}</b>"
            )
            
    except requests.exceptions.Timeout:
        await message.reply_text(f"{ggl} <b>Timeout! Server sedang sibuk.</b>")
    except requests.exceptions.ConnectionError:
        await message.reply_text(f"{ggl} <b>Gagal terhubung ke server!</b>")
    except Exception as e:
        await message.reply_text(f"{ggl} <b>Error: {str(e)[:100]}</b>")

@PY.UBOT("stalkwa")
async def stalk_wa(client, message):
    """Alias untuk wa command"""
    await wa_stalker(client, message)

@PY.BOT("wa")
async def wa_stalker_bot(client, message):
    """Handler untuk bot"""
    try:
        args = message.text.split()
        if len(args) < 2:
            await message.reply_text(
                "❌ Format salah!\n"
                "Contoh: /wa 628383838383"
            )
            return
        
        raw_number = args[1]
        phone_number = format_phone_number(raw_number)
        
        processing = await message.reply_text(f"🔍 Mencari info {phone_number}...")
        
        apikey = get_random_apikey()
        params = {"number": f"+{phone_number}"}
        headers = {"x-api-key": apikey}
        
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success") and data.get("result"):
                result = data["result"]
                
                text = f"""
📱 WHATSAPP STALKER

🌍 Negara: {result.get('country', '-')}
📞 Nomor: {result.get('name', phone_number)}
💼 Bisnis: {'Ya' if result.get('is_business') else 'Tidak'}
🔗 Link: {result.get('wa_link', '-')}

📝 Status: {result.get('status', '-')} {result.get('status_date', '')}
"""
                await processing.edit_text(text)
            else:
                await processing.edit_text("❌ Gagal mendapatkan info!")
        else:
            await processing.edit_text(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)[:100]}")
