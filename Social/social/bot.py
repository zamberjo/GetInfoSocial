
import os
import logging

from telegram.ext import CommandHandler, ConversationHandler, Filters, \
    MessageHandler, Updater

from .commands import ADD_OBJ_NAME, ADD_OBJ_EMAIL, ADD_OBJ_USERNAME, \
    ADD_OBJ_TRACE
from .commands import SHOW_OBJ_SELECT, SHOW_OBJ_ACTION, SHOW_OBJ_RM_EMAIL, \
    SHOW_OBJ_ADD_EMAIL, SHOW_OBJ_ADD_PASSWORD, SHOW_OBJ_RM_USERNAME, \
    SHOW_OBJ_ADD_USERNAME, SHOW_OBJ_RENAME, SHOW_OBJ_ADD_PHONE, SHOW_OBJ_RM_PHONE
from .commands import conv_ask_name, conv_ask_email, conv_ask_username, \
    cancel, conv_add_obj, help, start, conv_trace, trace_all, passwords, \
    conv_show_obj, conv_sel_obj, conv_do_action, error, conv_rm_email, \
    conv_add_password, conv_rm_username, conv_rename, conv_add_phone, \
    conv_rm_phone

_logger = logging.getLogger("GetSocialInfo")


def main():
    updater = Updater(os.environ["TELEGRAM_BOT_ID"], use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', conv_add_obj)],
        states={
            ADD_OBJ_NAME: [
                MessageHandler(
                    Filters.text, conv_ask_name, pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
            ADD_OBJ_EMAIL: [
                MessageHandler(
                    Filters.text, conv_ask_email,  pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
            ADD_OBJ_USERNAME: [
                MessageHandler(
                    Filters.text, conv_ask_username,  pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
            ADD_OBJ_TRACE: [
                MessageHandler(
                    Filters.text, conv_trace,  pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("trace_all", trace_all))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("passwords", passwords))

    conv_show_handler = ConversationHandler(
        entry_points=[CommandHandler('show', conv_show_obj)],
        states={
            SHOW_OBJ_SELECT: [
                MessageHandler(
                    Filters.text, conv_sel_obj, pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
            SHOW_OBJ_ACTION: [
                MessageHandler(
                    Filters.text, conv_do_action,  pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
            SHOW_OBJ_RM_EMAIL: [
                MessageHandler(
                    Filters.text, conv_rm_email,  pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
            SHOW_OBJ_ADD_EMAIL: [
                MessageHandler(
                    Filters.text, conv_ask_email,  pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
            SHOW_OBJ_ADD_PASSWORD: [
                MessageHandler(
                    Filters.text, conv_add_password,  pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
            SHOW_OBJ_RM_USERNAME: [
                MessageHandler(
                    Filters.text, conv_rm_username,  pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
            SHOW_OBJ_ADD_USERNAME: [
                MessageHandler(
                    Filters.text, conv_ask_username,  pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
            SHOW_OBJ_RENAME: [
                MessageHandler(
                    Filters.text, conv_rename,  pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
            SHOW_OBJ_ADD_PHONE: [
                MessageHandler(
                    Filters.text, conv_add_phone,  pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
            SHOW_OBJ_RM_PHONE: [
                MessageHandler(
                    Filters.text, conv_rm_phone,  pass_chat_data=True),
                CommandHandler('cancel', cancel)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_show_handler)

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()
