from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone

from fansx import *

__MODULE__ = "ᴅʙ ᴄᴏɴᴛʀᴏʟ"
__HELP__ = """
<blockquote><b>Bantuan Untuk DB Control</b></blockquote>

<blockquote><b>perintah : <code>{0}time</code>
    Untuk Menambah - Mengurangi Masa Aktif User</b></blockquote>

<blockquote><b>perintah : <code>{0}cek</code>
    Untuk Melihat Masa Aktif User</b></blockquote>

<blockquote><b>perintah : <code>{0}addadmin</code> - <code>{0}unadmin</code> - <code>{0}getadmin</code>
    Manajemen Admin (CEO/TK/ALLROLE)</b></blockquote>

<blockquote><b>perintah : <code>{0}addseles</code> - <code>{0}unseles</code> - <code>{0}getseles</code>
    Manajemen Seller (CEO/TK/ADMIN/ALLROLE)</b></blockquote>

<blockquote><b>perintah : <code>{0}addceo</code> - <code>{0}unceo</code> - <code>{0}getceo</code>
    Manajemen CEO (Owner/Allrole Only)</b></blockquote>

<blockquote><b>perintah : <code>{0}addtk</code> - <code>{0}untk</code> - <code>{0}gettk</code>
    Manajemen TK (CEO Only)</b></blockquote>

<blockquote><b>perintah : <code>{0}addallrole</code> - <code>{0}unallrole</code> - <code>{0}getallrole</code>
    Manajemen ALLROLE (Owner Only)</b></blockquote>

<blockquote><b>perintah : <code>{0}prem</code> - <code>{0}unprem</code> - <code>{0}getprem</code>
    Manajemen Premium (Seller/Admin/TK/CEO/ALLROLE)</b></blockquote>

<blockquote><b>perintah : <code>{0}superultra</code> - <code>{0}rmultra</code> - <code>{0}getultra</code>
    Manajemen SuperUltra (Seller/Admin/TK/CEO/ALLROLE)</b></blockquote>
"""

# ============================================
# CEK ROLE (DECORATORS)
# ============================================

async def get_user_role(client, user_id):
    """Mendapatkan role user berdasarkan hirarki"""
    owner_list = OWNER_ID if isinstance(OWNER_ID, list) else [OWNER_ID]
    ceo_list = await get_list_from_vars(client.me.id, "CEO_USERS")
    allrole_list = await get_list_from_vars(client.me.id, "ALLROLE_USERS")
    tk_list = await get_list_from_vars(client.me.id, "TK_USERS")
    admin_list = await get_list_from_vars(client.me.id, "ADMIN_USERS")
    seller_list = await get_list_from_vars(client.me.id, "SELER_USERS")
    
    if user_id in owner_list:
        return "OWNER"
    elif user_id in ceo_list:
        return "CEO"
    elif user_id in allrole_list:
        return "ALLROLE"
    elif user_id in tk_list:
        return "TK"
    elif user_id in admin_list:
        return "ADMIN"
    elif user_id in seller_list:
        return "SELLER"
    else:
        return "USER"

async def has_access(client, user_id, required_level):
    """
    Cek akses berdasarkan level:
    - OWNER: akses SEMUA (tertinggi)
    - ALLROLE: akses SEMUA KECUALI manage CEO & ALLROLE itu sendiri
    - CEO: akses CEO, TK, Admin, Seller, Premium
    - TK: akses TK, Admin, Seller, Premium
    - ADMIN: akses Admin, Seller, Premium
    - SELLER: akses Seller, Premium
    """
    role = await get_user_role(client, user_id)
    
    # Owner selalu punya akses tertinggi
    if role == "OWNER":
        return True
    
    # Mapping level akses
    if required_level == "OWNER":
        return role == "OWNER"
    
    elif required_level == "CEO":
        return role in ["CEO", "ALLROLE", "OWNER"]  # <-- CEO DITAMBAHKAN!
    
    elif required_level == "ALLROLE_MANAGE":
        return role in ["CEO", "OWNER"]  # <-- CEO DITAMBAHKAN!
    
    elif required_level == "TK":
        return role in ["TK", "ALLROLE", "CEO", "OWNER"]
    
    elif required_level == "ADMIN":
        return role in ["ADMIN", "TK", "ALLROLE", "CEO", "OWNER"]  # <-- ADMIN DITAMBAHKAN!
    
    elif required_level == "SELLER":
        return role in ["SELLER", "ADMIN", "TK", "ALLROLE", "CEO", "OWNER"]
    
    elif required_level == "PREMIUM":
        return role in ["SELLER", "ADMIN", "TK", "ALLROLE", "CEO", "OWNER"]
    
    return False

