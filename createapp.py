from fansx import *
import requests
import time
import asyncio
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

__MODULE__ = "ᴄʀᴇᴀᴛᴇ ᴀᴘᴘ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄʀᴇᴀᴛᴇ ᴀᴘᴘ ⦫</b>
<blockquote>
⎆ Perintah:
ᚗ <code>{0}createapp [url] [nama_app]</code> 
⊶ Membuat aplikasi Android dari website

ᚗ <code>{0}appstatus [appId]</code>
⊶ Cek status pembuatan aplikasi

ᚗ <code>{0}appdownload [appId]</code>
⊶ Download aplikasi yang sudah jadi

📌 Contoh:
<code>.createapp https://rumahotp.com Nokos</code>
</blockquote>
"""

# Base URL API
BASE_URL = "https://api.nvidiabotz.xyz/tools/toapp"

# Email default untuk pembuatan app
DEFAULT_EMAIL = "apppremium12@gmail.com"

# Dictionary untuk menyimpan data app sementara
app_data = {}

def clean_url(url):
    """Membersihkan dan memvalidasi URL"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

@PY.UBOT("createapp")
async def create_app(client, message):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        # Pengecekan args dengan benar
        args = message.text.split()
        if len(args) < 3:
            await message.reply_text(
                "❌ Format salah!\n"
                "Contoh: <code>.createapp https://rumahotp.com Nokos</code>"
            )
            return
        
        url = clean_url(args[1])
        app_name = args[2]
        
        # Ambil email dari argumen atau gunakan default
        email = args[3] if len(args) > 3 else DEFAULT_EMAIL
        
        # Icon default (pakai favicon dari website)
        app_icon = f"https://www.google.com/s2/favicons?domain={url}&sz=128"
        splash_icon = app_icon
        
        # Kirim pesan processing
        processing_msg = await message.reply_text(
            f"<blockquote><b>🔄 MEMBUAT APLIKASI</b>\n\n"
            f"🌐 <b>URL:</b> {url}\n"
            f"📱 <b>Nama:</b> {app_name}\n"
            f"📧 <b>Email:</b> {email}\n"
            f"⏳ Mohon tunggu...</blockquote>"
        )
        
        # Request ke API untuk membuat app
        params = {
            "url": url,
            "email": email,
            "appName": app_name,
            "appIcon": app_icon,
            "splashIcon": splash_icon
        }
        
        response = requests.get(f"{BASE_URL}/create", params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") and data.get("appId"):
                app_id = data["appId"]
                
                # Simpan data app
                app_data[app_id] = {
                    "url": url,
                    "app_name": app_name,
                    "email": email,
                    "created_at": time.time(),
                    "status": "starting",
                    "message": data.get("message", "App creation started")
                }
                
                # Buat keyboard dengan button
                keyboard = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("📊 Cek Status", callback_data=f"appstatus_{app_id}"),
                        InlineKeyboardButton("⬇️ Download", callback_data=f"appdownload_{app_id}")
                    ],
                    [
                        InlineKeyboardButton("❌ Batalkan", callback_data=f"appcancel_{app_id}")
                    ]
                ])
                
                await processing_msg.edit_text(
                    f"<blockquote><b>✅ APLIKASI DIBUAT</b>\n\n"
                    f"🆔 <b>App ID:</b> <code>{app_id}</code>\n"
                    f"🌐 <b>URL:</b> {url}\n"
                    f"📱 <b>Nama:</b> {app_name}\n"
                    f"📧 <b>Email:</b> {email}\n"
                    f"📝 <b>Status:</b> {data.get('message', 'Processing')}\n\n"
                    f"⏳ Tunggu 2-5 menit untuk proses build\n"
                    f"🔍 Gunakan tombol di bawah untuk cek status</blockquote>",
                    reply_markup=keyboard
                )
            else:
                await processing_msg.edit_text(
                    f"❌ Gagal membuat aplikasi!\n"
                    f"Error: {data.get('error', 'Unknown error')}"
                )
        else:
            await processing_msg.edit_text(
                f"❌ HTTP Error: {response.status_code}"
            )
            
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)[:100]}")

