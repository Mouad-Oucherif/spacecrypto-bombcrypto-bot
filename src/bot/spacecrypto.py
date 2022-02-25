# -*- coding: utf-8 -*-    
from cv2 import cv2
from os import listdir
from random import randint
from random import random
import numpy as np
import mss
import pyautogui
import time
import sys
import src.env as env

# Tempo entre ações
pyautogui.PAUSE = 0.5
global x_scroll
global y_scroll
global h_scroll
global w_scroll


def addRandomness(n, randomn_factor_size=None):
    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    return int(randomized_n)

def moveToWithRandomness(x,y,t):
    pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2)

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


def show(rectangles, img = None):
    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))
    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)

def clickBtn(img, timeout=3, threshold = 0.8, imageDefault = None):
    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(img, threshold=threshold, img=imageDefault)
        if(len(matches)==0):
            has_timed_out = time.time()-start > timeout
            continue
        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        moveToWithRandomness(pos_click_x,pos_click_y,0.5)
        pyautogui.click()
        return True

    return False

def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        return sct_img[:,:,:3]

def positions(target, threshold=0.8, img = None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]
    yloc, xloc = np.where(result >= threshold)
    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def scroll_ships():
    global x_scroll
    global y_scroll
    global h_scroll
    global w_scroll
    use_click_and_drag_instead_of_scroll = True
    click_and_drag_amount = 220
    scroll_size = 220

    moveToWithRandomness(x_scroll+(w_scroll/2),y_scroll+400+(h_scroll/2),1)
    if not use_click_and_drag_instead_of_scroll:
        pyautogui.scroll(-scroll_size)
    else:
        pyautogui.dragRel(0,-click_and_drag_amount,duration=1, button='left')


def finish_boss():
    finish_boss = positions(env.images_space['finish_boss'], threshold=0.9)
    if len(finish_boss)!=0 :
        clickBtn(env.images_space['finish_boss'])
        time.sleep(0.8)


def go_to_ship():
    if clickBtn(env.images_space['ship']):
        print('Encontrou ship buttom')
        return True
    else:
        return False

def go_to_fight():
    if clickBtn(env.images_space['fight-boss']):
        print('''Vai para fight boss!!
        ''')

def ships_15_15():
    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(env.images_space['15-15-boss'], 1)

        if(len(matches)==0):
            has_timed_out = time.time()-start > 3
            continue
        print('Encontrou 15-15 tela naves')
        return True
    return False

def ships_0_15():
    matches = positions(env.images_space['0-15'], 0.8)

    if(len(matches)==0):
        print('Encontrou 0-15 tela naves')
        return False
    return True

def ships_15_15_boss():
    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(env.images_space['15-15-boss'], 1)

        if(len(matches)==0):
            has_timed_out = time.time()-start > 3
            continue
        print('Encontrou 15-15 boss')
        return True
    return False

def time_is_zero():
    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(env.images_space['time-zero'], 0.8)

        if(len(matches)==0):
            has_timed_out = time.time()-start > 3
            continue
        print('Encontrou time-zero')
        return True
    print('Time diferente de zero')
    return False

def click_fight_ship_new():
    global x_scroll
    global y_scroll
    global h_scroll
    global w_scroll
    scrollCheck = positions(env.images_space['newlatter'], threshold=0.9)       

    for key,(x, y, w, h) in enumerate(scrollCheck):
        #print('key: ', key)
        if key == 0:
            x_scroll = x
            y_scroll = y
            h_scroll = h
            w_scroll = w   

    if env.space['fight_100'] == True:
        print('naves 100%')
        button_run_ships = env.images_space['fight-100']
    else:
        button_run_ships = env.images_space['fight']
    

    buttomFight = positions(button_run_ships, threshold=0.9)
    
    not_working_green_bars = []
    for bar in buttomFight:
        not_working_green_bars.append(bar)

        
    if len(not_working_green_bars) > 0:
        print('buttons with green bar detected', len(not_working_green_bars))
        print('Naves disponiveis', len(not_working_green_bars))

    ship_clicks_cnt = 0
    for (x, y, w, h) in not_working_green_bars:
        if len(not_working_green_bars) > 0 :
            if ships_15_15():
                return len(not_working_green_bars)

            for i in range(len(not_working_green_bars)):
                #pyautogui.click()

                clickBtn(env.images_space['fight-100'], 3, 0.9)

                global ship_clicks
                ship_clicks = ship_clicks + 1
                ship_clicks_cnt = ship_clicks_cnt + 1
                if ship_clicks > 15:
                    return            
            print("Qtd ship enviadas: " + str(ship_clicks_cnt) + ". " + "Qtd ship total enviadas: " + str(ship_clicks))   
            #print("Qtd ship total enviadas", ship_clicks) 
            click_fight_ship_new()
        else:
            return len(not_working_green_bars)
    return len(not_working_green_bars)

       
