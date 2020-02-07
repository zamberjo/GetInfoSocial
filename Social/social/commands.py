
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from .objective import Objective
from .utils import check_user

ADD_OBJ_NAME, ADD_OBJ_EMAIL, ADD_OBJ_USERNAME, ADD_OBJ_TRACE = range(4)
SHOW_OBJ_SELECT, SHOW_OBJ_ACTION, SHOW_OBJ_RM_EMAIL, SHOW_OBJ_ADD_EMAIL, \
    SHOW_OBJ_ADD_PASSWORD, SHOW_OBJ_RM_USERNAME, SHOW_OBJ_ADD_USERNAME, \
    SHOW_OBJ_RENAME, SHOW_OBJ_ADD_PHONE, SHOW_OBJ_RM_PHONE = range(10)

EMOTICONS = {
    # items
    "email": "📧",
    "passwords": "🔑",
    "usernames": "🤖",
    "socialnetwork": "👥",
    "phones": "📱",
    # actions
    "see": "👁",
    "add": "➕",
    "rm": "❌",
    "find": "🔎",
    "modify": "✏️",
}

_logger = logging.getLogger("GetSocialInfo")


def start(update, context):
    _logger.debug("[command][start]")
    update.message.reply_text(
        'Hi! My name is GetInfoSocial Bot. I will hold a conversation with '
        'you. Send /cancel to stop talking to me.',
        reply_markup=ReplyKeyboardRemove())


def only_for_me(func):
    def inner_only_for_me(update, context):
        try:
            user = update.message.from_user
            if not check_user(user):
                update.message.reply_text(
                    "You are note allowed for this bot :D!")
                return
            return func(update, context)
        except Exception:
            return
    return inner_only_for_me


@only_for_me
def conv_add_obj(update, context):
    _logger.debug("[command][conv_add_obj]")
    update.message.reply_text(
        'Send me a name',
        reply_markup=ReplyKeyboardRemove())
    return ADD_OBJ_NAME


@only_for_me
def conv_ask_name(update, context):
    _logger.debug("[command][conv_ask_name]")
    name = "".join([
        n.capitalize() for n in update.message.text.split()])
    context.chat_data['objective'] = Objective(name)
    update.message.reply_text(
        'Send me a email',
        reply_markup=ReplyKeyboardRemove())
    return ADD_OBJ_EMAIL


