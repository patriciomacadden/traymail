#!/usr/bin/python
# -*- coding: utf-8 -*-

import gobject
import pygtk
import gtk
import time

from controller.about_controller import *
from controller.accounts_controller import *
from controller.notification_controller import *
from controller.preferences_controller import *

from lib.i18n import _

from model.preferences import *

class TraymailController(object):
  """Traymail controller.
  Provides the application functionality through a status icon.
  """
  def __init__(self):
    """This method initializes a TraymailController instance."""
    self.create_status_icon()
    self.create_popup_menu()

    self.status_icon.connect("popup-menu", self.show_popup_menu)

    self.automatic_refresh()

    gtk.main()

  def get_preferences(self):
    """This method retrieves the preferences object (the first and only one). If it does not exist, returns a new one."""
    try:
      return Preferences.get(1)
    except:
      return Preferences()

  def automatic_refresh(self):
    """This method performs a periodic refresh."""
    preferences = self.get_preferences()
    self.refresh(None, preferences.notify_always)
    gobject.timeout_add(preferences.update_interval * 1000, self.refresh, None, preferences.notify_always)

  def create_status_icon(self):
    """This method creates the status icon."""
    self.status_icon = gtk.StatusIcon()
    self.status_icon.set_from_file("icons/indicator-messages.svg")
    self.status_icon.set_tooltip(_("Check your mail in the systray"))

  def create_popup_menu(self):
    """This method creates the popup menu and attachs it to the status icon."""
    self.popup_menu = gtk.Menu()

    menu_item = gtk.ImageMenuItem(gtk.STOCK_REFRESH)
    menu_item.connect("activate", self.refresh)
    self.popup_menu.append(menu_item)

    menu_item = gtk.SeparatorMenuItem()
    self.popup_menu.append(menu_item)

    menu_item = gtk.MenuItem(_("Accounts"))
    menu_item.connect("activate", self.open_accounts)
    self.popup_menu.append(menu_item)

    menu_item = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
    menu_item.connect("activate", self.open_preferences)
    self.popup_menu.append(menu_item)

    menu_item = gtk.SeparatorMenuItem()
    self.popup_menu.append(menu_item)

    menu_item = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
    menu_item.connect("activate", self.open_about_dialog)
    self.popup_menu.append(menu_item)

    menu_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    menu_item.connect("activate", self.destroy)
    self.popup_menu.append(menu_item)

  def destroy(self, widget):
    """This method closes the application."""
    gtk.main_quit()

  def show_popup_menu(self, widget, button, activate_time):
    """This method shows the popup menu when the status icon is right-clicked."""
    if button == 3:
      self.popup_menu.show_all()
      self.popup_menu.popup(None, None, None, button, activate_time)

  def refresh(self, widget, notify_no_new_messages = True):
    """This method refreshes the status icon if there is new mail."""
    self.status_icon.set_tooltip(_("Checking mail accounts"))
    accounts = Account.select()
    if accounts.count() > 0:
      messages_count_tuples = []
      total_messages = 0
      for account in accounts:
        # because sqlobject automatically saves objects:
        if account.is_valid():
          ac_total_messages = account.get_mail_count()
          total_messages += ac_total_messages
          messages_count_tuples.append((account, ac_total_messages))

      if total_messages:
        NotificationController.new_messages(messages_count_tuples)
        self.status_icon.set_from_file("icons/indicator-messages-new.svg")
      else:
        if notify_no_new_messages:
          NotificationController.no_new_messages()
        self.status_icon.set_from_file("icons/indicator-messages.svg")
    else:
      NotificationController.no_accounts()
      self.status_icon.set_from_file("icons/mail-mark-important.svg")
    self.status_icon.set_tooltip(_("Last revision at ")+time.strftime("%H:%M:%S"))
    return True

  def open_accounts(self, widget):
    """This method creates a new AccountsController instance."""
    AccountsController()

  def open_preferences(self, widget):
    """This method creates a new PreferencesController instance."""
    preferences = self.get_preferences()
    PreferencesController(preferences)

  def open_about_dialog(self, widget):
    """This method creates a new AboutController instance."""
    AboutController()
