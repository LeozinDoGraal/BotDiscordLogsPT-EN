## this bot will create the channels, after that put the code of newlogspt.
## By leozindotec

import discord
from discord.ext import commands

TOKEN = "YOUR_BOT_TOKEN"

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=".",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command(name="createlogs")
@commands.has_permissions(administrator=True)
async def create_logs(ctx):

    guild = ctx.guild

    categories = {

        "📁 LOGS | MEMBERS": [
            "member-join",
            "member-leave",
            "member-bans",
            "member-unbans",
            "member-kicks",
            "member-timeouts",
            "nickname-updates",
            "user-updates",
            "avatar-updates",
            "member-roles",
            "voice-updates"
        ],

        "📁 LOGS | ROLES": [
            "role-created",
            "role-deleted",
            "role-renamed",
            "role-permissions",
            "role-position",
            "role-mention",
            "role-icon"
        ],

        "📁 LOGS | CHANNELS": [
            "channel-created",
            "channel-deleted",
            "channel-renamed",
            "channel-moved",
            "channel-position",
            "channel-slowmode",
            "channel-permissions",
            "category-created",
            "category-deleted",
            "category-renamed",
            "voice-created",
            "voice-deleted",
            "voice-user-limit"
        ],

        "📁 LOGS | MESSAGES": [
            "message-deleted",
            "message-edited",
            "messages-cleared",
            "message-pinned",
            "message-unpinned",
            "thread-created",
            "thread-deleted",
            "thread-archived",
            "thread-unarchived",
            "thread-renamed"
        ],

        "📁 LOGS | SERVER": [
            "server-name",
            "server-icon",
            "server-notifications",
            "rules-channel"
        ],

        "📁 LOGS | BOTS": [
            "bot-added",
            "bot-removed",
            "integration-created",
            "integration-deleted",
            "integration-updated"
        ],

        "📁 LOGS | SECURITY": [
            "admin-role-created",
            "admin-role-granted",
            "everyone-channel-opened",
            "dangerous-permissions",
            "mass-bans",
            "mass-kicks",
            "mass-role-deletions",
            "mass-channel-deletions",
            "new-bot-added",
            "everyone-here-ping",
            "staff-role-given"
        ]
    }

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(
            view_channel=False
        ),

        guild.me: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            manage_channels=True
        )
    }

    await ctx.send("Creating log channels...")

    for category_name, channels in categories.items():

        category = await guild.create_category(
            name=category_name,
            overwrites=overwrites
        )

        for channel_name in channels:

            await guild.create_text_channel(
                name=channel_name,
                category=category,
                overwrites=overwrites
            )

    await ctx.send("All log channels created successfully!")


bot.run(TOKEN)  