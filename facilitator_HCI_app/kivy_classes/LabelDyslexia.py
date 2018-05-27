from kivy.uix.label import Label
from kivy.properties import ListProperty

from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<LabelDyslexia>:
  bcolor: 235/255.0, 234/255.0,236/255.0, 1
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

class LabelDyslexia(Label):
  bcolor = ListProperty([1, 1, 1 ,1])

Factory.register('KivyB', module='LabelDyslexia')