def PY_CEO(func):
    """Command untuk CEO ke atas (CEO, ALLROLE, OWNER)"""
    async def wrapper(client, message):
        if await has_access(client, message.from_user.id, "CEO"):
            return await func(client, message)
        else:
            await message.reply("<b>❌ Perintah ini hanya untuk CEO/ALLROLE!</b>")
            return
    return wrapper

def PY_ALLROLE(func):
    """Command untuk ALLROLE ke atas (ALLROLE, CEO, OWNER)"""
    async def wrapper(client, message):
        role = await get_user_role(client, message.from_user.id)
        if role in ["ALLROLE", "OWNER"]:
            return await func(client, message)
        else:
            await message.reply("<b>❌ Perintah ini hanya untuk ALLROLE!</b>")
            return
    return wrapper

def PY_TK(func):
    """Command untuk TK ke atas (TK, ALLROLE, CEO, OWNER)"""
    async def wrapper(client, message):
        if await has_access(client, message.from_user.id, "TK"):
            return await func(client, message)
        else:
            await message.reply("<b>❌ Perintah ini hanya untuk TK/ALLROLE!</b>")
            return
    return wrapper

def PY_ADMIN(func):
    """Command untuk Admin ke atas (ADMIN, TK, ALLROLE, CEO, OWNER)"""
    async def wrapper(client, message):
        if await has_access(client, message.from_user.id, "ADMIN"):
            return await func(client, message)
        else:
            await message.reply("<b>❌ Perintah ini hanya untuk Admin!</b>")
            return
    return wrapper

def PY_SELLER(func):
    """Command untuk Seller ke atas (SELLER, ADMIN, TK, ALLROLE, CEO, OWNER)"""
    async def wrapper(client, message):
        if await has_access(client, message.from_user.id, "SELLER"):
            return await func(client, message)
        else:
            await message.reply("<b>❌ Perintah ini hanya untuk Seller!</b>")
            return
    return wrapper

# ============================================
# MANAJEMEN ALLROLE (CEO & OWNER ONLY)
# ============================================

