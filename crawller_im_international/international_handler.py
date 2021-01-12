from abc import ABCMeta, abstractmethod

class InternationalHandler(metaclass=ABCMeta):
  @abstractmethod
  def handle(self): pass