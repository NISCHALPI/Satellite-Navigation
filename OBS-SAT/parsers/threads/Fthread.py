# Design a thread class for a functional threading
# Idea drawn from Stack Exchange
import time
from threading import Thread


# Custom thread class
class Fthread(Thread):
    """This is a custom thread class created by sub-classing threading.Threads calss
     Args: func  = callable
           args = arguments to func
     Return: self.get = func( *args)

     Takes function and argument to function
     Returns the output in self.get attribute

     """

    def __init__(self, func: callable, args: iter, ) -> None:
        super().__init__()
        self.get = None
        self.func = func
        self.args = args

    def run(self) -> None:
        if self.func is not None:
            self.get = self.func(*self.args)
