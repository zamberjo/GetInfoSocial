
import logging
import os
import subprocess
from pathlib import Path

from telegram import ReplyKeyboardRemove

from .karma import Core
from .utils import check_valid_email, save_file

_logger = logging.getLogger("GetSocialInfo")


class Objective(object):
    """Docstring for objective. """
    FILES = {
        'emails': 'emails_path',
        'passwd': 'passwd_path',
        'usernames': 'usernames_path',
        'phones': 'phones_path',
    }

    def __init__(self, name, usernames=None, passwords=None, emails=None):
        self.name = name
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        if self.usernames:
            pass

    @classmethod
    def get_all(cls):
        objectives = []
        for filename in Path(Objective.targets_path()).iterdir():
            if not filename.is_dir():
                continue
            objectives += [Objective(os.path.basename(filename))]
        return objectives

    @classmethod
    def targets_path(cls):
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "targets")

    @property
    def path(self):
        return os.path.join(Objective.targets_path(), self.name)

    @path.setter
    def path(self, value):
        os.rename(self.path, os.path.join(Objective.targets_path(), value))
        self.name = value

    def save_file(self, target, values):
        file_path = getattr(self, self.FILES[target])
        values = [e for e in list(set(values)) if '\n' != e]
        with open(file_path, "w") as f:
            f.write("\n".join(values))

    @property
    def phones(self):
        phones = []
        try:
            with open(self.phones_path, "r") as f:
                phones = f.readlines()
        except Exception:
            pass
        return [e.replace("\n", "") for e in phones if not e or "\n" != e]

    @phones.setter
    def phones(self, value):
        save_file(getattr(self, self.FILES["phones"]), value)

    @property
    def phones_path(self):
        return os.path.join(self.path, "phones")

    @property
    def phones_info_path(self):
        return os.path.join(self.path, "phones_info")

    @property
    def emails(self):
        emails = []
        try:
            with open(self.emails_path, "r") as f:
                emails = f.readlines()
        except Exception:
            pass
        return [e.replace("\n", "") for e in emails if not e or "\n" != e]

    @emails.setter
    def emails(self, value):
        value = [email for email in value if check_valid_email(email)]
        save_file(getattr(self, self.FILES["emails"]), value)

    @property
    def emails_path(self):
        return os.path.join(self.path, "emails")

    @property
    def passwords(self):
        passwords = []
        try:
            with open(self.passwd_path, "r") as f:
                passwords = f.readlines()
        except Exception:
            pass
        return [e.replace("\n", "") for e in passwords if not e or "\n" != e]

    @passwords.setter
    def passwords(self, value):
        save_file(getattr(self, self.FILES["passwords"]), value)

    @property
    def passwd_path(self):
        return os.path.join(self.path, "passwd")

    @property
    def usernames(self):
        usernames = []
        try:
            with open(self.usernames_path, "r") as f:
                usernames = f.readlines()
        except Exception:
            pass
        return [e.replace("\n", "") for e in usernames if not e or "\n" != e]

    @usernames.setter
    def usernames(self, value):
        save_file(getattr(self, self.FILES["usernames"]), value)

    @property
    def usernames_path(self):
        return os.path.join(self.path, "usernames")

    @property
    def socials(self):
        socials = []
        try:
            with open(self.social_path, "r") as f:
                socials = f.readlines()
        except Exception as e:
            _logger.exeption(e)
        socials = [e.replace("\n", "") for e in socials if not e or "\n" != e]
        return socials

    @property
    def social_path(self):
        return os.path.join(self.path, "socialnetworks")

    def trace_usernames(self, update=None):
        update.message.reply_text("Starting trace...")
        try:
            current_path = os.path.dirname(os.path.abspath(__file__))
            if not self.usernames:
                update.message.reply_text(
                    "This objective don't have usernames")
            for username in self.usernames:
                cmd = [
                    'python',
                    '/sherlock/sherlock.py',
                    username,
                    '--csv',
                    '--folderoutput',
                    '/tmp/',
                    '--print-found',
                    '--proxy',
                    'socks5://tor-node:9050'
                ]
                process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                csv_file = os.path.join(
                    current_path, "..", username + ".csv")
                lines = []
                with open(csv_file, "r") as f:
                    lines = [l for l in f.readlines() if ',no,' not in l]
                with open(self.social_path, "w") as f:
                    for line in lines[1:]:
                        columns = line.split(",")
                        line = ",".join([
                            columns[0],
                            columns[1],
                            columns[3],
                        ])
                        f.write(line + "\n")
                if update:
                    with open(self.social_path, "r") as f:
                        text = f.readlines()
                    update.message.reply_text(
                        "\n".join(text),
                        reply_markup=ReplyKeyboardRemove())
        except Exception as e:
            _logger.exception(e)
            if update:
                update.message.reply_text(
                    '[ERROR] {}'.format(e), reply_markup=ReplyKeyboardRemove())
        update.message.reply_text("End trace!")

    def trace_passwords(self, update=None):
        try:
            if update:
                update.message.reply_text(
                    'Trace started...', reply_markup=ReplyKeyboardRemove())
            _logger.debug("emails_path: {}".format(self.emails_path))
            pwndb = Core({
                "target": True,
                "search": False,
                "<target>": self.emails_path,
                "--proxy": "tor-node:9050",
            })
            results = pwndb.search_info()
            passwords = []
            for key in results.keys():
                email = str(results[key]["email"])
                passw = str(results[key]["passw"])
                _logger.debug("email: {} | passw: {}".format(email, passw))
                if email == "donate@btc.thx":
                    continue
                if passw in self.passwords:
                    continue
                passwords += [passw]
                if update:
                    update.message.reply_text(
                        'New pass! {}'.format(passw),
                        reply_markup=ReplyKeyboardRemove())
            passwd_path = os.path.join(os.path.dirname(
                self.emails_path), "passwd")
            _logger.debug("passwd_path: {}".format(passwd_path))
            if passwords:
                with open(passwd_path, "a+") as f:
                    f.write("\n".join(passwords))
            elif update:
                update.message.reply_text(
                    'No passwords founded!', reply_markup=ReplyKeyboardRemove())
        except Exception as e:
            _logger.exception(e)
            if update:
                update.message.reply_text(
                    '[ERROR] {}'.format(e), reply_markup=ReplyKeyboardRemove())
        update.message.reply_text("End trace!")

    def trace_phones(self, update=None):
        update.message.reply_text("Starting trace...")
        try:
            if not self.phones:
                update.message.reply_text(
                    "This objective don't have phones")
            cmd = [
                'python',
                '/PhoneInfoga/phoneinfoga.py',
                '--input',
                self.phones_path,
                '-o',
                self.phones_info_path,
                '--no-ansi',
                '--recon',
            ]
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            with open(self.phones_info_path, "r") as f:
                text = f.readlines()
            update.message.reply_text(
                "\n".join(text),
                reply_markup=ReplyKeyboardRemove())
        except Exception as e:
            _logger.exception(e)
            if update:
                update.message.reply_text(
                    '[ERROR] {}'.format(e), reply_markup=ReplyKeyboardRemove())
        update.message.reply_text("End trace!")

    def trace(self, update=None):
        self.trace_passwords(update=update)
        self.trace_usernames(update=update)
        self.trace_phones(update=update)
