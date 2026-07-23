from microbit import *

class UI:
    def __init__(self, controls, template, initFunc=None):
        self.template = template
        self.controls = controls
        self.data = None

        if initFunc != None:
            initFunc(self)
        
        templateLetters = {x for x in template if x.isalpha()}
        controlsLetters = set(controls.keys())
    
        assert templateLetters == controlsLetters, "Letters in the template and in the controls list should match"
    
        for c in controlsLetters:
            positions = [i for (i, x) in enumerate(template) if x == c]
            controls[c]["len"] = len(positions)
            controls[c]["positions"] = positions
    
            if controls[c]["type"] == "button":
                assert controls[c]["isInput"], "button can't not be an input"
                assert callable(controls[c]["callback"]), "button control's callback should be an appropriate callback function"
            else:
                if controls[c]["isInput"]:
                    assert callable(controls[c]["callback"]) or controls[c]["callback"] == None, "an input control's callback should be an appropriate callback function or None"
                    assert self.validateValue(controls[c]["type"], len(positions), controls[c]["initial"]), controls[c]["type"] + " control's initial value doesn't match requirements"

            if controls[c]["isInput"] == False:
                assert not "callback" in controls[c], "non-inputs should not have a callback"
                assert callable(controls[c]["getValue"]), "non-input controls' getValue should be an appropriate function"
            
            if controls[c]["type"] != "button":
                if controls[c]["isInput"]:
                    controls[c]["value"] = controls[c]["initial"]
                    if controls[c]["callback"] != None:
                        controls[c]["callback"](self, controls[c]["value"])
                else:
                    value = controls[c]["getValue"](self)
                    assert self.validateValue(controls[c]["type"], controls[c]["len"], value), "function getValue on " + controls[c]["type"] + " control returned value that doesn't match requirements"
                    controls[c]["value"] = value

        self.inputList = sorted([x for x in controls.keys() if controls[x]["isInput"]])
        self.selectedInput = 0 if len(self.inputList) > 0 else None

    @staticmethod
    def validateValue(type, length, value):
        if type == "toggle":
            return isinstance(value, bool)
        if type == "radio":
            return isinstance(value, int) and value >= 0 and value < length
        if type == "binary":
            return isinstance(value, int) and value >= 0 and value < (1<<length)
        return True
        
    def renderForDisplay(self):
        view = [(x if x != '.' else '0') for x in self.template]
        blinkState = running_time()//100 % 8 == 0

        for cont in self.controls.values():
            if cont["isInput"] == False:
                value = cont["getValue"](self)
                assert self.validateValue(cont["type"], cont["len"], value), "function getValue on " + cont["type"] + " returned value that doesn't match requirements"
                cont["value"] = value
        
        for (letter, cont) in self.controls.items():
            isSelected = self.selectedInput != None and self.inputList[self.selectedInput] == letter
            if blinkState and isSelected:
                for pos in cont["positions"]:
                    view[pos] = '5' if cont["type"] != "button" else '9'
            else:
                if cont["type"] == "button":
                    normalBlink = str(1 + abs(4 - (running_time()//200 % 8)))
                    for pos in cont["positions"]:
                        view[pos] = normalBlink
                    continue
                thisState = cont["value"]
                if cont["type"] == "toggle":
                    for pos in cont["positions"]:
                        view[ pos ] = '7' if thisState else '2'
                elif cont["type"] == "radio":
                    for (i, pos) in enumerate(cont["positions"]):
                        view[pos] = '7' if i == thisState else '2'
                elif cont["type"] == "binary":
                    for (i, pos) in enumerate(cont["positions"]):
                        view[pos] = '7' if thisState & (1<<(len(cont["positions"]) - i - 1)) else '2'

        return "".join(view)

    def nextControl(self):
        if self.selectedInput == None:
            return
        self.selectedInput = (self.selectedInput + 1) % len(self.inputList)

    def changeSelectedControl(self):
        if self.selectedInput == None:
            return
        cont = self.controls[self.inputList[self.selectedInput]]
        if cont["type"] == "button":
            cont["callback"](self)
            return
        elif cont["type"] == "toggle":
            cont["value"] = not cont["value"]
        elif cont["type"] == "radio":
            cont["value"] = (cont["value"]+1)%cont["len"]
        elif cont["type"] == "binary":
            cont["value"] = (cont["value"]+1)%(1<<cont["len"])
        if cont["callback"] != None:
            cont["callback"](self, cont["value"])
