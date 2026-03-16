from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone
from fansx.config import OWNER_ID
from fansx import *

# ============================================
# HIERARKI ROLE LENGKAP:
# OWNER > PT > ALLROLE > CEO > TK > ADMIN > SELLER
# ============================================

async def get_user_role(client, user_id):
    """Mendapatkan role user dengan hierarki lengkap"""
    owner_list = OWNER_ID if isinstance(OWNER_ID, list) else [OWNER_ID]
    pt_list = await get_list_from_vars(bot.me.id, "PT_USERS")
    allrole_list = await get_list_from_vars(bot.me.id, "ALLROLE_USERS")
    ceo_list = await get_list_from_vars(bot.me.id, "CEO_USERS")
    tk_list = await get_list_from_vars(bot.me.id, "TK_USERS")
    admin_list = await get_list_from_vars(bot.me.id, "ADMIN_USERS")
    seller_list = await get_list_from_vars(bot.me.id, "SELER_USERS")
    
    if user_id in owner_list:
        return "OWNER"
    elif user_id in pt_list:
        return "PT"
    elif user_id in allrole_list:
        return "ALLROLE"
    elif user_id in ceo_list:
        return "CEO"
    elif user_id in tk_list:
        return "TK"
    elif user_id in admin_list:
        return "ADMIN"
    elif user_id in seller_list:
        return "SELLER"
    else:
        return "USER"

async def check_role(client, user_id, required_level):
    """Cek apakah user memiliki akses ke level tertentu"""
    role = await get_user_role(client, user_id)  # ✅ FIX: tambah client
    
    role_hierarchy = {
        "OWNER": 6,
        "PT": 5,
        "ALLROLE": 4,
        "CEO": 3,
        "TK": 2,
        "ADMIN": 1,
        "SELLER": 0,
        "USER": -1
    }
    
    required_values = {
        "SELLER": 0,
        "ADMIN": 1,
        "TK": 2,
        "CEO": 3,
        "ALLROLE": 4,
        "PT": 5,
        "OWNER": 6
    }
    
    required_value = required_values.get(required_level, 0)
    user_value = role_hierarchy.get(role, -1)
    
    return user_value >= required_value

# ============================================
# DECORATORS UNTUK CEK ROLE
# ============================================

def PY_SELLER(func):
    """Akses untuk SELLER ke atas"""
    async def wrapper(client, message):
        if not await check_role(client, message.from_user.id, "SELLER"):  # ✅ FIX
            return await message.reply("❌ Perintah ini hanya untuk SELLER ke atas!")
        return await func(client, message)
    return wrapper

def PY_ADMIN(func):
    """Akses untuk ADMIN ke atas"""
    async def wrapper(client, message):
        if not await check_role(client, message.from_user.id, "ADMIN"):  # ✅ FIX
            return await message.reply("❌ Perintah ini hanya untuk ADMIN ke atas!")
        return await func(client, message)
    return wrapper

def PY_TK(func):
    """Akses untuk TK ke atas"""
    async def wrapper(client, message):
        if not await check_role(client, message.from_user.id, "TK"):  # ✅ FIX
            return await message.reply("❌ Perintah ini hanya untuk TK ke atas!")
        return await func(client, message)
    return wrapper

def PY_CEO(func):
    """Akses untuk CEO ke atas"""
    async def wrapper(client, message):
        if not await check_role(client, message.from_user.id, "CEO"):  # ✅ FIX
            return await message.reply("❌ Perintah ini hanya untuk CEO ke atas!")
        return await func(client, message)
    return wrapper

def PY_ALLROLE(func):
    """Akses untuk ALLROLE ke atas"""
    async def wrapper(client, message):
        if not await check_role(client, message.from_user.id, "ALLROLE"):  # ✅ FIX
            return await message.reply("❌ Perintah ini hanya untuk ALLROLE ke atas!")
        return await func(client, message)
    return wrapper

def PY_PT(func):
    """Akses untuk PT ke atas"""
    async def wrapper(client, message):
        if not await check_role(client, message.from_user.id, "PT"):  # ✅ FIX
            return await message.reply("❌ Perintah ini hanya untuk PT ke atas!")
        return await func(client, message)
    return wrapper

# ============================================
# MANAJEMEN ALLROLE (BISA DIAKSES PT & OWNER)
# ============================================

