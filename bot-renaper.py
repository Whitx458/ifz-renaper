import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)


TOKEN="" #agregar token

def formato_dato(dato):
    if dato is None or dato == []:
        return "Sin datos"
    return dato

print("""
      
                                        ██╗███████╗███████╗    ██████╗ ███████╗███╗   ██╗ █████╗ ██████╗ ███████╗██████╗ 
                                        ██║██╔════╝╚══███╔╝    ██╔══██╗██╔════╝████╗  ██║██╔══██╗██╔══██╗██╔════╝██╔══██╗
                                        ██║█████╗    ███╔╝     ██████╔╝█████╗  ██╔██╗ ██║███████║██████╔╝█████╗  ██████╔╝
                                        ██║██╔══╝   ███╔╝      ██╔══██╗██╔══╝  ██║╚██╗██║██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
                                        ██║██║     ███████╗    ██║  ██║███████╗██║ ╚████║██║  ██║██║     ███████╗██║  ██║
                                        ╚═╝╚═╝     ╚══════╝    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                                               
      """)


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📘 Comandos disponibles",
        description="Lista de comandos del bot RENAPER:",
        color=0x00b0f4
    )
    
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1335699823839543296/0f76cd407d3dc6beae2a9222cad308eb.png?size=512")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1326639302167367731/1358265204735082627/d309d610ff201301777a54a28c6a9283.png?ex=67f3368c&is=67f1e50c&hm=75a7d27a40a47eea386d1c3f3a17736d1d2c24f52f0b2a935f042fd569448918&")  
    embed.set_footer(text="Bot desarrollado por Inferzsquad 😎"),

    embed.add_field(
        name=".dni [DNI]",
        value="🔍 Muestra información personal básica del ciudadano.",
        inline=False
    )

    embed.add_field(
        name=".banco [DNI]",
        value="💰 Muestra información financiera del ciudadano, como deudas, cheques y afectaciones.",
        inline=False
    )

    embed.add_field(
        name=".propiedades [DNI]",
        value="🏠 Muestra las propiedades registradas del ciudadano.",
        inline=False
    )

    embed.add_field(
        name=".infoempleos [DNI]",
        value="🧾 Muestra la información laboral y empleadores del ciudadano.",
        inline=False
    )

    await ctx.send(embed=embed)

@bot.command()
async def dni(ctx, numero_dni):
    api = f"http://127.0.0.1:5000/api/ricardo/{numero_dni}"
    
    try:
        r = requests.get(api)
        data = r.json()
        
        padron = data.get("data", {}).get("padron", [])
        
        if not padron:
            await ctx.send("❌ No se encontraron datos de este ciudadano. Verifique el DNI.")
            return
        
        persona = padron[0]
        
        nombre = persona.get("nombre", "No disponible")
        documento = persona.get("documento", "No disponible")
        clase = persona.get("clase", "No disponible")
        domicilio = persona.get("domicilio", "No disponible")
        localidad = persona.get("localidad", "No disponible")
        profesion = persona.get("profesion", "No disponible")
        provincia = persona.get("provincia", "No disponible")
        sexo = persona.get("sexo", "No disponible")
        
        embed = discord.Embed(
            title=f"Informacion del DNI: {numero_dni}",
            color=0x00b0f4
        )
        
        embed.add_field(name="Nombre: ", value=formato_dato(nombre), inline=False)
        embed.add_field(name="Documento: ", value=formato_dato(documento), inline=False)
        embed.add_field(name="Sexo: ", value=formato_dato(sexo), inline=False)
        embed.add_field(name="Clase: ", value=formato_dato(clase), inline=False)
        embed.add_field(name="Provincia: ", value=formato_dato(provincia), inline=False)
        embed.add_field(name="Localidad: ", value=formato_dato(localidad), inline=False)
        embed.add_field(name="Domicilio: ", value=formato_dato(domicilio), inline=False)
        embed.add_field(name="Profesion: ", value=formato_dato(profesion), inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1326639302167367731/1358265204735082627/d309d610ff201301777a54a28c6a9283.png?ex=67f3368c&is=67f1e50c&hm=75a7d27a40a47eea386d1c3f3a17736d1d2c24f52f0b2a935f042fd569448918&")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1335699823839543296/0f76cd407d3dc6beae2a9222cad308eb.png?size=512")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send("❌ Error al consultar la API.")
        print("Error:", e)
        

