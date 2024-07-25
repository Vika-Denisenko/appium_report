import os
import time

from typing import Generator
from appium import webdriver as appium_webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

capabilities = dict(
    platformName="Android",
    platformVersion="13",
    automationName="UiAutomator2",
    deviceName="pixel_6a",
    appPackage="com.android.chrome",
    appActivity="com.google.android.apps.chrome.Main",
    # browserName="Chrome", If you need open/close browser
    noReset=True,
    fullReset=False,
    autoGrantPermissions=True,
)


def get_appium_android_studio_chrome_driver() -> AppiumWebDriver:
    appium_driver = appium_webdriver.Remote(
        command_executor="http://127.0.0.1:4723",
        options=UiAutomator2Options().load_capabilities(capabilities),
    )
    time.sleep(5)
    context = appium_driver.contexts[-1]
    appium_driver.switch_to.context(context)
    return appium_driver


def get_chrome_driver() -> WebDriver:
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    chrome_driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    return chrome_driver


@pytest.fixture(scope="module")
def driver() -> Generator[AppiumWebDriver | WebDriver, None, None]:
    drv = get_appium_android_studio_chrome_driver()
    yield drv
    drv.quit()


local_html_file_path = os.path.abspath("index.html")
# file_url = "https://Vika-Denisenko.github.io/appium_report/index.html"
file_url = "http://localhost:63342/appium_report/index.html?_ijt=1kr49n19k54rb1cj30psrn63rv&_ij_reload=RELOAD_ON_SAVE"


def test(driver: AppiumWebDriver | WebDriver) -> None:
    driver.get(file_url)
    input_field = driver.find_element(By.CSS_SELECTOR, "input")

    input_field.click()
    input_field.send_keys("Test+1234!")
    # time.sleep(5)
    submit_button = driver.find_element(By.CSS_SELECTOR, "button")
    submit_button.click()
    message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#message"))
    )
    assert message.text == "Hello, Appium!"
