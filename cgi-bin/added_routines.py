#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont

word_multipliers = {(0,3):3, (0,11):3, (1,5):2, (1,9):2, (3,0):3, (3,7):2, (3,14):3, (5,1):2, (5,13):2, (7,3):2, (7,11):2, (9,1):2, (9,13):2, (11,0):3, (11,7):2, (11,14):3, (13,5):2, (13,9):2, (14,3):3, (14,11):3}

letter_multipliers = {(0,6):3, (0,8):3, (1,2):2, (1,12):2, (2,1):2, (2,4):2, (2,10):2, (2,13):2, (3,3):3, (3,11):3, (4,2):2, (4,6):2, (4,8):2, (4,12):2, (5,5):3, (5,9):3, (6,0):3, (6,4):2, (6,10):2, (6,14):3, (8,0):3, (8,4):2, (8,10):2, (8,14):3, (9,5):3, (9,9):3, (10,2):2, (10,6):2, (10,8):2, (10,12):2, (11,3):3, (11,11):3, (12,4):2, (12,10):2, (13,2):2, (13,12):2, (14,6):3, (14,8):3}


def create_cell_dict(word_multipliers, letter__multipliers):
    '''returns 15 x 15 dict keyed to x,y with space for current char value, adjacent dict, word, and letter multipliers'''
    return_dict = {}
    null_current_letter_value = ""
    null_word_multiplier = 0
    null_letter_miultiplier = 0
    for x in range(15):
        for y in range(15):
            value_dict = {}
            value_dict['current_letter'] = null_current_letter_value
            value_dict['adjacent_dict'] = create_adjacent_dict(x,y)
            value_dict['word_multiplier'] = find_word_multiplier(x,y,word_multipliers)
            value_dict['letter_multiplier'] = find_letter_multiplier(x,y,letter__multipliers)
            return_dict[(x,y)] = value_dict
    return return_dict

def create_adjacent_dict(x,y):
    '''returns dict based on of perpendicular adjactents based'''
    result_dict = {}
    if x - 1 >= 0:
        result_dict['left'] = (True,(x - 1, y))
    else:
        result_dict['left'] = (False,(-1,-1))
    if x + 1 <= 14:
        result_dict['right'] = (True,(x + 1, y))
    else:
        result_dict['right'] = (False,(-1,-1))
    if y - 1 >= 0:
        result_dict['up'] = (True,(x, y - 1))
    else:
        result_dict['up'] = (False,(-1,-1))
    if y + 1 <= 14:
        result_dict['down'] = (True,(x, y + 1))
    else:
        result_dict['down'] = (False,(-1,-1))
    return result_dict

def find_word_multiplier(x,y,word_multipliers):
    multiplier = 0
    if (x,y) in word_multipliers:
        multiplier =  word_multipliers[(x,y)]
    return multiplier

def find_letter_multiplier(x,y,letter_multipliers):
    multiplier = 0
    if (x,y) in letter_multipliers:
        multiplier =  letter_multipliers[(x,y)]
    return multiplier

def find_spaces_remaining(direction, location, passed_dict):
    '''location as tuple and cell dict used to determine additional spaces to right or down'''
    x = location[0]
    y = location[1]
    count = 0
    if direction == 'right':
        while count > -1: 
            test = passed_dict[(x,y)]['adjacent_dict']['right'][0]
            if test:
                x += 1
                count += 1
            else:
                return count
    if direction == 'down':
        while count > -1: 
            test = passed_dict[(x,y)]['adjacent_dict']['down'][0]
            if test:
                y += 1
                count += 1
            else:
                return count

    return 9999

def make_empty_grid_png(passed_filename='default_grid.png'):
    '''requires font file in same directory path'''
    font = ImageFont.truetype("LiberationSerif-Regular.ttf",16)
    image = Image.new('RGBA', (460,560))
    draw = ImageDraw.Draw(image)
    for x in range(0,450,30):
        for y in range(0, 450,30):
            draw.rectangle((x,y,x+30,y+30), outline='black')
    font = ImageFont.truetype("LiberationSerif-Regular.ttf",36)
#    draw.text((7*30+4, 7*30-4),"+",fill='black',font=font)
    image.save(passed_filename)

def add_char_to_grid_image(character, location_tuple, passed_filename='default_grid.png'):
    im = Image.open(passed_filename)
    font = ImageFont.truetype("LiberationSerif-Regular.ttf",36)
    draw = ImageDraw.Draw(im)
    draw.text((int(location_tuple[0]*30)+4, int(location_tuple[1]*30)-4), character, fill='black',font=font)
    im.save(passed_filename)

def draw_grid_name(name_string, location_tuple, font_size, passed_filename):
    im = Image.open(passed_filename)
    font = ImageFont.truetype("LiberationSerif-Regular.ttf",font_size)
    draw = ImageDraw.Draw(im)
    draw.text((int(location_tuple[0]*30)+4, int(location_tuple[1]*30)-4), name_string, fill='black',font=font)
    im.save(passed_filename)

def redraw_grid(passed_dict, game_name, passed_filename='default_grid.png'):
    make_empty_grid_png(passed_filename)
    for x in range(15):
        for y in range(15):
            character = passed_dict[(x,y)]['current_letter']
            if character != '':
                add_char_to_grid_image(character,(x,y),passed_filename)
    draw_grid_name(game_name,(2,16), 22, passed_filename)


def add_word_to_dict_and_make_grid(word_str, location_tuple, direction, passed_dict, passed_filename='default_grid.png'):  

    if len(word_str) > find_spaces_remaining(direction,location_tuple,passed_dict):
        return
    if direction == 'right':
        for x in range(len(word_str)):
            passed_dict[int(location_tuple[0]) + x, int(location_tuple[1])]['current_letter'] = word_str[x]

    if direction == 'down':
        for x in range(len(word_str)):
            passed_dict[int(location_tuple[0]), int(location_tuple[1] + x)]['current_letter'] = word_str[x]

    redraw_grid(passed_dict, 'game_one', passed_filename='default_grid.png')
    



def main():
    '''this is a set of prototypes so nothing here yet'''
    print 'testing'


if __name__ == '__main__':
     main()
