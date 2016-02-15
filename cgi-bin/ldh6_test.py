#!/usr/bin/env python

import added_routines as AR, itertools, pickle, hashlib
from operator import itemgetter

###########################################################################
# This module creates a cell dictionary from added_routines and a SolutionObject
# which is an object based on the concept of taking each cell in the cell 
# dictionary and creating an object related to a specific cell (focus_cell)
# and a number of cells in a play direction (right or down). A SolutionObject
# will be create for each of the possible 15 x 15 cells for 1 to 7 spaces in 
# the 2 play directions. The concept is to populate the cell dictionary with
# current state 
#
#
###########################################################################

xxx = AR.create_cell_dict(AR.word_multipliers, AR.letter_multipliers)
ifile = open('words_hashed.pkl','r')
yyy = pickle.load(ifile)
ifile.close()

class SolutionObject(object):
    'contains solution value for one focal cell with numbers of cells at play'

    scores = []
    available_empty_spaces_in_main = 0 
    current_far_edge = (-1,-1)
    current_string_begin = (-1,-1)
    main_string_begin = (-1,-1)
    valid_and_initalized = False
    strings_contact_points = []
    current_number_free_cells = 0 
    open_cells_map_list = []
    contains_valid_solution = False
    solution_letters_list = []
    scored_solution_letters_list = []
    top_score = (-1,'zzz')

    def __init__(self, cell_dict, word_dict, focus_cell, number_of_cells_in_play, direction, letters_in_play):
        'SolutionObject initializer - takes game dict, location of focus cell, number of cells in play, and direction (right/down)'
	if not (direction == 'down' or direction == 'right') :
            raise ValueError('direction must be down or right')
        self.scores = []
        self.letter_value_dict = {'a':1, 'b':4, 'c':4, 'd':2, 'e':1, 'f':4, 'g':3, 'h':3, 'i':1, 'j':10, 'k':5, 'l':2, 'm':4, 'n':2, 'o':1, 'p':4, 'q':10, 'r':1, 's':1, 't':1, 'u':2, 'v':5, 'w':4, 'x':8, 'y':3, 'z':10}
        self.strings_contact_points = []
        self.cell_dict = cell_dict
        self.word_dict = word_dict
        self.focus_cell = focus_cell
        self.number_of_cells_in_play = number_of_cells_in_play
        self.direction = direction
        self.letters_in_play = letters_in_play
        self.discover_far_edge(cell_dict,focus_cell,direction)
        self.discover_string_begin(cell_dict,focus_cell,self.get_opposite_direction(direction))
        self.main_string_begin = self.current_string_begin
        self.discover_available_empty_spaces_in_main(cell_dict,focus_cell,direction)
        if self.available_empty_spaces_in_main < number_of_cells_in_play: #stop and leave valid_and_initalized as False
            return
        if cell_dict[focus_cell]['current_letter'] != '': #stop and leave valid_and_initalized as False
            return
        self.current_number_free_cells = self.number_of_cells_in_play
        self.discover_main_string_contact_points(focus_cell)
        if self.strings_contact_points == []: #no potential strings so stop and leave valid_and_initalized as False
            return
        self.valid_and_initalized = True
        self.create_strings_template()
        self.search_for_valid_solutions()
        if self.contains_valid_solution:
            self.score_solution()
            self.top_score = self.get_top_score()
    def get_opposite_direction(self,direction):
	if not (direction == 'down' or direction == 'right') :
            raise ValueError('direction must be down or right')
        if direction == 'right':
            return 'left'
        else:
            return 'up' 

    def get_perpendicular_back_direction(self,direction):
	if not (direction == 'down' or direction == 'right') :
            raise ValueError('direction must be down or right')
        if direction == 'right':
            return 'up'
        else:
            return 'left' 

    def get_perpendicular_forward_direction(self,direction):
	if not (direction == 'down' or direction == 'right') :
            raise ValueError('direction must be down or right')
        if direction == 'right':
            return 'down'
        else:
            return 'right' 

    def discover_string_begin(self,cell_dict,location,direction):
        'find string beginning and place return location'
	if not (direction == 'up' or direction == 'left') :
            raise ValueError('direction must be up or left')
        if cell_dict[location]['adjacent_dict'][direction][0]:
            if cell_dict[cell_dict[location]['adjacent_dict'][direction][1]]['current_letter'] != "":
                self.discover_string_begin(cell_dict, cell_dict[location]['adjacent_dict'][direction][1], direction)
            else:
                self.current_string_begin = location
        else:
            self.current_string_begin = location
  
    def get_top_score(self):
        return sorted(self.scored_solution_letters_list, key=itemgetter(1), reverse=True)[0]

    def discover_far_edge(self,cell_dict,location,direction):
        '''assumes dict structure populated as expected and global variable updates global far_edge with location'''
	if not (direction == 'down' or direction == 'right') :
            raise ValueError('direction must be down or right')
        current_far_edge = (-1,-1)
        if cell_dict[location]['adjacent_dict'][direction][0]:
            self.discover_far_edge(cell_dict, cell_dict[location]['adjacent_dict'][direction][1],direction)
        else:
            self.current_far_edge = location

    def discover_available_empty_spaces_in_main(self,cell_dict,location,direction):
        'used on object creation to determine if object is even viable in the scored_solution set since solution set cells in play must be equal or less than available empty spaces on main string'
	if not (direction == 'down' or direction == 'right') :
            raise ValueError('direction must be down or right')
        if cell_dict[location]['current_letter'] == '':
            self.available_empty_spaces_in_main += 1
        if cell_dict[location]['adjacent_dict'][direction][0]:
            self.discover_available_empty_spaces_in_main(cell_dict, cell_dict[location]['adjacent_dict'][direction][1],direction)        

    def discover_main_string_contact_points(self,location):
        'self.current_number_free_cells must be updated prior to call - finds empty cells on main string that touch cells with characters set and add to list'
        while self.current_number_free_cells > 0:
            found_at_least_one = False
            for x in ['up','down','right','left']:
                if self.cell_dict[location]['adjacent_dict'][x][0]:
                    if self.cell_dict[self.cell_dict[location]['adjacent_dict'][x][1]]['current_letter'] != '':
                        found_at_least_one = True
            if self.cell_dict[location]['current_letter'] == '':
               self.current_number_free_cells = self.current_number_free_cells - 1
               if found_at_least_one:
                   self.strings_contact_points.append(location)
            if self.cell_dict[location]['adjacent_dict'][self.direction][0]:
                location = self.cell_dict[location]['adjacent_dict'][self.direction][1]
            else:
                return
            self.discover_main_string_contact_points(location)
              
    def create_strings_template(self):
        'object must be valid and initalized as internals are used'
        if not self.valid_and_initalized:
            raise ValueError('create_string_template called on object not validated and initalized')
        self.current_string_list = [] # used to hold sequential locations of a string created by object and later added to strings_list as entry
        self.strings_list = [] # contains the locations for all strings created by object as sequential entries
        self.open_cells_map_list = [] # contains a mapping to dictionary of open cells in strings_list 
        self.current_number_free_cells = self.number_of_cells_in_play
        current_location = self.current_string_begin #start main template object which contains all open variable spaces
        while self.current_number_free_cells > 0:
            self.current_string_list.append(current_location)
            if self.cell_dict[current_location]['current_letter'] == '':
                self.current_number_free_cells = self.current_number_free_cells - 1
                self.open_cells_map_list.append(self.cell_dict[current_location])
            current_location = self.cell_dict[current_location]['adjacent_dict'][self.direction][1] # no validity test needed as object valid and initalized
        keep_going = True
        if current_location == (-1,-1): # if we moved to end above and are queued one cell beyond grid
            keep_going = False
        while keep_going:# so far got main from beginning throught last empty space, now next check for a following string 
            if self.cell_dict[current_location]['current_letter'] != '':
                self.current_string_list.append(current_location)
            else:
                keep_going = False  
            if self.cell_dict[current_location]['adjacent_dict'][self.direction][0]: 
                current_location = self.cell_dict[current_location]['adjacent_dict'][self.direction][1]
            else:
                keep_going = False
        self.strings_list.append(self.current_string_list)
        for x in self.strings_contact_points:  # main string done now to perpendicular strings
            self.current_string_list = [] # we captured main string mapping and now reset and do same with perpendicular side strings which if they exist will be off strings_ contact_points 
            p_back_direction = self.get_perpendicular_back_direction(self.direction)
            p_forward_direction = self.get_perpendicular_forward_direction(self.direction)
            string_after = False
            if self.cell_dict[x]['adjacent_dict'][p_back_direction][0]:
                if self.cell_dict[self.cell_dict[x]['adjacent_dict'][p_back_direction][1]]['current_letter'] != '' : #we have a perpendicular string before our contact point
                    self.discover_string_begin(self.cell_dict,x,p_back_direction)
                    known_empty_spaces = 1 # we are on the perpendicular before our space and will move to, decrement, and stop that while loop
                    current_location = self.current_string_begin
                    self.current_string_list.append(current_location)
                    while known_empty_spaces > 0:
                        current_location = self.cell_dict[current_location]['adjacent_dict'][p_forward_direction][1] #no validity check as must exist here
                        self.current_string_list.append(current_location)
                        if self.cell_dict[current_location]['current_letter'] == '':
                            known_empty_spaces = known_empty_spaces - 1
                    keep_going = True # captured details before and through empty cell now check past same
                    while keep_going:
                        if self.cell_dict[current_location]['adjacent_dict'][p_forward_direction][0]: 
                            current_location = self.cell_dict[current_location]['adjacent_dict'][p_forward_direction][1]
                            if self.cell_dict[current_location]['current_letter'] != '':
                                string_after = True
                                self.current_string_list.append(current_location)
                            else:
                                keep_going = False
                        else:
                            keep_going = False    
                    if self.current_string_list != []:
                        self.strings_list.append(self.current_string_list) # added a sting perpendicular and before and maybe after cell
            if not string_after: # as in we did not alread capture this with a sting before and after above
                self.current_string_list = [] # reset 
                initial_pass = True
                keep_going = True 
                current_location = x
                while keep_going:
                    if self.cell_dict[current_location]['adjacent_dict'][p_forward_direction][0]: 
                        current_location = self.cell_dict[current_location]['adjacent_dict'][p_forward_direction][1]
                        if self.cell_dict[current_location]['current_letter'] != '':
                            if initial_pass:
                                self.current_string_list.append(x)
                                initial_pass = False 
                            self.current_string_list.append(current_location)
                        else:
                           keep_going = False
                    else:
                       keep_going = False
                if self.current_string_list != []:
                    self.strings_list.append(self.current_string_list)

    def search_for_valid_solutions(self):
        'after validating strings_list contains entries check permutations of letters for solutions, toggle contains_valid_solution, and populate solution_letters_list'
        self.contains_valid_solution = False
        self.solution_letters_list = []
        if self.strings_list == []:
            return
        for permuted_letters_iter in itertools.permutations(self.letters_in_play,self.number_of_cells_in_play):
            targets_not_yet_passed = len(self.strings_list)
            for x in range(len(self.open_cells_map_list)):
                self.open_cells_map_list[x]['current_letter'] = permuted_letters_iter[x]
            for word_maps in self.strings_list:
               target_word = []
               for test_char_loc in word_maps:
                  target_word.append(self.cell_dict[test_char_loc]['current_letter'])
               if hashlib.md5("".join(target_word)).hexdigest() in self.word_dict:
                   targets_not_yet_passed = targets_not_yet_passed - 1 
            if targets_not_yet_passed == 0:
                validated_word = "".join(permuted_letters_iter)
                for count in range(len(self.open_cells_map_list)):
                    if self.open_cells_map_list[count]['letter_multiplier'] != 0 or self.open_cells_map_list[count]['word_multiplier'] != 0:
                        validated_word = list(validated_word)
                        validated_word[count] = validated_word[count].upper()
                        validated_word = "".join(validated_word)
                    count += 1
                self.contains_valid_solution = True
                self.solution_letters_list.append(validated_word)
        self.solution_letters_list = list(set(self.solution_letters_list)) #removing identical copies
        for x in range(len(self.open_cells_map_list)):
            self.open_cells_map_list[x]['current_letter'] = ''

    def score_solution(self):
        if not self.contains_valid_solution:
            return
        empty_slots = [] #list for cells that were updated and thus valid for multiples of letter and word if present  
        for x in self.open_cells_map_list:
            empty_slots.append(x['location'])
        self.scored_solution_letters_list = []
        self.scores = []
        for sol_ltrs in self.solution_letters_list:
            count = 0 #used to grab letters to place in open cells
            for x in self.open_cells_map_list:
                x['current_letter'] = sol_ltrs[count]
                count += 1 
            total_score = 0 #we have dict ready to score for this letter set
            for x in self.strings_list:
                current_score = 0
                word_multiple = 1 
                for y in x: #individual cells in solution list
                    letter_multiple = 1
                    if y in empty_slots: #thus multiple factor counts
                        if self.cell_dict[y]['word_multiplier'] != 0:
                            word_multiple = word_multiple * self.cell_dict[y]['word_multiplier']
                        if self.cell_dict[y]['letter_multiplier'] != 0:
                            letter_multiple = letter_multiple * self.cell_dict[y]['letter_multiplier']
                    current_score += (self.letter_value_dict[self.cell_dict[y]['current_letter'].lower()] * letter_multiple)
                total_score += current_score * word_multiple
            if len(self.open_cells_map_list) == 7:
                current_score += 35
            self.scored_solution_letters_list.append((total_score,sol_ltrs))
            self.scores.append(total_score)
        for x in range(len(self.open_cells_map_list)): #clean up by resetting by reference cell dict to original state
            self.open_cells_map_list[x]['current_letter'] = ''

