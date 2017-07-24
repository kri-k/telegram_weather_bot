# -*- coding: utf-8 -*-

from telegram.ext import ConversationHandler
from logger import *
import weather_api


REQUEST_LOCATION, GET_LOCATION = range(2)


def start(bot, update):
    user = update.message.from_user
    update.message.reply_text('Weather bot alpha\nPrint /help to get help')
    logger.info("User %s %s start conversation." % (user.first_name, user.last_name))


def help(bot, update):
    update.message.reply_text(
        '/help - show this message'
        '\n/location - set your location'
        '\n/now - get current weather forecast'
        '\n/info - show information about you'
    )


def cancel(bot, update):
    user = update.message.from_user
    update.message.reply_text('No problem😉')
    return ConversationHandler.END


def wrong_location(bot, update):
    update.message.reply_text('This is not a location🤔')
    return ConversationHandler.END


def request_location(bot, update):
    update.message.reply_text(
        'Send me your location so I can send you the weather forecast'
        '\nor /cancel to cancel')
    return GET_LOCATION


def get_location(bot, update, chat_data):
    chat_id = update.message.chat_id
    user = update.message.from_user
    user_location = update.message.location

    logger.info("Location of %s %s: %f / %f"
                % (user.first_name, user.last_name, user_location.latitude, user_location.longitude))

    chat_data['loc'] = user_location
    update.message.reply_text('got it😁')
    return ConversationHandler.END


def info(bot, update, chat_data):
    if 'loc' not in chat_data:
        update.message.reply_text('I have no information about you😥')
    else:
        try:
            user_location = chat_data['loc']
            update.message.reply_text('your location is: {}, {}'.format(user_location.latitude, user_location.longitude))
        except (IndexError, ValueError):
            chat_id = update.message.chat_id
            user = update.message.from_user
            logger.info('{} in chat_id {} has problems with /info'.format(user.first_name, chat_id))
            update.message.reply_text('I have no information about you😴')


def forecast_decorator(func):
    def wrapper(bot, update, chat_data):
        if 'loc' not in chat_data:
            update.message.reply_text("I don't know where are you\nType /location to set your location")
        else:
            try:
                user_location = chat_data['loc']
                update.message.reply_text(func(user_location.latitude, user_location.longitude))
            except (IndexError, ValueError):
                chat_id = update.message.chat_id
                user = update.message.from_user
                logger.info('{} in chat_id {} has problems with forecast'.format(user.first_name, chat_id))
                update.message.reply_text("Sorry, I can't😣")

    return wrapper


@forecast_decorator
def now(lat, lon):
    return weather_api.get_cur_forecast(lat, lon)


@forecast_decorator
def today(lat, lon):
    return weather_api.get_today_forecast(lat, lon)


@forecast_decorator
def tomorrow(lat, lon):
    return weather_api.get_tomorrow_forecast(lat, lon)


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))