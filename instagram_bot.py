from selenium import webdriver
import requests, random
import time
import os, notify2
from os import path, listdir, unlink
import shutil
from bs4 import BeautifulSoup
import pyautogui as screen_gui
from urllib.request import urlretrieve
from multiprocessing import Process

# wait exception
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException



class Bot:
    url = 'https://www.brainyquote.com/quote_of_the_day'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    img = soup.find('img')['alt']
    quote = img.split('-')[0]

    def __init__(self):

        url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
        self.browser = webdriver.Chrome(executable_path=r'/home/rohit/Downloads/chromedriver')
        self.browser.get(url)

        # exception for internet connection speed
        try:
            time.sleep(2)
            user = WebDriverWait(self.browser, 20).until(ec.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')))
            user.send_keys('  ')


            password = WebDriverWait(self.browser, 20).until(ec.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')))
            password.send_keys('  ')

            # log in click
            time.sleep(1)
            login = WebDriverWait(self.browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button')))
            login.click()

        except ConnectionError:
            self.notification('Sorry, Get a good internet connection. You internet is too sucks!')
            self.browser.close()



        # Image download process
        Process(target=self.image_download_way1).start()

        self.browser_start()


    # close browser
    def close_browser(self):
        return self.browser.close()


    @staticmethod
    def make_dir():
        folder = '/root/Documents/social_media'
        if os.path.exists(folder):
            return os.chdir(folder)
        else:
            os.mkdir(folder)
            return os.chdir(folder)


    # check if file found in database or not
    @staticmethod
    def database_check(file):
        with shutil.open(file) as file_name:
            if file in file_name:
                return True
            else:
                return False

    # show notification to process
    @staticmethod
    def notification(message):
        notify2.init('notice')
        notice = notify2.Notification('Instagram Bot', message=message)
        notice.set_timeout(5000)
        return notice.show()


    # delete images after job done
    def delete_image(self):
        folder = 'C:/Users/ABC/Documents/social_media'
        for i in listdir(folder):
            file = path.join(folder, i)
            try:
                if path.isfile(file):
                    unlink(file)
                    self.notification('Images has been deleted.')
                else:
                    shutil.rmtree(file)
            except IOError:
                self.notification('There was something error while deleting images!')


    def image_download_way1(self):
        api = f'https://api.unsplash.com/search/photos?query=programming&resolution=1500&orientation=landscape&client_id=71fab1070168597fcfd2bf922067b1b266a00074285460c4fa4e1967dff36384&page={random.randint(1,10)}&w=1500&dpi=2'
        res = requests.get(api).json()
        if not 'errors' in res:
            image_list = []
            try:
                for i in range(1,11):
                    url = res[i]['links']['download']

                    # checking dir is exists or not
                    self.make_dir()

                    name_of_image = str(res[i]['alt_description'])
                    img_name = '_'.join(name_of_image[:40].split(' '))
                    image_list.append([url, img_name+'.jpg'])
            except IndexError:
                self.notification('During image downloading we found an error: List index out of range!, we are retrying.')
                self.image_download_way1()

            img_select = random.randint(1, 10)
            # download one image
            urlretrieve(image_list[img_select][0], image_list[img_select][1])
            self.notification('Image has been downloaded in you disk.')

        else:
            self.notification('API is not valid. Get a new "Unsplash API"')
            self.browser.close()


    def browser_start(self):
        try:
            # press these keys to get 'Dev tool'
            screen_gui.hotkey('shift','ctrl', 'm')
            time.sleep(3)

            # waiting until page not load
            WebDriverWait(self.browser, 30).until(ec.visibility_of_element_located(
                (By.XPATH, '/html/body/span/section/main/section/div[2]/div[1]/div/article[1]')))

            # It's moving to click mobile view
            screen_gui.moveTo(x=697, y=253, duration=.2)
            time.sleep(1)
            screen_gui.click()

            # select device
            screen_gui.moveTo(x=679, y=276, duration=.2)
            screen_gui.click()

            # waiting until page not load
            WebDriverWait(self.browser, 30).until(ec.visibility_of_element_located(
                (By.XPATH, '/html/body/span/section/main/section/div[2]/div[1]/div/article[1]')))


            screen_gui.press('f5')
            time.sleep(1)

            # wait until page not load after refresh
            WebDriverWait(self.browser, 30).until(ec.visibility_of_element_located(
                (By.XPATH, '/html/body/span/section/main/section/div[2]/div[1]/div/article[1]')))


            # press keys to hide 'Dev tool'
            time.sleep(1)
            screen_gui.hotkey('shift', 'ctrl', 'j')



            # upload new image
            time.sleep(2)
            upload_image = WebDriverWait(self.browser, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]/span')))
            upload_image.click()

            # selection of folder and after image
            # folder = Documents
            time.sleep(2)
            screen_gui.click(x=217, y=218, duration=.2)
            time.sleep(2)


            # select first image inside Instagram photos folder
            screen_gui.click(x=385, y=186, duration=.2)
            time.sleep(2)
            screen_gui.click()

            # click on image
            screen_gui.click(x=406, y=158, duration=.2)
            time.sleep(2)
            screen_gui.click()
            screen_gui.doubleClick(x=406, y=158)


            # scroll down to zoom out image
            time.sleep(2)
            def scroll_down():
                [screen_gui.press('down') for _ in range(50)]
            scroll_down()

            # wait to load page
            WebDriverWait(self.browser, 30).until(ec.visibility_of_element_located((By.CLASS_NAME, 'haDwD')))

            # zoom out image size
            image_zoom_out = WebDriverWait(self.browser, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/div[2]/div[2]/div/div/div/button[1]/span')))
            image_zoom_out.click()

            # delete image
            self.delete_image()



            # click button to next
            next_button = WebDriverWait(self.browser, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/div[1]/header/div/div[2]/button')))
            next_button.click()


            # write caption of image
            image_caption = WebDriverWait(self.browser, 20).until(ec.element_to_be_selected((By.TAG_NAME, 'textarea')))
            image_caption.send_keys(self.quote + '.\n\n\n\n\n\n\nFollow @rohit_dalal_0 for Coding, Programming fun and Information.\n\n\n\n\n#programming #coding #programmer #programminglife# coder #javascript #fullstackdeveloper #codingmemesw #rohit_dalal__ #programmers #programmingisfun #developer #coders #neuralnetworks #html #webdeveloper #programmerslife #css #python #compiler #python3 #backenddeveloper #androiddeveloper #webdevelopment #hacking #cprogramming #programmingmemes #deeplearning #softwaredeveloper')


            # public image
            post_image = WebDriverWait(self.browser, 20).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/div[1]/header/div/div[2]/button')))
            post_image.click()


            self.notification('Image has been posted successfully.')


            #  <<<<<<<<<<<<<========================= finally close self.browser =======================================>>>>>>>>>>>>>>>>>>
            self.browser.close()

        except Exception as e:
            self.notification('Bullshit, There was something wrong!')
            self.browser.close()



if __name__ == "__main__":
    start = Bot()
