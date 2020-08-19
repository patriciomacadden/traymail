#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk
import gtk

from controller.account_controller import *

from lib.i18n import _
from lib.observer import *

from model.account import *

class AccountsController(Observer):
  def __init__(self):
    """This method initializes an AccountsController instance."""
    self.builder = gtk.Builder()
    self.builder.add_from_file("glade/accounts.glade")
    self.builder.connect_signals(self)

    # a little hack: internationalize this string.
    self.builder.get_object("window1").set_title(_(self.builder.get_object("window1").get_title()))

    self.create_treeview()
    self.populate_treeview()

  def update(self, subject):
    """This method updates the accounts treeview."""
    treeview = self.builder.get_object("treeview1")
    treeview.get_model().clear()
    self.populate_treeview()

  def create_treeview(self):
    """This method creates the account treeview."""
    treeview = self.builder.get_object("treeview1")

    liststore = gtk.ListStore(str, str)

    column = gtk.TreeViewColumn(_("Name"))
    cell = gtk.CellRendererText()
    column.pack_start(cell, True)
    column.add_attribute(cell, 'text', 0)
    treeview.append_column(column)

    column = gtk.TreeViewColumn(_("Protocol"))
    cell = gtk.CellRendererText()
    column.pack_start(cell, True)
    column.add_attribute(cell, 'text', 1)
    treeview.append_column(column)

    treeview.set_model(liststore)

  def populate_treeview(self):
    """This method populates the account treeview."""
    liststore = self.builder.get_object("treeview1").get_model()
    for account in Account.select():
      liststore.append([account.name, account.get_protocol_str()])

  def set_sensitive_buttons(self, widget):
    """This method sets the buttons as sensitive."""
    self.builder.get_object("button2").set_sensitive(True)
    self.builder.get_object("button3").set_sensitive(True)

  def set_insensitive_buttons(self):
    """This method sets the buttons as insensitive."""
    self.builder.get_object("button2").set_sensitive(False)
    self.builder.get_object("button3").set_sensitive(False)

  def add_account(self, widget):
    """This method creates a new account controller"""
    AccountController(self)

  def edit_account(self, widget):
    """This method creates a new account controller, with the selected account ready to edit."""
    treeview = self.builder.get_object("treeview1")
    ac_name = treeview.get_model().get_value(treeview.get_selection().get_selected()[1], 0)
    account = Account.select(Account.q.name == ac_name).getOne()

    AccountController(self, account)

  def delete_account(self, widget):
    """This method deletes de selected account, asking for a confirmation."""
    m_dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, _("Are you sure?"))
    if m_dialog.run() == gtk.RESPONSE_YES:
      treeview = self.builder.get_object("treeview1")
      ac_name = treeview.get_model().get_value(treeview.get_selection().get_selected()[1], 0)
      account = Account.select(Account.q.name == ac_name).getOne()
      account.destroySelf()
      self.update(None)
    m_dialog.destroy()
    self.set_insensitive_buttons()

  def destroy(self, widget):
    """This method closes the accounts window."""
    self.builder.get_object("window1").destroy()
