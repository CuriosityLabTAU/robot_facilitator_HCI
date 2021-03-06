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

    activity_statements = {"activity1":  ":םינוש דעי ילהק 3 ומשיר",
                            "activity3": ":תורופאטמ יגוס 3 ומשיר",
                            "activity5": ":םיקשממ יגוס 3 ומשיר"}
    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()

        # this bind is from the HebrewManager, to change the text order as it is printed
        # self.ids['text_input_1'].bind(text=HebrewManagement.text_change)
        # self.ids['text_input_2'].bind(text=HebrewManagement.text_change)
        # self.ids['text_input_3'].bind(text=HebrewManagement.text_change)
        # self.ids['text_input_4'].bind(text=HebrewManagement.text_change)
        # self.ids['text_input_5'].bind(text=HebrewManagement.text_change)

        # this bind is from the kivy_logger.py in order to log the text
        self.ids['text_input_1'].bind(text=self.ids['text_input_1'].on_text_change)
        self.ids['text_input_2'].bind(text=self.ids['text_input_2'].on_text_change)
        self.ids['text_input_3'].bind(text=self.ids['text_input_3'].on_text_change)
        self.ids['text_input_4'].bind(text=self.ids['text_input_4'].on_text_change)
        self.ids['text_input_5'].bind(text=self.ids['text_input_5'].on_text_change)

        self.number_done = 0
        self.activity = 'activity1'

    def on_enter(self, *args):
        pass


    def disable_screen(self):
        for id_i in self.ids:
            self.ids[id_i].disabled = True
        if self.the_app.condition == 'tablet':
            self.ids['btn_done'].disabled = False

    def on_btn_done(self, **kwargs):
        # called when the user clicks
        print ("screen_create_list: on_btn_done")
        if (self.the_app.condition == 'tablet'):   #todo: on tablet condition think what to do here...
            self.next_activity()
            # if self.number_done == 0:
            #     text = '2 רפסמ טלבאט לע תיתצובק המישר וניכהו ומייסי םלוכש וכח'
            #     self.ids['label_instructions'].text = text
            #     print("tablet_id",self.the_app.tablet_id)
            #     if (self.the_app.tablet_id != '2'):
            #         self.disable_screen()
            #     else:
            #         self.show_screen(self.activity, 'group')
            #     self.number_done += 1
            # else:
            #     self.next_activity()

    def next_activity(self):
        self.the_app.screen_manager.current = 'ScreenActivityIntroduction'
        if '1' in self.activity and 'individual' in self.activity_type:
            self.the_app.screen_manager.current_screen.show_screen('activity1', 'group')
        elif '1' in self.activity and 'group' in self.activity_type:
            self.the_app.screen_manager.current_screen.show_screen('activity2', 'individual')
        elif '3' in self.activity and 'individual' in self.activity_type:
            self.the_app.screen_manager.current_screen.show_screen('activity3', 'group')
        elif '3' in self.activity and 'group' in self.activity_type:
            self.the_app.screen_manager.current_screen.show_screen('activity4', 'individual')
        elif '5' in self.activity and 'individual' in self.activity_type:
            self.the_app.screen_manager.current_screen.show_screen('activity5', 'group')
        elif '5' in self.activity and 'group' in self.activity_type:
            self.the_app.screen_manager.current_screen.show_screen('activity6', 'individual')

    def data_received(self, data):
        print ("ScreenCreateList: data_received", data)
        # self.the_app.screen_manager.current = 'ScreenAudience'
        print("end")
        #self.ids['callback_label'].text = data

    def show_screen(self, activity, activity_type):
        print ("screen_create_list: show_screen ", activity, activity_type)
        self.activity = activity
        self.activity_type = activity_type
        self.update_label(activity,activity_type)
        if activity_type == "group":
            text = '2 רפסמ טלבאט לע תיתצובק המישר וניכהו ומייסי םלוכש וכח'
            self.ids['label_instructions'].text = text
            print("tablet_id", self.the_app.tablet_id)
            if (self.the_app.tablet_id != '2'):
                self.disable_screen()
            else:
                self.ids['text_input_4'].opacity = 1
                self.ids['text_input_5'].opacity = 1
                self.ids['text_input_1'].disabled = True
                self.ids['text_input_2'].disabled = True
                self.ids['text_input_3'].disabled = True
                self.ids['text_input_4'].disabled = False
                self.ids['text_input_5'].disabled = False

        elif activity_type == "individual":
            self.ids['text_input_4'].opacity = 0
            self.ids['text_input_5'].opacity = 0

    def update_label(self, activity, activity_type):
        print("screen_create_list: start_activity", activity)
        if (activity_type == 'group'):
            if (self.the_app.tablet_id != '2'):
                self.ids['label_instructions'].text = '2 רפסמ טלבאט לע תיתצובק המישר וניכה'
            else:
                self.ids['label_instructions'].text = ' תיתצובק המישר וניכה'
        elif (activity_type == 'individual'):
            self.ids['label_instructions'].text = self.activity_statements[activity]
        self.show_buttons('continue')
        self.ids['timer_time'].start_timer(int(120))

    def show_buttons(self, which):
        # call from manager
        # which = agree_disagree / continue
        if ("agree" in which):
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