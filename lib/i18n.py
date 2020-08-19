#!/usr/bin/python
# -*- coding: utf-8 -*-

import gettext
import locale
import os

APP_NAME = "traymail"
I18N_DIR = os.path.realpath(os.path.dirname(__file__))+"/../i18n"

gettext.bindtextdomain(APP_NAME, I18N_DIR)
gettext.textdomain(APP_NAME)

# get the language to use
lang = gettext.translation(APP_NAME, I18N_DIR, languages = ["es_AR"], fallback = True)

try:
  _ = lang.gettext
except:
  print "error"
  def _(s):
    return s
