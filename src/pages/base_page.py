import csv
import logging
import os
from selenium.common import TimeoutException, ElementNotInteractableException, NoSuchElementException, \
    WebDriverException
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


import logging
import sys
import coloredlogs


class TouchAction:
    pass


class BasePage:
    def __init__(self, driver, timeout=10):
        """
        Initialize BasePage with the WebDriver and optional timeout.
        :param driver: The WebDriver instance.
        :param timeout: Timeout in seconds (default is 10 seconds).
        """
        self.driver = driver
        self.timeout = timeout

        # Create logger for the BasePage class
        self.logger = logging.getLogger(self.__class__.__name__)
        self.set_up_logger()

    def set_up_logger(self):
        """Set up the logger configuration."""
        # Create the 'data' directory if it doesn't exist
        log_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'data')
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # Set the log file path
        log_file_path = os.path.join(log_directory, 'appium_test_log.log')

        # Set the log level (INFO level for general messages, DEBUG for debugging messages)
        self.logger.setLevel(logging.INFO)

        # Create a log handler that writes logs to the file in the 'data' folder
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)

        # Create a log formatter to structure the log messages
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)

        # Create a console handler to print logs to the console (optional)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, message):
        """Helper method to log messages."""
        self.logger.info(message)

    def log_error(self, message):
        """Helper method to log error messages."""
        self.logger.error(message)

    def log_warning(self, message):
        """Helper method to log warning messages."""
        self.logger.warning(message)

    def log_debug(self, message):
        """Helper method to log debug messages."""
        self.logger.debug(message)

    # def take_screenshot(self, screenshot_name):
    #     """Placeholder method to take a screenshot (if necessary)."""
    #     # You can implement the screenshot functionality here
    #     # For example, save it with the name screenshot_name
    #     self.logger.info(f"Screenshot saved: {screenshot_name}")

    def wait_for_element_to_be_clickable(self, locator):
        """
        Waits for an element to be clickable.
        :param locator: A tuple (locator_type, locator_value)
        :return: The clickable element if found, else raises an exception.
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element {locator} was not clickable within {self.timeout} seconds.")
            raise TimeoutException(f"Element {locator} was not clickable within {self.timeout} seconds.")
        except Exception as e:
            logger.error(f"An error occurred while waiting for element {locator}: {str(e)}")
            raise Exception(f"An error occurred while waiting for element {locator}: {str(e)}")

    def wait_for_element_to_be_visible(self, locator):
        """
        Waits for an element to be visible.
        :param locator: A tuple (locator_type, locator_value)
        :return: The visible element if found, else raises an exception.
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element {locator} was not visible within {self.timeout} seconds.")
            raise TimeoutException(f"Element {locator} was not visible within {self.timeout} seconds.")
        except Exception as e:
            logger.error(f"An error occurred while waiting for element {locator}: {str(e)}")
            raise Exception(f"An error occurred while waiting for element {locator}: {str(e)}")

    def wait_for_element_to_be_present(self, locator):
        """
        Waits for an element to be present in the DOM.
        :param locator: A tuple (locator_type, locator_value)
        :return: The present element if found, else raises an exception.
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element {locator} was not present within {self.timeout} seconds.")
            raise TimeoutException(f"Element {locator} was not present within {self.timeout} seconds.")
        except Exception as e:
            logger.error(f"An error occurred while waiting for element {locator}: {str(e)}")
            raise Exception(f"An error occurred while waiting for element {locator}: {str(e)}")

    def click_element(self, locator):
        """
        Waits for an element to be clickable and clicks it.
        :param locator: A tuple (locator_type, locator_value)
        """
        element = self.wait_for_element_to_be_clickable(locator)
        if element:
            try:
                element.click()
                logger.info(f"Clicked on the element with locator: {locator}")
            except ElementNotInteractableException as e:
                logger.error(f"Element {locator} is not interactable: {e}")
        else:
            logger.error(f"Element {locator} not found or not clickable.")

    def enter_text(self, locator, text):
        """
        Waits for an element to be visible and enters text into it.
        :param locator: A tuple (locator_type, locator_value)
        :param text: Text to enter into the field
        """
        element = self.wait_for_element_to_be_visible(locator)
        if element:
            element.clear()  # Clear the field before entering text
            element.send_keys(text)
            logger.info(f"Entered text into element with locator: {locator}")
        else:
            logger.error(f"Element {locator} not found or not visible.")


    def store_data_in_csv(self, file_name, data, headers=None):
        """
        Store data in a CSV file.
        :param file_name: Name of the CSV file.
        :param data: List of rows (each row is a list or tuple).
        :param headers: Optional headers for the CSV file.
        """
        file_path = os.path.join(os.getcwd(), "data", file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if headers:
                writer.writerow(headers)
            writer.writerows(data)
        logger.info(f"Data saved in CSV file: {file_path}")

    def is_element_present(self, locator):
        """ Check if an element is present in the DOM without waiting too long. """
        try:
            elements = self.driver.find_elements(*locator)  # Use `find_elements`, not `find_element`
            return len(elements) > 0  # True if at least one element is found
        except Exception as e:
            self.logger.error(f"❌ is_element_present error: {str(e)}")
            return False

    def is_element_visible(self, locator):
        """
        Check if an element is visible on the page.
        :param locator: A tuple (locator_type, locator_value)
        :return: True if element is visible, False otherwise.
        """
        element = self.wait_for_element_to_be_visible(locator)
        return element is not None and element.is_displayed()

    def swipe(self, start_x, start_y, end_x, end_y, duration=800):
        """
        Perform a swipe action using Appium TouchAction.
        :param start_x: Starting x-coordinate.
        :param start_y: Starting y-coordinate.
        :param end_x: Ending x-coordinate.
        :param end_y: Ending y-coordinate.
        :param duration: Duration of the swipe in milliseconds.
        """
        try:
            touch_action = TouchAction()
            touch_action.press(x=start_x, y=start_y).wait(ms=duration).move_to(x=end_x, y=end_y).release().perform()
            self.logger.info(f"Swiped from ({start_x},{start_y}) to ({end_x},{end_y}) successfully.")
        except Exception as e:
            self.logger.error(f"Swipe failed: {str(e)}")
            raise

    def scroll(self, direction="down"):
        """
        Perform a scroll action.
        :param direction: Scroll direction ("down", "up", "left", "right").
        """
        size = self.driver.get_window_size()
        start_x, start_y, end_x, end_y = 0, 0, 0, 0
        if direction == "down":
            start_x = size['width'] // 2
            start_y = size['height'] * 3 // 4
            end_x = start_x
            end_y = size['height'] // 4
        elif direction == "up":
            start_x = size['width'] // 2
            start_y = size['height'] // 4
            end_x = start_x
            end_y = size['height'] * 3 // 4
        elif direction == "left":
            start_x = size['width'] * 3 // 4
            start_y = size['height'] // 2
            end_x = size['width'] // 4
            end_y = start_y
        elif direction == "right":
            start_x = size['width'] // 4
            start_y = size['height'] // 2
            end_x = size['width'] * 3 // 4
            end_y = start_y
        else:
            raise ValueError("Invalid direction. Use 'down', 'up', 'left', or 'right'.")
        self.driver.swipe(start_x, start_y, end_x, end_y, 800)

    def long_press_element(self, locator, duration=2000):
        """
        Perform a long press on an element.
        :param locator: A tuple (locator_type, locator_value)
        :param duration: Duration of the long press in milliseconds.
        """
        element = self.driver.find_element(*locator)
        actions = ActionBuilder(self.driver, PointerInput(PointerInput.TOUCH, "touch"))
        actions.pointer_action.move_to(element).pointer_down().pause(duration / 1000).pointer_up()
        actions.perform()

    def tap_element(self, locator, x_offset=0, y_offset=0):
        """
        Tap an element at a specific offset.
        :param locator: A tuple (locator_type, locator_value)
        :param x_offset: Horizontal offset.
        :param y_offset: Vertical offset.
        """
        element = self.driver.find_element(*locator)
        actions = ActionBuilder(self.driver, PointerInput(PointerInput.TOUCH, "touch"))
        actions.pointer_action.move_to(element, x_offset, y_offset).pointer_down().pointer_up()
        actions.perform()

    def send_keys(self, locator, text, clear_field=True, wait_time=None):
        """
        Method to send text into an input field (e.g., chat box, search field).

        :param locator: The locator for the element (tuple).
        :param text: The text to be entered into the field.
        :param clear_field: Whether to clear the field before entering the text. Default is True.
        :param wait_time: Optional time to wait for the element to be clickable (defaults to None).
        """
        try:
            # If no specific wait_time is provided, use the default timeout value from the BasePage
            if wait_time is None:
                wait_time = self.timeout  # Assuming self.timeout is defined globally or in the constructor

            # Wait for the element to be clickable with the given wait_time
            element = self.wait_for_element_to_be_clickable(locator)

            if clear_field:
                element.clear()  # Clear the input field before entering new text

            element.send_keys(text)  # Send the text into the input field

            logger.info(f"Successfully entered text: '{text}' in element {locator}")
        except Exception as e:
            logger.error(f"Failed to send keys '{text}' to element {locator}: {str(e)}")
            raise

    def find_elements(self, locator, wait_time=None):
        """
        Finds multiple elements based on the provided locator.
        :param locator: Locator of the elements to be found (a tuple with locator type and value).
        :param wait_time: Optional parameter to specify a custom wait time for element visibility.
        :return: A list of elements found by the locator.
        """
        try:
            if wait_time is None:
                wait_time = self.timeout  # Use default timeout if no custom wait time is provided

            # Wait for the elements to be visible and return them
            elements = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            logger.error(f"Elements {locator} were not visible within {wait_time} seconds.")
            raise TimeoutException(f"Elements {locator} were not visible within {wait_time} seconds.")
        except NoSuchElementException:
            logger.error(f"No such elements found using locator {locator}.")
            raise NoSuchElementException(f"No such elements found using locator {locator}.")
        except Exception as e:
            logger.error(f"An error occurred while finding elements {locator}: {str(e)}")
            raise Exception(f"An error occurred while finding elements {locator}: {str(e)}")

    def take_screenshot(self, name):
        """
        Takes a screenshot and saves it with the specified name in the src/screenshots directory.
        """
        try:
            # Define the screenshot directory relative to the project root
            screenshot_dir = os.path.join(os.path.dirname(__file__),
                                          '../../src/screenshots')  # Adjust this to your structure

            # Ensure the screenshots directory exists
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            # Construct the full path for the screenshot
            screenshot_path = os.path.join(screenshot_dir, f"{name}.png")

            # Capture the screenshot
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")

    def safe_action(self, action, description=""):
        """
        Executes a given action with error handling, logging, and screenshot support.
        """
        try:
            action()
            logger.info(f"Success: {description}")
        except TimeoutException:
            self.take_screenshot("timeout_error")
            logger.error(f"Timeout during: {description}")
            raise
        except NoSuchElementException:
            self.take_screenshot("no_such_element_error")
            logger.error(f"Element not found during: {description}")
            raise
        except WebDriverException as e:
            self.take_screenshot("webdriver_error")
            logger.error(f"WebDriver error during: {description}. Error: {str(e)}")
            raise
        except Exception as e:
            self.take_screenshot("unexpected_error")
            logger.exception(f"Unexpected error during: {description}. Error: {str(e)}")
            raise

    def get_element_text(self, locator):
        """
        Retrieves the text of an element identified by the given locator.

        :param locator: Tuple (By, value) representing the element's locator.
        :return: Text of the element if found, else None.
        """
        try:
            element = self.wait_for_element_to_be_visible(locator)
            text = element.text
            self.logger.info(f"Retrieved text from element: {text}")
            return text
        except NoSuchElementException:
            self.logger.error(f"Element {locator} not found.")
        except TimeoutException:
            self.logger.error(f"Timeout while waiting for element {locator}.")
        except Exception as e:
            self.logger.error(f"Unexpected error while getting text: {str(e)}")
        return None

    def get_element(self, locator, timeout=10):
        """
        Retrieve an element using the provided locator.
        :param locator: Tuple (By.<METHOD>, "locator_value")
        :param timeout: Maximum wait time in seconds (default=10)
        :return: WebElement if found, else raises exception
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Timeout: Element not found - {locator}")
            raise
        except NoSuchElementException:
            self.logger.error(f"NoSuchElementException: Element not found - {locator}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in get_element: {str(e)}")
            raise

    def find_element(self, locator, timeout=10):
        """
        Find an element with an explicit wait.

        :param locator: Tuple (By.<LOCATOR_TYPE>, "<locator_value>")
        :param timeout: Maximum wait time for element (default: 10 seconds)
        :return: WebElement if found, else raises exception
        """
        try:
            self.logger.info(f"Waiting for element: {locator}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Timeout: Element not found within {timeout} seconds - {locator}")
            raise
        except NoSuchElementException:
            self.logger.error(f"Element not found: {locator}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while finding element {locator}: {str(e)}")
            raise


