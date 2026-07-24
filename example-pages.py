from microbit import *
from uilib import UI

ui = None
currMainPage = None
pages = [None] * 8
for i in range(1, 9):
    def pageInitFunc(s):
        s.data = {}
        s.data["pageNo"] = i
    pages[i-1] = UI({
        "r": {
            "type": "radio",
            "initial": i-1,
            "callback": lambda self, val: print("new radio value on some page: " + str(val)),
            "isInput": True
        },
        "n": {
            "type": "binary",
            "getValue": lambda self: self.data["pageNo"],
            "isInput": False
        },
        "b": {
            "type": "button",
            "callback": lambda self: openMainPage(),
            "isInput": True
        }
    }, ".rrrr:"
        "..b..:"
        ".nnnn:"
        ".....:"
        "rrrr.",
        pageInitFunc
    )


def openMainPage():
    global ui, currMainPage
    if currMainPage == None:
        def goToPageButton(self):
            global ui
            print("going to page " + str(self.controls["p"]["value"]))
            ui = pages[self.controls["p"]["value"]]
        currMainPage = UI({
            "p": {
                "type": "radio",
                "initial": 0,
                "callback": None,
                "isInput": True
            },
            "X": {
                "type": "button",
                "callback": goToPageButton,
                "isInput": True
            }
        }, "p.p.p:"
           ".p.p.:"
           "p.p.p:"
           ".....:"
           ".XXX."
        )
    ui = currMainPage


while True:
    if ui == None:
        openMainPage()

    display.show(Image(ui.renderForDisplay()))

    if button_a.was_pressed():
        ui.nextControl()
    if button_b.was_pressed():
        ui.interactWithControl()
