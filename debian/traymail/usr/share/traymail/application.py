#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from controller.traymail_controller import *

from model.account import *
from model.preferences import *

class Application(object):
  """Main application class.
  This is the front controller.
  """
  def __init__(self):
    """This method initializes an application instance."""
    if self.is_first_run():
      self.create_user_configuration()
    TraymailController()

  def is_first_run(self):
    return not os.path.exists(os.environ["HOME"]+"/.traymail")

  def create_user_configuration(self):
    traymail_dir = os.environ["HOME"]+"/.traymail"
    traymail_db_dir = traymail_dir+"/db"

    os.mkdir(traymail_dir)
    os.mkdir(traymail_db_dir)

    Preferences.createTable()
    Account.createTable()

if __name__ == "__main__":
  Application()
