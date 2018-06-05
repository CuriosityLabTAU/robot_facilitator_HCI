# -*- coding: utf-8 -*-

import numpy as np
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy_classes import *
from kivy_communication import *
from screen_register import *
from screen_create_list import *
from screen_scale_image import *
from screen_mark_list_image import *
from screen_robot_introduction import *
from kivy.clock import *


from kivy.properties import ListProperty, ObjectProperty, BooleanProperty

class MyScreenManager(ScreenManager):
    the_app = None

class TimerLabel(Label):
    time = -1
    def start_timer(self, duration=5):
        self.stop_timer()
        print("start_timer?")
        if (self.time>-1): # in case the timer was already on, unschedule it
            Clock.unschedule(self.event)

        self.time = duration
        self.event = Clock.schedule_interval(self.advance, 1)
        min,sec = divmod(duration, 60)
        str_time = "%d:%02d" % (min, sec)
        self.text = str_time

    def stop_timer(self):
        try:
            Clock.unschedule(self.event)
            self.time = -1
            self.text = ""
        except:
            print ("stop timer failed")

    def advance(self, dt):
        min, sec = divmod(self.time, 60)
        str_time = "%d:%02d ראשנ ןמז " % (min, sec)
        #print("self.time", self.time, str_time)
        self.text = str_time
        if self.time <= 0:
            Clock.unschedule(self.event)
            self.text = 'ןמזה רמגנ'
        else:
            self.time -= 1

