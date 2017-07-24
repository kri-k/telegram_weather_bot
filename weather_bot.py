#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, RegexHandler
from logger import *
from callbacks import *


def main():
    with open('telegram_bot_token.txt', 'r') as f:
        token = f.readline()

    updater = Updater(token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('info', info, pass_chat_data=True))
    dp.add_handler(CommandHandler('now', now, pass_chat_data=True))
    dp.add_handler(CommandHandler('today', today, pass_chat_data=True))
    dp.add_handler(CommandHandler('tomorrow', tomorrow, pass_chat_data=True))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('location', request_location)],

        states={
            GET_LOCATION: [
                MessageHandler(Filters.location, get_location, pass_chat_data=True),
                CommandHandler('cancel', cancel),
                RegexHandler('^.*$', wrong_location)
            ],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()