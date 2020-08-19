#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk
import gtk

from lib.i18n import _

class PreferencesController(object):
  """Preferences controller"""
  def __init__(self, preferences):
    """This method initializes a PreferencesController instance."""
    self.preferences = preferences
    self.builder = gtk.Builder()
    self.builder.add_from_file("glade/preferences.glade")
    self.builder.connect_signals(self)
    self.fillin_fields()

    # a little hack: internationalize this strings.
    self.builder.get_object("window1").set_title(_(self.builder.get_object("window1").get_title()))
    self.builder.get_object("label1").set_text(_(self.builder.get_object("label1").get_text()))
    self.builder.get_object("checkbutton1").set_label(_(self.builder.get_object("checkbutton1").get_label()))

  def fillin_fields(self):
    """This method fills in the form fields with the preferences object's values."""
    if not self.preferences.update_interval is None:
      self.builder.get_object("spinbutton1").set_value(self.preferences.update_interval)
    self.builder.get_object("checkbutton1").set_active(self.preferences.notify_always)

  def fillin_preferences(self):
    """This method fills in the preferences object's with the form fields' values."""
    self.preferences.update_interval = int(self.builder.get_object("spinbutton1").get_value())
    self.preferences.notify_always = self.builder.get_object("checkbutton1").get_active()

  def cancel(self, widget):
    """This method cancels the form saving."""
    self.builder.get_object("window1").destroy()

  def accept(self, widget):
    """This method saves the preferences object."""
    self.fillin_preferences()
    self.preferences.sync()
    self.builder.get_object("window1").destroy()
