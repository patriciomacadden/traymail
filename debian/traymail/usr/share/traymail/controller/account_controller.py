#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk
import gtk

from lib.i18n import _
from lib.subject import *

from model.account import *

class AccountController(Subject):
  """AccountController"""
  def __init__(self, observer, account = None):
    """This method initializes an AccountController instance."""
    Subject.__init__(self)
    self.attach(observer)
    self.account = account
    self.builder = gtk.Builder()
    self.builder.add_from_file("glade/account.glade")
    self.builder.connect_signals(self)

    # a little hack: internationalize this strings.
    self.builder.get_object("label1").set_text(_(self.builder.get_object("label1").get_text()))
    self.builder.get_object("label2").set_text(_(self.builder.get_object("label2").get_text()))
    self.builder.get_object("label3").set_text(_(self.builder.get_object("label3").get_text()))
    self.builder.get_object("label4").set_text(_(self.builder.get_object("label4").get_text()))
    self.builder.get_object("label5").set_text(_(self.builder.get_object("label5").get_text()))
    self.builder.get_object("label6").set_text(_(self.builder.get_object("label6").get_text()))
    self.builder.get_object("checkbutton1").set_label(_(self.builder.get_object("checkbutton1").get_label()))
    self.builder.get_object("label7").set_text(_(self.builder.get_object("label7").get_text()))

    if not self.account is None:
      self.builder.get_object("window1").set_title(_("Edit account"))
      self.fillin_fields()
    else:
      self.builder.get_object("window1").set_title(_("New account"))
      self.account = Account()

  def fillin_fields(self):
    """This method fills in the form fields with the account object's values."""
    self.builder.get_object("entry1").set_text(self.account.name)
    self.builder.get_object("combobox1").set_active(self.account.protocol)
    self.builder.get_object("entry2").set_text(self.account.host)
    if not self.account.port is None:
      self.builder.get_object("entry3").set_text(str(self.account.port))
    self.builder.get_object("entry4").set_text(self.account.username)
    self.builder.get_object("entry5").set_text(self.account.password)
    self.builder.get_object("checkbutton1").set_active(self.account.use_ssl)
    self.builder.get_object("entry6").set_text(self.account.custom_command)

  def fillin_account(self):
    """This method fills in the preferences object's with the form fields' values."""
    self.account.name = self.builder.get_object("entry1").get_text()
    self.account.protocol = self.builder.get_object("combobox1").get_active()
    self.account.host = self.builder.get_object("entry2").get_text()
    if self.builder.get_object("entry3").get_text() != "":
      self.account.port = int(self.builder.get_object("entry3").get_text())
    self.account.username = self.builder.get_object("entry4").get_text()
    self.account.password = self.builder.get_object("entry5").get_text()
    self.account.use_ssl = self.builder.get_object("checkbutton1").get_active()
    self.account.custom_command = self.builder.get_object("entry6").get_text()

  def toggle_insensitive_entries(self, widget):
    if self.builder.get_object("combobox1").get_active() == 3:
      self.builder.get_object("entry2").set_sensitive(False)
      self.builder.get_object("entry2").set_text("")
      self.builder.get_object("entry3").set_sensitive(False)
      self.builder.get_object("entry3").set_text("")
      self.builder.get_object("checkbutton1").set_sensitive(False)
    else:
      self.builder.get_object("entry2").set_sensitive(True)
      self.builder.get_object("entry3").set_sensitive(True)
      self.builder.get_object("checkbutton1").set_sensitive(True)

  def cancel(self, widget):
    """This method cancels the form saving."""
    if not self.account.is_valid():
      self.account.destroySelf()
    self.builder.get_object("window1").destroy()

  def display_errors(self):
    """This method displays all form errors."""
    errors = []
    if self.account.name == "":
      errors.append(_("name"))

    if self.account.protocol <= 0:
      errors.append(_("protocol"))

    # if account's protocol is IMAP or POP3
    if self.account.protocol == 1 or self.account.protocol == 2:
      # then the host is important
      if self.account.host == "":
        errors.append(_("host"))

    if self.account.username == "":
      errors.append(_("username"))

    if self.account.password == "":
      errors.append(_("password"))

    if len(errors):
      msg = _("The following fields are required: ")
      for error in errors:
        msg += error + ", "

      msg = msg[0:len(msg)-2]

      m_dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, msg)
      m_dialog.run()
      m_dialog.destroy()

  def accept(self, widget):
    """This method saves the account object."""
    self.fillin_account()
    if self.account.is_valid():
      self.account.sync()
      self.notify()
      self.builder.get_object("window1").destroy()
    else:
      self.display_errors()
