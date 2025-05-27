import time
from src.pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from pages.base_page import logger


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        ##############     Locators for login options   ###########################################

        # Google login
        self.verify_login_page = (AppiumBy.ID, "com.showtimeapp:id/googleLoginBtn")
        self.google_login_button = (AppiumBy.ID, "com.showtimeapp:id/googleLoginBtn")
        self.email_click = (AppiumBy.XPATH, "//android.widget.TextView[@resource-id='com.google.android.gms:id/account_name' and @text='automationloco@gmail.com']")

        # Facebook login
        self.facebook_login_button = (AppiumBy.ID, "com.showtimeapp:id/facebookLoginBtn")
        self.fb_email = (AppiumBy.XPATH,"//android.widget.TextView[@text='Mobile number or email address']")
        self.fbemail_text = (AppiumBy.ID,"m_login_email")
        self.fb_password = (AppiumBy.ID,"m_login_password")
        self.fb_loginBtn = (AppiumBy.XPATH,"//android.widget.Button[@text='Log in']")

        # Phone login
        self.phone_login_button = (AppiumBy.ID, "com.showtimeapp:id/phoneLoginBtn")
        self.phone_number_enter = (AppiumBy.ID, "com.showtimeapp:id/phoneNumberET")
        self.get_otp_button = (AppiumBy.ID, "com.showtimeapp:id/getOtpBtn")
        self.otp_fields = [
            (AppiumBy.ID, "com.showtimeapp:id/otp1"),
            (AppiumBy.ID, "com.showtimeapp:id/otp2"),
            (AppiumBy.ID, "com.showtimeapp:id/otp3"),
            (AppiumBy.ID, "com.showtimeapp:id/otp4")
        ]
        self.confirmOTP_button = (AppiumBy.ID, "com.showtimeapp:id/confirmBtn")

        self.countrycode_box = (AppiumBy.ID,"com.showtimeapp:id/countryCodeNew")
        self.countrycode_search = (AppiumBy.ID,"com.showtimeapp:id/etCountrySearch")
        self.countrycode_name = (AppiumBy.ID,"com.showtimeapp:id/tvCountryName")


        # Terms & Condition popup
        self.terms_condition_popup = (AppiumBy.XPATH, "//android.widget.TextView[@text='Update to Terms of Use']")
        self.terms_open_button = (AppiumBy.XPATH, "//android.widget.Button[@text='Terms of Use']")
        self.terms_accept_button = (AppiumBy.XPATH, "//android.widget.Button[@text='I Accept']")

        # Title On Home Page
        self.title = (AppiumBy.ID, "com.showtimeapp:id/titleLogo")

        # Home page buttom
        self.home_button = (AppiumBy.ACCESSIBILITY_ID, "Home")

        ##############     Locators for logout options   ###########################################

        self.avatar = (AppiumBy.ID, "com.showtimeapp:id/drawerUserAvatar")
        self.settings = (
            AppiumBy.XPATH,
            "//android.widget.TextView[@resource-id='com.showtimeapp:id/drawerMenuName' and @text='Settings']")
        self.logout_btn = (AppiumBy.ID, "com.showtimeapp:id/bgSignOut")
        self.confirm_logout = (AppiumBy.ID, "com.showtimeapp:id/positiveBtn")
        self.cancel_logout = (AppiumBy.ID, "com.showtimeapp:id/negativeBtn")

    ####################### METHODS ########################

    def login(self):
        """
        Login method that chooses which login type to proceed with based on the provided input.
        It can either log in via Google, Facebook, or Mobile Number.
        """
        try:
            self.verify_login_page_visible()

            # Google login by default, can be changed to other login types
            self.login_with_google()

        except AssertionError as e:
            self.take_screenshot('login_assertion_error')
            logger.error(f"Login page visibility check failed: {str(e)}")
        except Exception as e:
            self.take_screenshot('login_assertion_error')
            logger.exception(f"An error occurred during login: {str(e)}")

    def verify_login_page_visible(self):
        """
        Verifies if the login page is visible before proceeding with login actions.
        Raises:
            AssertionError: If login page is not visible.
        """
        if not self.wait_for_element_to_be_visible(self.verify_login_page):
            self.take_screenshot('verify_login_page_error')
            raise AssertionError("Login page is NOT visible after logout.")

        logger.info("Login page is visible after logout.")

    def login_with_google(self):
        """
        Automates the Google login process.
        """
        try:

            self.click_element(self.google_login_button)
            self.wait_for_element_to_be_clickable(self.email_click)
            # #time.sleep(5)
            self.click_element(self.email_click)
            self.wait_for_element_to_be_visible(self.title)
            self.verify_title_is_visible()
        except NoSuchElementException as e:
            self.take_screenshot('google_login_element_not_found')
            logger.error(f"Google login element not found: {str(e)}")
        except WebDriverException as e:
            self.take_screenshot('google_login_webdriver_error')
            logger.error(f"WebDriver error during Google login: {str(e)}")
        except AssertionError as e:
            self.take_screenshot('google_login_assertion_error')
            logger.error(f"Title visibility assertion failed: {str(e)}")
        except Exception as e:
            self.take_screenshot('google_login_unexpected_error')
            logger.exception(f"Unexpected error during Google login: {str(e)}")

    def login_with_facebook(self):
        """
        Automates the Facebook login process.
        """
        try:
            self.wait_for_element_to_be_clickable(self.facebook_login_button).click()
            time.sleep(7)

            # # Switch to WebView context
            # contexts = self.driver.contexts
            # self.logger.info(f"Available contexts: {contexts}")
            # for context in contexts:
            #     if "WEBVIEW_chrome" in context:
            #         self.driver.switch_to.context(context)
            #         self.logger.info(f"Switched to context: {context}")
            #         break
            # else:
            #     raise Exception("WEBVIEW context not found.")
            #
            #



            self.click_element(self.fb_email)
            self.wait_for_element_to_be_visible(self.fbemail_text)

            self.send_keys(self.fbemail_text,"...") #FB Email
            time.sleep(2)
            # self.wait_for_element_to_be_visible(self.fb_password)
            # self.send_keys(self.fb_password,"...",clear_field=True,wait_time=2) #fb Password
            # time.sleep(2)
            # self.wait_for_element_to_be_clickable(self.fb_loginBtn).click()
            # time.sleep(5)
            #
            # # Switch back to native context
            # self.driver.switch_to.context("NATIVE_APP")
            # self.logger.info("Switched back to native context after FB login.")
            #
            #
            #
            # self.wait_for_element_to_be_visible(self.title)
            # self.verify_title_is_visible()
        except NoSuchElementException as e:
            self.take_screenshot('facebook_login_element_not_found')
            logger.error(f"Facebook login element not found: {str(e)}")
        except WebDriverException as e:
            self.take_screenshot('facebook_login_webdriver_error')
            logger.error(f"WebDriver error during Facebook login: {str(e)}")
        except AssertionError as e:
            self.take_screenshot('facebook_login_assertion_error')
            logger.error(f"Title visibility assertion failed: {str(e)}")
        except Exception as e:
            self.take_screenshot('facebook_login_unexpected_error')
            logger.exception(f"Unexpected error during Facebook login: {str(e)}")

    def login_with_mobile_number(self, mobile_number, otp):
        """
        Automates the mobile number login process, including OTP input.
        """
        try:
            self.click_element(self.phone_login_button)
            self.wait_for_element_to_be_visible(self.countrycode_box).click()
            self.wait_for_element_to_be_visible(self.countrycode_search)
            self.send_keys(self.countrycode_search,"India")
            try:
                element = self.wait_for_element_to_be_visible(self.countrycode_name)
                country_text = element.text.strip()

                if country_text == "India":
                    self.logger.info("Country name is 'India'. Clicking on the element.")
                    element.click()
                else:
                    self.logger.info(f"Country name is not 'India'. Found: {country_text}")

            except Exception as e:
                self.logger.error(f"Error while checking and clicking country: {str(e)}")
                self.take_screenshot("click_country_if_india_error")
                raise
            self.wait_for_element_to_be_visible(self.phone_number_enter)
            self.enter_text(self.phone_number_enter, mobile_number)
            self.click_element(self.get_otp_button)


            for otp_field in self.otp_fields:
                self.wait_for_element_to_be_visible(otp_field)

            otp_values = list(str(otp))

            for i, otp_value in enumerate(otp_values):
                self.enter_text(self.otp_fields[i], otp_value)

            self.click_element(self.confirmOTP_button)
            time.sleep(2)
            self.wait_for_element_to_be_visible(self.title)
            self.verify_title_is_visible()
            logger.info("Mobile number login successful!")
        except NoSuchElementException as e:
            self.take_screenshot('mobile_login_element_not_found')
            logger.error(f"Mobile login element not found: {str(e)}")
        except WebDriverException as e:
            self.take_screenshot('mobile_login_webdriver_error')
            logger.error(f"WebDriver error during mobile number login: {str(e)}")
        except AssertionError as e:
            self.take_screenshot('mobile_login_assertion_error')
            logger.error(f"Title visibility assertion failed: {str(e)}")
        except Exception as e:
            self.take_screenshot('mobile_login_unexpected_error')
            logger.exception(f"Unexpected error during mobile number login: {str(e)}")

    def verify_title_is_visible(self):
        """
        Verifies if the title is visible after the login process.
        """
        try:
            title_element = self.driver.find_element(*self.title)
            assert title_element.is_displayed(), "Title is not visible on the screen."
            logger.info("Test Passed: Loco Title is visible on Home page. Sign in completed")
        except NoSuchElementException:
            self.take_screenshot('title_not_found')
            logger.error("Title element is not found.")
        except AssertionError as e:
            self.take_screenshot('title_visibility_error')
            logger.error(f"Test Failed: {str(e)}")
        except Exception as e:
            self.take_screenshot('title_unexpected_error')
            logger.exception(f"Unexpected error: {str(e)}")

    def is_user_logged_in(self):
        """
        Checks if the user is already logged in by verifying the presence of a known UI element.
        Returns True if logged in, otherwise False.
        """
        try:
            # Example: Check if the home screen title or avatar icon is visible
            return self.wait_for_element_to_be_visible(self.home_button)
        except Exception:
            return False

    ###########################################Logout Methods#####################3#############
    def click_avatar(self):
        """
        Clicks on the avatar to open the drawer.
        """
        try:
            self.wait_for_element_to_be_clickable(self.avatar).click()
            logger.info("Avatar clicked. Drawer opened.")
        except Exception as e:
            self.take_screenshot('avatar_click_error')
            logger.exception(f"Error clicking on avatar: {str(e)}")

    def click_settings(self):
        """
        Click on the 'Settings' option from the drawer menu.
        """
        try:
            self.wait_for_element_to_be_clickable(self.settings).click()
            logger.info("Settings clicked.")
        except Exception as e:
            self.take_screenshot('settings_click_error')
            logger.exception(f"Error clicking on settings: {str(e)}")

    def click_logout(self):
        """
        Click on the 'Logout' button in the settings page.
        """
        try:
            self.wait_for_element_to_be_clickable(self.logout_btn).click()
            logger.info("Logout clicked.")
        except Exception as e:
            self.take_screenshot('logout_click_error')
            logger.exception(f"Error clicking on logout: {str(e)}")

    def click_confirm_logout(self):
        """
        Confirm the logout action.
        """
        try:
            self.wait_for_element_to_be_clickable(self.confirm_logout).click()
            logger.info("Logout confirmed.")
        except Exception as e:
            self.take_screenshot('confirm_logout_error')
            logger.exception(f"Error confirming logout: {str(e)}")

    def cancel_logout(self):
        """
        Cancel the logout action.
        """
        try:
            self.wait_for_element_to_be_clickable(self.cancel_logout).click()
            logger.info("Logout canceled.")
        except Exception as e:
            self.take_screenshot('cancel_logout_error')
            logger.exception(f"Error canceling logout: {str(e)}")

    def logout_flow_from_home_page(self):
        """
        Performs the complete logout flow from the home page.
        Steps:
            1. Click on the avatar to open the drawer.
            2. Click on 'Settings' in the drawer.
            3. Click on 'Logout' in the settings page.
            4. Confirm the logout action.
            5. Verify that login page is visible.
        """
        try:
            # Step 1: Click on avatar to open the drawer
            self.click_avatar()

            # Step 2: Click on settings in the drawer
            self.click_settings()

            # Step 3: Click on logout button
            self.click_logout()

            # Step 4: Confirm the logout action
            self.click_confirm_logout()

            # Step 5: Verify that login page is visible
            time.sleep(3)
            if self.wait_for_element_to_be_visible(self.verify_login_page):
                logger.info("Logout flow completed successfully, login page is visible.")
            else:
                logger.error("Logout flow failed, login page is NOT visible.")
                self.take_screenshot("logout_verification_failed")

        except Exception as e:
            logger.exception(f"Error during the logout flow: {str(e)}")
            self.take_screenshot('logout_flow_error')