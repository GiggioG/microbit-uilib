from microbit import *
from uilib import UI

def btnCallback(self):
    if self.data["exampleProperty"]:
        display.scroll("Toggle is true")

def extraSetup(self):
    self.data = {}
    self.data["exampleProperty"] = False

def toggleCallback(self, val):
    self.data["exampleProperty"] = val

exampleScreen = UI({
    'r': {
        "type": "radio",
        "isInput": True,
        "initial": 1,    # the middle
        "callback": lambda self, x: print("new radio value " + str(x))
    },
    'B': {
        "type": "binary",
        "isInput": False,
        "getValue": lambda self: running_time()//200 % 8
    },
    't': {
        "type": "toggle",
        "isInput": True,
        "initial": False,
        "callback": toggleCallback
    },
    'X': {
        "type": "button",
        "isInput": "True",
        "callback": btnCallback
    }
}, "r.r.r:"
   ".....:"
   ".B.X.:"
   ".B...:"
   ".B.t.",
extraSetup)

while True:
    display.show(Image(exampleScreen.renderForDisplay()))

    if button_a.was_pressed():
        exampleScreen.nextControl()
    if button_b.was_pressed():
        exampleScreen.changeSelectedControl()
