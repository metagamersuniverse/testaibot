import os
import telegram
import replicae
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

model = replicae.models.get("salesforce/blip")
version = model.versions.get("2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746")

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, I'm a Telegram bot powered by the BLIP model.")

def image_captioning(update, context):
    photo = context.bot.getFile(update.message.photo[-1].file_id)
    photo.download("image.jpg")
    with open("image.jpg", "rb") as image:
        inputs = {
            'image': image,
            'task': "image_captioning",
        }
        output = version.predict(**inputs)
        context.bot.send_message(chat_id=update.effective_chat.id, text=output["caption"])

def main():
    TELEGRAM_TOKEN = os.environ["5903455401:AAH0z6XK3NCzyC3LvoAaPXzsC6r9RpjXXCw"]
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, image_captioning))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