@PY.BOT("addallrole")
async def add_allrole(client, message):
    """Tambah ALLROLE - hanya CEO dan Owner"""
    # Cek akses khusus untuk manage allrole
    role = await get_user_role(client, message.from_user.id)
    if role not in ["CEO", "OWNER"]:
        return await message.reply("<b>❌ Perintah ini hanya untuk CEO!</b>")
    
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    allrole_users = await get_list_from_vars(client.me.id, "ALLROLE_USERS")

    if user.id in allrole_users:
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> sudah menjadi ALLROLE</blockquote>
""")

    try:
        await add_to_vars(client.me.id, "ALLROLE_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> ALLROLE</blockquote>
""")
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("unallrole")
async def un_allrole(client, message):
    """Hapus ALLROLE - hanya CEO dan Owner"""
    role = await get_user_role(client, message.from_user.id)
    if role not in ["CEO", "OWNER"]:
        return await message.reply("<b>❌ Perintah ini hanya untuk CEO!</b>")
    
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    allrole_users = await get_list_from_vars(client.me.id, "ALLROLE_USERS")

    if user.id not in allrole_users:
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> bukan ALLROLE</blockquote>
""")

    try:
        await remove_from_vars(client.me.id, "ALLROLE_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> ALLROLE dihapus</blockquote>
""")
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("getallrole")
async def get_allrole(client, message):
    """Lihat daftar ALLROLE - CEO dan Owner"""
    role = await get_user_role(client, message.from_user.id)
    if role not in ["CEO", "OWNER"]:
        return await message.reply("<b>❌ Perintah ini hanya untuk CEO!</b>")
    
    Sh = await message.reply("sedang memproses...")
    allrole_users = await get_list_from_vars(client.me.id, "ALLROLE_USERS")

    if not allrole_users:
        return await Sh.edit("daftar ALLROLE kosong")

    allrole_list = []
    for user_id in allrole_users:
        try:
            user = await client.get_users(int(user_id))
            allrole_list.append(
                f"<blockquote><b>👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></blockquote></b>"
            )
        except:
            continue

    if allrole_list:
        response = (
            "📋 ᴅᴀғᴛᴀʀ ALLROLE:\n\n"
            + "\n".join(allrole_list)
            + f"\n\n<blockquote>⚜️ total ALLROLE: {len(allrole_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("tidak dapat mengambil daftar ALLROLE")

# ============================================
# MANAJEMEN CEO (OWNER ONLY)
# ============================================

@PY.BOT("addceo")
@PY.OWNER
async def add_ceo(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    ceo_users = await get_list_from_vars(client.me.id, "CEO_USERS")

    if user.id in ceo_users:
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> sudah menjadi CEO</blockquote>
""")

    try:
        await add_to_vars(client.me.id, "CEO_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> CEO</blockquote>
""")
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("unceo")
@PY.OWNER
async def un_ceo(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    ceo_users = await get_list_from_vars(client.me.id, "CEO_USERS")

    if user.id not in ceo_users:
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> bukan CEO</blockquote>
""")

    try:
        await remove_from_vars(client.me.id, "CEO_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> CEO dihapus</blockquote>
""")
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("getceo")
@PY.OWNER
async def get_ceo(client, message):
    Sh = await message.reply("sedang memproses...")
    ceo_users = await get_list_from_vars(client.me.id, "CEO_USERS")

    if not ceo_users:
        return await Sh.edit("daftar CEO kosong")

    ceo_list = []
    for user_id in ceo_users:
        try:
            user = await client.get_users(int(user_id))
            ceo_list.append(
                f"<blockquote><b>👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></blockquote></b>"
            )
        except:
            continue

    if ceo_list:
        response = (
            "📋 ᴅᴀғᴛᴀʀ CEO:\n\n"
            + "\n".join(ceo_list)
            + f"\n\n<blockquote>⚜️ total CEO: {len(ceo_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("tidak dapat mengambil daftar CEO")

# ============================================
# MANAJEMEN TK (CEO & ALLROLE)
# ============================================

@PY.BOT("addtk")
@PY_CEO  # CEO dan ALLROLE bisa akses
async def add_tk(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    tk_users = await get_list_from_vars(client.me.id, "TK_USERS")

    if user.id in tk_users:
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> sudah menjadi TK</blockquote>
""")

    try:
        await add_to_vars(client.me.id, "TK_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> TK</blockquote>
""")
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("untk")
@PY_CEO
async def un_tk(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    tk_users = await get_list_from_vars(client.me.id, "TK_USERS")

    if user.id not in tk_users:
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> bukan TK</blockquote>
""")

    try:
        await remove_from_vars(client.me.id, "TK_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> TK dihapus</blockquote>
""")
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("gettk")
@PY_CEO
async def get_tk(client, message):
    Sh = await message.reply("sedang memproses...")
    tk_users = await get_list_from_vars(client.me.id, "TK_USERS")

    if not tk_users:
        return await Sh.edit("daftar TK kosong")

    tk_list = []
    for user_id in tk_users:
        try:
            user = await client.get_users(int(user_id))
            tk_list.append(
                f"<blockquote><b>👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></blockquote></b>"
            )
        except:
            continue

    if tk_list:
        response = (
            "📋 ᴅᴀғᴛᴀʀ TK:\n\n"
            + "\n".join(tk_list)
            + f"\n\n<blockquote>⚜️ total TK: {len(tk_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("tidak dapat mengambil daftar TK")

# ============================================
# MANAJEMEN ADMIN (CEO, ALLROLE, TK)
# ============================================

@PY.BOT("addadmin")
@PY_TK  # TK, ALLROLE, CEO, OWNER bisa akses
async def add_admin(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if user.id in admin_users:
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> sudah dalam daftar</blockquote>
""")

    try:
        await add_to_vars(client.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> admin</blockquote>
""")
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("unadmin")
@PY_TK
async def un_admin(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if user.id not in admin_users:
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> tidak dalam daftar</blockquote>
""")

    try:
        await remove_from_vars(client.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> unadmin</blockquote>
""")
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("getadmin")
@PY_TK
async def get_admin(client, message):
    Sh = await message.reply("sedang memproses...")
    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if not admin_users:
        return await Sh.edit("daftar admin kosong")

    admin_list = []
    for user_id in admin_users:
        try:
            user = await client.get_users(int(user_id))
            admin_list.append(
                f"<blockquote><b>👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></blockquote></b>"
            )
        except:
            continue

    if admin_list:
        response = (
            "📋 ᴅᴀғᴛᴀʀ admin:\n\n"
            + "\n".join(admin_list)
            + f"\n\n<blockquote>⚜️ total admin: {len(admin_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("tidak dapat mengambil daftar admin")

# ============================================
# MANAJEMEN SELLER (ADMIN, TK, ALLROLE, CEO)
# ============================================

@PY.BOT("addseles")
@PY_ADMIN  # ADMIN, TK, ALLROLE, CEO, OWNER bisa akses
async def add_seles(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    seller_users = await get_list_from_vars(client.me.id, "SELER_USERS")

    if user.id in seller_users:
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> sudah seller</blockquote>
""")

    try:
        await add_to_vars(client.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> seller</blockquote>
""")
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("unseles")
@PY_ADMIN
async def un_seles(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    seller_users = await get_list_from_vars(client.me.id, "SELER_USERS")

    if user.id not in seller_users:
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> bukan seller</blockquote>
""")

    try:
        await remove_from_vars(client.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""
<blockquote><b>💬 INFORMATION</b>
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan:</b> unseller</blockquote>
""")
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("getseles")
@PY_ADMIN
async def get_seles(client, message):
    Sh = await message.reply("sedang memproses...")
    seller_users = await get_list_from_vars(client.me.id, "SELER_USERS")

    if not seller_users:
        return await Sh.edit("daftar seller kosong")

    seller_list = []
    for user_id in seller_users:
        try:
            user = await client.get_users(int(user_id))
            seller_list.append(
                f"<blockquote><b>👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></blockquote></b>"
            )
        except:
            continue

    if seller_list:
        response = (
            "📋 ᴅᴀғᴛᴀʀ seller:\n\n"
            + "\n".join(seller_list)
            + f"\n\n<blockquote>⚜️ total seller: {len(seller_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("tidak dapat mengambil daftar seller")

# ============================================
# MANAJEMEN PREMIUM (SELLER KE ATAS)
# ============================================

@PY.BOT("prem")
@PY_SELLER  # SELLER, ADMIN, TK, ALLROLE, CEO, OWNER bisa akses
async def add_prem(client, message):
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply("memproses...")
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username - bulan</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)
    if not get_bulan:
        get_bulan = 1

    prem_users = await get_list_from_vars(client.me.id, "PREM_USERS")

    if user.id in prem_users:
        return await msg.edit(f"""
<blockquote><b> Name : [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b> Id User :  {user.id}</b>
<b> Ket : Sudah premium</b>
<b> Expired : {get_bulan} Bulan</b></blockquote>
""")

    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        await set_expired_date(user_id, expired)
        await add_to_vars(client.me.id, "PREM_USERS", user.id)
        await msg.edit(f"""
<blockquote><b>⊱ Name : [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>⊱ Id user : {user.id}</b>
<b>⊱ Expired : {get_bulan} bulan</b>
<b>⊱ Silakan @{client.me.username} untuk membuat userbot</blockquote></b>

<blockquote> 「Cara membuat userbot」
1). silakan ( /start ) @ubotekik_bot dulu bot nya
2). tekan tombol ( buat userbot ) 
3). tinggal ikutin aja arahan dari bot nya</blockquote>
<blockquote><b>Note : jangan lupa baca arahan dari bot nya</b></blockquote>
"""
        )
        return await bot.send_message(
            OWNER_ID,
            f"🆔 id-seller: {message.from_user.id}\n\n🆔 id-customer: {user_id}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔱 seller",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "customer ⚜️", callback_data=f"profil {user_id}"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("unprem")
@PY_SELLER
async def un_prem(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    prem_users = await get_list_from_vars(client.me.id, "PREM_USERS")

    if user.id not in prem_users:
        return await msg.edit(f"""
<blockquote><b>name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>id: {user.id}</b>
<b>keterangan: tidak dalam daftar</b></blockquote>
""")
    try:
        await remove_from_vars(client.me.id, "PREM_USERS", user.id)
        await rem_expired_date(user_id)
        return await msg.edit(f"""
<blockquote><b>name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>id: {user.id}</b>
<b>keterangan: unpremium</b></blockquote>
""")
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("getprem")
@PY_SELLER
async def get_prem(client, message):
    text = ""
    count = 0
    prem = await get_list_from_vars(client.me.id, "PREM_USERS")
    prem_users = []

    for user_id in prem:
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"<blockquote><b>{userlist}\n</blockquote></b>"
    if not text:
        await message.reply_text("tidak ada pengguna yang ditemukan")
    else:
        await message.reply_text(text)

# ============================================
# MANAJEMEN SUPER ULTRA (SELLER KE ATAS)
# ============================================

@PY.BOT("superultra")
@PY_SELLER
async def add_superultra(client, message):
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply("memproses...")
    if not user_id:
        return await msg.edit(f"{message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)
    if not get_bulan:
        get_bulan = 1

    ultra_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    if user.id in ultra_users:
        return await msg.edit(f"""
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> {user.id}
<b>keterangan: sudah</b> <code>[SuperUltra]</code>
<b>expired:</b> <code>{get_bulan}</code> <b>bulan</b>
""")

    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        await set_expired_date(user_id, expired)
        await add_to_vars(client.me.id, "ULTRA_PREM", user.id)
        await msg.edit(f"""
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>expired:</b> <code>{get_bulan}</code> <b>bulan</b>
<b>silakan buka</b> @{client.me.mention} <b>untuk membuat userbot</b>
<b>status : </b><code>[SuperUltra]</code>
"""
        )
        return await bot.send_message(
            OWNER_ID,
            f"🆔 id-seller: {message.from_user.id}\n\n🆔 id-customer: {user_id}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔱 seller",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "customer ⚜️", callback_data=f"profil {user_id}"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("rmultra")
@PY_SELLER
async def rm_ultra(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    ultra_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    if user.id not in ultra_users:
        return await msg.edit(f"""
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan: tidak dalam daftar</b>
""")
    try:
        await remove_from_vars(client.me.id, "ULTRA_PREM", user.id)
        await rem_expired_date(user_id)
        return await msg.edit(f"""
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan: none superultra</b>
""")
    except Exception as error:
        return await msg.edit(error)

@PY.BOT("getultra")
@PY_SELLER
async def get_ultra(client, message):
    prem = await get_list_from_vars(client.me.id, "ULTRA_PREM")
    prem_users = []

    for user_id in prem:
        try:
            user = await client.get_users(user_id)
            prem_users.append(
                f"👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | {user.id}"
            )
        except Exception as error:
            return await message.reply(str(error))

    total_prem_users = len(prem_users)
    if prem_users:
        prem_list_text = "\n".join(prem_users)
        return await message.reply(
            f"📋 daftar superultra:\n\n{prem_list_text}\n\n⚜️ total superultra: {total_prem_users}"
        )
    else:
        return await message.reply("tidak ada pengguna superultra saat ini")

# ============================================
# COMMAND UMUM
# ============================================

@PY.BOT("time")
@PY_SELLER
async def time_command(client, message):
    Tm = await message.reply("processing . . .")
    bajingan = message.command
    if len(bajingan) != 3:
        return await Tm.edit(f"woi bang ! \nmohon gunakan /time user_id hari")
    user_id = int(bajingan[1])
    get_day = int(bajingan[2])
    print(user_id , get_day)
    try:
        get_id = (await client.get_users(user_id)).id
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    if not get_day:
        get_day = 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    await set_expired_date(user_id, expire_date)
    await Tm.edit(f"""
<blockquote><b>INFORMATION</b>
<b>name:</b> {user.mention}
<b>id:</b> {get_id}
<b>aktifkan_selama:</b> {get_day} hari</blockquote>
""")

@PY.BOT("cek")
@PY_SELLER
async def cek_command(client, message):
    Sh = await message.reply("processing . . .")
    user_id = await extract_user(message)
    if not user_id:
        return await Sh.edit("pengguna tidak temukan")
    try:
        get_exp = await get_expired_date(user_id)
        sh = await client.get_users(user_id)
    except Exception as error:
        return await Sh.edit(str(error))
    if get_exp is None:
        await Sh.edit(f"""
<blockquote><b>INFORMATION</b>
<b>name:</b> {sh.mention}
<b>plan:</b> none
<b>id:</b> {user_id}
<b>prefix:</b> .
<b>expired:</b> nonaktif</blockquote>
""")
    else:
        SH = await ubot.get_prefix(user_id)
        exp = get_exp.strftime("%d-%m-%Y")
        if user_id in await get_list_from_vars(client.me.id, "ULTRA_PREM"):
            status = "SuperUltra"
        else:
            status = "Premium"
        await Sh.edit(f"""
<blockquote><b>INFORMATION</b>
<b>name:</b> {sh.mention}
<b>plan:</b> {status}
<b>id:</b> {user_id}
<b>prefix:</b> {' '.join(SH)}
<b>expired:</b> {exp}</blockquote>
""")
