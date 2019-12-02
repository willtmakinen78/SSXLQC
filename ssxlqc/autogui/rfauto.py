import time
import pyautogui as pag
from ssxlqc.numtest import is_number

width, height = pag.size()

def collect(bot_num, save_location=None):

    if is_number(bot_num) == False:
        raise Exception("bot_num must be an number")

    # click application taskbar icon
    print("rf recording started")
    pag.click(0.047 * width, 0.98 * height)
    time.sleep(0.5)

    # click the diagnostics button
    pag.click(0.05 * width, 0.335 * height)
    time.sleep(1.5)

    # click the iBot Data tab
    print("switching to iBot Data tab, can be laggy so waiting 8 secs...")
    pag.click(0.4 * width, 0.033 * height)
    time.sleep(8)

    # click the UCID input box
    pag.click(0.135 * width, 0.105 * height)
    time.sleep(0.5)

    # type in the bot num
    pag.typewrite("\b\b\b\b\b\b" + str(bot_num))

    # click the add UCID button
    pag.click(0.135 * width, 0.133 * height)
    time.sleep(0.5)

    # click the Start Logging button
    pag.click(0.135 * width, 0.366 * height)
    print("logging started")
    time.sleep(0.5)

def stop():

    # cannot assume that window is still active, re-navigate back to it
    # click application taskbar icon
    print("ending recording")
    pag.click(0.047 * width, 0.98 * height)
    time.sleep(0.5)

    # click the diagnostics button
    pag.click(0.05 * width, 0.335 * height)
    time.sleep(1.5)

    # click the iBot Data tab
    print("switching to iBot Data tab, can be laggy so waiting 8 secs...")
    pag.click(0.4 * width, 0.033 * height)
    time.sleep(8)

    # click the Stop Logging button
    pag.click(0.135 * width, 0.41 * height)
    print("logging ended")
    time.sleep(0.5)

    # click the remove UCID button
    pag.click(0.135 * width, 0.155 * height)
    time.sleep(0.5)
