import tkinter
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

try:
    with open('directory.txt') as file:
        directories = file.readlines()
        if len(directories) != 2:
            raise FileNotFoundError
        chrome_path = directories[0].replace('\\', '\\\\')
        chrome_path = chrome_path.strip()
        driver_path = directories[1].replace('\\', '\\\\')
        driver_path = driver_path.strip()
except FileNotFoundError:
    with open('directory.txt', 'a+') as file:
        path = input("Enter the full path for your Chrome executable: ")
        file.write(path + '\n')
        path = input("Enter the full path for your Selenium Chrome Webdriver: ")
        file.write(path)
        file.seek(0)
        directories = file.readlines()
        chrome_path = directories[0].replace('\\', '\\\\')
        chrome_path = chrome_path.strip()
        driver_path = directories[1].replace('\\', '\\\\')
        driver_path = driver_path.strip()

try:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = chrome_path

    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
    driver.get("https://genius.com/")

    search = input("Enter in the song name and artist of the song you want the lyrics to: ")

    search_box = driver.find_element_by_xpath("""/html/body/div[1]/search-form/form/input""") #search field
    search_box.click()

    search_box.clear()
    search_box.send_keys(search)
    search_box.send_keys(Keys.RETURN)

    card_elements = ['mini_card', 'mini_card-info', 'u-quarter_vertical_margins u-clickable', 'mini_card--small',
                     'mini_card-thumbnail clipped_background_image--background_fill clipped_background_image']

    for i in range(len(card_elements)):
        try:
            result = driver.find_element_by_class_name(card_elements[i])    #results
            break
        except NoSuchElementException:
            if i + 1 < len(card_elements):
                i += 1
                pass
            else:
                print("The search failed... Try again.")
                time.sleep(2)
                raise

    result.click()

    lyrics = driver.find_elements_by_xpath("""/html/body/routable-page/ng-outlet/song-page/div/div/div[2]/div[1]/div
        /defer-compile[1]/lyrics/div/div/section/p""")

    text = ""
    for lyric in lyrics:
        text += lyric.text + '\n'

    screen = tkinter.Tk()
    w = Text(screen, bg='black', fg='white')
    w.insert(INSERT, text)
    w.insert(END, "")
    w.pack()
    screen.mainloop()
except Exception:                                                  # I only used this because I wasn't sure on how to
    driver.quit()                                                  # make the driver quit every time the program crashed

# Future Improvements
# Full GUI integration from launch
# Make background color of lyric screen have something to do with the song, like possibly how the album page of an
# iTunes uses the main color of the album art
