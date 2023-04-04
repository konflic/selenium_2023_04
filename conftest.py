import os.path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--drivers_folder", default="/home/mikhail/Downloads/drivers")
    parser.addoption("--headless", action="store_true")


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser")
    drivers_folder = request.config.getoption("--drivers_folder")
    headless = request.config.getoption("--headless")

    driver = None

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        if headless:
            options.add_argument('--headless=new')
        service = ChromeService(executable_path=os.path.join(drivers_folder, "chromedriver"))
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.headless = headless
        driver = webdriver.Firefox(executable_path=os.path.join(drivers_folder, "geckodriver"), options=options)
    elif browser_name == "safari":
        driver = webdriver.Safari()

    driver.maximize_window()

    yield driver

    driver.quit()
