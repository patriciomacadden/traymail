#!/usr/bin/python
# -*- coding: utf-8 -*-

import dbus
import pygtk
import gtk
import os

from lib.i18n import _

class NotificationController(object):
  """Notification controller"""
  @classmethod
  def new_messages(cls, messages_count_tuples):
    """This method creates a new notification for new messages."""
    total_messages = 0
    message_body = ""
    for account, ac_total_messages in messages_count_tuples:
      if ac_total_messages > 0:
        total_messages += ac_total_messages
        if ac_total_messages == 1:
          message_body += _("%(ac_total_messages)d new message at %(ac_name)s\n") % {'ac_total_messages': ac_total_messages, 'ac_name': account.name}
        else:
          message_body += _("%(ac_total_messages)d new messages at %(ac_name)s\n") % {'ac_total_messages': ac_total_messages, 'ac_name': account.name}
        if ac_total_messages and account.custom_command:
          # append an & for a command that can run indefinitely
          os.system(account.custom_command+"&")
    message_body = message_body[0:len(message_body)-1]
    if total_messages == 1:
      message_title = _("1 new message")
    else:
      message_title = _("%d new messages") % (total_messages)
    session_bus = dbus.SessionBus()
    notifications_object = session_bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
    notifications_interface = dbus.Interface(notifications_object, 'org.freedesktop.Notifications')
    notification_id = notifications_interface.Notify("traymail", 0, "notification-message-email", message_title, message_body, dbus.Array([], signature='s'), dbus.Array([], signature='(sv)'), -1)

  @classmethod
  def no_new_messages(cls):
    """This method creates a new notification for no new messages."""
    session_bus = dbus.SessionBus()
    notifications_object = session_bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
    notifications_interface = dbus.Interface(notifications_object, 'org.freedesktop.Notifications')
    notification_id = notifications_interface.Notify("traymail", 0, "notification-message-email", _("No new messages"), "", dbus.Array([], signature='s'), dbus.Array([], signature='(sv)'), -1)

  @classmethod
  def no_accounts(cls):
    """This method creates a new notification for no accounts."""
    session_bus = dbus.SessionBus()
    notifications_object = session_bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
    notifications_interface = dbus.Interface(notifications_object, 'org.freedesktop.Notifications')
    notification_id = notifications_interface.Notify("traymail", 0, "notification-message-IM", _("No accounts"), _("Please create a new account"), dbus.Array([], signature='s'), dbus.Array([], signature='(sv)'), -1)
