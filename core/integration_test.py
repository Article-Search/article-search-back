from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time



def test_login():
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    try:
        # Navigate to the login page
        driver.get("http://localhost:3000/signup")

        # Assume the login form has input fields with the IDs 'username' and 'password'
        first_name_field = driver.find_element(by=By.ID,value="firstName")
        last_name_field = driver.find_element(by=By.ID,value="lastName")
        username_field = driver.find_element(by=By.ID,value="email")
        password_field = driver.find_element(by=By.ID,value="password")

        # Enter some credentials
        first_name_field.send_keys("fares")
        last_name_field.send_keys("Aoufar")
        username_field.send_keys("testuser@test.com")
        password_field.send_keys("testpassword")

        # Submit the form
        submit_button = driver.find_element(by=By.ID, value="submit")
        submit_button.click()

        # Wait for the page to load and check if the user is signed in
        # This will depend on your application, for example you might check if a logout button is present
        # Here we just check if the title of the page has changed
        # assert "Logged In" in driver.title
        #instead check if the user is redirected to http://localhost:3000/search
        WebDriverWait(driver, 10).until(EC.url_to_be("http://localhost:3000/search"))
    finally:
        # Close the browser
        driver.quit()


test_login()
