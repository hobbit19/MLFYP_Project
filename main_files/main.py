from __future__ import division
import re
from random import random
import numpy as np
import pandas as pd
import os
import uuid

import pyinotify
from treys import Card as treys_card
import Hand
import Player as p
import low_level_functions as llf
import subprocess
import matplotlib
# import graphical_display


path_to_file_changed1 = '/usr/local/home/u180455/Desktop/Project/MLFYP_Project/MLFYP_Project/pokercasino/botfiles/'
path_to_file_changed2 = '/home/gary/Desktop/MLFYP_Project/MLFYP_Project/pokercasino/botfiles/'
most_recent_file_changed = ''
new_file_data = '0D0P'       


class Game():

    cards = []
    game_count = 0
    def __init__(self):
        global cards
        cards =  llf.create_cards_for_game()
        self.Player1 = p.Player(0 ,'Adam', p.CardHolding('-','-','-','-','-'), '', '/give_hand_bot0', cards, None)
        self.Player2 = p.Player(1 ,'Bill', p.CardHolding('-','-','-','-','-'), '', '/give_hand_bot1', cards, None)
        self.Player3 = p.Player(2 ,'Chris', p.CardHolding('-','-','-','-','-'), '', '/give_hand_bot2', cards, None)
        #Player4 = Player(uuid.uuid1() ,'Dennis', CardHolding('-','-','-','-','-'), 'CO', '/give_hand_bot3', cards, None)
        self.player_list = [self.Player1, self.Player2, self.Player3] #, Player3, Player4]
        p.save_player_list(self.player_list)
        #positions_at_table = {0: Player1.position, 1: Player2.position, 2: Player3.position} #, 3: Player4.position} # mutable
        self.parse_data_from_GHB()

    def parse_data_from_GHB(self):
        # GHB is an abbreviation for 'give_hand_botX'
        self.main_watch_manager = main_watch_manager(self.player_list)

    def return_table_list(self):
        return self.player_list



def get_status_from_file(file_name):
    data = ''
    with open(path_to_file_changed2 + file_name, 'rt') as f:
        data = f.read()
    return data

   
        

