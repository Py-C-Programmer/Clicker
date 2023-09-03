import time
import pickle
import re
import os
from threading import Thread
import keyboard as keyb
from pynput import mouse
from pynput import keyboard
import pyautogui as pag
#pag.FAILSAFE = True

UKR = 'йцукенгшщзхїфівапролджєячсмитьбю'
ENG = 'qwertyuiop  asdfghjkl  zxcvbnm  '
PRESS = []
T = 0
T1 = 0
END = False
PLAY = True
PAUSE = False

def playing():
    def escape_click(key):
        if key == keyboard.Key.esc:
            global PLAY
            PLAY = False
            return False
        elif key == keyboard.Key.space:
            global PAUSE
            PAUSE = True
        
    with keyboard.Listener(on_release=escape_click) as k_listener:
        k_listener.join()

def TIME():
    global T1
    while True:
        if END != True:
            T1 += 0.01
            time.sleep(0.01)
        else:
            break

def on_release(key):
    if key == keyboard.Key.esc:
        global END
        END = True
        return False
    k = '{0}_button'.format(
        key)
    global T, T1
    t = T1 - T
    PRESS.append(k)
    PRESS.append(str(t))
    T = T1
    
def on_click(x, y, button, pressed):
    global END
    if END == True:
        return False
    m = '{0}_{1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y))
    global T, T1
    t = T1 - T
    PRESS.append(m)
    PRESS.append(str(t))
    T = T1

def Play(PRESS):
    try:
        COUNT = int(input('Enter the number of repetitions of operations>>> '))
        SPEED = float(input('Enter a coefficient of operations speed>>> '))
        CHANGE = input('Do you want to add any changes to the program between the repetitions? (print "y" or "n")>>> ')

        if CHANGE == 'y':
            print('--------------------------------------------')
            clicks = []
            for i in PRESS[::2]:
                if 'Pressed' in i or 'DoubleClick' in i:
                    clicks.append(i)
            for i in clicks:
                print(PRESS.index(i), i)
            print('These are all your clicks in the program.')
            actionIndex = input('Enter (using spaces) the numbers of the clicks, coordinates of which you want to change>>> ')
            actionIndex = actionIndex.split(' ')
            changes = []
            for i in actionIndex:
                change_x = input(f'Enter the number you want to add to the previous x-coordinate of the click number {i} (the number must be an integer)>>> ')
                change_y = input(f'Enter the number you want to add to the previous y-coordinate of the click number {i} (the number must be an integer)>>> ')
                change = i + f'_({change_x}, {change_y})'
                changes.append(change)
                
        playing_stream = Thread(target = playing)
        playing_stream.start()

        global PAUSE
        
        for c in range(COUNT):
            for press in PRESS:
                if PLAY == True:
                    if PAUSE == True:
                        print("The program is paused!")
                        keyb.wait('ctrl')
                        print("The program is continuing...")
                        PAUSE = False
                    try:
                        if '_button' in press:
                            text = press.replace('_button', '')
                            if 'Key.' in press:
                                text = text.replace("Key.", '')
                                text = text.replace("_l", '')
                                time.sleep(0.05)
                                pag.press(text)
                            elif '\\x03' in press:
                                time.sleep(0.05)
                                pag.hotkey('ctrl', 'c')
                            elif '\\x16' in press:
                                time.sleep(0.05)
                                pag.hotkey('ctrl', 'v')
                            else:
                                text = text.replace("'", '')
                                if re.search(r'[^а-яА-Я]', text): #if there isn't any cyrillic letters
                                    time.sleep(0.05)
                                    pag.typewrite('{0}'.format(text))
                                else:
                                    text = ENG[UKR.index(text)]
                                    time.sleep(0.05)
                                    pag.typewrite('{0}'.format(text))
                                
                        elif 'Pressed_' in press:
                            p = press.replace('Pressed_', '')
                            p = p.replace('(', '')
                            p = p.replace(')', '')
                            coor = p.split(', ')
                            x, y = int(coor[0]), int(coor[1])

                            p1 = PRESS[PRESS.index(press) + 2]
                            p1 = p1.replace('Released_', '')
                            p1 = p1.replace('(', '')
                            p1 = p1.replace(')', '')
                            coor1 = p1.split(', ')
                            x1, y1 = int(coor1[0]), int(coor1[1])

                            if x == x1 and y == y1:
                                pag.moveTo(x, y, duration = float(PRESS[PRESS.index(press) + 1])/SPEED)
                                time.sleep(0.05)
                                pag.click(x, y)
                            else:
                                pag.moveTo(x, y, duration = float(PRESS[PRESS.index(press) + 1])/SPEED)
                                pag.dragTo(x1, y1, duration = float(PRESS[PRESS.index(press) + 3]))

                        elif 'DoubleClick_' in press:
                            p = press.replace('DoubleClick_', '')
                            p = p.replace('(', '')
                            p = p.replace(')', '')
                            coor = p.split(', ')
                            x, y = int(coor[0]), int(coor[1])

                            pag.moveTo(x, y, duration = float(PRESS[PRESS.index(press) + 1])/SPEED)
                            time.sleep(0.05)
                            pag.doubleClick(x, y)

                    except:  #Exception as e
                        pass

                else:
                    break

            if CHANGE == 'y':
                for i in changes:
                    m = i.split('_')
                    ind = int(m[0])
                    coor_new = m[1]
                    coor_new = coor_new.replace('(', '')
                    coor_new = coor_new.replace(')', '')
                    coor_new = coor_new.split(', ')
                    x_new, y_new = int(coor_new[0]), int(coor_new[1])
                            
                    p = PRESS[ind]
                            
                    if 'Pressed_' in p:
                        p = p.replace('Pressed_', '')
                        p = p.replace('(', '')
                        p = p.replace(')', '')
                        coor = p.split(', ')
                        x, y = int(coor[0]), int(coor[1])

                        p1 = PRESS[ind + 2]
                        p1 = p1.replace('Released_', '')
                        p1 = p1.replace('(', '')
                        p1 = p1.replace(')', '')
                        coor1 = p1.split(', ')
                        x1, y1 = int(coor1[0]), int(coor1[1])
                                    
                        x += x_new
                        x1 += x_new
                        y += y_new
                        y1 += y_new
                        PRESS[ind] = f'Pressed_({x}, {y})'
                        PRESS[ind+2] = f'Released_({x1}, {y1})'

                    elif 'DoubleClick_' in p:
                        p = p.replace('DoubleClick_', '')
                        p = p.replace('(', '')
                        p = p.replace(')', '')
                        coor = p.split(', ')
                        x, y = int(coor[0]), int(coor[1])

                        x += x_new
                        y += y_new
                        PRESS[ind] = f'DoubleClick_({x}, {y})'
            
    except:
        print('Sorry, but you maybe entered an incorrect value!')
            
