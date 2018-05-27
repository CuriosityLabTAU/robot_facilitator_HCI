from kivy.uix.label import Label
from kivy.properties import ListProperty

from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<LabelHeadingDyslexia>:
  bcolor: 1, 164/255.0, 15/255.0,1
  color: 0, 0, 0, 1
  size_hint_y: None
  height: '40dp'
  font_size: '18sp'
  font_name: 'fonts/the_font.ttf'
  text_size: self.width * 0.87, self.height
  halign: 'right'
  canvas.before:
    Color:
      rgba: self.bcolor
    Rectangle:
      pos: self.pos
      size: self.size
""")

class LabelHeadingDyslexia(Label):
  bcolor = ListProperty([1, 1, 1 ,1])

Factory.register('KivyB', module='LabelHeadingDyslexia')