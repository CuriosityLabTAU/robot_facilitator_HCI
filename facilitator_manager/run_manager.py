
import json
import rospy
from std_msgs.msg import String
import time
from threading import Timer
import threading
import random

class ManagerNode():

    number_of_tablets = 1
    tablets = {}    #in the form of {tablet_id_1:{"subject_id":subject_id, "tablet_ip";tablet_ip}
                                    #,tablet_id_2:{"subject_id":subject_id, "tablet_ip";tablet_ip}

    tablets_ips = {}
    tablets_ids = {}
    tablets_subjects_ids = {}

    tablet_audience_data = {}
    tablets_audience_agree = {}
    tablets_audience_done = {}  # by id
    count_audience_done = 0

    attention_tablet = {}
    listen_to_text = None
    text_audience_group = {}
    sleep_timer = None
    run_study_timer = None
    is_audience_done  = False

    waiting = False
    waiting_timer = False
    waiting_robot = False

    session = 'session1'
    robot_end_signal = {}
    tablets_done = {}
    tablets_agree = {}
    tablets_mark = {}
    tablets_continue = {}


    def __init__(self):
        print("init run_manager")
        self.robot_publisher = rospy.Publisher('to_nao', String, queue_size=10)
        self.tablet_publisher = rospy.Publisher('to_tablet', String, queue_size=10)
        rospy.init_node('manager_node') #init a listener:
        rospy.Subscriber('nao_state', String, self.callback_nao_state)
        rospy.Subscriber('tablet_to_manager', String, self.callback_to_manager)
        rospy.Subscriber('log', String, self.callback_log)
        self.waiting = False
        self.waiting_timer = False
        self.waiting_robot = False
        i=1
        while i <= self.number_of_tablets:
            self.tablets_audience_agree[i]= None
            i += 1

        print(self.tablets_audience_agree)

        self.robot_end_signal = {}
        self.tablets_done = {}
        self.tablets_agree = {}
        self.tablets_mark = {}
        self.tablets_continue = {}

        rospy.spin() #spin() simply keeps python from exiting until this node is stopped


    def run_study(self):
        #start running the study
        action = {"action": "wake_up"}
        self.run_robot_behavior(action)
        action = {"action": "show_screen", "screen_name": "ScreenDyslexia", "tablets": [1, 2, 3, 4, 5]}
        for tablet_id in action['tablets']:
            try:
                client_ip = self.tablets_ips[str(tablet_id)]
                message = {'action': 'show_screen', 'client_ip': client_ip, 'screen_name': action['screen_name']}
                self.tablet_publisher.publish(json.dumps(message))
            except:
                print('not enough tablets')
        # action3 = {"action":"say_text_to_speech", "parameters": ["hello all, how are you today?"]}
        action3 = {"action": "wake_up"}
        self.run_robot_behavior(action3)
        action4 = {'action': 'set_autonomous_state', 'parameters': ['solitary']}
        self.run_robot_behavior(action4)
        #threading._sleep(4.0)
        action5 = {'action': 'play_audio_file', 'parameters': ['/home/nao/naoqi/sounds/dyslexia/introduction.wav']}
        self.run_robot_behavior(action5)
        #action6 = {"action": "rest"}
        #self.run_robot_behavior(action6)

    def run_generic_script(self):
        print("run_study")
        data_file = open("robotator_study.json")
        logics_json = json.load(data_file)
        # self.poses_conditions = logics_json['conditions']
        self.study_sequence = logics_json[self.session]

        self.actions = {}

        for seq in self.study_sequence:
            self.actions[seq['tag']] = seq

        self.run_study_action(self.actions['start'])

    def run_study_action(self, action):
        print(action)
        if action['target'] == 'tablet':
            if "tablets" in action:
                for tablet_id in action['tablets']:
                    try:
                        client_ip = self.tablets_ips[str(tablet_id)]
                        message = action
                        message['client_ip'] = client_ip
                        self.tablet_publisher.publish(json.dumps(message))
                    except:
                        print('not enough tablets')
            next_action = self.actions[action['next']]
            self.run_study_action(next_action)

        elif action['target'] == 'robot':
            if action["action"] in ["run_behavior", "play_audio_file"]:
                # DEBUG
                action['parameters'] = ['robot_facilitator-ad2c5c/robotator_behaviors_old/r5', 'wait']
                action['action'] = 'run_behavior'
                nao_message = {"action": action['action'],
                               "parameters": action['parameters']}
                self.robot_end_signal[action['parameters'][0]] = False
                self.robot_publisher.publish(json.dumps(nao_message))
                while not self.robot_end_signal[action['parameters'][0]]:
                    pass
                if action['next'] != 'end':
                    next_action = self.actions[action['next']]
                    self.run_study_action(next_action)
                else:
                    self.the_end()
            elif action["action"] in ["sleep"]:
                print("start_timer")
                # either go on timeout
                self.sleep_timer = Timer(float(action["seconds"]), self.run_study_action,
                                         [self.actions[action["end"]["timeout"]]])
                self.sleep_timer.start()

                # or go on something else
                for k, v in action["end"].items():
                    self.robot_end_signal[k] = v

                if 'done' in action["end"].keys(): # get all done
                    self.tablets_done = {}
                elif 'agree' in action["end"].keys(): # get all agree or not all agree
                    self.tablets_agree = {}
                elif 'same' in action["end"].keys(): # get if all same or not
                    self.tablets_mark = {}
                    self.tablets_continue = {}

    def run_study_old(self):
        # self.run_study_timer.cancel()
        print("run_study")
        data_file = open("robotator_study.json")
        logics_json = json.load(data_file)
        # self.poses_conditions = logics_json['conditions']
        self.study_sequence = logics_json['sequence']

        for action in self.study_sequence:
            print ("@@@@@@@@@@@@@@@@@ study_sequence action=", action, "@@@@@@@@@@@@@@@@@")

            if action["action"] == "rest" or action["action"] == "wake_up":
                print("if", action)
                nao_message = action
                self.run_robot_behavior(nao_message)

            if action["action"] == "run_behavior":
                print("one_min_left", action["parameters"][0], self.is_audience_done)
                if ("one_min_left" in action["parameters"][0]) and (self.is_audience_done == True):
                    print("one_min_left and audience_done")
                elif ("TU10" in action["parameters"][0]):
                    if (self.is_audience_done == True):
                        nao_message = {"action": "run_behavior",
                                       "parameters": ["robot_facilitator-ad2c5c/robotator_behaviors/TU10a", "wait"]}
                    else:
                        nao_message = {"action": "run_behavior",
                                       "parameters": ["robot_facilitator-ad2c5c/robotator_behaviors/TU10b", "wait"]}
                    self.is_audience_done = False
                    self.run_robot_behavior(nao_message)

                elif ("TU12" in action["parameters"][0]):
                    if (self.is_audience_done == True):
                        nao_message = {"action": "run_behavior",
                                       "parameters": ["robot_facilitator-ad2c5c/robotator_behaviors/TU12a", "wait"]}
                    else:
                        nao_message = {"action": "run_behavior",
                                       "parameters": ["robot_facilitator-ad2c5c/robotator_behaviors/TU12b", "wait"]}
                    self.is_audience_done = False
                    self.run_robot_behavior(nao_message)


                elif ("TU13" in action["parameters"][0]):
                    all_agree = True
                    for value in self.tablets_audience_agree.values():
                        all_agree = all_agree and value
                        print("all_agree?", all_agree)

                    if not all_agree:
                        nao_message = {"action": "run_behavior",
                                       "parameters": ["robot_facilitator-ad2c5c/robotator_behaviors/TU13a", "wait"]}
                        self.run_robot_behavior(nao_message)
                        self.start_timer(60, [1, 2, 3, 4, 5])
                        self.start_sleep(35)
                        self.attention_tablet[tablet_id] = True
                    else:
                        nao_message = {'action': 'run_behavior',
                                       'parameters': ['robot_facilitator-ad2c5c/robotator_behaviors/TU13b', 'wait']}
                        self.run_robot_behavior(nao_message)
                else:
                    print("if", action)
                    nao_message = action
                    self.run_robot_behavior(nao_message)

            if action["action"] == "sleep":
                print("the action is sleep", action["seconds"], self.is_audience_done)
                if (self.is_audience_done == False):
                    self.start_sleep(float(action["seconds"]))
                    # float(action["seconds"])
                    # self.sleep_timer = Timer(float(action["seconds"]), self.timer_out)
                    # print("self.sleep_timer.start()")
                    # self.sleep_timer.start()
                    # self.waiting = True
                    # self.waiting_timer = True
                    # while self.waiting_timer:
                    #     pass
                    # print('done waiting_timer', action)
                    # nao_message = {'action': 'sound_tracker'}
                    # self.robot_publisher.publish(json.dumps(nao_message))
                    # time.sleep(float(action['seconds']))

            if action['action'] == 'start_timer':
                print("the action is start timer")
                for tablet_id in action['tablets']:
                    try:
                        client_ip = self.tablets_ips[str(tablet_id)]
                        message = {'action': 'start_timer', 'client_ip': client_ip,
                                   'seconds': action['seconds']}
                        self.tablet_publisher.publish(json.dumps(message))
                    except:
                        print('not enough tablets')

            if action['action'] == 'sound_tracker':
                self.robot_publisher.publish(json.dumps(action))

            if action['action'] == 'say_text_to_speech':
                self.robot_publisher.publish(json.dumps(action))

            if (action['action'] == 'show_screen'):
                self.init_audience_done()
                if "tablets" in action:
                    for tablet_id in action['tablets']:
                        try:
                            client_ip = self.tablets_ips[str(tablet_id)]
                            message = {'action': 'show_screen', 'client_ip': client_ip,
                                       'screen_name': action['screen_name'],
                                       'activity': action['activity'],
                                       'activity_type':action['activity_type']
                                       }
                            self.tablet_publisher.publish(json.dumps(message))
                        except:
                            print('not enough tablets')

            if (action['action'] == 'show_button'):
                self.init_audience_done()
                if "tablets" in action:
                    for tablet_id in action['tablets']:
                        try:
                            client_ip = self.tablets_ips[str(tablet_id)]
                            message = {'action': 'show_button', 'client_ip': client_ip,
                                       'which': action['which']}
                            self.tablet_publisher.publish(json.dumps(message))
                        except:
                            print('not enough tablets')
            if (action['action'] == 'disable_screen'):
                self.init_audience_done()
                if "tablets" in action:
                    for tablet_id in action['tablets']:
                        try:
                            client_ip = self.tablets_ips[str(tablet_id)]
                            message = {'action': 'disable_screen', 'client_ip': client_ip}
                            self.tablet_publisher.publish(json.dumps(message))
                        except:
                            print('not enough tablets')


    def run_study_timer_out(self):
        print("run_study_timer_out")
        #self.run_study_timer.cancel()
        # self.run_study()
        self.run_generic_script()

    def timer_out(self):
        print ("timer_out")
        self.sleep_timer.cancel()
        print ("self.sleep_timer.cancel()")
        self.waiting = False
        self.waiting_timer = False


    def run_robot_behavior(self, nao_message):
        print("run_manager: run_robot_behavior")
        self.robot_publisher.publish(json.dumps(nao_message))
        self.waiting = True
        self.waiting_robot = True
        while self.waiting_robot:
            pass
        print('done waiting_robot', nao_message["action"])


    def start_timer(self, seconds ,tablets):
        for tablet_id in tablets:
            try:
                client_ip = self.tablets_ips[str(tablet_id)]
                message = {'action': 'start_timer', 'client_ip': client_ip,
                           'seconds': float(seconds)}
                self.tablet_publisher.publish(json.dumps(message))
            except:
                print('not enough tablets')

    def start_sleep(self, seconds):
        self.sleep_timer = Timer(seconds, self.timer_out)
        print("start_timer")
        self.sleep_timer.start()
        self.waiting = True
        self.waiting_timer = True
        while self.waiting_timer:
            pass

    def init_audience_done(self):
        self.is_audience_done = False
        # restart the values for future screens
        self.count_audience_done = 0
        for key in self.tablets_audience_done.keys():
            self.tablets_audience_done[key] = False

    def audience_done (self, tablet_id, subject_id, client_ip):
        print("audience_done!!! tablet_id=", tablet_id)
        self.count_audience_done = 0
        print ("values before", self.tablets_audience_done.values())
        self.tablets_audience_done[tablet_id] =  True
        print ("values after",self.tablets_audience_done.values())
        for value in self.tablets_audience_done.values():
            if value ==True:
                self.count_audience_done += 1
                print("self.count_audience_done",self.count_audience_done)

        if (self.count_audience_done == self.number_of_tablets):
            print("self.count_audience_done == self.number_of_tablets",self.count_audience_done,self.number_of_tablets)
            try:
                self.sleep_timer.cancel()
                print("self.sleep_timer.cancel()")
            except:
                print("failed self.sleep_timer_cancel")
            self.waiting_timer = False
            self.is_audience_done = True
            #restart the values for future screens
            self.count_audience_done = 0
            #for key in self.tablets_audience_done.keys():
            #    self.tablets_audience_done[key]=False


    def register_tablet(self, tablet_id, group_id, client_ip):
        print("register_tablet", type(client_ip),client_ip)
        print(self.tablets)
        self.tablets[tablet_id] = {'subject_id':group_id, 'tablet_ip':client_ip}
        self.tablets_subjects_ids[tablet_id] = group_id
        self.tablets_ips[tablet_id] = client_ip
        self.tablets_ids[client_ip] = tablet_id
        self.tablets_audience_done[tablet_id] = False

        nao_message = {'action': 'say_text_to_speech', 'client_ip':client_ip,'parameters': ['register tablet', 'tablet_id',str(tablet_id), 'group id',str(group_id)]}
        self.robot_publisher.publish(json.dumps(nao_message))
        if (len(self.tablets) >= self.number_of_tablets):
            print("two tablets are registered")
            for key,value in self.tablets_ips.viewitems():
                print ("key, value", key, value)
                client_ip = value
                message = {'action':'registration_complete','client_ip':client_ip}
                self.tablet_publisher.publish(json.dumps(message))
            #time.sleep(2)
            self.run_study_timer = Timer(5.0, self.run_study_timer_out())
        print("finish register_tablet")



    def robot_play_audio_file (self, wav_path):
        nao_message = {'action': 'play_audio_file', 'parameters': [wav_path]}
        self.robot_publisher.publish(json.dumps(nao_message))
        print("end start")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CALLBACK FUNCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def callback_nao_state(self, data):
        print("manager callback_nao_state", data.data, self.waiting_robot)
        if 'register tablet' not in data.data and 'sound_tracker' not in data.data:
            self.waiting = False
            self.waiting_robot = False

            try:
                signal = json.loads(data.data)['parameters'][0]

                self.robot_end_signal[signal] = True
            except:
                pass
            # message = data.data
            # rospy.loginfo(message)
            # self.tablet_publisher.publish(message)
            # self.nao.parse_message(message)

    def callback_to_manager(self, data):
        print("start manager callback_to_manager", data.data)
        data_json = json.loads(data.data)
        action = data_json['action']
        if (action == 'register_tablet'):
            self.register_tablet(data_json['parameters']['tablet_id'], data_json['parameters']['group_id'],
                                 data_json['client_ip'])
            {'action': 'play_audio_file', 'parameters': ['/home/nao/naoqi/sounds/dyslexia/s_w15_m7.wav']}
        elif (action == 'audience_done'):
            print("audience_done")
            #self.audience_done(data_json['parameters']['tablet_id'], data_json['parameters']['subject_id'],
            #                   data_json['client_ip'])
        elif ("agree" in action):
            pass
        else:
            print('else', data.data)
            self.robot_publisher.publish(data.data)
        print ("finish manager callback_to_manager")


    def callback_log(self, data):
        # print('----- log -----')
        # print('----- log -----', data)
        log = json.loads(data.data)
        # print(log)

        if 'btn_done' in log['obj'] and log['action'] == 'press':
            client_ip = log['client_ip']
            tablet_id = self.tablets_ids[client_ip]
            subject_id = self.tablets_subjects_ids[tablet_id]
            self.count_done = 0
            self.tablets_done[tablet_id] = True
            for value in self.tablets_done.values():
                if value == True:
                    self.count_done += 1
            if (self.count_done == self.number_of_tablets):
                try:
                    self.sleep_timer.cancel()
                    print("self.sleep_timer.cancel()")
                except:
                    print("failed self.sleep_timer_cancel")
                self.count_done = 0
                self.run_study_action(self.actions[self.robot_end_signal['done']])

        if 'agree' in log['obj'] and log['action'] == 'press':
            client_ip = log['client_ip']
            tablet_id = self.tablets_ids[client_ip]
            subject_id = self.tablets_subjects_ids[tablet_id]
            self.tablets_agree[tablet_id] = True
            self.count_responded = len(self.tablets_agree.keys())
            if (self.count_responded == self.number_of_tablets):
                try:
                    self.sleep_timer.cancel()
                    print("self.sleep_timer.cancel()")
                except:
                    print("failed self.sleep_timer_cancel")
                self.count_responded = 0

                count_agree = 0
                for v in self.tablets_agree.values():
                    if v:
                        count_agree += 1
                if count_agree == self.number_of_tablets:
                    self.run_study_action(self.actions[self.robot_end_signal['all_agree']])
                else:
                    self.run_study_action(self.actions[self.robot_end_signal['not_all_agree']])

        if 'btn_continue' in log['obj'] and log['action'] == 'press':
            client_ip = log['client_ip']
            tablet_id = self.tablets_ids[client_ip]
            subject_id = self.tablets_subjects_ids[tablet_id]

            if tablet_id not in self.tablets_mark:
                self.tablets_mark[tablet_id] = []
            self.tablets_mark[tablet_id] = log['comment'] # TODO: parse the comment

            self.count_done = 0
            self.tablets_continue[tablet_id] = True
            for value in self.tablets_done.values():
                if value == True:
                    self.count_done += 1
            if (self.count_done == self.number_of_tablets):
                try:
                    self.sleep_timer.cancel()
                    print("self.sleep_timer.cancel()")
                except:
                    print("failed self.sleep_timer_cancel")
                self.count_done = 0

                # check if same, find two that are not
                tablet_pairs = []
                for t_id_1 in self.tablets_mark.keys():
                    for t_id_2 in self.tablets_mark.keys():
                        if t_id_1 != t_id_2:
                            if len(set(self.tablets_mark[t_id_1]).symmetric_difference(
                                    set(self.tablets_mark[t_id_2])
                            )) > 0: # there is some difference
                                tablet_pairs.append([t_id_1, t_id_2])
                if len(tablet_pairs) == 0: # they are all the same
                    self.run_study_action(self.actions[self.robot_end_signal['all_same']])
                else:
                    the_pair = random.choice(tablet_pairs)
                    self.actions[self.robot_end_signal['not_all_same']]["lookat"] = the_pair
                    self.run_study_action(self.actions[self.robot_end_signal['not_all_same']])


        # if 'audience_done' in log['obj'] and log['action'] == 'press':
        #     client_ip = log['client_ip']
        #     tablet_id = self.tablets_ids[client_ip]
        #     subject_id = self.tablets_subjects_ids[tablet_id]
        #     self.audience_done(tablet_id,subject_id,client_ip)
        #
        # if 'audience_group_done' in log['obj'] and log['action'] == 'press':
        #     client_ip = log['client_ip']
        #     tablet_id = self.tablets_ids[client_ip]
        #     subject_id = self.tablets_subjects_ids[tablet_id]
        #     self.audience_group_done(tablet_id,subject_id,client_ip)
        #
        # if 'audience_list' in log['obj']:
        #     if 'text' in log['action']:
        #         if self.tablets_ids[log['client_ip']] not in self.tablet_audience_data:
        #             self.tablet_audience_data[self.tablets_ids[log['client_ip']]] = 0
        #         self.tablet_audience_data[self.tablets_ids[log['client_ip']]] += 1
        #         print("self.tablet_audience_data", self.tablet_audience_data)
        #
        # if 'agree' in log['obj']:
        #     print("agree in")
        #     # if self.tablets_ids[log['client_ip']] not in self.tablets_audience_agree.values():
        #     #     self.tablets_audience_agree[int(self.tablets_ids[log['client_ip']])] = False
        #     if log['obj'] == 'agree_list' and log['action'] == 'down':
        #         print("agree_list True")
        #         self.tablets_audience_agree[int(self.tablets_ids[log['client_ip']])] = True
        #     elif (log['action'] == 'down'):  #dont_agree_list
        #         print("agree_list False")
        #         self.tablets_audience_agree[int(self.tablets_ids[log['client_ip']])] = False
        #
        #     allVoted = True
        #     i=1
        #     print("self.tablets_audience_agree=", self.tablets_audience_agree)
        #     while i <= self.number_of_tablets:
        #         if (self.tablets_audience_agree[i] == None):
        #             allVoted = False
        #         i += 1
        #     if (allVoted == True):
        #         self.waiting_timer = False
        #         self.sleep_timer.cancel()
        #         print("self.sleep_timer.cancel() ALL VOTED")
        #         self.waiting = False
        #         self.waiting_timer = False

        if self.listen_to_text:
            self.text_audience_group[log['obj']] = log['comment']

    def the_end(self):
        print('THE END')

if __name__ == '__main__':
    try:
        manager = ManagerNode()
        # manager.run_study()
    except rospy.ROSInterruptException:
        pass