class MyEventHandler(pyinotify.ProcessEvent):


    def my_init(self, **kargs):
        """
        This is your constructor it is automatically called from
        ProcessEvent.__init__(), And extra arguments passed to __init__() would
        be delegated automatically to my_init().
        """
        self.player_list = kargs["player_list"]
        self.game_count = 0

    # def process_IN_ACCESS(self, event):
    #     print("ACCESS event:", event.pathname)

    # def process_IN_ATTRIB(self, event):
    #     print("ATTRIB event:", event.pathname)

    # def process_IN_CLOSE_NOWRITE(self, event):
    #     print("CLOSE_NOWRITE event:", event.pathname)

    # def process_IN_MODIFY(self, event):
    #     print("MODIFY event:", event.pathname)

    # def process_IN_OPEN(self, event):
    #     #print(event.pathname)
    #     global file_changed
    #     arr = re.split(r'[/]',event.pathname)
    #     most_recent_file_changed = (arr[len(arr)-1])
    #     last_letter = most_recent_file_changed[len(most_recent_file_changed)-1]
    #     bot_number = last_letter if (last_letter =='0' or last_letter == '1' or last_letter =='2') else ''
    #     event_type = most_recent_file_changed if bot_number == '' else most_recent_file_changed[0:len(most_recent_file_changed)-1]
    #     filename = str(event_type+bot_number)
    #     file_data = ""
        
    #     if event_type == "botToCasino":
    #         pass #print("IN_OPEN event:", event.pathname)
            
            


    def process_IN_CLOSE_WRITE(self, event):
        ### declaring a bot_number and event_type 
        #print("IN_CLOSE_WRITE event:", event.pathname)
        
        global file_changed
        arr = re.split(r'[/]',event.pathname)
        most_recent_file_changed = (arr[len(arr)-1]) # last string in file path
        last_letter = most_recent_file_changed[len(most_recent_file_changed)-1]
        bot_number = last_letter if (last_letter =='0' or last_letter == '1' or last_letter == '2') else ''
        event_type = most_recent_file_changed if bot_number == '' else most_recent_file_changed[0:len(most_recent_file_changed)-1]
        filename = str(event_type+bot_number)
        file_data = get_status_from_file(str(filename))
        if event_type == "give_hand_bot":

            if bot_number == '0':
                self.player_list[0].card_holding = llf.GHB_Parsing(self.player_list[0], file_data) #check cards
                #PROBLEM: Cannot evaluate preflop without players position which is retrieved in casinoToBot file overwrite
                #he, evaluation, rc, score_desc, _ = self.player_list[0].hand_evaluate_preflop(self.player_list[0].card_holding, self.player_list[0].name)
                # bot 0 now has his cards

            elif bot_number == '1':
                self.player_list[1].card_holding = llf.GHB_Parsing(self.player_list[1], file_data) #check cards
                #print(self.player_list[0].card_holding)

                #PROBLEM: Cannot evaluate preflop without players position which is retrieved in casinoToBot file overwrite
                #he, evaluation, rc, score_desc, _ = self.player_list[1].hand_evaluate_preflop(self.player_list[1].card_holding, self.player_list[1].name)

                #bot 1 now has his cards
            
            elif bot_number == '2':
                self.player_list[2].card_holding = llf.GHB_Parsing(self.player_list[2], file_data) #check cards
                #print(self.player_list[0].card_holding)

                #PROBLEM: Cannot evaluate preflop without players position which is retrieved in casinoToBot file overwrite
                #he, evaluation, rc, score_desc, _ = self.player_list[1].hand_evaluate_preflop(self.player_list[1].card_holding, self.player_list[1].name)

                #bot 1 now has his cards    

        elif event_type == "casinoToBot":   # only on (second) iteration, is the casinoToBOT file written with the actions ie 'rrc'
            treys_card.print_pretty_cards([268446761, 134236965, 33589533] + [67115551, 16787479])
            with open("./test_file_data_change_CTB", 'a+') as f:
                f.write("\n"+file_data)
                f.close()
            ctb_file_content =  re.split(r'[DPFFFFTTRRSABSABWWE]',file_data) # DEBUG: test_file_data
            dealer_no = ctb_file_content[1]
            # casinoToBot is written: hand number> D <dealer button position> P <action by all players in order from first to act, e.g. fccrf...> F <flop card 1> F <flop 2> F <flop 3> F <flop action starting with first player to act>
            #  T <turn card> T <turn action> R <river card> R <river action>
            
            bot_n = int(bot_number)
            bot_cards = self.player_list[bot_n].card_holding
            bot_name = self.player_list[bot_n].name
            
            # we want to check if ONLY the preflop action is filled
            is_preflop_action_filled, is_flop_action_filled, is_turn_action_filled, is_river_action_filled = llf.casinoToBot_ParsingRead(self, ctb_file_content, self.player_list[bot_n], self.player_list, bot_number) # DEBUG: test_file_data #check cards
            flop_cards_present, turn_card_present, river_card_present = llf.check_cards_shown(file_data)
            first_meeting = {0: False, 1: False, 2: False, 3: False}
            is_new_game = False
            
            # PREFLOP
            if (flop_cards_present == False and turn_card_present == False and river_card_present == False):
                
                # first move (BTN)
                if(is_preflop_action_filled == False and is_flop_action_filled == False and is_turn_action_filled ==False and is_river_action_filled == False): # is only preflop filled?                he, evaluation, rc, score_desc, player_action = self.player_list[bot_n].hand_evaluate_preflop(bot_cards, bot_name)   # USE FOR DEBUGGING (files have alreayd been filled with debugger)
                    
                    for player in self.player_list:
                        player.is_new_game = True
                    first_meeting[0] = True
                    he, rc, score_desc, player_action = self.player_list[bot_n].hand_evaluate(bot_cards, bot_name, 'Preflop', first_meeting, True)   # USE FOR DEBUGGING (files have alreayd been filled with debugger)
                    self.player_list[bot_n].is_new_game = False
                    
                elif(is_preflop_action_filled == True and is_flop_action_filled == False and is_turn_action_filled ==False and is_river_action_filled == False): # is flop filled yet?

                    first_meeting[0] = False
                    he, rc, score_desc, player_action = self.player_list[bot_n].hand_evaluate(bot_cards, bot_name, 'Preflop', first_meeting, False)   # USE FOR DEBUGGING (files have alreayd been filled with debugger)
                    self.player_list[bot_n].is_new_game = False

            #POSTFLOP
            elif (flop_cards_present == True and turn_card_present == False and river_card_present == False):
                              
                #first move of flop (SB assuming he hasn't folded)
                if(is_preflop_action_filled == True and is_flop_action_filled == False and is_turn_action_filled ==False and is_river_action_filled == False): # is flop filled yet?
                    first_meeting[1] = True
                    self.player_list[bot_n].action_sent = False
                    he, rc, score_desc, player_action = self.player_list[bot_n].hand_evaluate(bot_cards, bot_name, 'Flop', first_meeting, False)    # USE FOR DEBUGGING (files have alreayd been filled with debugger)

                elif(is_preflop_action_filled == True and is_flop_action_filled == True and is_turn_action_filled ==False and is_river_action_filled == False): # is turn filled yet?
                    first_meeting[1] = False
                    self.player_list[bot_n].action_sent = False
                    he, rc, score_desc, player_action = self.player_list[bot_n].hand_evaluate(bot_cards, bot_name, 'Flop', first_meeting, False)   # USE FOR DEBUGGING (files have alreayd been filled with debugger)
                
            #TURN
            elif (flop_cards_present == True and turn_card_present == True and river_card_present == False):
                #print("inside TURN main")
                #print("\n", is_preflop_action_filled, is_flop_action_filled, is_turn_action_filled, is_river_action_filled)
                # first move of turn
                if(is_turn_action_filled ==False and is_river_action_filled == False): # is turn filled yet?
                    #print("inside TURN 1")
                    first_meeting[2] = True
                    self.player_list[bot_n].action_sent = False
                    he, rc, score_desc, player_action = self.player_list[bot_n].hand_evaluate(bot_cards, bot_name, 'Turn', first_meeting, False)  # USE FOR DEBUGGING (files have alreayd been filled with debugger)

                elif(is_turn_action_filled ==True and is_river_action_filled == False): #is river filled yet?
                    #print("inside TURN 2")
                    first_meeting[2] = False
                    self.player_list[bot_n].action_sent = False
                    he, rc, score_desc, player_action = self.player_list[bot_n].hand_evaluate(bot_cards, bot_name, 'Turn', first_meeting, False)    # USE FOR DEBUGGING (files have alreayd been filled with debugger)

            #RIVER
            elif (flop_cards_present == True and turn_card_present == True and river_card_present == True):

                # first move of river
                if(is_preflop_action_filled == True and is_flop_action_filled == True and is_turn_action_filled ==True and is_river_action_filled == False): #is river filled yet?
                    first_meeting[3] = True
                    self.player_list[bot_n].action_sent = False
                    he, rc, score_desc, player_action = self.player_list[bot_n].hand_evaluate(bot_cards, bot_name, 'River', first_meeting, False)   # USE FOR DEBUGGING (files have alreayd been filled with debugger)

                elif(is_preflop_action_filled == True and is_flop_action_filled == True and is_turn_action_filled ==True and is_river_action_filled == True): #is river filled yet?
                    first_meeting[3] = False
                    self.player_list[bot_n].action_sent = False
                    he, rc, score_desc, player_action = self.player_list[bot_n].hand_evaluate(bot_cards, bot_name, 'River', first_meeting, False)    # USE FOR DEBUGGING (files have alreayd been filled with debugger)
             
            # We may use the attributes collected here as training data from neural network



class main_watch_manager():

    def __init__(self, player_list ,communication_files_directory=path_to_file_changed2):
        self.communication_files_directory = communication_files_directory
        self.player_list = player_list

        # call bash for ./lasvegas
               
        # watch manager
        wm = pyinotify.WatchManager()
        wm.add_watch(self.communication_files_directory, pyinotify.ALL_EVENTS, rec=True)

        # event handler
        kwargs = {"player_list": self.player_list}
        eh = MyEventHandler(**kwargs)

        # automate process of using bash
        # wd = os.getcwd()
        # #os.chdir("/usr/local/home/u180455/Desktop/Project/MLFYP_Project/MLFYP_Project/pokercasino")
        # os.chdir("/home/gary/Desktop/MLFYP_Project/MLFYP_Project/pokercasino")
        # subprocess.Popen("./lasvegas")
        # os.chdir(wd)

        # notifier
        notifier = pyinotify.Notifier(wm, eh)

        notifier.loop()



if __name__ == '__main__':
    treys_card.print_pretty_cards([268446761, 134236965, 33589533] + [67115551, 16787479])
    
    game = Game()
    # graphics = graphical_display.main_draw(game)





