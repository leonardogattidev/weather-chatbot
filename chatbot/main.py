import logging

from dotenv import load_dotenv

from chatbot import bot

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def main() -> None:
    load_dotenv()
    bot.run()


if __name__ == "__main__":
    main()
