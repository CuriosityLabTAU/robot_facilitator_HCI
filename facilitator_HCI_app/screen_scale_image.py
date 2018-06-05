# -*- coding: utf-8 -*-

import numpy as np
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy_classes import *
from kivy_communication import *
import json

from kivy.properties import ListProperty, ObjectProperty, BooleanProperty


class ScreenScaleImage (Screen):
    the_app = None
    activity6_statements = {"statement_1": ":שמחל תחא ןיב 'תכרעמה בצמ לש תוארנ' הקיטסירויה תא וגרד",
                            "statement_2": ":שמחל תחא ןיב 'יתימאה םלועל תכרעמה ןיב המאתה' הקיטסירויה תא וגרד",
                            "statement_3": ":שמחל תחא ןיב 'םיטרדנטסו תויבקע' הקיטסירויה תא וגרד",
                            "statement_4": ":שמחל תחא ןיב 'תכרעמה בצמ לש תוארנ' הקיטסירויה תא וגרד"}
    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()
        #self.ids["tablet_id"].bind(text=self.ids["tablet_id"].on_text_change)
        #self.ids["group_id"].bind(text=self.ids["group_id"].on_text_change)
        #self.ids["subject_id"].bind(text=self.ids["subject_id"].on_text_change)

    def start_interaction(self):
        print(self.ids)

    def data_received(self, data):
        print ("ScreenRegister: data_received", data)
        # self.the_app.screen_manager.current = 'ScreenAudience'
        print("end")
        #self.ids['callback_label'].text = data

    def on_btn_done(self):
        print("screen_scale_image on_btn_done")
        if (self.the_app.condition == 'robot'):
            mark_list = []
            for ids in self.ids:
                if 'check' in ids:
                    if self.ids[ids].active:
                        mark_list.append(ids)
            KL.log.insert(action=LogAction.press, obj='btn_continue', comment=json.dumps(mark_list))
        elif (self.the_app.condition == 'tablet'):
            if (self.current_statement < len(self.activity6_statements)):
                self.show_screen(self.activity, "statement_" + str(self.current_statement + 1))

    def show_screen(self,activity,activity_type):
        # activity: "activity6"
        # activity_type: "statement_1"/"statement_2"/"statement_3"/"statement_4"
        for ids in self.ids:
            if 'check' in ids:
                self.ids[ids].active = False
        self.activity = activity
        self.current_statement = int(activity_type[10:])
        self.ids['label_instructions'].text = self.activity6_statements[activity_type]
        self.ids['timer_time'].start_timer(int(120))
