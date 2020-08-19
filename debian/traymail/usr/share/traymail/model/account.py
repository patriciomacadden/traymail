#!/usr/bin/python
# -*- coding: utf-8 -*-

import imaplib
import libgmail
import poplib
from sqlobject import *

from lib.database import *

class Account(SQLObject):
  """This class represents user preferences."""
  _connection = Database.get_connection()
  _lazyUpdate = True

  name = StringCol(default = None)
  protocol = IntCol(default = None)
  host = StringCol(default = None)
  port = IntCol(default = None)
  username = StringCol(default = None)
  password = StringCol(default = None)
  use_ssl = BoolCol(default = None)
  custom_command = StringCol(default = None)

  def get_protocol_str(self):
    """Returns the string representation of a protocol number."""
    if self.protocol == 1:
      return "IMAP"
    elif self.protocol == 2:
      return "POP3"
    elif self.protocol == 3:
      return "Gmail"

  def is_valid(self):
    """Returns true if this account is valid."""
    # if protocol is IMAP, POP3 or Gmail
    if self.protocol > 0:
      # if protocol is Gmail, host is not important
      if self.protocol == 3:
        valid = self.name != "" and self.username != "" and self.password != ""
      else:
        valid = self.name != "" and self.host != "" and self.username != "" and self.password != ""
    else:
      valid = False
    return valid

  def get_mail_count(self):
    """Returns the number of unseen mails in this account."""
    if self.protocol == 1:
      return self.get_imap_mail_count()
    elif self.protocol == 2:
      return self.get_pop_mail_count()
    elif self.protocol == 3:
      return self.get_gmail_mail_count()

  def get_imap_mail_count(self):
    """Returns the number of unseen mails in this IMAP4 account."""
    # if port is not set
    if self.port is None:
      # use the well known port for imap4
      port = 993
    else:
      port = self.port
    if self.use_ssl:
      imap = imaplib.IMAP4_SSL(self.host, port)
    else:
      imap = imaplib.IMAP4(self.host, port)
    imap.login(self.username, self.password)
    imap.select()
    typ, msgs = imap.search(None, "UNSEEN")
    imap.close()
    imap.logout()
    return len(msgs[0].split())

  def get_pop_mail_count(self):
    """Returns the number of unseen mails in this POP3 account."""
    # if port is not set
    if self.port is None:
      # use the well known port for pop3
      port = 995
    else:
      port = self.port
    if self.use_ssl:
      pop = poplib.POP3_SSL(self.host, port)
    else:
      pop = poplib.POP3(self.host, port)
    pop.user(self.username)
    pop.pass_(self.password)
    nb_msgs = len(pop.list()[1])
    pop.quit()
    return nb_msgs

  def get_gmail_mail_count(self):
    """Returns the number of unread mails in this Gmail account."""
    import time
    gmail = libgmail.GmailAccount(self.username, self.password)
    gmail.login()
    return len(gmail.getMessagesByQuery('is:unread', True))
