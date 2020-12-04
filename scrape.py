from selenium.webdriver import Chrome
from bs4 import BeautifulSoup

import time
import pandas as pd

with Chrome("chromedriver.exe") as driver:
	driver.get("https://www.courts.ca.gov/cms/slapp.htm")

	counties = driver.find_element_by_name("slapp")
	counties = [county.get_attribute("value") for county in counties.find_elements_by_tag_name("option") if county.get_attribute("value") != "X"]

	county_cases = {}

	for county in counties:
		driver.find_element_by_xpath("//select[@name='slapp']/option[text()='{}']".format(county)).click()
		driver.find_element_by_name("Submit").submit()

		table_len = len(driver.find_elements_by_xpath(".//table/tbody/tr"))

		cases = []
		for i in range(4, table_len, 16):
			case_num = driver.find_elements_by_xpath(".//table/tbody/tr[{}]/td[2]".format(i))[0].text
			cases.append(case_num)
		
		county_cases[county] = cases

		data = pd.DataFrame(cases, columns=[county])
		data.to_csv("data/{}.csv".format(county))