def ship_to_fight():    
    global ship_clicks
    go_to_continue()
    verify_error()
    
    finish_boss()

    #if time_is_zero():
    if go_to_ship():
        ship_clicks = 0
        buttonsClicked = 1
        empty_scrolls_attempts = env.space['qtScroll']
        while(empty_scrolls_attempts >0):
            buttonsClicked = click_fight_ship_new()
            if ships_15_15():
                break 
            if buttonsClicked == 0:
                empty_scrolls_attempts = empty_scrolls_attempts - 1
                       
            if ship_clicks > 15:
                break    
            scroll_ships()
            time.sleep(1)
        go_to_fight()
    else:
        return
    #else:
    #    return

def go_to_ship_tela_boss():
    if clickBtn(env.images_space['ship-boss']):
        print('Volta para naves, tela boss')
        return True
    else:   
        return False

def ship_tela_boss():
    if ships_15_15_boss():
        return
    elif ships_15_15_boss() == False:        
        if go_to_ship_tela_boss():
            time.sleep(5)
            buttonsClicked = 1
            empty_scrolls_attempts = env.space['qtScroll']


            while(empty_scrolls_attempts >0):
                buttonsClicked = click_fight_ship_new()
                if buttonsClicked == 0:
                    empty_scrolls_attempts = empty_scrolls_attempts - 1
                if ships_15_15():
                    break
                scroll_ships()
                time.sleep(2)
            
            go_to_fight()


def login():
    
    print("Verificando se o jogo foi desconectado")
    go_to_continue()
    verify_error()

    victory_boss()

    if_surrender()

    loginButton = positions(env.images_space['connect-wallet'], threshold=0.9)
    if len(loginButton)!=0 :
        if clickBtn(env.images_space['connect-wallet'], timeout = 10):
            print('Connect wallet encontrado')
            verify_error()

        if clickBtn(env.images_space['sign'], timeout=8):
            print('Sign button encontrado')
            
            if clickBtn(env.images_space['play'], timeout = 15):
                print('Botao play encontrado')
                print('''Jogo iniciado com sucesso!!

                ''')
                login_attempts = 0
            return
    return


