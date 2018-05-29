from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.togglebutton import ToggleButton

from kivy.factory import Factory
from kivy.lang import Builder
from kivy_communication import logged_widgets

Builder.load_string("""
<ButtonRobotator>:
  color: 1, 1, 1, 1
  size_hint: None, None
  height: '40dp'
  width: '80dp'
  font_size: '20sp'
  font_name: 'fonts/the_font.ttf'
  background_color: 0.5,0.5,0.5,1
  background_normal: ''
  on_press: app.on_btn_done()
""")

class ButtonRobotator(logged_widgets.LoggedButton):
  pass

Factory.register('KivyB', module='ButtonRobotator')