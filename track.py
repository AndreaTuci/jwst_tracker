import argparse
import datetime
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as firefoxOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import database as d


class TravelData:
    milesAway = ''
    l2 = ''
    percentage = ''
    speed = ''
    tempWarm = ''
    tempCold = ''

    def __init__(self, attr_list):
        self.milesAway = attr_list[0]
        self.l2 = attr_list[1]
        self.percentage = attr_list[2]
        self.speed = attr_list[3]
        self.tempWarm = attr_list[4]
        self.tempCold = attr_list[5]

    def standardize(self):
        for key in self.__dict__:
            self.__dict__[key] = self.__dict__[key].replace(" ", "")
            try:
                self.__dict__[key] = float(self.__dict__[key])
            except Exception:
                self.__dict__[key] = '---'

    def validate(self):
        validate = True
        if self.milesAway == 0:
            print(f'milesAway not valid: {self.milesAway}')
            validate = False
        if self.percentage == 0:
            print(f'percentage not valid: {self.percentage}')
            validate = False
        if self.speed == 0:
            print(f'speed not valid: {self.speed}')
            validate = False
        if self.tempWarm == '---':
            print(f'tempWarm not valid: {self.tempWarm}')
            validate = False
        if self.tempCold == '---':
            print(f'tempCold not valid: {self.tempCold}')
            validate = False
        return validate

    def print_obj(self):
        for key in self.__dict__:
            print(f'{key}: {self.__dict__[key]} [{type(self.__dict__[key])}]')


def find(root, file, first=False):
    found = False
    for directory, sub_directory, f in os.walk(root):
        if file in f:
            found = True
            if first:
                return "{1}".format(file, directory)
            else:
                print("{1}".format(file, directory))
    return found


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrap and save JWST travel data')
    parser.add_argument("-i", "--iterations", help="Number of surveys", default=1)
    parser.add_argument("-g", "--gap", help="Minutes between two surveys", default=2)
    args = parser.parse_args()
    gap = datetime.timedelta(minutes=int(args.gap))
    i = 1
    max_iterations = int(args.iterations)
    database = r"travel_data.db"
    conn = d.create_connection(database)
    d.main(conn)
    geckodriver = os.path.join(find('/', 'geckodriver', True), 'geckodriver')
    url = 'https://www.jwst.nasa.gov/content/webbLaunch/whereIsWebb.html?units=english'
    print(f'{max_iterations} iterations planned. {gap} minutes gap')
    ref_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
    print(f'Starting at {ref_time}')
    while i <= max_iterations:
        current_time = datetime.datetime.now().time()
        time_string = current_time.strftime("%H:%M:%S")
        # print(time_string, ref_time.strftime("%H:%M:%S"))
        if time_string == ref_time.time().strftime("%H:%M:%S"):
            print(f'Iteration {i}/{max_iterations} - \n{ref_time}\nNext survey: {ref_time + gap} minutes')
            ref_time = ref_time + gap
            i += 1
            while True:
                try:
                    service = Service(geckodriver)
                    firefox_options = firefoxOptions()
                    firefox_options.add_argument('--headless')
                    driver = webdriver.Firefox(service=service, options=firefox_options)
                    driver.get(url)

                    while True:
                        data = TravelData([
                            driver.find_element(By.ID, 'milesEarth').text,
                            driver.find_element(By.ID, 'milesToL2').text,
                            driver.find_element(By.ID, 'percentageCompleted').text,
                            driver.find_element(By.ID, 'speedMi').text,
                            driver.find_element(By.ID, 'tempWarmSide2F').text,
                            driver.find_element(By.ID, 'tempCoolSide2F').text,
                        ])
                        data.standardize()
                        if data.validate():
                            break
                        else:
                            print('Invalid data!')

                    driver.quit()
                    data.print_obj()
                    d.update(conn, data)
                    print('Data saved')
                    break

                except Exception as e:
                    print(e)
