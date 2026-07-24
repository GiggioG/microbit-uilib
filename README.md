# microbit-uilib
Simple ui-library for micro:bit's 5x5 screen with 10 brightness values per "pixel'

## TODO:
* [ ] javascript version
* [ ] better example usage
* [ ] optimise so it uses less memory

## Python API:
A UI screen is created with the `UI` constructor:
```python
def __init__(self, controls, template, initFunc=None):
```
It takes a dictionary of controls with their corresponding letters in the template, a template for how they are placed,
and an optional function for initial setup.

### Template syntax
The `template` argument is a string, corresponding to the `microbit.Image()` constructor's syntax: five groups of five
digits, separated by `:`. The rules are the following:
* Digits are static and correspond 1:1 to `microbit.Image()` brightnesses
* You can use `.` instead of `0` for clarity
* Capital and lowercase latin letters express controls, and each unique letter (lower and uppercase are considered
  differenct) is a unique control

Example template:
```python
"r.r.r:"
".....:"
".B.X.:"
".B...:"
".B.t."
```
Here, the three `r`'s are a part of the same control, despite not being connected. So are the `B`'s. The `X` and `t` are
separate.

### Types of controls
There are 4 types of controls, and 3 of them can also be used to display information.

* Radio control
    The `radio` control is like a radio button. Each pixel it occupies is a possible state, and only one can be on at a
    time. Its numerical value is the index of the pixel that is currently on (when looking linewise from top to bottom,
    left to right).
* Binary control
    The `binary` control represents a binary value. Each pixel is a seperate bit, and cycling it allows for every
    possible combination of the values (from 0 to 2^n-1, where n is the number of bits). The last bit (linewise top to
    bottom, left to right) is the **least** significant. Its numerical value is the number, represented in binary on the
    display.
* Toggle control
    The `toggle` control is a simple on-off toggle. All of its pixels behave together, and all show its value. Its representation is a boolean value, and the LEDs glowing represents `True`.
* Button control
    The `button` control is the only one that can't be used as an output. When not selected, it glows by slowly changing
    brightness. Clicking it activates its `callback` function.

When a control is set as an input, it can be selected by the user, and blinks when selected.

### Setting controls
In the `controls` dictionary of the `UI` constructor, **the keys are the letters from the template**, and **the values
are the control description**. Each description has the following fields

| Value | Type | Required | Description |
|-------|------|----------|-------------|
|`type` | "radio" \| "binary" \| "toggle" \| "button" | Yes | The type of control. |
|`isInput`| bool | Yes | Whether the control is selectable by the user and suceptable to change from them. For buttons should be always `True` |
|`callback` | function \| None | Only when `isInput` is `True` | A function that is called with the `UI` as its first argument and, if it's not a button, the control's new value as a second argument. It is called each time a control is interacted with (changed/pressed). *Notice that simply selecting a control doesn't count as interacting with it.* It is allowed to be `None` only when the input isn't a button. |
|`initial` | int \| bool | When `isInput` is `True` and it's not a `button` | An initial value for the control, before the user changes it. It should match the range that the control's size on the template imposes. |
|`getValue` | function | When `isInput` is `False` | A function that is called each screen refresh to update the value that is displayed. |

### Using the UI class
The class provides several other methods that are supposed to integrate with the _micro:bit_'s interface.
* The `renderForDisplay` method returns a string, that can be used with `display.show(microbit.Image(...))`. It is 5
  groups of 5 digits (representing brightness), each group separated by `:`.
* The `nextControl` method changes which control is currently selected, and if there are no selectable ones, it does
  nothing. The order is by ascii codes of the key letters in the template.
* The `interactWithControl` method is used to interact with the currently selected control. It increments binary and
  radio inputs, flips the toggles and clicks the buttons.

### Example usage
You can see simple demonstration of the controls in `example-simple.py`, and an example of a page system using this
library in `example-pages.py`.
