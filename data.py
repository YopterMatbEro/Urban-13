from aiogram import Bot
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
bot = Bot(token=config['telegram']['token'])
