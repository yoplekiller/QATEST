from selenium import webdriver

def test_parallel():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )
    driver.get("https://www.kurly.com/main")
    assert "Example" in driver.title
    driver.quit()