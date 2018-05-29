from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty

from kivy.factory import Factory
from kivy.lang import Builder
from kivy_communication import logged_widgets

Builder.load_string("""
<TextInputRobotator>:
    halign: 'right'
    text_size: self.width, self.height
    height: '50dp'
    size_hint_y: None
    multiline: False
    font_size: '20sp'
    text:""
    font_name: "fonts/the_font.ttf"
""")

class TextInputRobotator(logged_widgets.LoggedTextInput):
  pass

Factory.register('KivyB', module='TextInputRobotator')