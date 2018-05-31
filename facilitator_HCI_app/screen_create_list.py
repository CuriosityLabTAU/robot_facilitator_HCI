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


    #def on_enter(self, *args):
    #    self.start_activity()

    def start_activity(self, activity, activity_type):
        print("screen_create_list: start_activity", activity)
        if (activity=="activity1"):
            print("in")
            self.ids["label_instructions"].text = ":םינוש דעי ילהק 3 ומשיר"
        elif (activity=="activity3"):
            self.ids["label_instructions"].text = ":תורופאטמ יגוס 3 ומשיר"
        elif (activity=="activity5"):
            self.ids["label_instructions"].text = ":םיקשממ יגוס 3 ומשיר"
        self.show_buttons('continue')
        self.ids['timer_time'].start_timer(int(120))


    def show_buttons(self, which):
        #which = agree_disagree / continue
        if (which =='agree_disagree'):
            self.ids['btn_agree'].opacity = 1
            self.ids['btn_disagree'].opacity = 1
            self.ids['btn_done'].opacity = 0
            self.ids['btn_agree'].disabled = False
            self.ids['btn_disagree'].disabled = False
            self.ids['btn_done'].disabled = True
        elif (which == 'continue'):
            self.ids['btn_agree'].opacity = 0
            self.ids['btn_disagree'].opacity = 0
            self.ids['btn_done'].opacity = 1
            self.ids['btn_agree'].disabled = True
            self.ids['btn_disagree'].disabled = True
            self.ids['btn_done'].disabled = False

    def disable_tablet(self):
        for id_i in self.ids:
            self.ids[id_i].disabled = True

    def on_btn_done(self, **kwargs):
        print ("btn done screen create list pressed")
        if (self.the_app.condition == 'Robot'):   #todo: on tablet condition think what to do here...
            text = '2 רפסמ טלבאט לע תיתצובק המישר וניכה ונייסי םלוכש וקח'
            self.ids['label_instructions'].text = text
            print("tablet_id",self.the_app.tablet_id)
            if (self.the_app.tablet_id != '2'):
                self.disable_tablet()

    def reverse_text(self,text):
        return str((str(text)[::-1]))

    def data_received(self, data):
        print ("ScreenCreateList: data_received", data)
        # self.the_app.screen_manager.current = 'ScreenAudience'
        print("end")
        #self.ids['callback_label'].text = data

    def show_screen(self, activity, activity_type):
        print ("screen_create_list: show_screen ", activity, activity_type)
        self.start_activity(activity,activity_type)

        if activity_type == "group":
            # RINAT
            self.ids['label_instructions'].text = '2 רפסמ טלבאט לע תיתצובק המישר וניכה'

            if (self.the_app.tablet_id == '2'):
                self.ids['text_input_4'].opacity = True
                self.ids['text_input_5'].opacity = True

        elif activity_type == "individual":
            self.ids['text_input_4'].opacity = False
            self.ids['text_input_5'].opacity = False
