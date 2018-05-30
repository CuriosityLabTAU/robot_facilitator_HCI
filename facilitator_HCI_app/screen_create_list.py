# -*- coding: utf-8 -*-

import numpy as np
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy_classes import *
from kivy_communication import *
from hebrew_management import *
from kivy.properties import ListProperty, ObjectProperty, BooleanProperty


class ScreenCreateList (Screen):
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()

        # this bind is from the HebrewManager, to change the text order as it is printed
        self.ids["text_input_1"].bind(text=HebrewManagement.text_change)
        self.ids["text_input_2"].bind(text=HebrewManagement.text_change)
        self.ids["text_input_3"].bind(text=HebrewManagement.text_change)
        self.ids["text_input_4"].bind(text=HebrewManagement.text_change)
        self.ids["text_input_5"].bind(text=HebrewManagement.text_change)

        # this bind is from the kivy_logger.py in order to log the text
        self.ids["text_input_1"].bind(text=self.ids["text_input_1"].on_text_change)
        self.ids["text_input_2"].bind(text=self.ids["text_input_2"].on_text_change)
        self.ids["text_input_3"].bind(text=self.ids["text_input_3"].on_text_change)
        self.ids["text_input_4"].bind(text=self.ids["text_input_4"].on_text_change)
        self.ids["text_input_5"].bind(text=self.ids["text_input_5"].on_text_change)
        self.start_activity()

    def start_activity(self):
        session = self.the_app.session
        if (session =='session1'):
            activity = "activity1"
        elif (session == 'session3'):
            activity = "activity5"
        if (activity=="activity1"):
            self.ids["label_instructions"].text = ":םינוש דעי ילהק 5 ומשיר"
        elif (activity=="activity5"):
            self.ids["label_instructions"].text = ":םיקשממ יגוס 3 ומשיר"
        self.ids['timer_time'].start_timer(int(120))

    def show_buttons(self):
        self.ids['btn_agree'].opacity = 1
        self.ids['btn_disagree'].opacity = 1
        self.ids['btn_done'].opacity = 0
        self.ids['btn_agree'].disabled = False
        self.ids['btn_disagree'].disabled = False
        self.ids['btn_done'].disabled = True
    
    def on_btn_done(self, **kwargs):
        print ("btn done screen create list pressed")


    def data_received(self, data):
        print ("ScreenCreateList: data_received", data)
        # self.the_app.screen_manager.current = 'ScreenAudience'
        print("end")
        #self.ids['callback_label'].text = data