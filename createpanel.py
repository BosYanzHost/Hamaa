from fansx import *
import requests
import json
import os
import time
import asyncio
import random
from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

__MODULE__ = "ᴘᴀɴᴇʟ"
__HELP__ = """
<b>『 PANEL PTERODACTYL 』</b>

<b>⌲ Perintah:</b>
ᚗ <code>{0}panel [tipe] [nama]</code> 
⊶ Membuat panel dengan spesifikasi tertentu

ᚗ <code>{0}unli [nama]</code>
⊶ Membuat panel unlimited

ᚗ <code>{0}serverlist</code>
⊶ Melihat daftar server panel tersedia

<b>⌲ Tipe Panel:</b>
• 1gb, 2gb, 3gb, 4gb, 5gb
• 6gb, 7gb, 8gb, 9gb, 10gb
• unli (unlimited)

<b>⌲ Contoh:</b>
<code>.panel 1gb joko</code>
<code>.panel 5gb budi</code>
<code>.unli siti</code></blockquote>
"""

# ============================================
# FILE UNTUK MENYIMPAN DATA
# ============================================
SERVERS_FILE = "ptero_servers.json"

# Default eggs untuk berbagai tipe panel
DEFAULT_EGGS = {
    "1gb": [15, 16, 17, 18, 19],
    "2gb": [15, 16, 17, 18, 19],
    "3gb": [15, 16, 17, 18, 19],
    "4gb": [15, 16, 17, 18, 19],
    "5gb": [15, 16, 17, 18, 19],
    "6gb": [15, 16, 17, 18, 19],
    "7gb": [15, 16, 17, 18, 19],
    "8gb": [15, 16, 17, 18, 19],
    "9gb": [15, 16, 17, 18, 19],
    "10gb": [15, 16, 17, 18, 19],
    "unli": [15, 16, 17, 18, 19]
}

# Spesifikasi untuk setiap tipe panel
PANEL_SPECS = {
    "1gb": {"memo": "1024", "disk": "5120", "cpu": "100"},
    "2gb": {"memo": "2048", "disk": "10240", "cpu": "150"},
    "3gb": {"memo": "3072", "disk": "15360", "cpu": "200"},
    "4gb": {"memo": "4096", "disk": "20480", "cpu": "250"},
    "5gb": {"memo": "5120", "disk": "25600", "cpu": "300"},
    "6gb": {"memo": "6144", "disk": "30720", "cpu": "350"},
    "7gb": {"memo": "7168", "disk": "35840", "cpu": "400"},
    "8gb": {"memo": "8192", "disk": "40960", "cpu": "450"},
    "9gb": {"memo": "9216", "disk": "46080", "cpu": "500"},
    "10gb": {"memo": "10240", "disk": "51200", "cpu": "550"},
    "unli": {"memo": "0", "disk": "0", "cpu": "0"}
}

# Default location
DEFAULT_LOC = "1"

# Default gambar panel
PANEL_IMAGE = "https://files.catbox.moe/a7ljii.jpeg"  # Ganti dengan URL gambar lo

# ============================================
# FUNGSI UTILITY
# ============================================

def load_json(filename, default=None):
    """Load data dari file JSON"""
    if default is None:
        default = {}
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
    return default

