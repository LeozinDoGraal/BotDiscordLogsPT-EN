## This bot gonna create a complete log channels structure, organized by categories, to facilitate the monitoring of server activities. It is ideal for servers that want to keep a detailed record of important events, such as member joins and leaves, role changes, channel activities and much more. Just use the command `.criarlogs` and the bot will take care of the rest, creating the necessary categories and channels for efficient management of server logs.
## By leozindotec

import discord
from discord.ext import commands

TOKEN = "YOUR_BOT_TOKEN"

SOURCE_GUILD_ID = 000000000000000000
PING_ROLE_ID = 000000000000000000

LOGS = {

    # MEMBERS
    "member-join": 0,
    "member-leave": 0,
    "member-bans": 0,
    "member-unbans": 0,
    "member-kicks": 0,
    "member-timeouts": 0,
    "nickname-updates": 0,
    "user-updates": 0,
    "avatar-updates": 0,
    "member-roles": 0,
    "voice-updates": 0,

    # ROLES
    "role-created": 0,
    "role-deleted": 0,
    "role-renamed": 0,
    "role-permissions": 0,
    "role-position": 0,
    "role-mention": 0,
    "role-icon": 0,

    # CHANNELS
    "channel-created": 0,
    "channel-deleted": 0,
    "channel-renamed": 0,
    "channel-moved": 0,
    "channel-position": 0,
    "channel-slowmode": 0,
    "channel-permissions": 0,
    "category-created": 0,
    "category-deleted": 0,
    "category-renamed": 0,
    "voice-created": 0,
    "voice-deleted": 0,
    "voice-user-limit": 0,

    # MESSAGES
    "message-deleted": 0,
    "message-edited": 0,
    "messages-cleared": 0,
    "message-pinned": 0,
    "message-unpinned": 0,
    "thread-created": 0,
    "thread-deleted": 0,
    "thread-archived": 0,
    "thread-unarchived": 0,
    "thread-renamed": 0,

    # SERVER
    "server-name": 0,
    "server-icon": 0,
    "server-notifications": 0,
    "rules-channel": 0,

    # BOTS
    "bot-added": 0,
    "bot-removed": 0,
    "integration-created": 0,
    "integration-deleted": 0,
    "integration-updated": 0,

    # SECURITY
    "admin-role-created": 0,
    "admin-role-granted": 0,
    "everyone-channel-opened": 0,
    "dangerous-permissions": 0,
    "mass-bans": 0,
    "mass-kicks": 0,
    "mass-role-deletions": 0,
    "mass-channel-deletions": 0,
    "new-bot-added": 0,
    "everyone-here-ping": 0,
    "staff-role-given": 0,
}

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=".",
    intents=intents
)


def is_source_guild(guild):
    return guild and guild.id == SOURCE_GUILD_ID


async def send_log(
    channel_name,
    title,
    description,
    color=discord.Color.blurple()
):

    channel_id = LOGS.get(channel_name)

    if not channel_id:
        return

    channel = bot.get_channel(channel_id)

    if not channel:
        return

    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )

    embed.timestamp = discord.utils.utcnow()

    await channel.send(
        content=f"<@&{PING_ROLE_ID}>",
        embed=embed,
        allowed_mentions=discord.AllowedMentions(
            roles=True
        )
    )


async def get_audit(guild, action):
    try:
        async for entry in guild.audit_logs(
            limit=1,
            action=action
        ):
            return entry
    except:
        return None

    return None


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# =========================
# MEMBERS
# =========================

@bot.event
async def on_member_join(member):

    if not is_source_guild(member.guild):
        return

    channel = (
        "bot-added"
        if member.bot
        else "member-join"
    )

    await send_log(
        channel,
        "📥 Member Joined",
        f"**User:** {member.mention}\n"
        f"**ID:** `{member.id}`",
        discord.Color.green()
    )

    if member.bot:
        await send_log(
            "new-bot-added",
            "🤖 New Bot Added",
            f"**Bot:** {member.mention}\n"
            f"**ID:** `{member.id}`",
            discord.Color.orange()
        )


