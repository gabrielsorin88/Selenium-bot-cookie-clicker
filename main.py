from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


game_on = True
chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", value=True)

url = "https://orteil.dashnet.org/experiments/cookie/"

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)



coockie = driver.find_element(By.ID, "cookie")

store_items = driver.find_elements(By.CSS_SELECTOR, value="#store div")
ids_item = [item.get_attribute("id") for item in store_items]

check_time = 5
timeout = time.time() + check_time
five_min  = time.time() + 60*5


while game_on:
    coockie.click()

    #stop after 5 min
    if five_min < time.time():
        game_on = False

    #every 5 seconds
    if timeout < time.time():
        #get all elements in store
        all_prices = driver.find_elements(By.CSS_SELECTOR, value="#store b")
        item_prices_int = []

        #get every price to the item_prices_int list as an int
        for price in all_prices:
            price_text  = price.text
            if price_text != "":
                item_prices_int.append(int(price_text.split("-")[1].strip().replace(",", "")))

        #dict of store prices and items
        items_dict = {}
        for ind in range(len(item_prices_int)):
            items_dict[item_prices_int[ind]]= ids_item[ind]

        #get the current cookie/money count as an int
        current_money_str= driver.find_element(By.ID, value="money").text
        if "," in current_money_str :
            current_money_str = current_money_str.replace(",", "")
        current_money = int(current_money_str)

        #look for the affordable store updates
        affordable_updates = {}
        for cost, id in items_dict.items():
            if cost < current_money:
                affordable_updates[cost] = id

        #buy the most expensive update from the affordable_updates dict
        most_expensive_item_key= max(affordable_updates)
        most_expensive_item_id =  affordable_updates[most_expensive_item_key]

        driver.find_element(By.ID, value=most_expensive_item_id).click()

        #adding 10 more seconds until the next check
        check_time+=10
        timeout = time.time() + check_time