def save_json(filename, data):
    """Simpan data ke file JSON"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

# ============================================
# FUNGSI MANAJEMEN SERVER PANEL
# ============================================

def get_servers():
    """Mendapatkan daftar server panel"""
    return load_json(SERVERS_FILE, {"servers": []})

def save_servers(servers_data):
    """Menyimpan daftar server panel"""
    return save_json(SERVERS_FILE, servers_data)

def get_server_by_name(name):
    """Mendapatkan server berdasarkan nama"""
    servers = get_servers()
    for server in servers.get("servers", []):
        if server["name"].lower() == name.lower():
            return server
    return None

async def get_valid_egg(server, egg_ids):
    """Mendapatkan egg yang valid dari server"""
    if not egg_ids or len(egg_ids) == 0:
        raise Exception("Daftar egg kosong")
    
    for egg_id in egg_ids:
        try:
            response = requests.get(
                f"{server['domain']}/api/application/nests/5/eggs/{egg_id}",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {server['plta']}"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if not data.get("errors") and data.get("attributes"):
                    return {
                        "eggId": egg_id,
                        "startup": data["attributes"]["startup"]
                    }
        except Exception as e:
            print(f"Error cek egg {egg_id}: {e}")
            continue
    
    raise Exception(f"Tidak ada egg valid di server {server['name']}")

# ============================================
# COMMAND SETTING SERVER (UNTUK SEMUA USER)
# ============================================

@PY.UBOT("setpanel")
async def setpanel_command(client, message):
    """Command untuk menambah/mengatur server panel - SEMUA USER BISA"""
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text(
            f"<blockquote><b>❌ FORMAT SETPANEL</b>\n\n"
            f"<b>Untuk menambah server:</b>\n"
            f"<code>.setpanel add [nama] [domain] [PLTA] [PLTC]</code>\n\n"
            f"<b>Untuk menghapus server:</b>\n"
            f"<code>.setpanel del [nama/id]</code>\n\n"
            f"<b>Untuk melihat daftar server:</b>\n"
            f"<code>.setpanel list</code>\n\n"
            f"<b>Contoh:</b>\n"
            f"<code>.setpanel add server1 https://panel.domain.com plta_key_xxx ptc_key_xxx</code></blockquote>"
        )
        return
    
    action = args[1].lower()
    
    # ===== ADD SERVER =====
    if action == "add":
        if len(args) < 5:
            await message.reply_text(f"{ggl} Format: .setpanel add [nama] [domain] [PLTA] [PLTC]")
            return
        
        name = args[2]
        domain = args[3].rstrip('/')
        plta = args[4]
        pltc = args[5] if len(args) > 5 else plta
        
        # Validasi domain
        if not domain.startswith(('http://', 'https://')):
            domain = 'https://' + domain
        
        # Cek apakah nama sudah ada
        if get_server_by_name(name):
            await message.reply_text(f"{ggl} Server dengan nama '{name}' sudah ada!")
            return
        
        # Test koneksi ke API
        try:
            test_response = requests.get(
                f"{domain}/api/application/servers",
                headers={"Authorization": f"Bearer {plta}"},
                timeout=10
            )
            
            if test_response.status_code not in [200, 201]:
                await message.reply_text(f"{ggl} Gagal konek ke API! Cek domain/PLTA lo.")
                return
        except Exception as e:
            await message.reply_text(f"{ggl} Error koneksi: {str(e)[:100]}")
            return
        
        # Simpan server baru
        servers = get_servers()
        server_id = str(int(time.time()))
        
        new_server = {
            "id": server_id,
            "name": name,
            "domain": domain,
            "plta": plta,
            "pltc": pltc,
            "created_at": time.time(),
            "created_by": message.from_user.id
        }
        
        servers["servers"].append(new_server)
        save_servers(servers)
        
        await message.reply_text(
            f"<blockquote><b>✅ SERVER BERHASIL DITAMBAH</b>\n\n"
            f"📛 <b>Nama:</b> {name}\n"
            f"🌐 <b>Domain:</b> {domain}\n"
            f"🆔 <b>ID:</b> <code>{server_id}</code>\n"
            f"🔑 <b>PLTA:</b> <code>{plta[:15]}...</code>\n"
            f"🔑 <b>PLTC:</b> <code>{pltc[:15]}...</code></blockquote>"
        )
    
    # ===== DELETE SERVER =====
    elif action in ["del", "delete", "remove"]:
        if len(args) < 3:
            await message.reply_text(f"{ggl} Format: .setpanel del [nama/id]")
            return
        
        identifier = args[2]
        servers = get_servers()
        
        found_index = -1
        found_server = None
        
        for i, server in enumerate(servers["servers"]):
            if server["name"].lower() == identifier.lower() or server["id"] == identifier:
                found_index = i
                found_server = server
                break
        
        if found_index == -1:
            await message.reply_text(f"{ggl} Server '{identifier}' tidak ditemukan!")
            return
        
        del servers["servers"][found_index]
        save_servers(servers)
        
        await message.reply_text(
            f"<blockquote><b>✅ SERVER DIHAPUS</b>\n\n"
            f"📛 <b>Nama:</b> {found_server['name']}\n"
            f"🌐 <b>Domain:</b> {found_server['domain']}</blockquote>"
        )
    
    # ===== LIST SERVERS =====
    elif action == "list":
        servers = get_servers()
        
        if not servers["servers"]:
            await message.reply_text(f"{ggl} Belum ada server terdaftar!\nGunakan .setpanel add untuk menambah server.")
            return
        
        text = "<blockquote><b>📋 DAFTAR SERVER PANEL</b>\n\n"
        for i, server in enumerate(servers["servers"], 1):
            text += f"<b>{i}. {server['name']}</b>\n"
            text += f"🆔 ID: <code>{server['id']}</code>\n"
            text += f"🌐 Domain: {server['domain']}\n"
            text += f"━━━━━━━━━━━━━━━━━━\n"
        
        text += f"Total: {len(servers['servers'])} server</blockquote>"
        await message.reply_text(text)

# ============================================
# COMMAND UNLI (PAKAI NAMA AJA)
# ============================================

@PY.UBOT("unli")
async def unli_command(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    
    # Cek format - LANGSUNG NAMA AJA
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text(
            f"<blockquote><b>❌ FORMAT UNLI</b>\n\n"
            f"<b>Contoh:</b>\n"
            f"<code>.unli joko</code>\n"
            f"<code>.unli siti</code>\n"
            f"<code>.unli budi</code></blockquote>"
        )
        return
    
    username = args[1].strip()
    
    # Validasi username (hanya huruf dan angka)
    if not username.isalnum():
        await message.reply_text(f"{ggl} Username hanya boleh huruf dan angka (tanpa spasi)!")
        return
    
    # Proses pembuatan panel
    processing = await message.reply_text(f"{prs} Membuat panel UNLI untuk {username}...")
    
    # Ambil server pertama yang tersedia
    servers = get_servers()
    if not servers["servers"]:
        await processing.edit_text(f"{ggl} Tidak ada server panel terdaftar!\nGunakan .setpanel add untuk menambah server.")
        return
    
    # Pilih server pertama
    selected_server = servers["servers"][0]
    
    try:
        # Generate data
        panel_name = f"{username}unli"
        password = username + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=5))
        email = f"{username}@unli.zyura"
        
        # Startup script
        startup_script = (
            'if [[ -d .git ]] && [[ {{AUTO_UPDATE}} == "1" ]]; then git pull; fi; '
            'if [[ ! -z ${NODE_PACKAGES} ]]; then /usr/local/bin/npm install ${NODE_PACKAGES}; fi; '
            'if [[ ! -z ${UNNODE_PACKAGES} ]]; then /usr/local/bin/npm uninstall ${UNNODE_PACKAGES}; fi; '
            'if [ -f /home/container/package.json ]; then /usr/local/bin/npm install; fi; '
            '/usr/local/bin/${CMD_RUN}'
        )
        
        # CREATE USER
        await processing.edit_text(f"{prs} Membuat user {username} di panel...")
        
        user_response = requests.post(
            f"{selected_server['domain']}/api/application/users",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {selected_server['plta']}"
            },
            json={
                "email": email,
                "username": username,
                "first_name": username,
                "last_name": username,
                "language": "en",
                "password": password
            },
            timeout=30
        )
        
        if user_response.status_code not in [200, 201]:
            error_data = user_response.json()
            error_msg = error_data.get("errors", [{}])[0].get("detail", "Unknown error")
            raise Exception(f"Gagal buat user: {error_msg}")
        
        user_data = user_response.json()
        user = user_data["attributes"]
        
        # Cek egg valid
        await processing.edit_text(f"{prs} Mengecek egg valid...")
        egg_data = await get_valid_egg(selected_server, DEFAULT_EGGS["unli"])
        
        # CREATE SERVER
        await processing.edit_text(f"{prs} Membuat server {panel_name}...")
        
        specs = PANEL_SPECS["unli"]
        
        server_response = requests.post(
            f"{selected_server['domain']}/api/application/servers",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {selected_server['plta']}"
            },
            json={
                "name": panel_name,
                "user": user["id"],
                "egg": int(egg_data["eggId"]),
                "docker_image": "ghcr.io/parkervcp/yolks:nodejs_20",
                "startup": startup_script,
                "environment": {
                    "INST": "npm",
                    "USER_UPLOAD": "0",
                    "AUTO_UPDATE": "0",
                    "CMD_RUN": "npm start"
                },
                "limits": {
                    "memory": int(specs["memo"]),
                    "swap": 0,
                    "disk": int(specs["disk"]),
                    "io": 500,
                    "cpu": int(specs["cpu"])
                },
                "feature_limits": {
                    "databases": 5,
                    "backups": 5,
                    "allocations": 1
                },
                "deploy": {
                    "locations": [int(DEFAULT_LOC)],
                    "dedicated_ip": False,
                    "port_range": []
                }
            },
            timeout=30
        )
        
        if server_response.status_code not in [200, 201]:
            # Rollback: hapus user jika server gagal
            try:
                requests.delete(
                    f"{selected_server['domain']}/api/application/users/{user['id']}",
                    headers={"Authorization": f"Bearer {selected_server['plta']}"}
                )
            except:
                pass
            
            error_data = server_response.json()
            error_msg = error_data.get("errors", [{}])[0].get("detail", "Unknown error")
            raise Exception(f"Gagal buat server: {error_msg}")
        
        server_data = server_response.json()
        server = server_data["attributes"]
        
        await processing.delete()
        
        # Kirim detail ke CHAT DIMANA USER NGETIK
        await client.send_photo(
            chat_id=message.chat.id,
            photo=PANEL_IMAGE,
            caption=f"""
