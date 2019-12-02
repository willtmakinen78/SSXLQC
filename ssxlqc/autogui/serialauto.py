import time
import datetime
import os.path
import pyautogui as pag
from ssxlqc.numtest import is_number

width, height = pag.size()

def collect(bot_num, test_type, save_location=None):

    if is_number(bot_num) == False:
        raise Exception("bot_num must be an number")

    if test_type != "track" and test_type != "conveyer":
        raise Exception("test_type must be an 'track' or 'conveyer'")

    if save_location != None:
        if os.path.exists(save_location) == False:
            raise Exception("save_location does not exist")

    print("beginning serial test")

    # click on ELMO composer icon
    pag.click(0.078 * width, 0.9815 * height)
    time.sleep(0.5)

    # click open communication directly
    print("opening serial port")
    pag.click(0.3932 * width, 0.0556 * height)
    time.sleep(0.5)

    # click finish
    pag.click(0.5156 * width, 0.6528 * height)
    time.sleep(2)

    # click ELMO studio button
    print("swithing to ELMO Studio")
    pag.click(0.1823 * width, 0.0556 * height)
    time.sleep(1.5)

    # ctr-o to open a file
    print("opening .ehl file")
    pag.hotkey('ctrl', 'o')
    time.sleep(1)

    # type in the script filename
    if test_type == "track":
        pag.typewrite("SSXL_Track_Test.ehl")
    elif test_type == "conveyer":
        pag.typewrite("SSXL_Conveyer_Test.ehl")
    pag.press('enter')
    time.sleep(1)

    # build script
    pag.press('f7')
    time.sleep(10)
    print("building script")

    # click ELMO composer icon
    print("opening motion monitor")
    pag.click(0.078 * width, 0.9815 * height)
    time.sleep(0.8)

    # open motion monitor
    pag.click(0.1683 * width, 0.0556 * height)
    time.sleep(0.5)

    # click on resolution down arrow
    print("inputting recording parameters")
    pag.click(0.0635 * width, 0.4769 * height)
    time.sleep(0.3)

    # choose 14.4 msec/point
    pag.click(0.0312 * width, 0.5648 * height)
    time.sleep(0.3)

    # click start recording
    pag.click(0.1849 * width, 0.5 * height)
    time.sleep(0.3)
    print("motion monitor started")

    # click ELMO studio button
    pag.click(0.1823 * width, 0.0556 * height)
    time.sleep(1)

    # start program
    pag.hotkey('ctrl', 'f5')
    print("running script")
    time.sleep(36)

    # export data
    print("exporting data")
    pag.hotkey('ctrl', 'e')
    time.sleep(1)

    # click path bar
    pag.click(0.3594 * width, 0.0417 * height)
    time.sleep(1)

    # enter file path
    if save_location != None:
        pag.typewrite(save_location)
    pag.press('enter')
    time.sleep(0.3)

    # click file type chooser
    pag.click(0.4036 * width, 0.4259 * height)
    time.sleep(0.3)

    # choose .txt file type
    pag.click(0.4036 * width, 0.4583 * height)
    time.sleep(0.3)

    # click filename bar
    pag.click(0.4036 * width, 0.4028 * height)
    time.sleep(0.3)

    # save with the current date and time in the filename
    now = datetime.datetime.now()
    date_time = now.strftime("_%Y%m%d_%H%M%S")
    filename = "SSXL{}".format(bot_num) + date_time

    pag.typewrite(filename)
    pag.press('enter')
    print("data saved")
    time.sleep(1)

    # click ELMO composer icon
    print("closing connection")
    pag.click(0.078 * width, 0.9815 * height)
    time.sleep(0.5)

    # click end connection
    pag.click(0.4068 * width, 0.0454 * height)
    time.sleep(0.5)

    # click yes to confirm close
    pag.click(0.5026 * width, 0.5296 * height)

    print("test complete")
    
# path: C:\Users\Opex\Documents\QC Automation\SSXLQC-0.1.0\ssxlqc\data\conveyer
    