@PY.UBOT("appstatus")
async def app_status(client, message):
    try:
        args = message.text.split()
        if len(args) < 2:
            await message.reply_text(
                "❌ Masukkan App ID!\n"
                "Contoh: <code>.appstatus 590a1766851f64f2232d8ce9067c5416</code>"
            )
            return
        
        app_id = args[1]
        
        processing_msg = await message.reply_text(
            f"<blockquote><b>🔍 MENGECEK STATUS</b>\n\n"
            f"🆔 <b>App ID:</b> <code>{app_id}</code>\n"
            f"⏳ Mohon tunggu...</blockquote>"
        )
        
        # Cek status dari API
        params = {"appId": app_id}
        response = requests.get(f"{BASE_URL}/status", params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status"):
                build_status = data.get("buildStatus", "unknown")
                details = data.get("details", {})
                
                # Tentukan emoji berdasarkan status
                status_emoji = {
                    "building": "🔨",
                    "completed": "✅",
                    "failed": "❌",
                    "pending": "⏳",
                    "unknown": "❓"
                }.get(build_status, "❓")
                
                # Update data lokal
                if app_id in app_data:
                    app_data[app_id]["status"] = build_status
                
                # Buat caption
                caption = f"""
<blockquote><b>{status_emoji} STATUS APLIKASI</b>

🆔 <b>App ID:</b> <code>{app_id}</code>
📊 <b>Status:</b> {build_status.upper()}

🌐 <b>URL:</b> {details.get('url', 'N/A')}
📱 <b>Nama:</b> {details.get('appName', 'N/A')}
📧 <b>Email:</b> {details.get('email', 'N/A')}"""
                
                # Tambahkan info file jika ada
                if build_status == "completed" and details.get("buildFile"):
                    caption += f"\n\n📦 <b>File APK:</b> Tersedia"
                
                caption += "\n\n🔍 Gunakan <code>.appdownload [appId]</code> untuk download</blockquote>"
                
                # Buat keyboard
                keyboard = None
                if build_status == "completed":
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("⬇️ Download APK", callback_data=f"appdownload_{app_id}")]
                    ])
                
                await processing_msg.edit_text(caption, reply_markup=keyboard)
            else:
                await processing_msg.edit_text(
                    f"❌ Gagal cek status!\n"
                    f"Error: {data.get('error', 'Unknown error')}"
                )
        else:
            await processing_msg.edit_text(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)[:100]}")

@PY.UBOT("appdownload")
async def app_download(client, message):
    try:
        args = message.text.split()
        if len(args) < 2:
            await message.reply_text(
                "❌ Masukkan App ID!\n"
                "Contoh: <code>.appdownload 590a1766851f64f2232d8ce9067c5416</code>"
            )
            return
        
        app_id = args[1]
        
        processing_msg = await message.reply_text(
            f"<blockquote><b>📦 MENYIAPKAN DOWNLOAD</b>\n\n"
            f"🆔 <b>App ID:</b> <code>{app_id}</code>\n"
            f"⏳ Mohon tunggu...</blockquote>"
        )
        
        # Cek status dulu
        params = {"appId": app_id}
        status_response = requests.get(f"{BASE_URL}/status", params=params, timeout=10)
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            build_status = status_data.get("buildStatus", "unknown")
            
            if build_status != "completed":
                await processing_msg.edit_text(
                    f"❌ Aplikasi belum siap!\n"
                    f"Status saat ini: {build_status}\n"
                    f"Gunakan <code>.appstatus {app_id}</code> untuk cek status terbaru."
                )
                return
            
            # Request download
            download_response = requests.get(f"{BASE_URL}/download", params=params, timeout=15)
            
            if download_response.status_code == 200:
                download_data = download_response.json()
                
                if download_data.get("status") and download_data.get("details", {}).get("buildFile"):
                    build_file = download_data["details"]["buildFile"]
                    
                    if build_file and len(build_file) > 0:
                        # Ambil URL download pertama
                        download_url = build_file[0] if isinstance(build_file, list) else build_file
                        
                        details = download_data.get("details", {})
                        app_name = details.get("appName", "Aplikasi")
                        
                        await processing_msg.edit_text(
                            f"<blockquote><b>✅ LINK DOWNLOAD APLIKASI</b>\n\n"
                            f"📱 <b>Nama:</b> {app_name}\n"
                            f"🆔 <b>App ID:</b> <code>{app_id}</code>\n\n"
                            f"🔗 <b>Link Download:</b>\n"
                            f"<code>{download_url}</code>\n\n"
                            f"⬇️ Klik link di atas untuk download</blockquote>"
                        )
                    else:
                        await processing_msg.edit_text(
                            f"❌ File download tidak ditemukan!"
                        )
                else:
                    await processing_msg.edit_text(
                        f"❌ Gagal mendapatkan link download!\n"
                        f"Error: {download_data.get('error', 'Unknown error')}"
                    )
            else:
                await processing_msg.edit_text(f"❌ HTTP Error: {download_response.status_code}")
        else:
            await processing_msg.edit_text(f"❌ HTTP Error: {status_response.status_code}")
            
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)[:100]}")

