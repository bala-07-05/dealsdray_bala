import time

from pywinauto import Application
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

# Initialize the WebDriver (make sure to replace with the path to your WebDriver executable)
driver = webdriver.Chrome(executable_path="C://Users//balaj//Downloads//chromedriver-win64//chromedriver.exe")
driver.maximize_window()
driver.implicitly_wait(10)

# Open the webpage
driver.get('https://demo.dealsdray.com/')

# Locate the username field and enter the username
username_field = driver.find_element(By.NAME, 'username')  # Adjust selector if needed
username_field.send_keys('prexo.mis@dealsdray.com')

# Locate the password field and enter the password
password_field = driver.find_element(By.NAME, 'password')  # Adjust selector if needed
password_field.send_keys('prexo.mis@dealsdray.com')

# Locate the login button and click it
login_button = driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div/div[2]/div/form/div[3]/div/button')  # Adjust selector if needed
login_button.click()

order_click = driver.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root.has-submenu.compactNavItem.css-46up3a")
order_click.click()
time.sleep(3)
elements = driver.find_elements(By.CSS_SELECTOR, '.sidenavHoverShow.MuiBox-root.css-i9zxpg')
elements[-2].click()
time.sleep(3)

bulk_ord = driver.find_element(By.XPATH, "(//button[normalize-space()='Add Bulk Orders'])[1]")
bulk_ord.click()
time.sleep(5)

# Find the element using the corrected XPath
'''
pyautogui = driver.find_element(By.XPATH, "//*[@id='root']/div/div/div[2]/div/div/div[2]/div[3]/div/div")
pyautogui.click()
pyautogui.write('C:/Users/balaj/Downloads/demo-data.xlsx')
time.sleep(2)
'''
file_input = driver.find_element(By.XPATH,
                                 "//*[@id='root']/div/div/div[2]/div/div/div[2]/div[3]/div/div")  # or By.NAME, By.XPATH, etc.
file_input.click()
time.sleep(2)
# Set the file path
file_path = ('C:\\Users\\balaj\\OneDrive\\Documents\\demo-data.xlsx')

app = Application().connect(title_re="Open")  # "Open" is the title of the dialog
dialog = app.Open
dialog.Edit.type_keys(file_path)
dialog.Open.click()
time.sleep(2)

import_file = driver.find_element(By.XPATH, "//*[@id='root']/div/div/div[2]/div/div/div[2]/div[3]/button")
import_file.click()
time.sleep(2)

validate_data=driver.find_element(By.CSS_SELECTOR,"div[class='MuiBox-root css-1xi4464'] button[type='button']")
validate_data.click()
time.sleep(5)
alert = driver.switch_to.alert
alert.accept()

submit=driver.find_element(By.XPATH,"//*[@id='root']/div/div/div[2]/div/div/div[2]/div[3]/button")
submit.click()
time.sleep(5)
alert = driver.switch_to.alert
alert.accept()
time.sleep(3)