#SELENIUM AUTOMATION CODE TO DRAG AND DROP in page using ActionChains
#Importing Webdriver module from Selenium library
from selenium import webdriver
# To import Chrome Service from Selenium and start the ChromeDriver executable
from selenium.webdriver.chrome.service import Service
# To import ChromeDriverManager which allows to manage the correct version of Chrome
from webdriver_manager.chrome import ChromeDriverManager
# To import By class which helps to locate the elements in DOM
from selenium.webdriver.common.by import By
# ActionChains are separate class provided by Selenium for performing complex tasks like hover,click,keypress,drag and drop
from selenium.webdriver.common.action_chains import ActionChains
#To import time library for use of time.sleep()
import time


#Creating WebDriver instance to open Chrome browser
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# get() navigates to jquery page and opens the page in Chrome Browser
driver.get("https://jqueryui.com/droppable/")
# This is used to view the Chrome Browser in maximized window
driver.maximize_window()


# To perform Drag and Drop operation in the page first the drag and drop boxes are present inside a frame
# Using driver.switch_to.frame() switches to the frame and driver.find_element() is used to locate the element inside frame
# By.CSS_SELECTOR, is a faster way to locate the elements. Here used class value so mentioned it using ".demo-frame"
# <iframe src="/resources/demos/droppable/default.html" class="demo-frame"></iframe>
driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR,".demo-frame"))
# To locate the "Drag me to my target", used find_element() and using its id value and stored in variable "source"
# <div id="draggable" class="ui-widget-content ui-draggable ui-draggable-handle" style="position: relative;">
source = driver.find_element(By.ID, "draggable")
# To locate "Drop here" ,used find_element() and using its id value and stored in variable "target"
# <div id="droppable" class="ui-widget-header ui-droppable"></div>
target = driver.find_element(By.ID, "droppable")


# action is an object created for ActionChains class to perform drag and drop in the webpage
# ActionChains perform complex user interactions like hover,click,keypress,click and hold
action = ActionChains(driver)
# action.drag_and_drop(source,target) drags the source box and drops it in the target box which changes into Yellow colour
# perform() is used to create and execute chain of actions. It is mandatory to be used under ActionChains class to perform the chain of actions
action.drag_and_drop(source,target).perform()

# This pauses the execution of script for 4 seconds
time.sleep(4)
#Closes the Chrome Window and ends the WebDriver session
driver.quit()