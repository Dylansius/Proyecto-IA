import discord
from discord.ext import commands
import datetime
import pytz
import random

# Configura los intents para el bot
intents = discord.Intents.default()
intents.messages = True  # Activa el manejo de eventos de mensajes

# Configura el prefijo del bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Lista de chistes
chistes = [
    "¿Cómo se despiden los químicos? Ácido un placer.",
    "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.",
    "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
    "¿Cuál es el café más peligroso del mundo? ¡El ex-preso!",
    "¿Cómo se llama un cinturón con un reloj incorporado? ¡Una correa de tiempo!",
    "¿Qué hace una impresora en una fiesta? ¡Imprimiendo buen ambiente!",
    "¿Cómo le dice un jardinero a otro? ¡Nos vemos cuando podamos!",
]

# Variable para almacenar el número a adivinar
numero_adivinar = None

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.command(name='fecha_hora')
async def obtener_fecha_hora(ctx):
    # Obtiene la fecha y hora actual en UTC
    fecha_hora_utc = datetime.datetime.utcnow()

    # Convierte la fecha y hora UTC a la zona horaria de Guadalajara
    tz_guadalajara = pytz.timezone('America/Mexico_City')
    fecha_hora_guadalajara = fecha_hora_utc.replace(tzinfo=pytz.utc).astimezone(tz_guadalajara)

    # Formatea la fecha y hora actual en la zona horaria de Guadalajara
    fecha_hora_actual = fecha_hora_guadalajara.strftime('%Y-%m-%d %I:%M %p')

    # Envía la fecha y hora actual al canal donde se ejecutó el comando con separación de líneas
    await ctx.send(f'La fecha y hora actual en Guadalajara, Jalisco es:\n{fecha_hora_actual}')

@bot.command(name='chiste')
async def contar_chiste(ctx):
    # Mezcla la lista de chistes
    random.shuffle(chistes)
    # Selecciona el primer chiste después de mezclar
    chiste_aleatorio = chistes[0]
    await ctx.send(chiste_aleatorio)

@bot.command(name='saludo')
async def saludar(ctx):
    await ctx.send(f'Hola, {ctx.author.mention}!')

@bot.command(name='info_servidor')
async def info_servidor(ctx):
    servidor = ctx.guild
    await ctx.send(f'Servidor: {servidor.name}\nID: {servidor.id}\nMiembros: {servidor.member_count}')

@bot.command(name='info_usuario')
async def info_usuario(ctx, miembro: discord.Member = None):
    # Si no se proporciona un miembro, se toma el autor del mensaje como el miembro
    if miembro is None:
        miembro = ctx.author

    # Obtiene información del miembro
    nombre = miembro.name
    apodo = miembro.nick
    id_usuario = miembro.id
    fecha_ingreso = miembro.joined_at.strftime('%Y-%m-%d %I:%M %p')
    fecha_creacion = miembro.created_at.strftime('%Y-%m-%d %I:%M %p')

    # Muestra la información del usuario en el canal donde se ejecutó el comando
    await ctx.send(f'Información de {nombre}:\n'
                   f'ID: {id_usuario}\n'
                   f'Apodo: {apodo}\n'
                   f'Fecha de Ingreso al Servidor: {fecha_ingreso}\n'
                   f'Fecha de Creación de la Cuenta: {fecha_creacion}')

@bot.command(name='ayuda')
async def mostrar_ayuda_personalizada(ctx):
    embed = discord.Embed(title="¡Bienvenido a Mi Bot!", description="Aquí tienes una lista de comandos disponibles:")
    embed.add_field(name="!fecha_hora", value="Obtiene la fecha y hora actual en Guadalajara, Jalisco.")
    embed.add_field(name="!chiste", value="Cuenta un chiste aleatorio.")
    embed.add_field(name="!saludo", value="Saluda al usuario que ejecuta el comando.")
    embed.add_field(name="!info_servidor", value="Proporciona información sobre el servidor.")
    embed.add_field(name="!info_usuario [usuario]", value="Proporciona información sobre un usuario (o sobre ti mismo).")
    embed.add_field(name="!dado", value="Lanza un dado de seis caras.")
    embed.add_field(name="!adivina", value="Inicia un juego de adivinanzas.")
    embed.add_field(name="!intento [número]", value="Intenta adivinar el número en el juego de adivinanzas.")
    embed.set_footer(text="¡Diviértete con el bot!")

    await ctx.send(embed=embed)

@bot.command(name='dado')
async def lanzar_dado(ctx):
    resultado = random.randint(1, 6)  # Número aleatorio entre 1 y 6
    await ctx.send(f'{ctx.author.mention} lanzó un dado y obtuvo: {resultado}')

@bot.command(name='adivina')
async def iniciar_adivinanza(ctx):
    global numero_adivinar
    # Inicia un nuevo juego generando un número aleatorio entre 1 y 100
    numero_adivinar = random.randint(1, 100)
    await ctx.send(f'He pensado en un número entre 1 y 100. ¡Adivina cuál es!')

@bot.command(name='intento')
async def intentar_adivinanza(ctx, intento: int):
    global numero_adivinar
    # Verifica si el número adivinado es correcto
    if numero_adivinar is None:
        await ctx.send('Debes iniciar un juego con `!adivina` antes de intentar adivinar.')
    elif intento == numero_adivinar:
        await ctx.send(f'¡Felicidades, {ctx.author.mention}! Has adivinado el número.')
        numero_adivinar = None  # Reinicia la variable para un nuevo juego
    elif intento < numero_adivinar:
        await ctx.send('Demasiado bajo. ¡Inténtalo de nuevo!')
    else:
        await ctx.send('Demasiado alto. ¡Inténtalo de nuevo!')

@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Latencia del bot en milisegundos
    await ctx.send(f'Pong! Latencia: {latency}ms')

# Token de tu bot de Discord
TOKEN = 'MTE3ODM3NTMzNjM3NTg5ODE0Mw.GldyPc.oQBQuWTQkXnrF7ft0coT77FxsAMu-OMS05OS8Q'

# Conecta el bot al servidor de Discord
bot.run(TOKEN)