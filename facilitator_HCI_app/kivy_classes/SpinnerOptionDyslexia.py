# -*- coding: utf-8 -*-

from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.spinner import SpinnerOption

from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_string("""
<SpinnerOptionDyslexia>:
    font_name: "fonts/the_font.ttf"
    font_size: '18sp'
    height: '40px'
""")

class SpinnerOptionDyslexia(SpinnerOption):
    pass

Factory.register('KivyB', module='SpinnerOptionDyslexia')