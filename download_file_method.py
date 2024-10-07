def download_file_method(re_download_element, browser_instance):
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