@PY.UBOT("addallrole")
@PY_PT  # PT ke atas bisa manage ALLROLE
async def add_allrole(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    allrole_users = await get_list_from_vars(bot.me.id, "ALLROLE_USERS")

    if user.id in allrole_users:
        return await msg.edit(f"""
<blockquote><b>❌ SUDAH ALLROLE</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Sudah menjadi ALLROLE</blockquote>""")

    try:
        await add_to_vars(bot.me.id, "ALLROLE_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ BERHASIL MENAMBAH ALLROLE</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: ALLROLE</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("unallrole")
@PY_PT
async def remove_allrole(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    allrole_users = await get_list_from_vars(bot.me.id, "ALLROLE_USERS")

    if user.id not in allrole_users:
        return await msg.edit(f"""
<blockquote><b>❌ BUKAN ALLROLE</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Bukan ALLROLE</blockquote>""")

    try:
        await remove_from_vars(bot.me.id, "ALLROLE_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ BERHASIL MENGHAPUS ALLROLE</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: ALLROLE dihapus</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("getallrole")
@PY_PT
async def get_allrole(client, message):
    prs = await EMO.PROSES(client)
    
    Sh = await message.reply(f"{prs} Mengambil daftar ALLROLE...")
    allrole_users = await get_list_from_vars(bot.me.id, "ALLROLE_USERS")

    if not allrole_users:
        return await Sh.edit("<b>📭 Daftar ALLROLE kosong</b>")

    allrole_list = []
    for user_id in allrole_users:
        try:
            user = await client.get_users(int(user_id))
            allrole_list.append(
                f"🌟 <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> | <code>{user.id}</code>"
            )
        except:
            continue

    if allrole_list:
        response = (
            "<blockquote><b>📋 DAFTAR ALLROLE</b>\n\n"
            + "\n".join(allrole_list)
            + f"\n\n<b>📊 Total ALLROLE:</b> {len(allrole_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<b>❌ Tidak dapat mengambil daftar ALLROLE</b>")

# ============================================
# MANAJEMEN PT (OWNER ONLY)
# ============================================

@PY.UBOT("addpt")
async def add_pt(client, message):
    if message.from_user.id != OWNER_ID:
        return
    
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    pt_users = await get_list_from_vars(bot.me.id, "PT_USERS")

    if user.id in pt_users:
        return await msg.edit(f"""
<blockquote><b>❌ SUDAH PT</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Sudah menjadi Pemilik Tim</blockquote>""")

    try:
        await add_to_vars(bot.me.id, "PT_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ BERHASIL MENAMBAH PT</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Pemilik Tim</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("unpt")
async def remove_pt(client, message):
    if message.from_user.id != OWNER_ID:
        return
    
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    pt_users = await get_list_from_vars(bot.me.id, "PT_USERS")

    if user.id not in pt_users:
        return await msg.edit(f"""
<blockquote><b>❌ BUKAN PT</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Bukan Pemilik Tim</blockquote>""")

    try:
        await remove_from_vars(bot.me.id, "PT_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ BERHASIL MENGHAPUS PT</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: PT dihapus</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("getpt")
async def get_pt(client, message):
    if message.from_user.id != OWNER_ID:
        return
    
    prs = await EMO.PROSES(client)
    
    Sh = await message.reply(f"{prs} Mengambil daftar PT...")
    pt_users = await get_list_from_vars(bot.me.id, "PT_USERS")

    if not pt_users:
        return await Sh.edit("<b>📭 Daftar PT kosong</b>")

    pt_list = []
    for user_id in pt_users:
        try:
            user = await client.get_users(int(user_id))
            pt_list.append(
                f"👑 <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> | <code>{user.id}</code>"
            )
        except:
            continue

    if pt_list:
        response = (
            "<blockquote><b>📋 DAFTAR PEMILIK TIM (PT)</b>\n\n"
            + "\n".join(pt_list)
            + f"\n\n<b>📊 Total PT:</b> {len(pt_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<b>❌ Tidak dapat mengambil daftar PT</b>")

# ============================================
# MANAJEMEN CEO (PT & OWNER)
# ============================================

@PY.UBOT("addceo")
@PY_PT
async def add_ceo(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    ceo_users = await get_list_from_vars(bot.me.id, "CEO_USERS")

    if user.id in ceo_users:
        return await msg.edit(f"""
<blockquote><b>❌ SUDAH CEO</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Sudah menjadi CEO</blockquote>""")

    try:
        await add_to_vars(bot.me.id, "CEO_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ BERHASIL MENAMBAH CEO</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: CEO</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("unceo")
@PY_PT
async def remove_ceo(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    ceo_users = await get_list_from_vars(bot.me.id, "CEO_USERS")

    if user.id not in ceo_users:
        return await msg.edit(f"""
<blockquote><b>❌ BUKAN CEO</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Bukan CEO</blockquote>""")

    try:
        await remove_from_vars(bot.me.id, "CEO_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ BERHASIL MENGHAPUS CEO</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: CEO dihapus</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("getceo")
@PY_PT
async def get_ceo(client, message):
    prs = await EMO.PROSES(client)
    
    Sh = await message.reply(f"{prs} Mengambil daftar CEO...")
    ceo_users = await get_list_from_vars(bot.me.id, "CEO_USERS")

    if not ceo_users:
        return await Sh.edit("<b>📭 Daftar CEO kosong</b>")

    ceo_list = []
    for user_id in ceo_users:
        try:
            user = await client.get_users(int(user_id))
            ceo_list.append(
                f"⚜️ <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> | <code>{user.id}</code>"
            )
        except:
            continue

    if ceo_list:
        response = (
            "<blockquote><b>📋 DAFTAR CEO</b>\n\n"
            + "\n".join(ceo_list)
            + f"\n\n<b>📊 Total CEO:</b> {len(ceo_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<b>❌ Tidak dapat mengambil daftar CEO</b>")

# ============================================
# MANAJEMEN TK (CEO, ALLROLE, PT, OWNER)
# ============================================

@PY.UBOT("addtk")
@PY_CEO  # CEO ke atas bisa manage TK
async def add_tk(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    tk_users = await get_list_from_vars(bot.me.id, "TK_USERS")

    if user.id in tk_users:
        return await msg.edit(f"""
<blockquote><b>❌ SUDAH TK</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Sudah menjadi Tim Khusus</blockquote>""")

    try:
        await add_to_vars(bot.me.id, "TK_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ BERHASIL MENAMBAH TK</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Tim Khusus</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("untk")
@PY_CEO
async def remove_tk(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    tk_users = await get_list_from_vars(bot.me.id, "TK_USERS")

    if user.id not in tk_users:
        return await msg.edit(f"""
<blockquote><b>❌ BUKAN TK</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Bukan Tim Khusus</blockquote>""")

    try:
        await remove_from_vars(bot.me.id, "TK_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ BERHASIL MENGHAPUS TK</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: TK dihapus</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("gettk")
@PY_CEO
async def get_tk(client, message):
    prs = await EMO.PROSES(client)
    
    Sh = await message.reply(f"{prs} Mengambil daftar TK...")
    tk_users = await get_list_from_vars(bot.me.id, "TK_USERS")

    if not tk_users:
        return await Sh.edit("<b>📭 Daftar TK kosong</b>")

    tk_list = []
    for user_id in tk_users:
        try:
            user = await client.get_users(int(user_id))
            tk_list.append(
                f"🔰 <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> | <code>{user.id}</code>"
            )
        except:
            continue

    if tk_list:
        response = (
            "<blockquote><b>📋 DAFTAR TIM KHUSUS (TK)</b>\n\n"
            + "\n".join(tk_list)
            + f"\n\n<b>📊 Total TK:</b> {len(tk_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<b>❌ Tidak dapat mengambil daftar TK</b>")

# ============================================
# MANAJEMEN ADMIN (TK, CEO, ALLROLE, PT, OWNER)
# ============================================

@PY.UBOT("addadmin")
@PY_TK  # TK ke atas bisa manage Admin
async def add_admin(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    admin_users = await get_list_from_vars(bot.me.id, "ADMIN_USERS")

    if user.id in admin_users:
        return await msg.edit(f"""
<blockquote><b>❌ SUDAH ADMIN</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Sudah menjadi admin</blockquote>""")

    try:
        await add_to_vars(bot.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ BERHASIL MENAMBAH ADMIN</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Admin</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("unadmin")
@PY_TK
async def remove_admin(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    admin_users = await get_list_from_vars(bot.me.id, "ADMIN_USERS")

    if user.id not in admin_users:
        return await msg.edit(f"""
<blockquote><b>❌ BUKAN ADMIN</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Bukan admin</blockquote>""")

    try:
        await remove_from_vars(bot.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ BERHASIL MENGHAPUS ADMIN</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Admin dihapus</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("getadmin")
@PY_TK
async def get_admins(client, message):
    prs = await EMO.PROSES(client)
    
    Sh = await message.reply(f"{prs} Mengambil daftar admin...")
    admin_users = await get_list_from_vars(bot.me.id, "ADMIN_USERS")

    if not admin_users:
        return await Sh.edit("<b>📭 Daftar admin kosong</b>")

    admin_list = []
    for user_id in admin_users:
        try:
            user = await client.get_users(int(user_id))
            admin_list.append(
                f"👤 <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> | <code>{user.id}</code>"
            )
        except:
            continue

    if admin_list:
        response = (
            "<blockquote><b>📋 DAFTAR ADMIN</b>\n\n"
            + "\n".join(admin_list)
            + f"\n\n<b>📊 Total Admin:</b> {len(admin_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<b>❌ Tidak dapat mengambil daftar admin</b>")

# ============================================
# MANAJEMEN SELLER (ADMIN, TK, CEO, ALLROLE, PT, OWNER)
# ============================================

@PY.UBOT("addseles")
@PY_ADMIN  # Admin ke atas bisa manage Seller
async def add_seller(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    seller_users = await get_list_from_vars(bot.me.id, "SELER_USERS")

    if user.id in seller_users:
        return await msg.edit(f"""
<blockquote><b>❌ SUDAH SELLER</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Sudah menjadi seller</blockquote>""")

    try:
        await add_to_vars(bot.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ BERHASIL MENAMBAH SELLER</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Seller</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("unseles")
@PY_ADMIN
async def remove_seller(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    seller_users = await get_list_from_vars(bot.me.id, "SELER_USERS")

    if user.id not in seller_users:
        return await msg.edit(f"""
<blockquote><b>❌ BUKAN SELLER</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Bukan seller</blockquote>""")

    try:
        await remove_from_vars(bot.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ BERHASIL MENGHAPUS SELLER</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Seller dihapus</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("getseles")
@PY_ADMIN
async def get_sellers(client, message):
    prs = await EMO.PROSES(client)
    
    Sh = await message.reply(f"{prs} Mengambil daftar seller...")
    seller_users = await get_list_from_vars(bot.me.id, "SELER_USERS")

    if not seller_users:
        return await Sh.edit("<b>📭 Daftar seller kosong</b>")

    seller_list = []
    for user_id in seller_users:
        try:
            user = await client.get_users(int(user_id))
            seller_list.append(
                f"👤 <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> | <code>{user.id}</code>"
            )
        except:
            continue

    if seller_list:
        response = (
            "<blockquote><b>📋 DAFTAR SELLER</b>\n\n"
            + "\n".join(seller_list)
            + f"\n\n<b>📊 Total Seller:</b> {len(seller_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<b>❌ Tidak dapat mengambil daftar seller</b>")

# ============================================
# MANAJEMEN PREMIUM (SELLER KE ATAS)
# ============================================

@PY.UBOT("prem")
@PY_SELLER  # Seller ke atas bisa manage Premium
async def add_premium(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply(f"{prs} Memproses...")
    
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username - bulan")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")
    
    if not get_bulan:
        get_bulan = 1

    prem_users = await get_list_from_vars(bot.me.id, "PREM_USERS")

    if user.id in prem_users:
        return await msg.edit(f"""
<blockquote><b>❌ SUDAH PREMIUM</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Sudah premium</blockquote>""")

    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        await set_expired_date(user_id, expired)
        await add_to_vars(bot.me.id, "PREM_USERS", user.id)
        
        await msg.edit(f"""
<blockquote><b>✅ PREMIUM BERHASIL DITAMBAH</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
⏰ Expired: {get_bulan} bulan
🤖 Bot: @{bot.me.username}

📌 Cara Buat Userbot:
1. /start ke @MyUbotpremium_bot
2. Klik tombol "Buat Userbot"
3. Ikuti arahan dari bot</blockquote>""")
        
        return await bot.send_message(
            OWNER_ID,
            f"• ID Seller: <code>{message.from_user.id}</code>\n• ID Customer: <code>{user_id}</code>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("👤 Seller", callback_data=f"profil {message.from_user.id}"),
                    InlineKeyboardButton("Customer 👤", callback_data=f"profil {user_id}")
                ]
            ])
        )
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("unprem")
@PY_SELLER
async def remove_premium(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    prem_users = await get_list_from_vars(bot.me.id, "PREM_USERS")

    if user.id not in prem_users:
        return await msg.edit(f"""
<blockquote><b>❌ BUKAN PREMIUM</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Tidak terdaftar</blockquote>""")
    
    try:
        await remove_from_vars(bot.me.id, "PREM_USERS", user.id)
        await rem_expired_date(user_id)
        return await msg.edit(f"""
<blockquote><b>✅ PREMIUM DIHAPUS</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Premium dihapus</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("getprem")
@PY_SELLER
async def get_premium(client, message):
    prs = await EMO.PROSES(client)
    
    processing = await message.reply(f"{prs} Mengambil daftar premium...")
    
    text = ""
    count = 0
    prem = await get_list_from_vars(bot.me.id, "PREM_USERS")

    for user_id in prem:
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> | <code>{user.id}</code>"
        except Exception:
            continue
        text += f"<blockquote>{userlist}</blockquote>"
    
    if not text:
        await processing.edit_text("📭 Tidak ada user premium")
    else:
        await processing.edit_text(
            f"<blockquote><b>📋 DAFTAR PREMIUM</b>\n\n{text}\n\n<b>📊 Total: {count}</b></blockquote>"
        )

# ============================================
# MANAJEMEN SUPER ULTRA (SELLER KE ATAS)
# ============================================

@PY.UBOT("addultra")
@PY_SELLER
async def add_ultra(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    ultra_users = await get_list_from_vars(bot.me.id, "ULTRA_PREM")

    if user.id in ultra_users:
        return await msg.edit(f"""
<blockquote><b>❌ SUDAH SUPER ULTRA</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Sudah menjadi Super Ultra</blockquote>""")

    try:
        await add_to_vars(bot.me.id, "ULTRA_PREM", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ BERHASIL MENAMBAH SUPER ULTRA</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Super Ultra</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

@PY.UBOT("rmultra")
@PY_SELLER
async def remove_ultra(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    
    msg = await message.reply(f"{prs} Memproses...")
    user_id = await extract_user(message)
    
    if not user_id:
        return await msg.edit(f"{ggl} {message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

    ultra_users = await get_list_from_vars(bot.me.id, "ULTRA_PREM")

    if user.id not in ultra_users:
        return await msg.edit(f"""
<blockquote><b>❌ BUKAN SUPER ULTRA</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Tidak terdaftar</blockquote>""")

    try:
        await remove_from_vars(bot.me.id, "ULTRA_PREM", user.id)
        return await msg.edit(f"""
<blockquote><b>✅ SUPER ULTRA DIHAPUS</b>
👤 Nama: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
🆔 ID: <code>{user.id}</code>
📌 Status: Super Ultra dihapus</blockquote>""")
    except Exception as error:
        return await msg.edit(f"{ggl} {error}")

# ============================================
# CEK INFORMASI USER (SEMUA BISA)
# ============================================

@PY.UBOT("cek")
async def check_user(client, message):
    Sh = await message.reply("🔄 Processing...")
    user_id = await extract_user(message)
    
    if not user_id:
        user_id = message.from_user.id
    
    try:
        get_exp = await get_expired_date(user_id)
        sh = await client.get_users(user_id)
    except Exception as error:
        return await Sh.edit(f"❌ {error}")
    
    SH = await ubot.get_prefix(user_id)
    exp = get_exp.strftime("%d-%m-%Y") if get_exp else "Nonaktif"
    
    if user_id in await get_list_from_vars(bot.me.id, "ULTRA_PREM"):
        status = "⭐ SUPER ULTRA"
    elif user_id in await get_list_from_vars(bot.me.id, "PREM_USERS"):
        status = "💎 PREMIUM"
    else:
        status = "🆓 REGULAR"
    
    role_name = await get_user_role(client, user_id)
    
    # Emoji untuk role
    role_emoji = {
        "OWNER": "👑",
        "PT": "🏢",
        "ALLROLE": "🌟",
        "CEO": "⚜️",
        "TK": "🔰",
        "ADMIN": "👤",
        "SELLER": "💼",
        "USER": "👤"
    }
    
    emoji = role_emoji.get(role_name, "👤")
    
    await Sh.edit(f"""
<blockquote><b>📊 INFORMASI USER</b>

{emoji} <b>Nama:</b> {sh.mention}
🆔 <b>ID:</b> <code>{user_id}</code>
🎭 <b>Role:</b> {role_name}
💎 <b>Plan:</b> {status}
⚡ <b>Prefix:</b> <code>{' '.join(SH)}</code>
⏰ <b>Expired:</b> {exp}</blockquote>""")

# ============================================
# TIME MANAGEMENT (PT & OWNER)
# ============================================

@PY.UBOT("time")
@PY_PT  # PT ke atas bisa set time
async def set_time(client, message):
    Tm = await message.reply("🔄 Processing...")
    args = message.command
    
    if len(args) != 3:
        return await Tm.edit("❌ Format: .time user_id hari")
    
    user_id = int(args[1])
    get_day = int(args[2])
    
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(f"❌ {error}")
    
    if not get_day:
        get_day = 30
    
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    await set_expired_date(user_id, expire_date)
    
    await Tm.edit(f"""
<blockquote><b>✅ TIME UPDATED</b>
👤 User: {user.mention}
🆔 ID: <code>{user_id}</code>
⏰ Aktif: {get_day} hari</blockquote>""")