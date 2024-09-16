import telebot
import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATA_BASE_API = os.getenv("NOTION_TASK_DB")
notion = Client(auth=NOTION_TOKEN)
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        """\
Hello, I'm a bot that helps you write down tasks/ideas in Notion via telegram!\
""",
    )


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    new_page = {
        "Name": {"title": [{"text": {"content": f"{message.text}"}}]},
        "List": {
            "id": "Yn%40W",
            "type": "select",
            "select": {
                "id": "12c077de-940d-4104-9ce5-005e60a68bec",
                "name": "Trash",
                "color": "gray",
            },
        },
    }
    notion.pages.create(parent={"database_id": DATA_BASE_API}, properties=new_page)
    bot.send_message(
        message.chat.id, f"The following task has been added to cart:\n'{message.text}'"
    )


bot.infinity_polling()
