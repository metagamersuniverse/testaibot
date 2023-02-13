from telethon import TelegramClient, events
import replicate

API_ID = "25301791"
API_HASH = "8026659a7682925e989360a85035396c"
BOT_TOKEN = "6139635960:AAFEW4SQvo5s_g9HyqyCC7cw2qVpdqm96-c"
imagebot = TelegramClient('imagebot', api_id=API_ID, api_hash=API_HASH)

@imagebot.on(events.NewMessage(pattern="^[?!/]image"))
async def _(event):
    title = ' '.join(event.text[7:])
    if not title:
        await event.reply("Please Give Meh A Query.")
        return
    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478")
    output = version.predict(prompt=f"{title}")
    await event.client.send_file(event.chat_id, output, caption=None)
    
@imagebot.on(events.NewMessage(pattern="^[?!/]start"))
async def _(event):
    welcome_message = "Hi! Welcome to AI POP. Send me a photo and I'll generate a description for you. Type 'help' if you need assistance. Let's get started!"
    await event.reply(welcome_message)

@imagebot.on(events.NewMessage(incoming=True))
async def _(event):
    if event.text.startswith("/"):
        return
    if not event.media:
        await event.reply("```Don't send Just text please.Please send A Sticker / Image.```")
        return
    file = await event.client.download_media(event.media)
    model = replicate.models.get("salesforce/blip")
    version = model.versions.get("2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746")
    inputs = {
        'image': open(file, "rb"),
        'task': "image_captioning",
    }
    output = version.predict(**inputs)
    await event.reply(output)

imagebot.start(bot_token=BOT_TOKEN)
imagebot.run_until_disconnected()
