import logging
import random
import sys
import os
import config
import radarcheck
from PIL import Image
import cv2

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

if config.MODE == "dev":
    def run(updater):
        updater.start_polling()
elif config.MODE == "prod":
    def run(updater):
        updater.start_webhook(listen="0.0.0.0",
                              port=config.PORT,
                              url_path=config.TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(config.HEROKU_APP_NAME, config.TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def start_handler(bot, update):
    logger.info("User {} started bot".format(update.effective_user["id"]))
    update.message.reply_text("Search 'ukbb radar' images in google and send me snapshots of the radar. I will read from image and tell you the direction and speed of the wind")


def random_handler(bot, update):
    number = random.randint(0, 10)
    logger.info("User {} randomed number {}".format(update.effective_user["id"], number))
    update.message.reply_text("Random number: {}".format(number))


def wind_direction_handler(bot, update):
    image = radarcheck.UrlToImage(radarcheck.radar_image_url)
    wind_dir = radarcheck.GetWindDirection(image)
    logger.info("User {} wind direction {}".format(update.effective_user["id"], wind_dir))
    update.message.reply_text(wind_dir);


def photo_handler(bot, update):
    telegram_file = update.message.photo[-1]
    logger.info("User {} sent photo".format(update.effective_user["id"]))
    if telegram_file.width == 654 and telegram_file.height == 479:
        url = telegram_file.get_file().file_path
        img = radarcheck.UrlToImage(url)
        wind_dir = radarcheck.GetWindDirection(img)
        wind_speed = radarcheck.GetWindSpeed(img)
        reply = "{}\n{}".format(wind_dir, wind_speed)
        update.message.reply_text(reply)
    else:
        update.message.reply_text("Expected image size is 654x479")
        logger.info("Unexpected photo size: {} x {}".format(telegram_file.width, telegram_file.height))

if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(config.TOKEN)

    updater.dispatcher.add_handler(CommandHandler("wind_direction", wind_direction_handler))
    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("random", random_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))

    run(updater)
