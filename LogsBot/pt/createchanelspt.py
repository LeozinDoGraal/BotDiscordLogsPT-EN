## esse bot vai criar os canais, depois disso coloque o codigo do newlogspt. 
## By leozindotec

import discord
from discord.ext import commands

TOKEN = "SEU_TOKEN_AQUI"

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=".",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"✅ Online como {bot.user}")


@bot.command(name="criarlogs")
@commands.has_permissions(administrator=True)
async def criar_logs(ctx):

    guild = ctx.guild

    categorias = {

        "📁 LOGS | MEMBROS": [
            "entrada-membros",
            "saida-membros",
            "banimentos",
            "desbanimentos",
            "expulsoes",
            "timeouts",
            "nicknames",
            "usuarios",
            "avatares",
            "cargos-membros",
            "voz-membros"
        ],

        "📁 LOGS | CARGOS": [
            "cargo-criado",
            "cargo-deletado",
            "cargo-renomeado",
            "cargo-permissoes",
            "cargo-posicao",
            "cargo-mencao",
            "cargo-icone"
        ],

        "📁 LOGS | CANAIS": [
            "canal-criado",
            "canal-deletado",
            "canal-renomeado",
            "canal-movido",
            "canal-posicao",
            "canal-slowmode",
            "canal-permissoes",
            "categoria-criada",
            "categoria-deletada",
            "categoria-renomeada",
            "voz-criada",
            "voz-deletada",
            "limite-usuarios-voz"
        ],

        "📁 LOGS | MENSAGENS": [
            "mensagem-deletada",
            "mensagem-editada",
            "mensagens-limpas",
            "mensagem-fixada",
            "mensagem-desfixada",
            "thread-criada",
            "thread-deletada",
            "thread-arquivada",
            "thread-desarquivada",
            "thread-renomeada"
        ],

        "📁 LOGS | SERVIDOR": [
            "nome-servidor",
            "icone-servidor",
            "notificacoes-servidor",
            "canal-regras"
        ],

        "📁 LOGS | BOTS": [
            "bot-adicionado",
            "bot-removido",
            "integracao-criada",
            "integracao-deletada",
            "integracao-atualizada"
        ],

        "📁 LOGS | SEGURANÇA": [
            "cargo-admin-criado",
            "cargo-ganhou-admin",
            "canal-liberado-everyone",
            "permissao-perigosa",
            "muitos-bans",
            "muitos-kicks",
            "muitos-cargos-deletados",
            "muitos-canais-deletados",
            "bot-novo-adicionado",
            "everyone-here-massa",
            "cargo-staff-dado"
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

    await ctx.send("⏳ Criando canais de logs...")

    for nome_categoria, canais in categorias.items():

        categoria = await guild.create_category(
            name=nome_categoria,
            overwrites=overwrites
        )

        for nome_canal in canais:

            await guild.create_text_channel(
                name=nome_canal,
                category=categoria,
                overwrites=overwrites
            )

    await ctx.send(
        "✅ Todos os canais de logs foram criados!"
    )


bot.run(TOKEN)