@bot.event
async def on_member_remove(member):

    if not is_source_guild(member.guild):
        return

    await send_log(
        "member-leave",
        "📤 Member Left",
        f"**User:** `{member}`\n"
        f"**ID:** `{member.id}`",
        discord.Color.orange()
    )


@bot.event
async def on_member_ban(guild, user):

    if not is_source_guild(guild):
        return

    audit = await get_audit(
        guild,
        discord.AuditLogAction.ban
    )

    author = audit.user if audit else "Unknown"

    await send_log(
        "member-bans",
        "🔨 Member Banned",
        f"**User:** `{user}`\n"
        f"**By:** {author}",
        discord.Color.red()
    )


@bot.event
async def on_member_unban(guild, user):

    if not is_source_guild(guild):
        return

    await send_log(
        "member-unbans",
        "🔓 Member Unbanned",
        f"**User:** `{user}`",
        discord.Color.green()
    )


@bot.event
async def on_member_update(before, after):

    if not is_source_guild(after.guild):
        return

    if before.nick != after.nick:

        await send_log(
            "nickname-updates",
            "✏️ Nickname Updated",
            f"**Member:** {after.mention}\n"
            f"**Before:** `{before.nick}`\n"
            f"**After:** `{after.nick}`",
            discord.Color.blue()
        )

    if before.timed_out_until != after.timed_out_until:

        await send_log(
            "member-timeouts",
            "⏳ Timeout Updated",
            f"**Member:** {after.mention}",
            discord.Color.orange()
        )

    roles_before = set(before.roles)
    roles_after = set(after.roles)

    added_roles = roles_after - roles_before
    removed_roles = roles_before - roles_after

    for role in added_roles:

        await send_log(
            "member-roles",
            "➕ Role Added",
            f"**Member:** {after.mention}\n"
            f"**Role:** {role.mention}",
            discord.Color.green()
        )

        if role.permissions.administrator:

            await send_log(
                "staff-role-given",
                "🚨 Admin Role Given",
                f"**Member:** {after.mention}\n"
                f"**Role:** {role.mention}",
                discord.Color.red()
            )

    for role in removed_roles:

        await send_log(
            "member-roles",
            "➖ Role Removed",
            f"**Member:** {after.mention}\n"
            f"**Role:** {role.mention}",
            discord.Color.red()
        )


# =========================
# USERS
# =========================

@bot.event
async def on_user_update(before, after):

    guild = bot.get_guild(SOURCE_GUILD_ID)

    if not guild:
        return

    member = guild.get_member(after.id)

    if not member:
        return

    if before.name != after.name:

        await send_log(
            "user-updates",
            "👤 Username Updated",
            f"**Before:** `{before.name}`\n"
            f"**After:** `{after.name}`",
            discord.Color.blue()
        )

    if before.avatar != after.avatar:

        await send_log(
            "avatar-updates",
            "🖼️ Avatar Updated",
            f"**User:** {after.mention}",
            discord.Color.blue()
        )


# =========================
# VOICE
# =========================

@bot.event
async def on_voice_state_update(
    member,
    before,
    after
):

    if not is_source_guild(member.guild):
        return

    if before.channel != after.channel:

        await send_log(
            "voice-updates",
            "🔊 Voice Movement",
            f"**Member:** {member.mention}\n"
            f"**Before:** "
            f"{before.channel.mention if before.channel else 'None'}\n"
            f"**After:** "
            f"{after.channel.mention if after.channel else 'None'}",
            discord.Color.blue()
        )


# =========================
# ROLES
# =========================