@bot.command()
async def banco(ctx, numero_dni):
    api = f"http://127.0.0.1:5000/api/ricardo/{numero_dni}"
    
    try:
        r = requests.get(api)
        data = r.json()
        
        bcra = data.get("data", {}).get("bcra", {})
        deudas = bcra.get("deudas", []) 
        actualizacion = bcra.get("actualizacion", "No disponible")
        bcraActualizacionCheques = data.get("data", {}).get("bcraActualizacionCheques", "No disponible")  # ojo con el nombre (termina en 's')
        bcraResumenCheques = data.get("data", {}).get("bcraResumenCheques", "No disponible")
        datosPersonales = data.get("data", {}).get("datosPersonales", [])
        afectaciones = data.get("data", {}).get("afectaciones", [])
        afectacionesJudiciales = data.get("data", {}).get("afectacionesJudiciales", [])
        afectacionesQuiebras = data.get("data", {}).get("afectacionesQuiebras", [])
        lastLoaded = data.get("data", {}).get("lastLoaded", {})
        cargaMoras = lastLoaded.get("cargaMoras", "No disponible")
        inscripcionAfip = data.get("data", {}).get("lastLoaded", {}).get("inscripcionAfip", "No disponible")

        embed=discord.Embed(
            title=f"Informacion bancaria del DNI: {numero_dni}",
            color=0x00b0f4
        )
        
        embed.add_field(name="Actualizacion BCRA: ", value=formato_dato(actualizacion), inline=False)
        embed.add_field(name="Deudas: ", value=formato_dato(deudas), inline=False)
        embed.add_field(name="Actualizacion de cheques: ", value=formato_dato(bcraActualizacionCheques), inline=False)
        embed.add_field(name="Resumen de cheques: ", value=formato_dato(bcraResumenCheques), inline=False)
        embed.add_field(name="Datos personales: ", value=formato_dato(datosPersonales), inline=False)
        embed.add_field(name="Problemas financieros o administrativos: ", value=formato_dato(afectaciones), inline=False)
        embed.add_field(name="Problemas judiciales: ", value=formato_dato(afectacionesJudiciales), inline=False)
        embed.add_field(name="Quiebras: ", value=formato_dato(afectacionesQuiebras), inline=False)
        embed.add_field(name="Ultima carga de moras: ", value=formato_dato(cargaMoras), inline=False)
        embed.add_field(name="inscripcionAfip: ", value=formato_dato(inscripcionAfip), inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1326639302167367731/1358265204735082627/d309d610ff201301777a54a28c6a9283.png?ex=67f3368c&is=67f1e50c&hm=75a7d27a40a47eea386d1c3f3a17736d1d2c24f52f0b2a935f042fd569448918&")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1335699823839543296/0f76cd407d3dc6beae2a9222cad308eb.png?size=512")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send("a ocurrido un error con la informacion del ciudadano.")
        print("Error:", e)
        
@bot.command()
async def propiedades(ctx, numero_dni):
    api = f"http://127.0.0.1:5000/api/ricardo/{numero_dni}"
    
    try:
        r = requests.get(api)
        data = r.json()  
        
        propiedades = data.get("data", {}).get("propiedades", [])
        padron = data.get("data", {}).get("padron", [])
        
        embed=discord.Embed(
            title=f"Propiedades del DNI: {numero_dni}",
            color=0x00b0f4
        )
        
        embed.add_field(name="Propiedades: ", value=formato_dato(propiedades), inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1326639302167367731/1358265204735082627/d309d610ff201301777a54a28c6a9283.png?ex=67f3368c&is=67f1e50c&hm=75a7d27a40a47eea386d1c3f3a17736d1d2c24f52f0b2a935f042fd569448918&")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1335699823839543296/0f76cd407d3dc6beae2a9222cad308eb.png?size=512")
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send("ocurrio un error a buscar las propiedades del sujeto")
        print(f"error {e}")
        
@bot.command()
async def infoempleos(ctx, numero_dni):
    api = f"http://127.0.0.1:5000/api/ricardo/{numero_dni}"
    
    try:
        r = requests.get(api)
        data = r.json()
        
        empleador = data.get("data", {}).get("refEmpleadores", "No disponible")
        laborales = data.get("data", {}).get("refLaborales", [])
        
        embed=discord.Embed(
            title=f"Informacion de trabajo del dni: {numero_dni}",
            color=0x00b0f4
        )
        
        embed.add_field(name="empleador: ", value=formato_dato(empleador), inline=False)
        embed.add_field(name="laborales: ", value=formato_dato(laborales), inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1326639302167367731/1358265204735082627/d309d610ff201301777a54a28c6a9283.png?ex=67f3368c&is=67f1e50c&hm=75a7d27a40a47eea386d1c3f3a17736d1d2c24f52f0b2a935f042fd569448918&")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1335699823839543296/0f76cd407d3dc6beae2a9222cad308eb.png?size=512")
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send("ocurrio un error al buscar informacion de empleo del ciudadano")
        print(f"error {e}")
bot.run(TOKEN)
