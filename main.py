from telethon import TelegramClient, events
import replicate

API_ID = "25301791"
API_HASH = "8026659a7682925e989360a85035396c"
BOT_TOKEN = "6248093145:AAEjbFKh9LkCLekaYlEgrZh69QM4_c9loZw"
imagebot = TelegramClient('imagebot', api_id=API_ID, api_hash=API_HASH)

@imagebot.on(events.NewMessage(pattern="^[?!/]image"))
async def _(event):
    title = ' '.join(event.text[7:])
    if not title:
        await event.reply("Please Give Meh A Query.")
        return
    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("de37751f75135f7ebbe62548e27d6740d5155dfefdf6447db35c9865253d7e06")
    output = version.predict(prompt=f"{title}")
    await event.client.send_file(event.chat_id, output, caption=None)
    

@imagebot.on(events.NewMessage(pattern="^[?!/]start"))
async def _(event):
    welcome_message = "Hi! Welcome to bot. Send me a photo and I'll generate a description for you. Type 'help' if you need assistance. Let's get started!"
    await event.reply(welcome_message)
    
@imagebot.on(events.NewMessage(pattern="^[?!/]help"))
async def _(event):
    help_message = "Hi! I'm here to help you with bot.\n\nTo get started, simply send me a photo and I'll generate a description for you.\n\nIf you need additional assistance, you can check out our guide at this link: https://google.com\n\nIf you have any questions or need further assistance, feel free to ask!"
    await event.reply(help_message)
    
@imagebot.on(events.NewMessage(incoming=True))
async def _(event):
    if event.text.startswith("/"):
        return
    if not event.media:
        await event.reply("```Don't send Just text please.Please send A Sticker / Image.```")
        return
    file = await event.client.download_media(event.media)
    model = replicate.models.get("j-min/clip-caption-reward")
    version = model.versions.get("de37751f75135f7ebbe62548e27d6740d5155dfefdf6447db35c9865253d7e06")
    inputs = {
        'image': open(file, "rb"),
        'task': "image_captioning",
    }
    output = version.predict(**inputs)
    await event.reply(output)

imagebot.start(bot_token=BOT_TOKEN)
imagebot.run_until_disconnected()
