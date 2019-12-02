import pyautogui

print('Press Ctrl-C to quit.')

width, height = pyautogui.size()

try:
    while True:
        # Get and print the mouse coordinates.
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        xpercent = x / width
        ypercent = y / height
        positionStr += ' X%: ' + str(round(xpercent, 4)).rjust(4) + ' Y%: ' + str(round(ypercent, 4)).rjust(4)
        pixelColor = pyautogui.screenshot().getpixel((x, y))
        positionStr += ' RGB: (' + str(pixelColor[0]).rjust(3)
        positionStr += ', ' + str(pixelColor[1]).rjust(3)
        positionStr += ', ' + str(pixelColor[2]).rjust(3) + ')'
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\nDone.')