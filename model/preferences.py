#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlobject import *

from lib.database import *

class Preferences(SQLObject):
  """This class represents user preferences."""
  _connection = Database.get_connection()
  _lazyUpdate = True

  update_interval = IntCol(default = 60)
  notify_always = BoolCol(default = False)
