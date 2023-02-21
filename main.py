from telethon import TelegramClient, events
import replicate

API_ID = "25301791"
API_HASH = "8026659a7682925e989360a85035396c"
BOT_TOKEN = "6269227625:AAHu1ZR0Na8fD9L3puZrHX-sfiOlsZwkyHM"
imagebot = TelegramClient('imagebot', api_id=API_ID, api_hash=API_HASH)


@imagebot.on(events.NewMessage(pattern="^[?!/]start"))
async def _(event):
    welcome_message = "Hi! Welcome to AI POP bot. Send me a photo and I'll generate a description for you. Type 'help' if you need assistance. Let's get started!"
    await event.reply(welcome_message)
    
@imagebot.on(events.NewMessage(pattern="^[?!/]help"))
async def _(event):
    help_message = "Hi! I'm here to help you with bot.\n\nTo get started, simply send me a photo and I'll generate a description for you.\n\nIf you need additional assistance, you can check out our guide at this link: https://docs.ai-pop.com/guides/ai-pop-bot-use\n\nIf you have any questions or need further assistance, feel free to ask in chat!"
    await event.reply(help_message)
    
@imagebot.on(events.NewMessage(incoming=True))
async def _(event):
    if event.text.startswith("/"):
        return
    if not event.media:
        await event.reply("```Don't send Just text please.Please send A Image.```")
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
    result = output.get('caption')
    result = result.replace("Caption: ","")
    await event.reply(result)

imagebot.start(bot_token=BOT_TOKEN)
imagebot.run_until_disconnected()
