from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import csv

rep = [('<span class="block">',''),('<p>',''),('</span>',' '),('</p>',''),('amp; ','')] 
 #Loading the page 
starbucksUrl = 'https://www.starbucks.com/store-locator?map=39.635307,-101.337891,5z'
driver = webdriver.Chrome() 
driver.get(starbucksUrl)
sleep(5)

cities = ['Guwahati','Vijayawada','Raipur','Bhubaneswar','Delhi','Mumbai','Pune','Nashik','Nagpur','Kolhapur','Panaji','Banglore','Chennai','Hyderabad','Kolkata','Siliguri'
,'Chandigarh','Zirakpur','Amritsar','Ludhiana','Jalandhar','Ahmedabad',	'Surat', 'Vadodara', 'Vapi','Statue of Unity','Kanpur','Muzzafarnagar','Noida',	'Kochi',	'Thiruvananthapuram',
'Kozhikode','Bhopal','Indore','Rajasthan','Jaipur','Udaipur','Dehradun']
for c in range(len(cities)):
   
    #Automating search box fill up
    inputFormula = driver.find_element(By.NAME,'place')
    inputFormula.send_keys(f'{cities[c]}, India')
    inputFormula.send_keys(Keys.ENTER)
    sleep(2)

    #Getting the number of nearby cafes
    resultList = driver.find_elements(By.CSS_SELECTOR, 'article.base___3LiS9.linkOverlay.sb-global-gutters.py3.relative')
    resultSize = len(resultList)
    iterations = int(resultSize)
    results=[]

    #Getting th address of each cafe
    for i in range(iterations):
        #Clicking the infobtn
        infoBtn = resultList[i].find_element(By.CSS_SELECTOR, 'a.relative.pl5.color-textBlackSoft')
        driver.execute_script("arguments[0].click();", infoBtn)
        sleep(1)
        #Extracting the address
        getStoreAddress = driver.find_elements(By.CSS_SELECTOR, 'div.gridItem.size6of12') 
        results.append(getStoreAddress[0].get_attribute('innerHTML'))
        #Clicking the close button
        element = driver.find_element(By.CSS_SELECTOR, 'button.sb-iconButton.relative.sb-closeButton.sb-overlay__closeBtn.color-textBlackSoft')
        element.click()
        sleep(1)
    
   
    for k in range(len(results)):
        for i,j in rep:
            results[k] = results[k].replace(i,j)

    #making the csv file
    with open('Restaurants.csv', mode='a', newline='') as outputFile:
        restaurantCSV = csv.writer(outputFile, delimiter=',', quotechar='"', quoting = csv.QUOTE_MINIMAL)
        
        restaurantName = 'Starbucks'
        country = 'India'
        for restaurant in results:
            street = restaurant.split("/n")[0]
            zipCode = restaurant.split(",")[-1]

            restaurantCSV.writerow([restaurantName, street, zipCode, country])

    inputFormula.clear()
    if c in [5,10,15,20]:
        starbucksUrl = 'https://www.starbucks.com/store-locator?map=39.635307,-101.337891,5z'
        driver = webdriver.Chrome() 
        driver.get(starbucksUrl)
        sleep(5)
    


    
#Removing unneccesary html syntax, I couldnt extract the address without them using selenium    
driver.close()


