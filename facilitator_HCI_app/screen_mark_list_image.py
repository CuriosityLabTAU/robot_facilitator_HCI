# -*- coding: utf-8 -*-

import numpy as np
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy_classes import *
from kivy_communication import *
from kivy.core.window import Window
import json

from kivy.properties import ListProperty, ObjectProperty, BooleanProperty


class ScreenMarkListImage (Screen):
    the_app = None
    screen_2_positions = ((0.918 , 0.893),(0.918 , 0.773),(0.918 , 0.653),(0.918 , 0.533),(0.918 , 0.413),(0.918 , 0.293),(0.918 , 0.173),(0.918 , 0.053))
    screen_4_positions = ((0.817 , 0.476), (0.835 , 0.368), (0.587 , 0.341), (0.400 , 0.365), (0.655 , 0.62), (0.528 , 0.841), (0.832 , 0.909), (0.184 , 0.428))

    activity2_statements = {"statement_1": ":רושיאה תייטה םע תולאשה תא ונמס",
                           "statement_2": ":ןווקמ ןולאשל תומיאתמש תולאשה תא ונמס",
                           "statement_3": ":דוקימ תצובקל תומיאתמש  תולאשה תא ונמס",
                           "statement_4": "ךתעדל רתויב תובוטה תולאשה שמח תא ונמס"}

    activity4_statements = {"statement_1": ":הרישי הייחנהל םימיאתמש םיביכרמה תא ונמס",
                           "statement_2": ":ןוילע רושייל םימיאתמש םיביכרמה תא ונמס",
                           "statement_3": ":זוכרמל םימיאתמש םיביכרמה תא ונמס",
                           "statement_4": "'פירס ןס' טנופל םימיאתמש םיביכרמה תא ונמס"}


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

        # self.show_screen('activity2','statement_1')

    def start_interaction(self):
        print(self.ids)

    def data_received(self, data):
        print ("ScreenRegister: data_received", data)
        # self.the_app.screen_manager.current = 'ScreenAudience'
        print("end")
        #self.ids['callback_label'].text = data

    def on_btn_done(self):
        print("screen_mark_list_image on_btn_done")
        if (self.the_app.condition == 'robot'):
            mark_list = []
            for ids in self.ids:
                if 'check' in ids:
                    if self.ids[ids].active:
                        mark_list.append(ids)
            KL.log.insert(action=LogAction.press, obj='btn_continue', comment=json.dumps(mark_list))
        elif (self.the_app.condition =='tablet'):
            self.show_next_statement()

    def show_next_statement(self):
        # this function is only called in the tablet condition. move to the next statement
        print("show_next_statement", self.activity, self.current_statement)
        if (self.activity=='activity2'):
            statements= self.activity2_statements
        elif (self.activity=='activity4'):
            statements= self.activity4_statements
        if (self.current_statement < len(statements)):
            self.show_screen(self.activity, "statement_"+str(self.current_statement+1))

    def show_screen(self, activity, activity_type):
        # activity: "activity1"/"activity2"
        # activity_type: "statement_1"/"statement_2"/"statement_3"/"statement_4"
        print("screen_mark_list_image show_screen", activity, activity_type)
        self.activity = activity
        self.activity_type = activity_type
        self.current_statement = int(activity_type[10:])
        if (activity =='activity2'):
            self.ids['label_instructions'].text = self.activity2_statements[activity_type]
        elif (activity=='activity4'):
            self.ids['label_instructions'].text = self.activity4_statements[activity_type]

        self.ids['screenshot'].source = 'images/' + activity + '.png'
        self.arrange_checkboxes(activity)
        self.ids['timer_time'].start_timer(int(120))

    def arrange_checkboxes(self, activity):
        #uncheck all the checkboxes
        for ids in self.ids:
            if 'check' in ids:
                self.ids[ids].active = False

        # change the positions of the checkboxes based on the activity
        if (activity=='activity2'):
            positions = self.screen_2_positions
        elif (activity=='activity4'):
            positions = self.screen_4_positions

        print("window.width", Window.width)

        # I used this code as the Window.width is known from the start.
        parent_width = Window.width * 0.9
        parent_height = Window.height * 0.8
        parent_x = Window.width * 0.05
        parent_y = Window.height * 0.1

        for i,pos in enumerate(positions,1):
            print('pos=',pos)
            self.ids['checkbox_'+str(i)].pos = parent_x + parent_width * pos[0], parent_y + parent_height * pos[1]
            print(self.ids['checkbox_'+str(i)].pos)

        # I didn't use the following code because we call this function before "on_enter" and the parent values are still not initiated
        # parent_width = self.ids['checkbox_1'].parent.width
        # parent_height = self.ids['checkbox_1'].parent.height
        # parent_x = self.ids['checkbox_1'].parent.x
        # parent_y = self.ids['checkbox_1'].parent.y