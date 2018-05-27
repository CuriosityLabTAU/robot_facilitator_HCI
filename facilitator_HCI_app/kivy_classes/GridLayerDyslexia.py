from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.uix.spinner import Spinner
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

Builder.load_string("""
<GridLayoutDyslexia>:
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: self.pos
            size: self.size
    id: gridlayout
    cols: 5
    rows: 200
    spacing: 2
    size_hint_y: None
    padding: '50dp'
    height: self.minimum_height
    size_hint_x: 1
""")

Builder.load_string("""
<GridLayoutDyslexia4>:
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: self.pos
            size: self.size
    id: gridlayout
    cols: 4
    rows: 200
    spacing: 2
    size_hint_y: None
    padding: '50dp'
    height: self.minimum_height
    size_hint_x: 1
""")

Builder.load_string("""
<GridLayoutDyslexia3>:
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: self.pos
            size: self.size
    id: gridlayout
    cols: 3
    rows: 200
    spacing: 2
    size_hint_y: None
    padding: '50dp'
    height: self.minimum_height
    size_hint_x: 1
""")


Builder.load_string("""
<GridLayoutDyslexia2>:
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: self.pos
            size: self.size
    id: gridlayout
    cols: 2
    rows: 200
    spacing: 2
    size_hint_y: None
    padding: '50dp'
    height: self.minimum_height
    size_hint_x: 1
""")

class GridLayoutDyslexia(GridLayout):
  bcolor = ListProperty([235/255.0, 234/255.0,236/255.0,1])

class GridLayoutDyslexia4(GridLayout):
  bcolor = ListProperty([235/255.0, 234/255.0,236/255.0,1])

class GridLayoutDyslexia3(GridLayout):
  bcolor = ListProperty([235/255.0, 234/255.0,236/255.0,1])

class GridLayoutDyslexia2(GridLayout):
  bcolor = ListProperty([235/255.0, 234/255.0,236/255.0,1])

Factory.register('KivyB', module='GridLayoutDyslexia')
Factory.register('KivyB', module='GridLayoutDyslexia4')
Factory.register('KivyB', module='GridLayoutDyslexia3')
Factory.register('KivyB', module='GridLayoutDyslexia2')