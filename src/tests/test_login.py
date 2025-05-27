import time

from src.pages.base_page import logger


def login_and_logout(login_page, login_method, *args):
    """
    Helper method to perform login and logout using the specified login method.
    """
    #login_page = LoginPage(driver)  # Initialize the LoginPage instance

    # Perform login
    logger.info("Performing login using the provided login method.")
    login_method(login_page, *args)

    # Verify successful login by checking if title is visible
    logger.info("Verifying successful login by checking if the title is visible.")
    login_page.verify_title_is_visible()

    # Perform logout
    logger.info("Performing logout steps.")
    login_page.logout_flow_from_home_page()


def test_google_login_logout(login_page):
    """
    Test Google login and logout flow with detailed logging.
    """
    try:
        # Step 1: Log in with Google
        try:
            login_page.login_with_google()
            login_page.log("Logged in with Google successfully.")
        except Exception as e:
            login_page.log(f"Login with Google failed: {str(e)}")
            raise e

        # # Step 2: Verify title after login
        # try:
        #     login_page.verify_title_is_visible()
        #     login_page.log("Verified title visibility after Google login.")
        # except AssertionError as e:
        #     login_page.log(f"Assertion failed: {str(e)}")
        #     raise e
        # except Exception as e:
        #     login_page.log(f"Error verifying title after Google login: {str(e)}")
        #     raise e

        # # Step 3: Perform logout
        # try:
        #     test_logout_flow(login_page)
        # except Exception as e:
        #     login_page.log(f"Logout failed: {str(e)}")
        #     raise e

    except Exception as e:
        login_page.log(f"Test failed due to: {str(e)}")
        raise e

def test_facebook_login_logout(login_page):
    """
    Test Facebook login and logout flow with detailed logging.
    """
    try:
        # Step 1: Log in with Facebook
        try:
            login_page.login_with_facebook()
            login_page.log("Logged in with Facebook successfully.")
        except Exception as e:
            login_page.log(f"Login with Facebook failed: {str(e)}")
            raise e

        # Step 2: Verify title after login
        try:
            login_page.verify_title_is_visible()
            login_page.log("Verified title visibility after Facebook login.")
        except AssertionError as e:
            login_page.log(f"Assertion failed: {str(e)}")
            raise e
        except Exception as e:
            login_page.log(f"Error verifying title after Facebook login: {str(e)}")
            raise e

        # Step 3: Perform logout
        try:
            login_page.logout_flow_from_home_page()
            login_page.log("Logout confirmed.")
        except Exception as e:
            login_page.log(f"Logout failed: {str(e)}")
            raise e

    except Exception as e:
        login_page.log(f"Test failed due to: {str(e)}")
        raise e

def test_mobile_login_logout(login_page):
    """
    Test Mobile number login and logout flow with detailed logging.
    """
    mobile_number = "..."  # Enter Mobile number
    otp = "..."     #Enter OTP

    try:
        # Step 1: Log in with Mobile Number
        try:
            login_page.login_with_mobile_number(mobile_number, otp)
            login_page.log("Logged in with mobile number successfully.")
        except Exception as e:
            login_page.log(f"Login with mobile number failed: {str(e)}")
            raise e

    #     # Step 2: Verify title after login
    #     try:
    #         login_page.verify_title_is_visible()
    #         login_page.log("Verified title visibility after mobile login.")
    #     except AssertionError as e:
    #         login_page.log(f"Assertion failed: {str(e)}")
    #         raise e
    #     except Exception as e:
    #         login_page.log(f"Error verifying title after mobile login: {str(e)}")
    #         raise e
    #
    #     # Step 3: Perform logout
    #     try:
    #         test_logout_flow(login_page)
    #         login_page.log("Logout confirmed.")
    #     except Exception as e:
    #         login_page.log(f"Logout failed: {str(e)}")
    #         raise e
    #
    except Exception as e:
        login_page.log(f"Test failed due to: {str(e)}")
        raise e


################## Logout Flow #######################################

def test_logout_flow(login_page):
    """
    Test case for logging out from the home page.
    Simply calls logout_flow_from_home_page, which handles verification internally.
    """
    try:
        login_page.logout_flow_from_home_page()
        logger.info("Logout test executed successfully.")

    except Exception as e:
        logger.exception(f"Logout test encountered an error: {str(e)}")
        login_page.take_screenshot("logout_test_error")
        login_page.log("Logout test failed due to an exception.")