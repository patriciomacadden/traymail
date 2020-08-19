#!/usr/bin/python
# -*- coding: utf-8 -*-

class Subject(object):
  """This class represents the Subject in the Observer design pattern."""
  def __init__(self):
    """This method initializes an observer instance."""
    self._observers = []

  def attach(self, observer):
    """This method attachs an observer to the subject (self)."""
    if not observer in self._observers:
      self._observers.append(observer)

  def detach(self, observer):
    """This method detachs an observer to the subject (self)."""
    try:
      self._observers.remove(observer)
    except ValueError:
      pass

  def notify(self, modifier = None):
    """This method notifies all observers that the subject changed."""
    for observer in self._observers:
      if modifier != observer:
        observer.update(self)
