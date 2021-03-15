# Pager

With this module it is possible to create a kind of 'paged' screen with the Piface 2 CAD.

You can define one or more pages: 
- A page with just 1 or 2 lines of text ('simple page')
- A page with a custom text on the first row of the LCD and custom actions which are assigned to the 5 push buttons ('action page')
  On the second row a visual indication of these actions can be displayed in the second row of the LCD, either with a 1 letter label or a custom bitmap.

The rocker switch is used to cycle between pages (left = previous, right = next) and if you press the rocker switch it will display the first page.

## How to use
A full [example](pager_example.py) is included in this repo. Here is a short overview:

### Page definition
The definition of a page consists of a `dictionary` of items:
- Simple page:
  ```python
  simple_page_def = {"line1": "This is line 1", "line2": "This is line 2"}
  ```
  - `line1` will show up on the first line of the LCD
  - `line2` will show up on the second line of the LCD
  
  Only the first 16 characters of a line will be displayed, the rest is ignored.


- Action page
  ```python
  action_page_def = {"text": "P0 (labels)",
                    "actions": [{"label": "A", "action": "pager_example.actionA"},
                                {"label": "B", "action": "pager_example.actionB"},
                                {"label": "C", "action": "pager_example.actionC"},
                                {"label": "D", "action": "pager_example.actionD"},
                                {"bitmap": [0x4, 0xe, 0x15, 0x15, 0x11, 0xe, 0x0, 0x0], "action": "pager_example.standby"}]},
  ```

- `caption` is the title of the page, which is shown on the first row of the lcd.
- `actions` contain a list of action elements:
   - An action element contains either a `label` or a `bitmap` field which controls what is displayed in the bottom row of the lcd.
   - The `label` field contains a character.
   - The `bitmap` field defines a bitmap according to [here](http://pifacecad.readthedocs.io/en/latest/creating_custom_bitmaps.html).
   - The `action` field contains the full qualified name (module.(class).function) of a Python method which is executed when the button is pushed.
- All the actions are assigned to the buttons left to right, so action A is assigned to the left most button, action B to the second from left etc.
- The maximum of actions is 5 since there are only 5 buttons available

### Initializing and displaying pages
The `PageController` class takes care of everything. 

#### Initialize an instance:
`page_controller = PageController(lcd_controller)`

-`lcd_controller` is an **already** initialized (but doesn't have to be `started` yet) [`PifaceController`](../lcd_control/piface_controller.py)  object

#### Add a page
`page_controller.add(content)`
- `content` is a dictionary containing the page definition as described above.
- This can only be called after the 'PifaceController' is started, otherwise you get undefined behaviour.

#### Display a page
`page_controller.display(page_index)`
- Displays page 'index' (0 based) or if argument is left out, the current page will be displayed

#### Update a page
`page_controller.update_page(page_index, new_content)`
- Updates page 'page_index' (0 based) or if argument is left out, the current page with new content as specified in 'new_content'

#### Clean up
`screen1.clean_up()`

Cleans up resources (needs **always** to be called after finishing the application)

## Live example
[![Example](https://img.youtube.com/vi/cJd8QzbMm24/0.jpg)](http://www.youtube.com/watch?v=cJd8QzbMm24)