class RobotatorHCIApp(App):
    #Robotator
    def build(self):
        self.the_app = self
        Builder.load_file("robotatorHCI.kv")
        self.basic_server_ip = '192.168.0.10'
        self.server_ip_end = 0
        self.tablet_id = 0
        self.condition = 'tablet'
        self.session = 'session1'
        self.screen_manager = MyScreenManager()
        screen_register = ScreenRegister(self)
        screen_mark_list_image = ScreenMarkListImage(self)
        screen_create_list = ScreenCreateList(self)
        screen_scale_image = ScreenScaleImage(self)
        screen_robot_introduction = ScreenRobotIntroduction(self)
        self.screen_manager.add_widget(screen_register)
        self.screen_manager.add_widget(screen_create_list)
        self.screen_manager.add_widget(screen_mark_list_image)
        self.screen_manager.add_widget(screen_scale_image)
        self.screen_manager.add_widget(screen_robot_introduction)

        #self.screen_manager.current = 'ScreenCreateList'  #'ScreenRegister'
        #self.screen_manager.current_screen.show_screen('activity1', 'individual')

        #self.screen_manager.current = 'ScreenMarkListImage'
        #self.screen_manager.current_screen.show_screen('activity2', 'statement_1')

        # self.screen_manager.current = 'ScreenScaleImage'
        # self.screen_manager.current_screen.show_screen('activity6', 'statement_1')

        self.screen_manager.current = 'ScreenRegister'
        #self.screen_manager.current = 'ScreenRobotIntroduction'


        #self.screen_manager.current_screen.start_activity()

        self.try_connection()
        return self.screen_manager

    # ==========================================================================
    # ==== communicatoin to twisted server  KC: KivyClient KL: KivyLogger=====
    # ==========================================================================

    def try_connection(self):
        server_ip = self.basic_server_ip + str(self.server_ip_end)
        KC.start(the_parents=[self], the_ip=server_ip)  # 127.0.0.1
        KL.start(mode=[DataMode.file, DataMode.communication, DataMode.ros], pathname=self.user_data_dir,
                 the_ip=server_ip)

    def failed_connection(self):
        print("failed_connection", self.server_ip_end)
        self.server_ip_end += 1
        if self.server_ip_end < 10:
            self.try_connection()
        else:
           self.screen_manager.get_screen('ScreenRegister').ids['callback_label'].text = 'stand alone ' + str(self.server_ip_end)

    def success_connection(self):
        self.server_ip_end = 99
        # self.screen_manager.current = 'Screen2'

    def on_connection(self):
        KL.log.insert(action=LogAction.data, obj='HCIApp', comment='start')
        print("the client status on_connection ", KC.client.status)
        if (KC.client.status == True):
            self.screen_manager.get_screen('ScreenRegister').ids['callback_label'].text = 'connected'

    def select_condition(self,toggle_inst):
        print("select_condition",toggle_inst.text)
        self.condition = toggle_inst.text
        KL.log.insert(action=LogAction.data, obj='select_condition', comment=str(toggle_inst.text))

    def select_session(self, toggle_inst):
        print("select_session", toggle_inst.text)
        self.session = toggle_inst.text
        KL.log.insert(action=LogAction.data, obj='select_session', comment=str(toggle_inst.text))

    def register_tablet(self):
        print("trying to register tablet. KC.client.status is ", KC.client.status)
        self.tablet_id = self.screen_manager.current_screen.ids['tablet_id'].text
        group_id = self.screen_manager.current_screen.ids['group_id'].text
        message = {'tablet_to_manager': {'action': 'register_tablet',
                                         'parameters': {'group_id': group_id, 'tablet_id': self.tablet_id,
                                                        'condition': self.condition,
                                                        'session': self.session}}}
        #if KC.client.status == True:
        if self.condition == 'robot':
            message_str = str(json.dumps(message))
            print("register_tablet", message_str)
            KC.client.send_message(message_str)
        elif self.condition =='tablet':
            if (self.session == 'session1'):
                self.screen_manager.current = 'ScreenRobotIntroduction'
                self.screen_manager.current_screen.show_screen('introduction', 'individual')
            elif (self.session =='session2'):
                self.screen_manager.current = 'ScreenCreateList'
                self.screen_manager.current_screen.show_screen('activity3', 'individual')
            elif (self.session =='session3'):
                self.screen_manager.current = 'ScreenCreateList'
                self.screen_manager.current_screen.show_screen('activity5', 'individual')

    def data_received(self, data):
        print ("robotator_app: data_received", data)
        self.screen_manager.get_screen('ScreenRegister').ids['callback_label'].text = data
        try:
            json_data = [json.loads(data)]
        except:
            json_data = []
            spl = data.split('}{')
            print(spl)
            for k in range(0, len(spl)):
                the_msg = spl[k]
                if k > 0:
                    the_msg = '{' + the_msg
                if k < (len(spl) - 1):
                    the_msg = the_msg + '}'
                json_msg = json.loads(the_msg)
                json_data.append(json_msg)
                # print("data_received err", sys.exc_info()) v

        for data in json_data:
            print("data['action']", data['action'])
            if (data['action'] == 'registration_complete'):
                self.screen_manager.get_screen('ScreenRegister').data_received(data)
                print("registration_complete")

            if (data['action'] == 'show_screen'):
                print(data)
                self.screen_manager.current = data['screen_name']
                self.screen_manager.current_screen.show_screen(data['activity'],data['activity_type'])

                #if 'parameters' in data:
                #    self.screen_manager.current_screen.show_screen(data['parameters'])

                if 'role' in data:
                    self.screen_manager.current_screen.update_role_bias(role=data['role'], bias=int(data['bias']))

            if (data['action'] == 'start_timer'):
                self.screen_manager.current_screen.ids['timer_time'].start_timer(int(data['seconds']))

            if data['action'] == 'set_widget_text':
                self.screen_manager.current_screen.ids[data['widget_id']].text = data['text']

            if data['action'] == 'show_buttons':
                self.screen_manager.current_screen.show_buttons(data['which'])
                #self.screen_manager.current_screen.show_buttons()

            if data['action'] == 'disable_screen':
                self.screen_manager.current_screen.disable_screen()

    # ==========================================================================
    # Interaction in ScreenCreateList
    # ==========================================================================

    def on_btn_done(self,**kwargs):
        print ("btn done screen create list pressed")
        self.screen_manager.current_screen.on_btn_done()


    # ==========================================================================
    # Interaction in ScreenDyslexia
    # ==========================================================================

    def mistake_type_selected(self,spinner_inst):
        # the student picked mistake type. update the relevant variables
        self.screen_manager.get_screen('ScreenDyslexia').mistake_type_selected(spinner_inst)

    def press_help_button(self,btn_inst):
        print("press_help_button",btn_inst.id)
        self.screen_manager.get_screen('ScreenDyslexia').press_help_button(btn_inst)

    def press_close_help(self):
        print("press_close_help")
        self.screen_manager.get_screen('ScreenDyslexia').press_close_help()

    def change_tab(self, tab_name):
        # student clicked on one of the menu tabs ('single'/'tefel'/'summary')
        print ('state:', 'screen_name', tab_name)
        self.screen_manager.get_screen('ScreenDyslexia').change_tab(tab_name)

if __name__ == "__main__":
    RobotatorHCIApp().run()  # the call is from main.py