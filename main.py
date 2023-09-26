from PIL.Image import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
from PIL import ImageGrab, Image
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# -----------------FUNCTIONS-------------------
def jump():
    ActionChains(driver).key_down(Keys.SPACE).perform()


def get_image():
    screenshot = ImageGrab.grab(bbox=(40, 400, 990, 700))
    # screenshot.save("img.png") #  for adjusting ImageGrab.grab(bbox=(starting x coordinates, starting y coordinates,
    #                                                                  last x coordinates, last y coordinates ))
    screenshot_np = np.array(screenshot)
    return screenshot_np


def detect_revers(screen):
    field = screen[1:2, 1:2]
    gray = np.mean(field, axis=2)
    detect = (gray < 100).astype(np.uint8) * 255
    if 255 in detect[:, :]:
        return True
    else:
        return False


def reversed_obstacle(screen):
    t_rex = screen[95:155, 90:300]

    # For checking detect field dimensions. Its need to be complete white or black in reversed_obstacle functions
    # img = Image.fromarray(t_rex, 'RGB')
    # img.save('field.png')

    gray = np.mean(t_rex, axis=2)
    detect_field = (gray > 100).astype(np.uint8) / 255

    # print(detect_field) it's show content in np.array
    return np.any(detect_field)


def obstacle(screen):
    t_rex = screen[95:155, 90:280]

    # For checking detect field dimensions. Its need to be complete white or black in reversed_obstacle functions
    # img = Image.fromarray(t_rex, 'RGB')
    # img.save('field.png')

    gray = np.mean(t_rex, axis=2)
    detect_field = (gray < 100).astype(np.uint8) * 255

    # print(detect_field) it's show content in np.array
    return np.any(detect_field)

# ----------------------------------------------------------------------------

WEB_ADDRESS = "https://elgoog.im/t-rex/"

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

driver.get(WEB_ADDRESS)

time.sleep(4)  # You can adjust sleep length accordingly to your internet speed.
jump()

try:
    while True:
        screen = get_image()
        reverse = detect_revers(screen)
        if reverse:
            if reversed_obstacle(screen):
                jump()
        else:
            if obstacle(screen):
                jump()
except KeyboardInterrupt:
    # Exit ctrl+c
    driver.quit()
