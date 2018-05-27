from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.togglebutton import ToggleButton

from kivy.factory import Factory
from kivy.lang import Builder
from kivy_communication import logged_widgets

Builder.load_string("""
<ButtonDyslexia>:
  color: 1, 1, 1, 1
  size_hint_y: None
  height: '40dp'
  font_size: '18sp'
  font_name: 'fonts/the_font.ttf'
  on_press: app.press_help_button(self)
""")

class ButtonDyslexia(logged_widgets.LoggedButton):
  pass

Factory.register('KivyB', module='ButtonDyslexia')