class CompleteSet(object):
    'Captures all 15x15x2x7 SolutionObjects'
    def __init__(self,cell_dict,word_dict,letters_in_play):
        self.total = {}
        for x in range(15):
            for y in range(15):
                for z in range(1,8):
                    for direction in ['right', 'down']:
                         self.total[(x,y,z,direction)] = SolutionObject(cell_dict,word_dict,(x,y),z,direction,letters_in_play)
        self.capture_valid_solutions()
    def print_valid_solutions(self):
        for x in self.total.keys():
            if self.total[x].contains_valid_solution:
                print '--------------------'
                print x
                print self.total[x].solution_letters_list    
    def capture_valid_solutions(self):
        self.valid_solution_objects = {}
        for x in self.total.keys():
            if self.total[x].contains_valid_solution:
                self.valid_solution_objects[x] = self.total[x]

    def dump_valid_solutions(self,dump_name='solution_dump'):
        ifile = open(dump_name,'w')
        for x in self.total.keys():
            if self.total[x].contains_valid_solution:
                ifile.write('--------------------\n')
                ifile.write(str(len(self.total[x].strings_list)) + ' --- ')
                ifile.write(str(x) + '\n')
                ifile.write(str(self.total[x].scored_solution_letters_list) + '\n')
        ifile.close()

    def print_top_scores_in_order(self):
        if not self.valid_solution_objects:
            return
        total_list = []
        for x in self.valid_solution_objects.keys():
            total_list.append((self.total[x].top_score[0],self.total[x].top_score[1], x))
        sorted_total_list =  sorted(total_list, key=itemgetter(0), reverse=True)
        print sorted_total_list[:5]
    
    def dump_top_scores_in_order(self,dump_name='scores_dump'):
        if not self.valid_solution_objects:
            return
        total_list = []
        ifile = open(dump_name,'a')
        for x in self.valid_solution_objects.keys():
            total_list.append((self.total[x].top_score[0],self.total[x].top_score[1], x))
        sorted_total_list =  sorted(total_list, key=itemgetter(0), reverse=True)
        ifile.write(str(sorted_total_list[:5]))
        ifile.write('\n')
        ifile.close()
