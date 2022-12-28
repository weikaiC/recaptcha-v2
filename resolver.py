from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import urllib
import pydub
from speech_recognition import Recognizer, AudioFile

from time import sleep
from random import randint

import os


def check_multiple(driver):
    """check if answer is correct or not
    """
    driver.switch_to.default_content()
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    driver.switch_to.frame(frames[0])
    try:
        error = driver.find_element(By.CSS_SELECTOR, "#recaptcha-anchor").get_attribute('aria-checked')
        
        if error == 'false':
            
            return False
        
        else:
            print(error)

            return True
    except:
        return True
    
def reaptcha_bypass(driver):
    """try to pass google recaptcha
    """
    
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    wav_path = os.path.join(path, 'audio.wav')
    mp3_path = os.path.join(path, 'audio.mp3')
    check = False

    frames = driver.find_elements(By.TAG_NAME, "iframe")
    driver.switch_to.frame(frames[0])
    sleep(randint(2, 4))
    driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border").click()

    driver.switch_to.default_content()

    frames = driver.find_element(By.XPATH,
        "/html/body/div[2]/div[4]").find_elements(By.TAG_NAME, "iframe")

    sleep(randint(2, 4))

    driver.switch_to.default_content()

    frames = driver.find_elements(By.TAG_NAME, "iframe")

    driver.switch_to.frame(frames[-1])

    driver.find_element(By.ID, "recaptcha-audio-button").click()

    while check == False:
        driver.switch_to.default_content()

        frames = driver.find_elements(By.TAG_NAME, "iframe")

        driver.switch_to.frame(frames[-1])
        sleep(randint(2, 4))

        driver.find_element(By.XPATH, "/html/body/div/div/div[3]/div/button").click()
        src = driver.find_element(By.ID, "audio-source").get_attribute("src")
        # print(src)
        urllib.request.urlretrieve(src, mp3_path)

        sound = pydub.AudioSegment.from_mp3(
            mp3_path).export(wav_path, format="wav")

        recognizer = Recognizer()

        recaptcha_audio = AudioFile(wav_path)

        with recaptcha_audio as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio, language="de-DE")

        # print(text)

        inputfield = driver.find_element(By.ID, "audio-response")
        sleep(randint(2, 4))
        inputfield.send_keys(text.lower())
        sleep(1)
        inputfield.send_keys(Keys.ENTER)
        sleep(1)
        check = check_multiple(driver)

    print('recaptcha_pass')
    
if __name__ == "__main__":
    from Browser import Browser
    
    browser = Browser.get_chrome(headless=False, incognito=False, user_agent=False, from_script=True)
    url = "https://www.google.com/recaptcha/api2/demo" # google recaptcha demo
    browser.get(url)
    reaptcha_bypass(driver=browser)
