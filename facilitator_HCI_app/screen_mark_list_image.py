# -*- coding: utf-8 -*-

import numpy as np
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy_classes import *
from kivy_communication import *

from kivy.properties import ListProperty, ObjectProperty, BooleanProperty


class ScreenMarkListImage (Screen):
    the_app = None

    def __init__(self, the_app):
        self.the_app = the_app
        super(Screen, self).__init__()
        #self.ids["tablet_id"].bind(text=self.ids["tablet_id"].on_text_change)
        #self.ids["group_id"].bind(text=self.ids["group_id"].on_text_change)
        #self.ids["subject_id"].bind(text=self.ids["subject_id"].on_text_change)

    def on_enter(self, *args):
        #init the check boxes if marked previously
        for ids in self.ids:
            if 'check' in ids:
                self.ids[ids].active = False

    def start_interaction(self):
        print(self.ids)

    def data_received(self, data):
        print ("ScreenRegister: data_received", data)
        # self.the_app.screen_manager.current = 'ScreenAudience'
        print("end")
        #self.ids['callback_label'].text = data

    def on_btn_done(self):
        mark_list = []
        for ids in self.ids:
            if 'check' in ids:
                if self.ids[ids].active:
                    mark_list.append(ids)
        KL.log.insert(action=LogAction.press, obj='btn_continue', comment=str(mark_list))

    def show_screen(self, parameters):
        for ids in self.ids:
            if 'check' in ids:
                self.ids[ids].active = False
        # parameters[0] = 'statement_1' ==> from json
        self.ids['label_instructions'].text = parameters[0] # RINAT TODO