import scrapy
from selenium import webdriver
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from scrapy.selector import Selector
import selenium
import time
from shutil import which
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
class RentSpider(scrapy.Spider):
    name = 'rent'
    allowed_domains = ['irealtor.iproperty.com.sg']
    start_urls = ['https://irealtor.iproperty.com.sg/']
   
    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://irealtor.iproperty.com.sg/',
            wait_time = 3,
            screenshot = True,
            callback = self.parse
        )
   
    
        
    #     driver.close()
    def parse(self, response):
        driver = response.meta['driver']        
        # self.html = driver.page_source
        # resp = Selector(text=self.html)
        #enter username & password
        username_input = driver.find_element_by_xpath("//input[@name = 'txtUserName']")
        username_input.send_keys("88521208")
        password_input = driver.find_element_by_xpath("//input[@name = 'txtPassword']")
        password_input.send_keys("170795AaJ24101116")
        password_input.send_keys(Keys.ENTER)
        driver.get("https://irealtor.iproperty.com.sg/agentools/search.aspx")
        time.sleep(1)
        agent_tools = driver.find_element_by_xpath("//li[@id='menu5']/a").click()
        time_usage_approval = driver.find_element_by_xpath("//input[@id='popup_ok']").click()

        for_rent_btn = driver.find_element_by_xpath("//input[@id='cbForRent']")
        for_rent_btn.click()

        select_owner_btn = driver.find_element_by_xpath("//input[@id='cboOwnership_1']")
        select_owner_btn.click()
        
        enter_posted_date_start = driver.find_element_by_xpath("//input[@id='txtDateFrom']").click()
        select_posted_year = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/div/div[2]/select").click()
        enter_posted_year = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/div/div[2]/select/option[6]").click()
        select_posted_month = driver.find_element_by_xpath("//button[@class='pika-next']").click()
        select_posted_month = driver.find_element_by_xpath("//button[@class='pika-next']").click()
        enter_posted_date = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/table/tbody/tr[2]/td[1]/button").click()

        time.sleep(2)
        enter_posted_date_end = driver.find_element_by_xpath("//input[@id='txtDateTo']").click()
        select_posted_year_end = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/div/div[2]/select").click()
        enter_posted_year_end = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/div/div[2]/select/option[7]").click()
        # time.sleep(2)
        # select_posted_month_end = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/div/button").click()
        # time.sleep(2)
        # select_posted_month_end = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/div/button").click()
        # #March 2018
        select_posted_date_end = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/table/tbody/tr[2]/td[1]/button").click()
    
        search_btn = driver.find_element_by_xpath("//input[@id='btnSearch']").click()
        time.sleep(1)
        driver.set_window_size(3000,5000)
        size_10 = driver.find_element_by_xpath("//div[@class='size']").click()
        time.sleep(1)
        
        #To access each row
        column = driver.find_elements_by_xpath("//div[@id='grid']/div/table/tbody/tr")
        time.sleep(0.5)
        for columns in column:
            details = columns.find_element_by_xpath(".//td[4]/a")
            details.click()
            
            driver.switch_to.frame(driver.find_element_by_xpath("//div[@id='jq-content']/div/iframe"))
            html = driver.page_source
            response_obj = Selector(text=html) 
            location = response_obj.xpath("//form[@name='form1']/table/tbody/tr[3]/td/table/tbody/tr/td[2]/text()").get()
            name = response_obj.xpath("//form[@name='form1']/table/tbody/tr[5]/td[1]/table/tbody/tr[1]/td[2]/text()").get()
            contact = response_obj.xpath("//form[@name='form1']/table/tbody/tr[5]/td[1]/table/tbody/tr[2]/td[2]/text()").get()
            date = response_obj.xpath("//form[@name='form1']/table/tbody/tr[5]/td[2]/table/tbody/tr[2]/td[2]/text()").get()
            property_type = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[2]/td[2]/text()").get()
            bedroom = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[2]/table/tbody/tr[1]/td[2]/text()").get()
            bathroom = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[2]/table/tbody/tr[2]/td[2]/text()").get()
            asking_price = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[4]/td[2]/text()").get()
            asking_psf = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[5]/td[2]/text()").get()
            build_up = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[6]/td[2]/text()").get()
            tenure = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[7]/td[2]/text()").get()
            first_ad_date = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[2]/table/tbody/tr[8]/td[2]/text()").get()
            living_flr = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[2]/table/tbody/tr[4]/td[2]/text()").get()
            dining_flr = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[2]/table/tbody/tr[5]/td[2]/text()").get()
            bedroom_flr = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[2]/table/tbody/tr[6]/td[2]/text()").get()
            kitchen_flr = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[2]/table/tbody/tr[7]/td[2]/text()").get()
            remarks = response_obj.xpath("//form[@name='form1']/table/tbody/tr[9]/td/table/tbody/tr[4]/td[2]/text()").get()
            
            
            yield{
                    'Location': location,
                    'name' : name,
                    'contact number': contact,
                    'date posted' : date,
                    '1st ad date' : first_ad_date,
                    'type' : property_type,
                    'bedroom': bedroom,
                    'bathroom' : bathroom,
                    'asking price' : asking_price,
                    'asking psf' : asking_psf,
                    'build up' : build_up,
                    'tenure' : tenure,
                    'living_flr' : living_flr,
                    'dining_flr' : dining_flr,
                    'bedroom_flr' : bedroom_flr,
                    'kitchen_flr' : kitchen_flr,
                    'remarks ' : remarks,

                }
            
            
            driver.switch_to.default_content()
            close_path_driver = driver.find_element_by_xpath("//div[@id='jq-img-close']")
            close_path_driver.click()
        
                 
        
        while (driver.find_elements_by_xpath("//div[@title='Next Page']")):
            btn = driver.find_element_by_xpath("//div[@title='Next Page']").click()
            time.sleep(1)    
            column = driver.find_elements_by_xpath("//div[@id='grid']/div/table/tbody/tr")
            for columns in column:
                details = columns.find_element_by_xpath(".//td[4]/a")
                details.click()
                
                driver.switch_to.frame(driver.find_element_by_xpath("//div[@id='jq-content']/div/iframe"))
                html = driver.page_source
                response_obj = Selector(text=html) 
                location = response_obj.xpath("//form[@name='form1']/table/tbody/tr[3]/td/table/tbody/tr/td[2]/text()").get()
                name = response_obj.xpath("//form[@name='form1']/table/tbody/tr[5]/td[1]/table/tbody/tr[1]/td[2]/text()").get()
                contact = response_obj.xpath("//form[@name='form1']/table/tbody/tr[5]/td[1]/table/tbody/tr[2]/td[2]/text()").get()
                date = response_obj.xpath("//form[@name='form1']/table/tbody/tr[5]/td[2]/table/tbody/tr[2]/td[2]/text()").get()
                property_type = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[2]/td[2]/text()").get()
                bedroom = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[2]/table/tbody/tr[1]/td[2]/text()").get()
                bathroom = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[2]/table/tbody/tr[2]/td[2]/text()").get()
                asking_price = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[4]/td[2]/text()").get()
                asking_psf = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[5]/td[2]/text()").get()
                build_up = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[6]/td[2]/text()").get()
                tenure = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[7]/td[2]/text()").get()
                
                yield {
                    'Location': location,
                    'name' : name,
                    'contact number': contact,
                    'date posted' : date,
                    'type' : property_type,
                    'bedroom': bedroom,
                    'bathroom' : bathroom,
                    'asking price' : asking_price,
                    'asking psf' : asking_psf,
                    'build up' : build_up,
                    'tenure' : tenure,
                }
                
                
                driver.switch_to.default_content()
                close_path_driver = driver.find_element_by_xpath("//div[@id='jq-img-close']")
                close_path_driver.click() 
                
        


