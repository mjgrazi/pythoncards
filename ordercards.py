from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pygsheets
import pandas as pd
import pandas
import time

def buyFunction():
    gc = pygsheets.authorize(service_file='Card Automation-6eafa9ab3972.json')
    sh = gc.open('Recyclers')
    wks = sh[0]
    row = wks.get_row(2)
    completed_sheet = sh[1]
    info_table = sh[2]
    info = info_table.get_row(1)

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    options.add_argument("--user-data-dir=/Users/graz/Library/Application Support/Google/Chrome/Default") # change to profile path
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    driver.get("https://givingassistant.org/out/store/giftcardmall.com/direct")

    time.sleep(8)

    driver.get("https://www.giftcardmall.com/visa-gift-cards/slick-silver-visa-gift-card")

    driver.find_element_by_id("ddpGcCustomPrice").send_keys("494")
    qtyField = driver.find_element_by_id("ddpGcQty")
    # driver.execute_script("document.getElementById('ddpGcQty').value='10'")
    driver.find_element_by_id("ddpGcSenderName").send_keys(info[0] + " " + info[1])
    driver.find_element_by_id("ddpGcRecipientName").send_keys(info[0] + " " + info[1])
    driver.find_element_by_xpath("//select[@id='ddpGcOccasions']/option[text()=' ANNIVERSARY ']").click()
    driver.find_element_by_class_name('ddp-gc-buy-wrap').click()
    driver.find_element_by_class_name("greeting-card-img-wrap").click()
    driver.find_element_by_css_selector('.btn.btn-big').click()
    driver.find_element_by_css_selector('.order-review-action-btn.order-review-action-add.orderReviewAdd').click()

    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, '.shipping-methods-select.shippingMethod_js.shippingMethod_23325_23379'))
        WebDriverWait(driver,4).until(element_present)
    except TimeoutException:
        print("Timeout occurred")

    select_ship = Select(driver.find_element_by_css_selector('.shipping-methods-select.shippingMethod_js.shippingMethod_23325_23379'))
    select_ship.select_by_index(0)
    time.sleep(1)
    driver.find_element_by_css_selector(".gbButton.cart-checkout-btn.cart-checkout-btn_bottom.cartCheckoutBtn_js").click()
    time.sleep(2)
    driver.find_element_by_id("cardholderFirstName").send_keys(info[0])
    driver.find_element_by_id("cardholderLastName").send_keys(info[1])
    driver.find_element_by_id("phoneNumber").send_keys(info[6])
    driver.find_element_by_id("address").send_keys(info[2])
    driver.find_element_by_id("city").send_keys(info[3])
    driver.find_element_by_id("cardNumber").send_keys(row[0])
    driver.find_element_by_id("cardCsc").send_keys(row[1])
    driver.find_element_by_id("addressZipBillingForm").send_keys(info[5])
    Select(driver.find_element_by_id("statesListBillingForm")).select_by_value(info[4])
    Select(driver.find_element_by_id("cardExpirationMonth")).select_by_value(row[2])
    Select(driver.find_element_by_id("cardExpirationYear")).select_by_value("20" + row[3])
    driver.find_element_by_id("saveForLater").click()

    time.sleep(3)
    driver.find_element_by_xpath("//*[@href='http://www.giftcardmall.com/mygift']").send_keys(Keys.PAGE_DOWN)
    # driver.find_element_by_css_selector(".cart-agreement-content.agreementContent.buyFlowV2completeOrderBox").send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    element = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart-agreement-accept-field.agreementAcceptedCheckbox")))
    element.click()

    time.sleep(2)
    driver.find_element_by_css_selector(".checkout-type-link.checkout-type-link_guest.guestCheckoutTabLink_js").click()
    last4 = row[0][-4:]
    driver.find_element_by_css_selector(".guest-form-field.guest-email-field.guestEmail_js").send_keys(info[7] + "+" + last4 + "@gmail.com")

    driver.find_element_by_id("ccCompliteButton").click()

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'buy-confirm-purchase-title')))
        ordernumber = driver.find_element_by_class_name("buy-confirm-purchase-title").text
        ordernumber = ''.join(filter(lambda x: x.isdigit(), ordernumber))
        row[4] = ordernumber
        cardvalue = driver.find_element_by_class_name("confirm-total-box-value").text
        row[5] = cardvalue
        ordervalue = driver.find_element_by_css_selector(".confirm-total-box-value.confirm-total-amount-val").text
        row[6] = ordervalue

        completed_sheet.insert_rows(row = 1, values = row)
        wks.delete_rows(2)
        driver.close()
        buyFunction()
    except TimeoutException:
        print("something went wrong")

buyFunction()
