#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from sqlobject import *

class Database(object):
  """This class provides database access, though the SQLObject ORM."""
  @classmethod
  def get_connection(cls):
    """This class method returns the connection against the database."""
    connection = connectionForURI("sqlite://"+os.environ["HOME"]+"/.traymail/db/traymail.db")
    sqlhub.processConnection = connection
    return connection
