# -*- coding: utf-8 -*-

import numpy as np
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy_classes import *
from kivy_communication import *

from kivy.properties import ListProperty, ObjectProperty, BooleanProperty


class ScreenRobotIntroduction (Screen):
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()
        #self.ids["tablet_id"].bind(text=self.ids["tablet_id"].on_text_change)
        #self.ids["group_id"].bind(text=self.ids["group_id"].on_text_change)
        #self.ids["subject_id"].bind(text=self.ids["subject_id"].on_text_change)

    def start_interaction(self):
        print(self.ids)

    def data_received(self, data):
        print ("ScreenRobotIntroduction: data_received", data)
        # self.the_app.screen_manager.current = 'ScreenAudience'
        print("end")
        #self.ids['callback_label'].text = data

    def show_screen(self, activity, activity_type):
        # activity: "activity1"/"activity2"
        # activity_type: "statement_1"/"statement_2"/"statement_3"/"statement_4"
        print("screen_robot_introduction", activity, activity_type)
        if (self.the_app.condition =='robot'):
            self.ids['intro_image'].source = 'images/introduction_robot.png'
            self.ids['intro_continue'].opacity = 0
            self.ids['intro_continue'].disabled = True
        elif (self.the_app.condition =='tablet'):
            self.ids['intro_image'].source = 'images/introduction_tablet.png'
