#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk
import gtk

from lib.i18n import _

class AboutController(object):
  """AboutController"""
  def __init__(self):
    """This method initializes an AboutController instance."""
    self.builder = gtk.Builder()
    self.builder.add_from_file("glade/about.glade")
    self.builder.connect_signals(self)

  def response(self, widget, response_id):
    """This method destroys the about dialog"""
    self.builder.get_object("aboutdialog1").destroy()
