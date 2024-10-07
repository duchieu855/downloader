import os
from time import sleep
from download_file_method import download_file_method

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

try:
    URL = "file:///Users/hieuduc/Desktop/automate_download/ex.html"
    # Khởi động trình duyệt
    browser_instance = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Điều hướng đến trang download dữ liệu
    browser_instance.get(URL)

    # Lấy URL hiện tại của trang
    current_url = browser_instance.current_url
    print("Current URL:", current_url)

    if (current_url != URL):
        # Loading lại trang download dữ liệu
        browser_instance.get(URL)

    # Đợi cho tài liệu tải xong
    WebDriverWait(browser_instance, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )

    # Lấy tất cả các thẻ <input> button bằng XPath
    elements = browser_instance.find_elements(By.XPATH,
                                              "/ html / body / table / tbody / tr / td / fieldset / center / table / tbody/tr[not(.//font[(contains(text(), 'đã tải'))])]//input")
    # / html / body / table / tbody / tr / td / fieldset / center / table / tbody / tr / td / font / b / font
    # In ra danh sách các liên kết
    for element in elements:
        print(element.get_attribute('value'))

        # Click down on
        element.click()

        # Đợi đến khi hộp thoại xuất hiện và chấp nhận confirm
        try:
            WebDriverWait(browser_instance, 10).until(EC.alert_is_present())
            alert = browser_instance.switch_to.alert
            sleep(2)
            alert.accept()
            print("Alert accepted")
        except TimeoutException:
            print("No alert appeared.")
        sleep(2)

    # Tải lại tab hiện tại
    browser_instance.refresh()

    # Lấy tất cả các thẻ b chứa tên file đã tải bằng XPath
    downloaded_elements = browser_instance.find_elements(By.XPATH,
                                                         "/ html / body / table / tbody / tr / td / fieldset / center / table / tbody/tr[.//font[(contains(text(), 'đã tải'))]]//td[2]//b")
    # /html/body/table/tbody/tr/td/fieldset/center/table/tbody/tr[2]/td[3]/font
    # /html/body/table/tbody/tr/td/fieldset/center/table/tbody/tr[4]/td[2]/font/b/text()

    file_name_downloaded = [e.text[:-9] for e in downloaded_elements]
    for e in file_name_downloaded:
        print(e)

    # Đường dẫn đến thư mục Downloads
    DOWNLOAD_PATH = os.path.expanduser("/Users/hieuduc/Downloads")

    # Kiểm tra thư mục tồn tại và lấy danh sách file trong thư mục Downloads
    if os.path.exists(DOWNLOAD_PATH):
        files = os.listdir(DOWNLOAD_PATH)
        print("Files in Downloads:")
        for file in files:
            print(file)

        # List files downloading error
        list_files_name_error = [file_name_web for file_name_web in file_name_downloaded if file_name_web not in files]

        # In ra ds files error
        print("files error in downloads: ")
        for file in list_files_name_error:
            print(file)

            # "/ html / body / table / tbody / tr / td / fieldset / center / table / tbody/tr[not(.//font[(contains(text(), 'đã tải'))])]//input"
            xpath_element = f"/html/body/table/tbody/tr/td/fieldset/center/table/tbody/tr[(.//b[(contains(text(), '{file}'))])]//input"

            print(xpath_element)
            # Lấy thẻ input của file download error
            re_download_element = browser_instance.find_element(By.XPATH, xpath_element)


            # In tên thẻ input
            print(re_download_element.get_attribute('value'))

            # download_file_method(re_download_element, browser_instance)

            # Click down on
            re_download_element.click()

            # Đợi đến khi hộp thoại xuất hiện và chấp nhận confirm
            try:
                WebDriverWait(browser_instance, 10).until(EC.alert_is_present())
                alert = browser_instance.switch_to.alert
                sleep(2)
                alert.accept()
                print("Alert accepted")
            except TimeoutException:
                print("No alert appeared.")
            sleep(2)




    # Mở tab mới bằng cách thực thi JavaScript
    browser_instance.execute_script("window.open('', '_blank');")

    # Lấy danh sách tất cả các tab (cửa sổ)
    tabs = browser_instance.window_handles

    # Chuyển đến tab thứ hai (tab Google)
    browser_instance.switch_to.window(tabs[1])

    browser_instance.get("chrome://downloads/")

    sleep(5)

except TimeoutException:
    print("Lỗi: Đợi quá thời gian cho tài liệu tải xong.")
except WebDriverException as e:
    print(f"Lỗi WebDriver: {e}")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")
finally:
    # Đảm bảo trình duyệt được đóng lại dù có lỗi hay không
    browser_instance.quit()
