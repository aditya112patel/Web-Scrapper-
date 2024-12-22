from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json


def scroll():          #This function is to scroll the list of bestseller in particular category to load all items
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, 0.85*document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break 
        last_height = new_height

driver = webdriver.Chrome("chromedriver-win32/chromedriver.exe")  #Path to chrome driver
login_link="https://www.amazon.in/ap/signin?openid.return_to=https%3A%2F%2Fwww.amazon.in&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&%26ref_%3D=ab_reg_consignin&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
categories=[
    "Baby Products",
    "Bags, Wallets and Luggage",
    "Beauty",
    "Books",
    "Car & Motorbike",
    "Clothing & Accessories",
    "Computers & Accessories",
    "Electronics",
    "Garden & Outdoors",
    "Gift Cards"
]
username = "**********"   #Your amazon username
password = "**********"   #Your password 
prod_list=[]
filename="data.json"

try:
    driver.get(login_link)
    try:  #For logging in
        email_in =driver.find_element("id", "ap_email")
        email_in.send_keys(username)
        continue_button=driver.find_element("id", "continue")
        continue_button.click()
        password_in=driver.find_element("id", "ap_password")
        password_in.send_keys(password)
        signin=driver.find_element("id", "signInSubmit")
        signin.click()
        bestseller=driver.find_element(By.LINK_TEXT,"Best Sellers")
        bestseller.click()
    except NoSuchElementException:
        print("Login Error! Try Again")

    try:  #For extracting product info
        for cat in categories:
            link=driver.find_element(By.LINK_TEXT,cat)
            link.click()
            rank=1
            for i in range(2):
                scroll()
                elements = driver.find_elements(By.CLASS_NAME, "_cDEzb_p13n-sc-css-line-clamp-3_g3dy1")
                
                for name in elements:
                    x=dict()
                    x["name"]=name.text
                    x["rank"]=rank
                    x["category"]=cat
                    name.click()
                    
                    try:
                        x["price"]=driver.find_element(By.CLASS_NAME,"a-price-whole").text
                        discount=driver.find_element(By.CSS_SELECTOR,".savingsPercentage").text
                        x["discount"]=abs(int(discount.strip('%')))
                        x["Sold by"]=driver.find_elements(By.CSS_SELECTOR,'[tabular-attribute-name="Sold by"]')[-1].text
                        x["rating"]=driver.find_element(By.CLASS_NAME,"mvt-cm-cr-review-stars-small-popover").text
                        x["past month"]=driver.find_element("id","social-proofing-faceout-title-tk_bought").text
                        x["description"]=driver.find_element(By.CSS_SELECTOR,".a-unordered-list.a-vertical.a-spacing-mini").text
                        img=driver.find_element(By.CSS_SELECTOR,".a-dynamic-image.a-stretch-vertical")
                        x["image"]=img.get_attribute("src")
                    except NoSuchElementException:
                        x["rating"]="NAN"
                        x["price"]="NAN"
                        x["discount"]="NAN"
                        x["Sold by"]="NAN"
                        x["past month"]="NAN"
                        x["description"]="NAN"
                        x["image"]="NAN"
                        
                    if x['discount']>=50 or x["discount"]=="NAN":  # Append only if discount >=50 or not available
                        prod_list.append(x)
                    back_button=driver.find_element("id","breadcrumb-back-link")
                    back_button.click()
                    rank=rank+1
                    
                if i==0:
                    next_page=driver.find_element(By.LINK_TEXT,"Next page")   
                    next_page.click()
            back_button=driver.find_element(By.LINK_TEXT,"Any Department")
            back_button.click()

        with open(filename, "w") as json_file:
            json.dump(prod_list, json_file, indent=4)
    except NoSuchElementException:
        print("Element Not found!")
    except TimeoutError:
        print("Driver Timed out")
except NoSuchElementException:
    print("Element Not found!")
except TimeoutError:
    print("Driver Timed out")
finally:
    driver.quit()

