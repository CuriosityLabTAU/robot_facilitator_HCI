from kivy.uix.checkbox import CheckBox
from kivy.properties import ListProperty

from kivy.factory import Factory
from kivy.lang import Builder
from kivy_communication import logged_widgets


Builder.load_string("""
<CheckBoxRobotator>:
  bcolor: 235/255.0, 234/255.0,236/255.0, 1
  color: 0, 0, 0, 1
  size_hint_y: None
  height: '40dp'
  font_size: '18sp'
  font_name: 'fonts/the_font.ttf'
  canvas.before:
    Color:
      rgba: self.bcolor
    Rectangle:
      pos: self.pos
      size: self.size
""")
class CheckBoxRobotator(logged_widgets.LoggedCheckBox):
  bcolor = ListProperty([1, 1, 1 ,1])

Factory.register('KivyB', module='CheckBoxRobotator')