<blockquote><b>✅ PANEL UNLIMITED BERHASIL DIBUAT</b>

<b>👤 Informasi Akun</b>
• Username: <code>{username}</code>
• Password: <code>{password}</code>
• Email: <code>{email}</code>
• ID User: <code>{user['id']}</code>

<b>📊 Spesifikasi Server</b>
• Memory: Unlimited
• Disk: Unlimited
• CPU: Unlimited
• Egg ID: {egg_data['eggId']}

<b>🌐 Akses Login</b>
<a href="{selected_server['domain']}">🔗 KLIK DISINI UNTUK LOGIN</a>

<b>📌 Rules Panel</b>
• No DDOS
• No Share/Free
• Garansi 15 hari
• Simpan Data Akun</blockquote>
"""
        )
        
    except requests.exceptions.Timeout:
        await processing.edit_text(f"{ggl} Timeout! Server panel lambat.")
    except Exception as e:
        await processing.edit_text(f"{ggl} Gagal: {str(e)[:200]}")

# ============================================
# COMMAND PANEL 1GB - 10GB (PAKAI NAMA AJA)
# ============================================

@PY.UBOT("panel")
async def panel_command(client, message):
    """Handler untuk command panel 1gb-10gb - PAKAI NAMA AJA"""
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    
    # Parse command (format: .panel [tipe] [nama])
    args = message.text.split()
    if len(args) < 3:
        await message.reply_text(
            f"<blockquote><b>❌ FORMAT PANEL</b>\n\n"
            f"<b>Contoh:</b>\n"
            f"<code>.panel 1gb joko</code>\n"
            f"<code>.panel 2gb budi</code>\n"
            f"<code>.panel 5gb siti</code>\n\n"
            f"<b>Tipe tersedia:</b> 1gb, 2gb, 3gb, 4gb, 5gb, 6gb, 7gb, 8gb, 9gb, 10gb</blockquote>"
        )
        return
    
    cmd_type = args[1].lower()
    username = args[2].strip()
    
    # Validasi username
    if not username.isalnum():
        await message.reply_text(f"{ggl} Username hanya boleh huruf dan angka (tanpa spasi)!")
        return
    
    # Validasi tipe panel
    valid_types = ["1gb", "2gb", "3gb", "4gb", "5gb", "6gb", "7gb", "8gb", "9gb", "10gb"]
    if cmd_type not in valid_types:
        await message.reply_text(f"{ggl} Tipe panel tidak valid! Pilih: {', '.join(valid_types)}")
        return
    
    # Proses pembuatan panel
    processing = await message.reply_text(f"{prs} Membuat panel {cmd_type.upper()} untuk {username}...")
    
    # Ambil server pertama yang tersedia
    servers = get_servers()
    if not servers["servers"]:
        await processing.edit_text(f"{ggl} Tidak ada server panel terdaftar!\nGunakan .setpanel add untuk menambah server.")
        return
    
    # Pilih server pertama
    selected_server = servers["servers"][0]
    
    try:
        # Generate data
        panel_name = f"{username}{cmd_type}"
        password = username + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=5))
        email = f"{username}@{cmd_type}.zyura"
        
        # CREATE USER
        await processing.edit_text(f"{prs} Membuat user {username} di panel...")
        
        user_response = requests.post(
            f"{selected_server['domain']}/api/application/users",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {selected_server['plta']}"
            },
            json={
                "email": email,
                "username": username,
                "first_name": username,
                "last_name": username,
                "language": "en",
                "password": password
            },
            timeout=30
        )
        
        if user_response.status_code not in [200, 201]:
            error_data = user_response.json()
            error_msg = error_data.get("errors", [{}])[0].get("detail", "Unknown error")
            raise Exception(f"Gagal buat user: {error_msg}")
        
        user_data = user_response.json()
        user = user_data["attributes"]
        
        # Cek egg valid
        await processing.edit_text(f"{prs} Mengecek egg valid...")
        egg_data = await get_valid_egg(selected_server, DEFAULT_EGGS.get(cmd_type, DEFAULT_EGGS["1gb"]))
        
        # CREATE SERVER
        await processing.edit_text(f"{prs} Membuat server {panel_name}...")
        
        specs = PANEL_SPECS[cmd_type]
        
        startup_script = (
            'if [[ -d .git ]] && [[ {{AUTO_UPDATE}} == "1" ]]; then git pull; fi; '
            'if [[ ! -z ${NODE_PACKAGES} ]]; then /usr/local/bin/npm install ${NODE_PACKAGES}; fi; '
            'if [[ ! -z ${UNNODE_PACKAGES} ]]; then /usr/local/bin/npm uninstall ${UNNODE_PACKAGES}; fi; '
            'if [ -f /home/container/package.json ]; then /usr/local/bin/npm install; fi; '
            '/usr/local/bin/${CMD_RUN}'
        )
        
        server_response = requests.post(
            f"{selected_server['domain']}/api/application/servers",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {selected_server['plta']}"
            },
            json={
                "name": panel_name,
                "user": user["id"],
                "egg": int(egg_data["eggId"]),
                "docker_image": "ghcr.io/parkervcp/yolks:nodejs_18",
                "startup": startup_script,
                "environment": {
                    "INST": "npm",
                    "USER_UPLOAD": "0",
                    "AUTO_UPDATE": "0",
                    "CMD_RUN": "npm start"
                },
                "limits": {
                    "memory": int(specs["memo"]),
                    "swap": 0,
                    "disk": int(specs["disk"]),
                    "io": 500,
                    "cpu": int(specs["cpu"])
                },
                "feature_limits": {
                    "databases": 5,
                    "backups": 5,
                    "allocations": 1
                },
                "deploy": {
                    "locations": [int(DEFAULT_LOC)],
                    "dedicated_ip": False,
                    "port_range": []
                }
            },
            timeout=30
        )
        
        if server_response.status_code not in [200, 201]:
            # Rollback: hapus user jika server gagal
            try:
                requests.delete(
                    f"{selected_server['domain']}/api/application/users/{user['id']}",
                    headers={"Authorization": f"Bearer {selected_server['plta']}"}
                )
            except:
                pass
            
            error_data = server_response.json()
            error_msg = error_data.get("errors", [{}])[0].get("detail", "Unknown error")
            raise Exception(f"Gagal buat server: {error_msg}")
        
        server_data = server_response.json()
        server = server_data["attributes"]
        
        await processing.delete()
        
        # Kirim detail ke CHAT DIMANA USER NGETIK
        memory_text = "Unlimited" if specs['memo'] == '0' else f"{specs['memo']} MB"
        disk_text = "Unlimited" if specs['disk'] == '0' else f"{specs['disk']} MB"
        
        await client.send_photo(
            chat_id=message.chat.id,
            photo=PANEL_IMAGE,
            caption=f"""
