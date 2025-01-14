import keyboard
import pyautogui
import numpy as np
import time

current_keys = set()

win_colour = [164,170,57]
grey_colour = [164,157,156]
threshold = 1

def gamble(count):
    current_keys.clear()
    next_scratch(count+1)
    time.sleep(1.25)

def next_scratch(count):
    pyautogui.moveTo(1850,1300)
    pyautogui.click()
    if count % 5 == 0:
        keyboard.press("s")
        time.sleep(2)
        keyboard.release("s")
        keyboard.press("w")
        time.sleep(2)
        keyboard.release("w")
        time.sleep(10)
    pyautogui.moveTo(1280,1340)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(980,660)
    keyboard.press("w")
    time.sleep(0.15)
    pyautogui.click()
    keyboard.release("w")
    time.sleep(1.5)
    pyautogui.moveTo(1060,1370)
    pyautogui.click()
    time.sleep(0.25)
    region = (980, 660, 600, 500)
    screenshot = pyautogui.screenshot(region=region)
    screenshot_np = np.array(screenshot)

    is_scratch_card_up = True
    for x in range(len(screenshot_np)):
        for y in range(len(screenshot_np[x])):
            current_colour = [int(_) for _ in screenshot_np[x,y]]
            abs_diff = abs(current_colour[0] - grey_colour[0]) + abs(current_colour[1] - grey_colour[1]) + abs(current_colour[2] - grey_colour[2])
            if abs_diff > 10:
                is_scratch_card_up = False
    
    if is_scratch_card_up:
        scratch()
        gamble(count)
    else:
        print("Out of scratch cards :(")

def scratch():
    pyautogui.moveTo(928,580)
    pyautogui.mouseDown()
    for y in range(582,1198,30):
        pyautogui.moveTo(900,y)
        pyautogui.moveTo(1630,y)
    pyautogui.mouseUp()

def on_press(event):
    current_keys.add(event.name)
    if 'ctrl' in current_keys and 'g' in current_keys:
        gamble(1)

def on_release(event):
    current_keys.remove(event.name)

keyboard.on_press(on_press)
keyboard.on_release(on_release)
keyboard.wait('\\')
