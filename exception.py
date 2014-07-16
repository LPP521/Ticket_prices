#coding=utf-8
class InputDateError(RuntimeError):
   def __init__(self, arg):
      self.args = arg
