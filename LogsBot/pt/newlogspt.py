
## Esse bot vai criar uma estrutura de canais de logs completa, organizada por categorias, para facilitar o monitoramento das atividades do servidor. Ele é ideal para servidores que desejam manter um registro detalhado de eventos importantes, como entradas e saídas de membros, alterações de cargos, atividades em canais e muito mais. Basta usar o comando `.criarlogs` e o bot cuidará do resto, criando as categorias e canais necessários para uma gestão eficiente dos logs do servidor.
## By leozindotec


import discord
from discord.ext import commands

TOKEN = "Token do seu bot aqui"

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=".",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"✅ Bot online: {bot.user}")


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
            "cargo-cor",
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
        "✅ Todos os canais de logs foram criados com sucesso!"
    )


bot.run("Coloca o token do seu bot aqui")  