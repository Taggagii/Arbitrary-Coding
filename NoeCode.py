'''
Home made cipher joke, it's lost all effectiveness now that it's posted online. But it was just me playing around to see if I made some weird and arbitrary 
encoding technique then could I find a way to decode it too. Was fun to make. Nearly useless. Outputs in binary so the user can send the messages without loss
from things like discord, which take certain characters (* `) to mean different things than literals
'''


import math
def prime(n):
    n = int(n)
    if n <= 3: return n > 1
    if n % 2 == 0 or n % 3 == 0: return False
    for i in range(5, int(math.sqrt(n))+1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def is_digit(number):
    try:
        int(number)
        return True
    except:
        return False
    
def square_free_int(number):
    number = int(number)
    if number % 2 == 0:
        number //= 2
        if number % 2 == 0: return False
    p = 1
    while number > 2 and not prime(number):
        p += 2
        if prime(p):
            if number % p == 0:
                number //= p
                if number % p == 0: return False
    return True

def make_key_string(key, message):
    key_size = len(key)
    key_string = ''
    for i in range(len(message)):
        if message[i] == ' ':
            yield ' '
            continue
        yield key[i%key_size]
    return key_string

def to_bin(message):
    message = list(message)
    for i in range(len(message)):
        message[i] = bin(ord(message[i]))[2:]
    return ' '.join(message)

def from_bin(message):
    message = message.split()
    for i in range(len(message)):
        message[i] = '0b' + message[i]
    for i in range(len(message)):
        message[i] = chr(int(message[i], 2))
    return ''.join(message)

def bin_check(message):
    for i in message:
        if i != '0' and i != '1' and i != ' ':
            return False
    return True

def prep_decode(message):
    message = list(message)
    for i in range(len(message)):
        if is_digit(message[i]):
            if message[i-1] == '^' and message[i-2] == '^':
                message[i-1] = ''
                message[i-2] = ''
                message[i] = 'b' + str(ord(message[i]))
                continue
            if message[i-1] == '~' and message[i-2] == '~':
                message[i-1] = ''
                message[i-2] = ''
                message[i] = str(-ord(message[i]))
                continue
            message[i] = ord(message[i])
    for i in range(len(message)):
        if is_digit(message[i]) or message[i] == ' ': continue
        if message[i] == '': continue
        if message[i][0] == 'b': continue
        if message[i] == '|' and message[i+1] == '|':
            message[i] = ''
            message[i+1] = '0'
            continue
        if message[i] == '~' and message[i+1] == '~':
            message[i] = ''
            message[i+1] = ''
            message[i+2] = str(-ord(message[i+2]))
            continue
        if message[i] == '^' and message[i+1] == '^':
            message[i] = ''
            message[i+1] = ''
            message[i+2] = 'b' + str(ord(message[i+2]))
            continue
        elif message[i] != '':
            message[i] = str(ord(message[i]))
    for i in range(message.count('')): del(message[message.index('')])
    fake_message = []
    for i in message:
        if i == ' ': fake_message.append(' ')
        else: fake_message.append('0')
    return message, ''.join(fake_message)

def encode(letter, key_letter):
    if letter == ' ': return ' '
    asc = ord(letter)
    key = ord(key_letter)
    value = asc + key
    if square_free_int(value): return chr(value)
    value = asc - key
    if value < 0: return '~~' + chr(-value)
    if value == 0: return '||'
    if square_free_int(value): return '^^' + chr(value)
    return chr(value) 


def decode(asc, key):
    inverse = False
    if asc == 0: return key
    if asc == ' ': return ' '
    if str(asc)[0] == 'b':
        asc = asc[1:]
        inverse = True
    try:
        asc, key = int(asc), int(ord(key))
        value = asc - key
        if square_free_int(asc) and not inverse: return chr(value)
        return chr(asc + key)
    except Exception as e:
        return chr(asc + key)

import pynput as pp
import pyautogui as p
import sys
counter = 0
leave = False

key, message, compressed = '', '', ''
def on_press(key):
    global counter
    if key == pp.keyboard.Key.f6:
        counter -= 1
        p.press('enter')
    if key == pp.keyboard.Key.esc:
        global leave
        counter = -1
        leave = True
        key, message = '', ''
        p.press('enter')
        return False

def clear():
    output = ['\n']*44
    output.insert(9, 'Press ESC to leave at any time\n')
    if message != '': output.insert(10, f'Message: {message}\n')
    if key != '': output.insert(11, f'Key: {key}{compressed}')
    print(''.join(output))
    
l = pp.keyboard.Listener(on_press = on_press)
l.start()

while not leave:
    if counter <= 0:
        message, key = '', ''
        clear()
        print('\nWelcome thethe NoeCode Encrypter / Decrypter\nWould you like to perform an encryption or a decryption? (press esc at any point to leave)')
        action = input()
        if counter < 0: continue
        if any(i in action for i in ('e', 'encrypt', 'enc', 'encode')): action = 'e'
        else: action = 'd'
        counter = 1
    if counter == 1:
        message, key = '', ''
        clear()
        txt = input('\nWould you like to read from a txt? (f6 for back): ')
        if counter < 1: continue
        if any(i in txt for i in ('y', 'yes', 'sure', 'yeah')): txt = True
        else: txt = False
        counter = 2
    if counter == 2:
        while True:
            message = ''
            key = ''
            clear()
            if not txt: message = input('Enter a message (f6 for back): ')
            else:
                while True:
                    try:
                        clear()
                        name = input('\nEnter the name of the txt (leave off .txt from the end) (f6 for back): ')
                        if counter < 2: break
                        message = open(f'{name}.txt', 'r').read()
                        break
                    except:
                        pass
            if counter < 2: break
            counter = 3
            if message != '' and message != '': break
    if counter == 3:
        while True:
            key = ''
            compressed = ''
            clear()
            key = input('\nEnter the key (f6 for back): ')
            if counter < 3: break
            if len(key) > len(message):
                key = key[:len(message)]
                compressed = ' (compressed to fit message size)'
            counter = 4
            if key != '' and key != '': break
    if counter == 4:
        clear()
        txt = input('\nWould you like to print the result to a txt? (f6 for back): ')
        if counter < 4: continue
        if any(i in txt for i in ('y', 'yes', 'sure', 'yeah')): txt = True
        else:
            txt = False 
        yes = txt
        counter = 5
    if counter == 5:
        clear()
        if txt:
            name = input('Enter the name of the txt to write to (leave off .txt from the end) (f6 for back): ')
            txt = open(f'{name}.txt', 'w')
            if counter < 5: continue
        counter = 6
    if counter == 6:
        clear()
        if action == 'e':

            key_gen = make_key_string(key, message)
            thing = ''
            for i in message:
                thing += encode(i, next(key_gen))
            print('\nKey: ' + key, end = '\nThe encryption is: \n')
            print(''.join(['=']*6) + 'START'+ ''.join(['=']*6))
            print(thing)
            print(''.join(['=']*6) + 'END'+ ''.join(['=']*8))
            print('As binary:')
            print(to_bin(thing))
            if yes:
                txt.write(to_bin(thing))
                txt.close()
                print('Written to', f'{name}.txt')
            input('Press ENTER to restart or ESC to leave: ')
            if counter < 6:
                counter = 4
                continue
            counter = 0
        if action == 'd':
            clear()
            if bin_check(message):
                message = from_bin(message)
            message_copy, fake_message = prep_decode(message)
            key_gen = make_key_string(key, fake_message)
            thing = ''
            for i in message_copy:
                thing += decode(i, next(key_gen))
            print('The decoded message is:\n', thing)
            if yes:
                txt.write(thing)
                txt.close()
                
                print('Written to', f'{name}.txt')
            input('Press ENTER to restart or ESC to leave: ')
            if counter < 6:
                counter = 4
                continue
            counter = 0
clear()
print(''.join(['\n']*10))
print('Thank you for using the NoeCode Encrypter / Decrypter\nHave a nice day!')
