from telethon import TelegramClient, events
import replicate

API_ID = "25301791"
API_HASH = "8026659a7682925e989360a85035396c"
BOT_TOKEN = "6248093145:AAEjbFKh9LkCLekaYlEgrZh69QM4_c9loZw"
imagebot = TelegramClient('imagebot', api_id=API_ID, api_hash=API_HASH)

@imagebot.on(events.NewMessage(pattern="^[?!/]image"))
async def _(event):
    title = ''.join(event.text[7:].split())
    if not title:
        await event.reply("Please give me a query.")
        return
    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1")
    inputs = {
        'prompt': f"{title}",
        'width': 768,
        'height': 768,
        'prompt_strength': 0.8,
        'num_outputs': 1,
        'num_inference_steps': 50,
        'guidance_scale': 7.5,
        'scheduler': "DPMSolverMultistep"
    }
    output = version.predict(**inputs)
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