@bot.event
async def on_guild_role_create(role):

    if not is_source_guild(role.guild):
        return

    await send_log(
        "role-created",
        "➕ Role Created",
        f"**Role:** {role.mention}",
        discord.Color.green()
    )

    if role.permissions.administrator:

        await send_log(
            "admin-role-created",
            "🚨 Admin Role Created",
            f"**Role:** {role.mention}",
            discord.Color.red()
        )


@bot.event
async def on_guild_role_delete(role):

    if not is_source_guild(role.guild):
        return

    await send_log(
        "role-deleted",
        "🗑️ Role Deleted",
        f"**Role:** `{role.name}`",
        discord.Color.red()
    )


@bot.event
async def on_guild_role_update(
    before,
    after
):

    if not is_source_guild(after.guild):
        return

    if before.name != after.name:

        await send_log(
            "role-renamed",
            "✏️ Role Renamed",
            f"**Before:** `{before.name}`\n"
            f"**After:** `{after.name}`",
            discord.Color.blue()
        )

    if before.permissions != after.permissions:

        await send_log(
            "role-permissions",
            "🔐 Role Permissions Updated",
            f"**Role:** {after.mention}",
            discord.Color.orange()
        )

    if before.position != after.position:

        await send_log(
            "role-position",
            "📌 Role Position Updated",
            f"**Role:** {after.mention}",
            discord.Color.blue()
        )

    if before.mentionable != after.mentionable:

        await send_log(
            "role-mention",
            "📢 Role Mention Updated",
            f"**Role:** {after.mention}",
            discord.Color.blue()
        )


# =========================
# CHANNELS
# =========================

@bot.event
async def on_guild_channel_create(channel):

    if not is_source_guild(channel.guild):
        return

    name = "channel-created"

    if isinstance(channel, discord.CategoryChannel):
        name = "category-created"

    elif isinstance(channel, discord.VoiceChannel):
        name = "voice-created"

    await send_log(
        name,
        "➕ Channel Created",
        f"**Channel:** `{channel.name}`",
        discord.Color.green()
    )


@bot.event
async def on_guild_channel_delete(channel):

    if not is_source_guild(channel.guild):
        return

    name = "channel-deleted"

    if isinstance(channel, discord.CategoryChannel):
        name = "category-deleted"

    elif isinstance(channel, discord.VoiceChannel):
        name = "voice-deleted"

    await send_log(
        name,
        "🗑️ Channel Deleted",
        f"**Channel:** `{channel.name}`",
        discord.Color.red()
    )


@bot.event
async def on_guild_channel_update(
    before,
    after
):

    if not is_source_guild(after.guild):
        return

    if before.name != after.name:

        name = "channel-renamed"

        if isinstance(
            after,
            discord.CategoryChannel
        ):
            name = "category-renamed"

        await send_log(
            name,
            "✏️ Channel Renamed",
            f"**Before:** `{before.name}`\n"
            f"**After:** `{after.name}`",
            discord.Color.blue()
        )

    if before.position != after.position:

        await send_log(
            "channel-position",
            "📌 Channel Position Updated",
            f"**Channel:** {after.mention}",
            discord.Color.blue()
        )

    if hasattr(before, "slowmode_delay"):

        if before.slowmode_delay != after.slowmode_delay:

            await send_log(
                "channel-slowmode",
                "🐢 Slowmode Updated",
                f"**Channel:** {after.mention}",
                discord.Color.orange()
            )

    if before.overwrites != after.overwrites:

        await send_log(
            "channel-permissions",
            "🔐 Channel Permissions Updated",
            f"**Channel:** {after.mention}",
            discord.Color.orange()
        )

    if isinstance(after, discord.VoiceChannel):

        if before.user_limit != after.user_limit:

            await send_log(
                "voice-user-limit",
                "👥 Voice User Limit Updated",
                f"**Channel:** {after.mention}\n"
                f"**Before:** `{before.user_limit}`\n"
                f"**After:** `{after.user_limit}`",
                discord.Color.blue()
            )


# =========================
# MESSAGES
# =========================

