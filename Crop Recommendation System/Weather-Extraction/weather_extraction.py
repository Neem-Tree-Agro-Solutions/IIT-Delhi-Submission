import os
import time
import argparse
import glob

import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, NoAlertPresentException, TimeoutException, \
    UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains


class DataError(Exception):
    # Constructor or Initializer
    def __init__(self, val):
        self.val = val
    # __str__ is to print() the val

    def __str__(self):
        return self.val + " is not found"


class Extractor():
    def __init__(self, download_path=None):
        self.download_path = download_path
        if self.download_path is None:
            # creating a download path
            self.download_path = os.getcwd().split(os.sep)[:-1:]
            self.download_path = os.path.join(
                os.sep, *self.download_path, 'data', 'climate', '')

        # changing default download directory
        options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        }
        options.add_experimental_option('prefs', prefs)

        # starting chrome webdriver
        try:
            self.chrome_driver = webdriver.Chrome(options=options)
        except WebDriverException:
            self.chrome_driver = webdriver.Chrome(
                ChromeDriverManager().install(), options=options)

    def wait_until_clickable(self, xpath, wait_time=15):
        """
        Wait until element found by xpath is clickable

        Args
        ----
        xpath : str
            path to element
        wait_time : int
            wait time with default of 15 seconds
        """
        try:
            WebDriverWait(self.chrome_driver, wait_time).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        except(NoAlertPresentException, TimeoutException) as py_ex:
            print("Alert not present")
            print(py_ex)
            print(py_ex.args)

    def open(self):
        """
        Open Climate webpage
        """
        self.chrome_driver.get(
            'https://climate.northwestknowledge.net/NWTOOLBOX/formattedDownloads.php')

    def enter_location(self, location, wait_time=10):
        """
        Fill in location in the geolocation field

        Args
        ----
        location : str
            location in the format ~> district, state
        wait_time: int
            default wait time of 10 seconds
        """
        try:
            WebDriverWait(self.chrome_driver, wait_time).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@class='btn btn-large btn-default'][@data-dismiss='modal']["
                               "@data-toggle='modal']"))
            )
            set_location_button = self.chrome_driver.find_element_by_xpath(
                "//button[@class='btn btn-large btn-default'][@data-dismiss='modal'][@data-toggle='modal']")
            ActionChains(self.chrome_driver).move_to_element(
                set_location_button).click(set_location_button).perform()
        except(TimeoutException):
            # open up location search
            self.wait_until_clickable(
                "//button[@class='btn btn-large btn-primary pull-right']", wait_time=wait_time)
            self.chrome_driver.find_element_by_xpath(
                "//button[@class='btn btn-large btn-primary pull-right']").click()

        # fill in geolocation
        self.wait_until_clickable(
            "//input[@id='address']", wait_time=wait_time)
        self.chrome_driver.find_element_by_xpath(
            "//input[@id='address']").clear()
        self.chrome_driver.find_element_by_xpath(
            "//input[@id='address']").send_keys(location)  # district, state : str

        # click on set location
        self.wait_until_clickable("//input[@value='SET LOCATION'][@class='btn btn-large btn-primary pull-right']",
                                  wait_time=wait_time)
        self.chrome_driver.find_element_by_xpath(
            "//input[@value='SET LOCATION'][@class='btn btn-large btn-primary pull-right']").click()

    def set_columns(self, weather_columns):
        """
        change columns on weather page to desired ones

        Arg
        ----
        weather_columns : list
            List of column names
        """
        # select product
        self.chrome_driver.find_element_by_xpath(
            "//select[@id='product']/option[@value='terraclimate']").click()  # 'metdata', 'terraclimate'

        n_cols = len(weather_columns)+1
        assert n_cols <= 8

        # change number of columns
        self.chrome_driver.find_element_by_xpath(
            f"//select[@name='numCol']/option[text()='{n_cols}']").click()

        # Select desired columns
        for i in range(1, n_cols):
            self.chrome_driver.find_elements_by_xpath(
                f"//tr/td/select[@id='varCSV{i}']/option[text()='{weather_columns[i-1]}']")[0].click()

    def download(self):
        """
        Download weather data
        """
        time.sleep(2)
        # download csv
        download_button = self.chrome_driver.find_elements_by_xpath(
            "//button[@class='btn btn-large btn-primary pull-right'][@id='form-button']")[0]
        ActionChains(self.chrome_driver).move_to_element(
            download_button).click(download_button).perform()

        # wait until progress bar disappears
        progress_bar_close = "//button[@class='btn btn-default btn-close']"
        progress_bar = "//div[@class='progress progress-striped active']"

        self.wait_until_clickable(progress_bar_close)
        print("Progress bar appeared")

        WebDriverWait(self.chrome_driver, 300).until(
            EC.invisibility_of_element_located((By.XPATH, progress_bar))
        )
        print("Download has started")

    def change_filename(self, new_fname):
        """
        change default filename from website

        Args
        ----
        new_fname : str
            new filename ~> state_district.txt
        """
        old_f = glob.glob(os.path.join(
            self.download_path, 'terraclimate_*.txt'))  # 'metdata_*.txt', 'terraclimate_*.txt'
        os.rename(old_f[0], os.path.join(self.download_path, new_fname))


if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', metavar='p', type=str, help='download path')
    parser.add_argument('--state', metavar='s', type=str,
                        help='states to select')
    parser.add_argument('--index', metavar='i', type=int,
                        help='index to start searching at')
    parser.add_argument('--end', metavar='e', type=int,
                        help='index to stop searching at')
    args = parser.parse_args()

    # initializing data
    weather_columns = pd.read_csv(
        '../data/weather_cols_terra.csv', header=None)[0].to_list()
    india_district = pd.read_csv(
        "../data/india_district.csv")

    # checking if state is available
    state = vars(args)['state']
    if state is not None:
        state_district_df = india_district[india_district.state == state]
        state_district_df.reset_index(inplace=True, drop=True)
        if state_district_df.empty:
            raise DataError(state)
    else:
        state_district_df = india_district.copy()

    extractor = Extractor()
    extractor.open()

    # iterating through states and districts
    for index, row in state_district_df.loc[vars(args)['index']:vars(args)['end']].iterrows():
        state_district = row['district'] + ', ' + row['state']
        print(index, state_district)
        extractor.enter_location(state_district)
        extractor.set_columns(weather_columns)
        try:
            extractor.download()
        except UnexpectedAlertPresentException:
            # try again with essential columns
            extractor.set_columns(
                weather_columns[0:3])
            try:
                extractor.download()
            except UnexpectedAlertPresentException:
                continue
        extractor.change_filename(f"{row['state']}_{row['district']}.txt")
        time.sleep(10)
