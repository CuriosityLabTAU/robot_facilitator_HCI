# -*- coding: utf-8 -*-

from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.spinner import SpinnerOption
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ListProperty, ObjectProperty, BooleanProperty
from SpinnerOptionDyslexia import SpinnerOptionDyslexia
from kivy.uix.gridlayout import GridLayout
from kivy_communication import logged_widgets
#from kivy_communication import *


Builder.load_string("""
<SpinnerDyslexia>:
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: self.pos
            size: self.size
    font_size: '18sp'
    font_name: 'fonts/the_font.ttf'
    height: '40dp'
    on_text: app.mistake_type_selected(self)

""")


class SpinnerDyslexia(logged_widgets.LoggedSpinner):
    pass

Factory.register('KivyB', module='SpinnerDyslexia')