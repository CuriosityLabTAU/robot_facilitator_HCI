from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.uix.spinner import Spinner
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

Builder.load_string("""
<GridLayoutRobotator>:
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
<GridLayoutRobotator4>:
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
<GridLayoutRobotator3>:
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
<GridLayoutRobotator2>:
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

class GridLayoutRobotator(GridLayout):
  bcolor = ListProperty([235/255.0, 234/255.0,236/255.0,1])

class GridLayoutRobotator4(GridLayout):
  bcolor = ListProperty([235/255.0, 234/255.0,236/255.0,1])

class GridLayoutRobotator3(GridLayout):
  bcolor = ListProperty([235/255.0, 234/255.0,236/255.0,1])

class GridLayoutRobotator2(GridLayout):
  bcolor = ListProperty([235/255.0, 234/255.0,236/255.0,1])

Factory.register('KivyB', module='GridLayoutRobotator')
Factory.register('KivyB', module='GridLayoutRobotator4')
Factory.register('KivyB', module='GridLayoutRobotator3')
Factory.register('KivyB', module='GridLayoutRobotator2')