def if_surrender():
    boss_3 = positions(env.images_space['boss-3'], threshold=0.95)
    boss_4 = positions(env.images_space['boss-4'], threshold=0.95)
    boss_5 = positions(env.images_space['boss-5'], threshold=0.95)
    boss_6 = positions(env.images_space['boss-6'], threshold=0.95)
    boss_7 = positions(env.images_space['boss-7'], threshold=0.95)
    boss_8 = positions(env.images_space['boss-8'], threshold=0.95)
    boss_9 = positions(env.images_space['boss-9'], threshold=0.95)
    boss_10 = positions(env.images_space['boss-10'], threshold=0.95)
    boss_11 = positions(env.images_space['boss-11'], threshold=0.95)
    boss_12 = positions(env.images_space['boss-12'], threshold=0.95)

    if env.space['surrender_boss'] == 3:
        print('Surrender BOSS 3')
        if len(boss_3) != 0 or len(boss_4) != 0 or len(boss_5) != 0 or len(boss_6) != 0 or len(boss_7) != 0 or len(boss_8) != 0 or len(boss_9) != 0 or len(boss_10) != 0 or len(boss_11) != 0 or len(boss_12) != 0:
            print('Encontrou o boss')
            surrender()

    if env.space['surrender_boss'] == 4:
        print('Surrender BOSS 4')
        if len(boss_4) != 0 or len(boss_5) != 0 or len(boss_6) != 0 or len(boss_7) != 0 or len(boss_8) != 0 or len(boss_9) != 0 or len(boss_10) != 0 or len(boss_11) != 0 or len(boss_12) != 0:
            print('Encontrou o boss')
            surrender()
        
    if env.space['surrender_boss'] == 5:
        print('Surrender BOSS 5')
        if len(boss_5) != 0 or len(boss_6) != 0 or len(boss_7) != 0 or len(boss_8) != 0 or len(boss_9) != 0 or len(boss_10) != 0 or len(boss_11) != 0 or len(boss_12) != 0:
            print('Encontrou o boss')
            surrender()
    
    if env.space['surrender_boss'] == 6:
        print('Surrender BOSS 6')
        if len(boss_6) != 0 or len(boss_7) != 0 or len(boss_8) != 0 or len(boss_9) != 0 or len(boss_10) != 0 or len(boss_11) != 0 or len(boss_12) != 0:
            print('Encontrou o boss')
            surrender()
    
    if env.space['surrender_boss'] == 7:
        print('Surrender BOSS 7')
        if len(boss_7) != 0 or len(boss_8) != 0 or len(boss_9) != 0 or len(boss_10) != 0 or len(boss_11) != 0 or len(boss_12) != 0:
            print('Encontrou o boss')
            surrender()
    
    if env.space['surrender_boss'] == 8:
        print('Surrender BOSS 8')
        if len(boss_8) != 0 or len(boss_9) != 0 or len(boss_10) != 0 or len(boss_11) != 0 or len(boss_12) != 0:
            print('Encontrou o boss')
            surrender()
    
    if env.space['surrender_boss'] == 9:
        print('Surrender BOSS 9')
        if len(boss_9) != 0 or len(boss_10) != 0 or len(boss_11) != 0 or len(boss_12) != 0:
            print('Encontrou o boss')
            surrender()
    
    if env.space['surrender_boss'] == 10:
        print('Surrender BOSS 10')
        if len(boss_10) != 0 or len(boss_11) != 0 or len(boss_12) != 0:
            print('Encontrou o boss')
            surrender()
    
    if env.space['surrender_boss'] == 11:
        print('Surrender BOSS 11')
        if len(boss_11) != 0 or len(boss_12) != 0:
            print('Encontrou o boss')
            surrender()
    
    if env.space['surrender_boss'] == 12:
        print('Surrender BOSS 12')
        if len(boss_12) != 0:
            print('Encontrou o boss')
            surrender()
    
def surrender():
    print('Surrender Success')
    button_surrender = positions(env.images_space['surrender'], threshold=0.9)
    if len(button_surrender) != 0:
        clickBtn(env.images_space['surrender'])
        print('Click surrender')
        time.sleep(1)

def confirm_surrender():
    print('Confirm Surrender')
    button_surrender = positions(env.images_space['confirm-surrender'], threshold=0.9)
    if len(button_surrender) != 0:
        clickBtn(env.images_space['confirm-surrender'])
        print('Click confirm surrender')
        time.sleep(0.8)

def victory_boss():
    victory = positions(env.images_space['victory'], threshold=0.9)
    if len(victory)!=0 :
        print('Victory Success!')
        clickBtn(env.images_space['victory-button'])
        time.sleep(0.8)

def verify_error():
    if clickBtn(env.images_space['error'], timeout = 8):
        print('Erro Login')
        pyautogui.hotkey('ctrl','f5')
        time.sleep(0.6)
        login()
        return

def go_to_continue():
    if clickBtn(env.images_space['confirm']):
        print('Encontrou confirm')
        time.sleep(0.6)
        return True
    else:
        return False