@bot.event
async def on_message_delete(message):

    if not message.guild:
        return

    if not is_source_guild(message.guild):
        return

    if message.author.bot:
        return

    await send_log(
        "message-deleted",
        "🗑️ Message Deleted",
        f"**Author:** {message.author.mention}\n"
        f"**Channel:** {message.channel.mention}\n\n"
        f"```"
        f"{message.content[:1500] if message.content else 'No content'}"
        f"```",
        discord.Color.red()
    )


@bot.event
async def on_message_edit(
    before,
    after
):

    if not before.guild:
        return

    if not is_source_guild(before.guild):
        return

    if before.author.bot:
        return

    if before.content == after.content:
        return

    await send_log(
        "message-edited",
        "✏️ Message Edited",
        f"**Author:** {before.author.mention}\n"
        f"**Channel:** {before.channel.mention}\n\n"
        f"**Before:**\n```{before.content[:800]}```\n"
        f"**After:**\n```{after.content[:800]}```",
        discord.Color.blue()
    )


@bot.event
async def on_bulk_message_delete(messages):

    if not messages:
        return

    guild = messages[0].guild

    if not is_source_guild(guild):
        return

    await send_log(
        "messages-cleared",
        "🧹 Messages Cleared",
        f"**Amount:** `{len(messages)}`",
        discord.Color.red()
    )


# =========================
# THREADS
# =========================

@bot.event
async def on_thread_create(thread):

    if not is_source_guild(thread.guild):
        return

    await send_log(
        "thread-created",
        "🧵 Thread Created",
        f"**Thread:** `{thread.name}`",
        discord.Color.green()
    )


@bot.event
async def on_thread_delete(thread):

    if not is_source_guild(thread.guild):
        return

    await send_log(
        "thread-deleted",
        "🗑️ Thread Deleted",
        f"**Thread:** `{thread.name}`",
        discord.Color.red()
    )


@bot.event
async def on_thread_update(
    before,
    after
):

    if not is_source_guild(after.guild):
        return

    if before.archived != after.archived:

        channel = (
            "thread-archived"
            if after.archived
            else "thread-unarchived"
        )

        await send_log(
            channel,
            "🧵 Thread Status Updated",
            f"**Thread:** `{after.name}`",
            discord.Color.orange()
        )

    if before.name != after.name:

        await send_log(
            "thread-renamed",
            "✏️ Thread Renamed",
            f"**Before:** `{before.name}`\n"
            f"**After:** `{after.name}`",
            discord.Color.blue()
        )


# =========================
# SERVER
# =========================

@bot.event
async def on_guild_update(
    before,
    after
):

    if not is_source_guild(after):
        return

    if before.name != after.name:

        await send_log(
            "server-name",
            "✏️ Server Name Updated",
            f"**Before:** `{before.name}`\n"
            f"**After:** `{after.name}`",
            discord.Color.blue()
        )

    if before.icon != after.icon:

        await send_log(
            "server-icon",
            "🖼️ Server Icon Updated",
            f"**Server:** `{after.name}`",
            discord.Color.blue()
        )

    if (
        before.default_notifications
        != after.default_notifications
    ):

        await send_log(
            "server-notifications",
            "🔔 Notifications Updated",
            f"**Server:** `{after.name}`",
            discord.Color.orange()
        )

    if before.rules_channel != after.rules_channel:

        await send_log(
            "rules-channel",
            "📜 Rules Channel Updated",
            f"**Server:** `{after.name}`",
            discord.Color.orange()
        )


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if (
        "@everyone" in message.content
        or "@here" in message.content
    ):

        await send_log(
            "everyone-here-ping",
            "🚨 Everyone/Here Ping",
            f"**Author:** {message.author.mention}\n"
            f"**Channel:** {message.channel.mention}",
            discord.Color.red()
        )

    await bot.process_commands(message)


bot.run(TOKEN)