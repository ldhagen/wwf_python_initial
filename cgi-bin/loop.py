#!/usr/bin/env python
import cgi
import cgitb 
from PIL import Image, ImageDraw, ImageFont
import added_routines as AR
import pickle, os

master_game_dict = {}
current_game_dict = {}
current_game_name = ""

header = '''Content-Type: text/html\n\n'''

formhtml = '''<HTML><HEAD><TITLE>
Lance Proto One</TITLE></HEAD>
<BODY><img src="../default_grid.png">
<form action="/cgi-bin/loop.py" method="POST">
<p>      New Word: <input type="text" name="new_word"></br>
Start Postion: x <input type="text" name="x_pos"> and y <input type="text" name="y_pos"></br> 
Direction: <input type="radio" name="direction" value="right">Right
           <input type="radio" name="direction" value="down">Down</br></br>
<input type="submit" name="submit_action" value="Add Word"></br></br></br>
<input type="reset" value="Clear Form" />
</p>
</BODY>'''

def process():
    global current_game_name
    load_master_game_dict()
    form = cgi.FieldStorage()
    if form.has_key('GameName'):
        current_game_name = form['GameName'].value
    else:
        current_game_name = 'starting new game'

    if current_game_name in master_game_dict:
         global current_game_dict
         current_game_dict = master_game_dict[current_game_name]
    else:
        aaa = AR.create_cell_dict(AR.word_multipliers, AR.letter_multipliers)
        current_game_dict = aaa
        master_game_dict[current_game_name] = current_game_dict
        save_master_game_dict()
    if form.has_key('submit_action'):
        if form['submit_action'].value == 'Add Word':
            AR.add_word_to_dict_and_make_grid(form['new_word'].value, (int(form['x_pos'].value), int(form['y_pos'].value)),form['direction'].value, current_game_dict)
#            AR.add_word_to_dict_and_make_grid('two',(11,5),'down', current_game_dict)
            save_master_game_dict()
    AR.redraw_grid(current_game_dict,current_game_name)
    showForm()

def load_master_game_dict(master_game_dict_name=r'master_game_dict.pkl'):
    if os.path.isfile(master_game_dict_name):
        global master_game_dict
        ifile = open(master_game_dict_name, 'r')
        master_game_dict = pickle.load(ifile)
        ifile.close()     

def save_master_game_dict(master_game_dict_name=r'master_game_dict.pkl'):
        global master_game_dict
        ifile = open(master_game_dict_name, 'w')
        master_game_dict = pickle.dump(master_game_dict, ifile)
        ifile.close()     

def showForm():
    global formhtml
    global current_game_name
    added_str = r'<input type="hidden" name="GameName" value=' + current_game_name + r'>'
    formhtml += added_str
    print header + formhtml

if __name__ == '__main__':
     process()

