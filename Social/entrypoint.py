#!/usr/bin/env python3

import logging
import os

from social import bot, formatter


def str2bool(s):
    return bool(s.lower().capitalize() == 'True')


debug = str2bool(os.environ["DEBUG"])
_logger = logging.getLogger("GetSocialInfo")
_logger.setLevel(logging.DEBUG if debug else logging.INFO)

logger_ch = logging.StreamHandler()
logger_ch.setLevel(logging.DEBUG if debug else logging.INFO)
logger_ch.setFormatter(formatter.CustomFormatter())
_logger.addHandler(logger_ch)


if __name__ == '__main__':
    bot.main()
