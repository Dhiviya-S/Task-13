#To import pytest modules and filename should be test_filename.py or \filename_test.py
import pytest
#To import time library for use of time.sleep()
import time
#Importing Webdriver module from Selenium library
from selenium import webdriver
# ActionChains are separate class provided by Selenium for performing complex tasks like hover,click,keypress,drag and drop
from selenium.webdriver.common.action_chains import ActionChains
# To import By class which helps to locate the elements in DOM
from selenium.webdriver.common.by import By
# To import specific Exceptions in selenium
# NoSuchElementException element cannot be found. NoSuchFrameException the frame doesn't exist in the page
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
# MoveTargetOutOfBoundsException happens in drag and drop or click and hold, when the target is not within visible viewport
# JavascriptException which defines execution of invalid javascript
from selenium.common import MoveTargetOutOfBoundsException, JavascriptException


# Fixtures are functions in pytest used to prepare environment for test execution.Scope by default it is "function".
@pytest.fixture()
# driver() function shows the opening of Chrome in headless browser and navigating to jqueryui.com page and performing tests and ends the webdriver session
# options.add_argument('--headless') Headless browsing where the Chrome runs in background without opening a visible window
def driver():
    options=webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://jqueryui.com/droppable/")
    # yield is used for setup and teardown logic. This performs all the tests and gets back to yield again
    yield driver
    #Closes the Chrome Window and ends the WebDriver session
    driver.quit()


# test_positive_action(driver) performs positive test case like drag the source and drops the target box correctly
def test_positive_action(driver):
    # To perform Drag and Drop operation in the page first the drag and drop boxes are present inside a frame
    # Using driver.switch_to.frame() switches to the frame and driver.find_element() is used to locate the element inside frame
    # By.CSS_SELECTOR, is a faster way to locate the elements. Here used class value so mentioned it using ".demo-frame"
    # <iframe src="/resources/demos/droppable/default.html" class="demo-frame"></iframe>
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR,".demo-frame"))
    # To locate the "Drag me to my target", used find_element() and using its id value and stored in variable "source"
    # <div id="draggable" class="ui-widget-content ui-draggable ui-draggable-handle" st
    source = driver.find_element(By.ID, "draggable")
    # To locate "Drop here" ,used find_element() and using its id value and stored in variable "target"
    # <div id="droppable" class="ui-widget-header ui-droppable"></div>
    target = driver.find_element(By.ID, "droppable")
    # action is an object created for ActionChains class to perform drag and drop in the webpage
    action = ActionChains(driver)
    # action.drag_and_drop(source,target) drags the source box and drops it in the target box which changes into Yellow colour
    # perform() is used to create and execute chain of actions. It is mandatory to be used under ActionChains class to perform the chain of actions
    action.drag_and_drop(source,target).perform()
    time.sleep(5)


# test_negative_action() performs negative test case to raise error "NoSuchFrameException".
# This test "passes" since it got the raised exception. The test fails only when the exception raised is not present.
def test_negative_action(driver):
    # pytest.raises() asserts that a specific exception is raised during the execution of a block of code.
    # NoSuchFrameException means the mentioned frame is not found in the given page
    with pytest.raises(NoSuchFrameException):
        # this frame doesn't exist in the webpage so it raises exception
        driver.switch_to.frame("non-existing")
        source = driver.find_element(By.ID, "drag")
        target = driver.find_element(By.ID, "droppable")
        action = ActionChains(driver)
        action.drag_and_drop(source, target).perform()


# test_negative_not_raise() performs negative test case where the code runs properly without raising error
# This test fails because the exception is not raised
def test_negative_not_raise(driver):
    # pytest.raises() asserts that a specific exception is raised during the execution of a block of code.
    # NoSuchFrameException means the mentioned frame is not found in the given page
    with pytest.raises(NoSuchFrameException):
        # this frame exist in the webpage so it does not raise any exception
        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, ".demo-frame"))
        source = driver.find_element(By.ID, "draggable")
        target = driver.find_element(By.ID, "droppable")
        action = ActionChains(driver)
        action.drag_and_drop(source, target).perform()


# test_negative_action_chain() performs negative test case using try and except block.
# Here the find_element() is used to find the elements which is not present in the webpage
# This test "passes" since there are different except blocks to execute the code. Usually negative test cases fail but here except block handles all the errors.
def test_negative_action_chain(driver):
    # A try block in Python is used to handle exceptions gracefully during the execution of code that may potentially cause errors.
    # Code that might raise an exception. Here all the element values are changed to raise error
    try:
        # find_element() values are changed to value which is not in webpage to raise an error
        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, ".emo"))
        source = driver.find_element(By.ID, "drag")
        target = driver.find_element(By.ID, "drop")
        action = ActionChains(driver)
        action.drag_and_drop(source, target).perform()
    #except block is used to handle errors.Code that runs if an exception occurs
    #NoSuchElementException-Selenium cannot find an element on the page using the locator provided.
    except NoSuchElementException:
         print("No such element found!")
    #NoSuchFrameException-Selenium tries to switch to a frame that does not exist using driver.switch_to.frame()
    except NoSuchFrameException:
         print("No such frame found!")
    #Catches any kind of exception from the Exception class and assigns the exception to variable e
    except Exception as e:
        print(f"exception:{e}")
    # else gets executed when there is no error in try block. When no except block gets executed else will run.
    else:
        print("Drag and drop executed successfully")


# test_negative_script() performs negative test case using try and except block.
# Here the invalid javascript statement is added in the code.
# This test "passes" since there are different except blocks to execute the code.
def test_negative_script(driver):
   try:
        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, ".demo-frame"))
        source = driver.find_element(By.CSS_SELECTOR, "div#draggable")
        target = driver.find_element(By.CSS_SELECTOR, "div#droppable")
        # target is considered as arguments[0] that is the first element, where top view port is done using scrollIntoView()
        # but False makes it align to bottom viewport
        driver.execute_script("arguments[0].scrollIntoView(False);",target)
        action = ActionChains(driver)
        # click_and_hold() press and holds the source and move_to_element() moves the mouse to the target element while still holding the mouse button down.
        # release() releases the mouse button so that target element get placed in target
        # perform() is used to perform chain of actions
        action.click_and_hold(source).move_to_element(target).release().perform()
   # MoveTargetOutOfBoundsException-Selenium attempts to perform a mouse movement or drag operation to an element that is out of bounds
   except MoveTargetOutOfBoundsException:
       # pytest.fail()-makes the test intentionally fail
       pytest.fail("Target is out of visible port")
   # JavascriptException- Selenium raises an error when executing invalid JavaScript through execute_script() method
   except JavascriptException:
        print("Invalid javascript")
   #  finally block always runs even if the error is present or not present in the code
   finally:
       print("Done execution")


#To generate HTML Report of Pytest cases:pytest -v -s test_jquery.py --html=report.html
#report.html(to be opened in Browser) is attached