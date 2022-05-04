import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

browser = webdriver.Chrome("chromedriver", options=chrome_options)

browser.get("http://localhost:5000/")

assert browser.title == 'ArtTown'