@only_for_me
def conv_ask_email(update, context):
    _logger.debug("[command][conv_ask_email]")
    email = update.message.text
    objective = context.chat_data['objective']
    objective.emails += [email]

    reply_keyboard = [['/skip']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Send me an username', reply_markup=markup)
    return ADD_OBJ_USERNAME


@only_for_me
def conv_ask_username(update, context):
    _logger.debug("[command][conv_ask_username]")
    username = update.message.text
    if username != "/skip":
        objective = context.chat_data['objective']
        objective.usernames += [username]

    reply_keyboard = [['Yes', 'No']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        'Done! Want you start the tracer?', reply_markup=markup)
    return ADD_OBJ_TRACE


@only_for_me
def conv_trace(update, context):
    _logger.debug("[command][conv_trace]")
    objective = context.chat_data['objective']
    objective.trace(update=update)


@only_for_me
def trace_all(update, context):
    _logger.debug("[command][trace_all]")
    update.message.reply_text(
        'Trace started...', reply_markup=ReplyKeyboardRemove())
    for objective in Objective.get_all():
        objective.trace()
    update.message.reply_text(
        'Trace ends!', reply_markup=ReplyKeyboardRemove())


@only_for_me
def cancel(update, context):
    _logger.debug("[command][cancel]")
    update.message.reply_text(
        'Cancelled',
        reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(update, context):
    _logger.debug("[command][error]")
    """Log Errors caused by Updates."""
    _logger.warning('[ERROR] %s', context.error)


@only_for_me
def help(update, context):
    message = """
start - Show start message
add - Add new target
trace_all - Trace all targets
show - Show all targets
passwords - Show all passwords
cancel - Fallback
skip - Fallback
    """
    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())


@only_for_me
def passwords(update, context):
    for objective in Objective.get_all():
        for passwd in objective.passwords:
            update.message.reply_text(
                passwd, reply_markup=ReplyKeyboardRemove())


@only_for_me
def conv_show_obj(update, context):
    reply_keyboard = sorted([obj.name for obj in Objective.get_all()])
    reply_keyboard = [[d] for d in reply_keyboard]
    reply_keyboard += [["/cancel"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        'Select objective', reply_markup=markup)
    return SHOW_OBJ_SELECT


def show_actions(update):
    reply_keyboard = [
        [
            EMOTICONS["modify"],
        ],
        [
            " ".join([EMOTICONS["see"], EMOTICONS["email"]]),
            " ".join([EMOTICONS["rm"], EMOTICONS["email"]]),
            " ".join([EMOTICONS["add"], EMOTICONS["email"]]),
        ],
        [
            " ".join([EMOTICONS["see"], EMOTICONS["usernames"]]),
            " ".join([EMOTICONS["rm"], EMOTICONS["usernames"]]),
            " ".join([EMOTICONS["add"], EMOTICONS["usernames"]]),
        ],
        [
            " ".join([EMOTICONS["see"], EMOTICONS["passwords"]]),
            " ".join([EMOTICONS["rm"], EMOTICONS["passwords"]]),
            " ".join([EMOTICONS["add"], EMOTICONS["passwords"]]),
        ],
        [
            " ".join([EMOTICONS["see"], EMOTICONS["phones"]]),
            " ".join([EMOTICONS["rm"], EMOTICONS["phones"]]),
            " ".join([EMOTICONS["add"], EMOTICONS["phones"]]),
        ],
        [
            " ".join([EMOTICONS["see"], EMOTICONS["socialnetwork"]]),
        ],
        [
            " ".join([EMOTICONS["find"], EMOTICONS["passwords"]]),
            " ".join([EMOTICONS["find"], EMOTICONS["usernames"]]),
            " ".join([EMOTICONS["find"], EMOTICONS["phones"]]),
        ],
        [
            " ".join([EMOTICONS["find"], "ALL"]),
        ],
        ['/cancel'],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Select action', reply_markup=markup)


@only_for_me
def conv_sel_obj(update, context):
    objective = update.message.text
    context.chat_data['objective'] = Objective(objective)
    show_actions(update)
    return SHOW_OBJ_ACTION


@only_for_me
def conv_do_action(update, context):
    _logger.debug("[conv_do_action]")
    objective = context.chat_data['objective']
    action = update.message.text
    if not objective or not action:
        update.message.reply_text('Error!', reply_markup=ReplyKeyboardRemove())
        return

    next_step = SHOW_OBJ_ACTION
    elements = []
    if EMOTICONS["email"] in action:
        _logger.debug("-> email")
        elements = objective.emails
    elif EMOTICONS["passwords"] in action:
        _logger.debug("-> passwords")
        elements = objective.passwords
    elif EMOTICONS["usernames"] in action:
        _logger.debug("-> usernames")
        elements = objective.usernames
    elif EMOTICONS["socialnetwork"] in action:
        _logger.debug("-> socialnetwork")
        for social in objective.socials:
            social = social.split(",")
            element = "[{}] {} {}".format(
                social[0], social[1], social[2])
            elements += [element]
    elif EMOTICONS["phones"] in action:
        _logger.debug("-> phones")
        elements = objective.phones

    if EMOTICONS["modify"] in action:
        _logger.debug("-> modify")
        update.message.reply_text(
            'Send me the name', reply_markup=ReplyKeyboardRemove())
        next_step = SHOW_OBJ_RENAME

    elif EMOTICONS["see"] in action:
        _logger.debug("-> see")
        update.message.reply_text(
            "\n".join(elements) or "->None<-",
            reply_markup=ReplyKeyboardRemove())

    elif EMOTICONS["rm"] in action:
        _logger.debug("-> rm")
        reply_keyboard = []
        for element in elements:
            reply_keyboard += [[element]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            'Which one do you want to delete?', reply_markup=markup)

        next_step = None
        if EMOTICONS["email"] in action:
            next_step = SHOW_OBJ_RM_EMAIL
        elif EMOTICONS["passwords"] in action:
            update.message.reply_text(
                'Action not allowed sorry :D',
                reply_markup=ReplyKeyboardRemove())
        elif EMOTICONS["usernames"] in action:
            next_step = SHOW_OBJ_RM_USERNAME
        elif EMOTICONS["phones"] in action:
            next_step = SHOW_OBJ_RM_PHONE

    elif EMOTICONS["add"] in action:
        _logger.debug("-> add")
        next_step = None
        if EMOTICONS["email"] in action:
            update.message.reply_text(
                'Send me the email', reply_markup=ReplyKeyboardRemove())
            next_step = SHOW_OBJ_ADD_EMAIL
        elif EMOTICONS["passwords"] in action:
            update.message.reply_text(
                'Send me the password', reply_markup=ReplyKeyboardRemove())
            next_step = SHOW_OBJ_ADD_PASSWORD
        elif EMOTICONS["usernames"] in action:
            update.message.reply_text(
                'Send me the username', reply_markup=ReplyKeyboardRemove())
            next_step = SHOW_OBJ_ADD_USERNAME
        elif EMOTICONS["phones"] in action:
            update.message.reply_text(
                'Send me the phone', reply_markup=ReplyKeyboardRemove())
            next_step = SHOW_OBJ_ADD_PHONE

    elif EMOTICONS["find"] in action:
        _logger.debug("-> find")
        if EMOTICONS["passwords"] in action or "ALL" in action:
            objective.trace_passwords(update=update)
        if EMOTICONS["usernames"] in action or "ALL" in action:
            objective.trace_usernames(update=update)
        if EMOTICONS["phones"] in action or "ALL" in action:
            objective.trace_phones(update=update)

    else:
        _logger.debug("-> default")
        update.message.reply_text(
            "DEFAULT", reply_markup=ReplyKeyboardRemove())

    _logger.debug("next_step: {}".format(next_step))
    if next_step == SHOW_OBJ_ACTION:
        show_actions(update)
    return next_step


@only_for_me
def conv_rm_email(update, context):
    try:
        _logger.debug("[conv_rm_email]")
        objective = context.chat_data['objective']
        objective.emails = [
            e for e in objective.emails if update.message.text != e
        ]
        update.message.reply_text(
            'Done! Email deleted.', reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        _logger.exception(e)
    show_actions(update)
    return SHOW_OBJ_SELECT


@only_for_me
def conv_add_password(update, context):
    try:
        _logger.debug("[conv_add_password]")
        objective = context.chat_data['objective']
        objective.passwords += [update.message.text]
        update.message.reply_text(
            'Done! Pasword added.', reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        _logger.exception(e)
    show_actions(update)
    return SHOW_OBJ_SELECT


@only_for_me
def conv_rm_username(update, context):
    try:
        _logger.debug("[conv_rm_username]")
        objective = context.chat_data['objective']
        objective.usernames = [
            e for e in objective.usernames if update.message.text != e
        ]
        update.message.reply_text(
            'Done! Username deleted.', reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        _logger.exception(e)
    show_actions(update)
    return SHOW_OBJ_SELECT


@only_for_me
def conv_rename(update, context):
    try:
        _logger.debug("[conv_rename]")
        objective = context.chat_data['objective']
        objective.path = "".join([
            n.capitalize() for n in update.message.text.split()])
        update.message.reply_text(
            'Done! Renamed.', reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        _logger.exception(e)
    show_actions(update)
    return SHOW_OBJ_SELECT


@only_for_me
def conv_add_phone(update, context):
    try:
        _logger.debug("[conv_add_phone]")
        objective = context.chat_data['objective']
        objective.phones += [update.message.text]
        update.message.reply_text(
            'Done! Phone added.', reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        _logger.exception(e)
    show_actions(update)
    return SHOW_OBJ_SELECT


@only_for_me
def conv_rm_phone(update, context):
    try:
        _logger.debug("[conv_rm_phone]")
        objective = context.chat_data['objective']
        objective.phones = [
            e for e in objective.phones if update.message.text != e
        ]
        update.message.reply_text(
            'Done! Phone deleted.', reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        _logger.exception(e)
    show_actions(update)
    return SHOW_OBJ_SELECT
