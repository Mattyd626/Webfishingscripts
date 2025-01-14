import keyboard
import pyautogui
import numpy as np
import pytesseract
import cv2
import time

current_keys = set()

win_colour = [164,170,57]
grey_colour = [164,157,156]
threshold = 1

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def gamble(count):
    current_keys.clear()
    next_scratch(count+1)
    time.sleep(1.25)
    # log_result()    #Optional if u wanna know ur earnings?

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

def log_result():
    region = (929, 582, 701, 616)
    screenshot = pyautogui.screenshot(region=region)
    screenshot_np = np.array(screenshot)

    for x in range(len(screenshot_np)):
        for y in range(len(screenshot_np[x])):
            current_colour = [int(_) for _ in screenshot_np[x,y]]
            abs_diff = abs(current_colour[0] - win_colour[0]) + abs(current_colour[1] - win_colour[1]) + abs(current_colour[2] - win_colour[2])
            if abs_diff < threshold:
                screenshot_np[x,y] = [0,0,0]
            else:
                screenshot_np[x,y] = [255,255,255]

    for x in range(1,len(screenshot_np)-1):
        for y in range(1,len(screenshot_np[x])-1):
            if screenshot_np[x,y,0] == 0:
                neighbours = -1
                for x1 in range(-1,2):
                    for y1 in range(-1,2):
                        if screenshot_np[x+x1,y+y1,0] == 0:
                            neighbours += 1

                if neighbours < 2:
                    screenshot_np[x,y] = [255,255,255]

    gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    with open("gambling_data.txt", "a") as f:
        wins = []
        for value in text.split("\n"):
            if '$' in value:
                number = value[1:value.find('.')]
                print(f"Gained ${number}")
                wins.append(number)
        if len(wins) == 0:
            f.write("0\n")
        else:
            f.write(f"{','.join(wins)}\n")

def on_press(event):
    current_keys.add(event.name)
    if 'ctrl' in current_keys and 'g' in current_keys:
        gamble(1)

def on_release(event):
    current_keys.remove(event.name)

keyboard.on_press(on_press)
keyboard.on_release(on_release)
keyboard.wait('\\')