<blockquote><b>✅ PANEL {cmd_type.upper()} BERHASIL DIBUAT</b>

<b>👤 Informasi Akun</b>
• Username: <code>{username}</code>
• Password: <code>{password}</code>
• Email: <code>{email}</code>
• ID User: <code>{user['id']}</code>

<b>📊 Spesifikasi Server</b>
• Memory: {memory_text}
• Disk: {disk_text}
• CPU: {specs['cpu']}%
• Egg ID: {egg_data['eggId']}

<b>🌐 Akses Login</b>
<a href="{selected_server['domain']}">🔗 KLIK DISINI UNTUK LOGIN</a>

<b>📌 Rules Panel</b>
• No DDOS
• No Share/Free
• Garansi 15 hari
• Simpan Data Akun</blockquote>
"""
        )
        
    except requests.exceptions.Timeout:
        await processing.edit_text(f"{ggl} Timeout! Server panel lambat.")
    except Exception as e:
        await processing.edit_text(f"{ggl} Gagal: {str(e)[:200]}")

# ============================================
# COMMAND SERVERLIST
# ============================================

@PY.UBOT("serverlist")
async def serverlist_command(client, message):
    """Melihat daftar server yang tersedia"""
    servers = get_servers()
    
    if not servers["servers"]:
        await message.reply_text("❌ Belum ada server panel terdaftar!\nGunakan .setpanel add untuk menambah server.")
        return
    
    text = "<blockquote><b>📋 SERVER TERSEDIA</b>\n\n"
    for i, server in enumerate(servers["servers"], 1):
        text += f"<b>{i}. {server['name']}</b>\n"
        text += f"🌐 {server['domain']}\n\n"
    
    text += f"Total: {len(servers['servers'])} server</blockquote>"
    await message.reply_text(text)