def Record():
    stream = Thread(target = TIME)
    stream.start()
    
    try:    
        with keyboard.Listener(on_release=on_release) as k_listener, mouse.Listener(on_click=on_click) as m_listener:
            k_listener.join()
            m_listener.join()
    except KeyboardInterrupt:
        pass

    for i in PRESS:
        try:
            if 'Pressed_' in i and i == PRESS[PRESS.index(i)+4] and float(PRESS[PRESS.index(i)+5]) <= 0.07:
                i1 = i.replace('Pressed', 'DoubleClick')
                PRESS[PRESS.index(i):(PRESS.index(i)+8)] = i1, PRESS[PRESS.index(i)+1]
            if "'\\x03'_button" in i or "'\\x16'_button" in i:
                if PRESS[PRESS.index(i)+2] == 'Key.ctrl_l_button':
                    PRESS.pop(PRESS.index(i)+3)
                    PRESS.pop(PRESS.index(i)+2)
                    PRESS.pop(PRESS.index(i)+1)
                else:
                    PRESS.pop(PRESS.index(i)+1)
        except:
            pass
    
    print('Recording is finished!')
    save = input('Do you want to save this program? (print "y" or "n")>>> ')
    if save == 'y':
        name = input('Enter the name of the program>>> ')
        name = 'C:\\key_press_detect_programes\\' + name + '.pickle'
        with open(name, "wb") as f:
            pickle.dump(PRESS, f)
        print('The program is saved into <C:\key_press_detect_programes>')
    else:
        print('The program is not saved!')
    play = input('Do you want to play the program? (print "y" or "n")>>> ')
    if play == 'y':
        Play(PRESS)

###Start###
if os.path.exists('C:\\key_press_detect_programes') == False:
    os.mkdir('C:\\key_press_detect_programes')

print('Saved programs:')
i = 1
files = []
for r,d,f in os.walk("C:\\key_press_detect_programes"):
    files = f
for file in files:
    print(i, file)
    i += 1
if i == 1:
    print('0')


main = input('If you want to play one of them, enter "p". If you want to record a new one, enter "r">>> ')
if main == 'p':
    prog = input('Enter the name of the program>>> ')
    with open(f"C:\\key_press_detect_programes\\{prog}", "rb") as f:
        operations = pickle.load(f)
    Play(operations)
elif main == 'r':
    print('Recording will start in 5 seconds...')
    time.sleep(1)
    seconds = 4
    for sec in range(5):
        print(seconds, 'seconds')
        seconds -= 1
        time.sleep(1)
    print('Recording has been started!')
    Record()