# Callback handlers
@PY.CALLBACK("appstatus_")
async def callback_appstatus(client, callback_query):
    app_id = callback_query.data.replace("appstatus_", "")
    
    await callback_query.answer("Mengecek status...")
    
    params = {"appId": app_id}
    response = requests.get(f"{BASE_URL}/status", params=params, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        
        if data.get("status"):
            build_status = data.get("buildStatus", "unknown")
            details = data.get("details", {})
            
            status_emoji = {
                "building": "🔨",
                "completed": "✅",
                "failed": "❌",
                "pending": "⏳",
                "unknown": "❓"
            }.get(build_status, "❓")
            
            caption = f"""
<blockquote><b>{status_emoji} STATUS APLIKASI</b>

🆔 <b>App ID:</b> <code>{app_id}</code>
📊 <b>Status:</b> {build_status.upper()}

🌐 <b>URL:</b> {details.get('url', 'N/A')}
📱 <b>Nama:</b> {details.get('appName', 'N/A')}"""
            
            keyboard = None
            if build_status == "completed":
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬇️ Download APK", callback_data=f"appdownload_{app_id}")]
                ])
            
            await callback_query.message.edit_text(caption, reply_markup=keyboard)
        else:
            await callback_query.answer("Gagal cek status!", show_alert=True)
    else:
        await callback_query.answer("HTTP Error!", show_alert=True)

@PY.CALLBACK("appdownload_")
async def callback_appdownload(client, callback_query):
    app_id = callback_query.data.replace("appdownload_", "")
    
    await callback_query.answer("Menyiapkan download...")
    
    params = {"appId": app_id}
    response = requests.get(f"{BASE_URL}/download", params=params, timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        
        if data.get("status") and data.get("details", {}).get("buildFile"):
            build_file = data["details"]["buildFile"]
            
            if build_file and len(build_file) > 0:
                download_url = build_file[0] if isinstance(build_file, list) else build_file
                
                details = data.get("details", {})
                app_name = details.get("appName", "Aplikasi")
                
                await callback_query.message.reply_text(
                    f"<blockquote><b>✅ LINK DOWNLOAD APLIKASI</b>\n\n"
                    f"📱 <b>Nama:</b> {app_name}\n"
                    f"🆔 <b>App ID:</b> <code>{app_id}</code>\n\n"
                    f"🔗 <b>Link Download:</b>\n"
                    f"<code>{download_url}</code></blockquote>"
                )
                await callback_query.answer("Link download siap!")
            else:
                await callback_query.answer("File tidak ditemukan!", show_alert=True)
        else:
            await callback_query.answer("Gagal mendapatkan link!", show_alert=True)
    else:
        await callback_query.answer("HTTP Error!", show_alert=True)

@PY.CALLBACK("appcancel_")
async def callback_appcancel(client, callback_query):
    app_id = callback_query.data.replace("appcancel_", "")
    
    # Hapus dari data lokal
    if app_id in app_data:
        del app_data[app_id]
    
    await callback_query.answer("Pembuatan aplikasi dibatalkan!")
    await callback_query.message.edit_text(
        f"<blockquote><b>❌ PEMBUATAN DIBATALKAN</b>\n\n"
        f"🆔 <b>App ID:</b> <code>{app_id}</code>\n"
        f"Proses pembuatan aplikasi telah dibatalkan.</blockquote>"
    )
