# Pager

With this module it is possible to create a kind of 'paged' screen with the Piface 2 CAD.

You can define multiple pages with a custom text on the first row of the LCD and custom actions which are assigned to the 5 push buttons.

A visual indication of these actions can be displayed in the second row of the LCD, either with a 1 letter label or a custom bitmap.

The rocker switch is used to cycle between pages (left = previous, right = next) and if you press the rocker switch it will display the first page.

## How to use
A full [example](/example_pager.py) is included in this repo. Here is an short overview:

### Page definition
The screen is defined with a list of dictionaries, in which every element describes one page, for example:

```python
pages = [{"text": "P0 (labels)",
              "actions": [{"label": "A", "action": "pager_example.actionA"},
                          {"label": "B", "action": "pager_example.actionB"},
                          {"label": "C", "action": "pager_example.actionC"},
                          {"label": "D", "action": "pager_example.actionD"},
                          {"bitmap": [0x4, 0xe, 0x15, 0x15, 0x11, 0xe, 0x0, 0x0], "action": "pager_example.standby"}]},
        {"text": "P2 with no actions",
         "actions": []},
        {"text": "P3 (less actions)",
         "actions": [{"label": "A", "action": "pager_example.actionA"},
                     {"label": "B", "action": "pager_example.actionB"},
                     {"label": "C", "action": "pager_example.actionC"}]}

             ]
```

- `text` is the title of the page, which is shown on the first row of the lcd.
- `actions` contain a list of action elements:
   - An action element contains either a `label` or a `bitmap` field which controls what is displayed in the bottom row of the lcd.
   - The `label` field contains a character.
   - The `bitmap` field defines a bitmap according to [here](http://pifacecad.readthedocs.io/en/latest/creating_custom_bitmaps.html).
   - The `action` field contains the full qualified name (module.(class).function) of a Python method which is executed when the pushbutton is pushed.
- All the actions are assigned to the buttons left to right, so action A is assigned to the left most button, action B to the second from left etc.
- It is also possible to have no actions (like `P2`) at all or another number of actions than 5 (like `P3`), but 5 is the maximum, there are only 5 pushbuttons available)

### Initializing and displaying pages
The pager is contained in `PagedScreen` class.

#### Initialize an instance:

`screen1 = PagedScreen(cad=initialized_pifacecad, pages=pagesList)`

- `cad` is an **already** initialized `pifacecad.PiFaceCAD()` object
- `pages` is the page definition like above

#### Display a page

`screen1.display(page=pageno)`

Displays page pageno (0 based)

#### Clean up

`screen1.clean_up()`

Cleans up resources (needs **always** to be called after finishing the application)

## Live example
[![Example](https://img.youtube.com/vi/cJd8QzbMm24/0.jpg)](http://www.youtube.com/watch?v=cJd8QzbMm24)
