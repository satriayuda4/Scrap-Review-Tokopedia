from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def chrome_driver_headless():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        PATH = 'chromedriver.exe'
        driver = webdriver.Chrome(PATH, options = chrome_options)
        return driver
    except:
        print("Please check your chrome driver version")
    
def chrome_driver():
    PATH = 'chromedriver.exe'
    driver = webdriver.Chrome(PATH)
    return driver

def input_link():
    link = input("Copy and Paste the page here: ")
    return link

def open_link(driver, link):
    driver.get(link)
    driver.implicitly_wait(2)

def slowly_scroll(driver,n):
    y = 1000
    for timer in range(0,n):
         driver.execute_script("window.scrollTo(0, "+str(y)+")")
         y += 1000  
         time.sleep(1)

def close_link(driver):
    driver.quit()

def scrap_title():
    path = '//*[@id="pdp_comp-product_content"]/div/h1'
    element = driver.find_element_by_xpath(path)
    title = element.text
    return title

def total_review():
    path = '//*[@id="pdp_comp-review"]/h2[4]'
    element = driver.find_element_by_xpath(path)
    text = str(element.text)
    num = text.split()[-1]
    num = num.replace("(","")
    num = num.replace(")","")
    return num

def total_pages():
    path = '//*[@id="pdp_comp-review"]/div[15]/div/div/button[10]'
    element = driver.find_element_by_xpath(path)
    text = str(element.text)
    return text

def scrap_one_review(path):
    element = driver.find_element_by_xpath(path)
    text = str(element.text)
    return text

def scrap_review(array,n):
    for i in range(n):
        i += 5
        review = scrap_one_review('//*[@id="pdp_comp-review"]/div[' + str(i) + ']/div/div[2]/p/span')
        array.append(review)

def click_next(driver):
    driver.implicitly_wait(5)
    #path = '//*[@id="header-main-wrapper"]/div[5]/nav/div/div[2]/div/div[2]'
    path = '//*[@id="pdp_comp-review"]/div[15]/div/div/button[11]'
    driver.find_element_by_xpath(path).click()
    driver.implicitly_wait(5)
    print('click next')

def click_ulasan(driver):
    path = '//*[@id="header-main-wrapper"]/div[5]/nav/div/div[2]/div/div[2]'
    driver.find_element_by_xpath(path).click()
    driver.implicitly_wait(5)

def main():
    print("Hello World!")

if __name__ == "__main__":
    link = input_link()
    driver = chrome_driver()
    open_link(driver, link)
    slowly_scroll(driver,12)
    time.sleep(6)
    
    #scraping info
    title = scrap_title()
    review_num = int(total_review())
    pages = total_pages()
    
    #display scrap info
    print('Product title: ' + str(title))
    print('Total review ' + str(review_num))
    print('Total pages ' + str(pages))
    time.sleep(5)

    #last page num
    last = int(review_num)%10
    print(last)
    
    #click the review page
    print('click ulasan')
    click_ulasan(driver)
    time.sleep(2)

    #Generate storing array
    reviews = []
    
    #
    for i in range(review_num):
        click_ulasan(driver)
        
        if (i+1) == review_num:
            scrap_review(reviews,total_review%10)
        else:
            scrap_review(reviews,10)
            time.sleep(5)
            click_next(driver)
        if reviews[-1] == '':
            break
            
    
    #driver.quit()
    #print(title)
    df = pd.DataFrame({'Review': reviews})
    title = title.split()
    title = title[0] + ' ' + title[1]
    title += '.csv'
    df.to_csv('Export/'+title,index=False)
    print(reviews)
    time.sleep(3)
    driver.quit()
    #print(pages)
    #print(review_num)