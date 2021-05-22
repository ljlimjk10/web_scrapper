import scrapy
from selenium import webdriver
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
import selenium
import time
from .config import ENV


class ContactsSpider(scrapy.Spider):
    name = 'contacts'
    allowed_domains = [ENV.BASE_URL]    
    start_urls = [f'{ENV.BASE_URL}/']
   
    def start_requests(self):
        yield SeleniumRequest(
            url = f'{ENV.BASE_URL}/',
            wait_time = 3,
            screenshot = True,
            callback = self.parse
        )
   
    def parse(self, response):
        driver = response.meta['driver']        

        self.user_will_login(driver)
        self.user_search(driver)
        
        # First page
        listings = self.user_get_listings(driver)
        for listing in listings:
            info = self.user_will_get_info_from_listing(driver, listing)
            yield info

        # Subsequent pages
        while (driver.find_elements_by_xpath("//div[@title='Next Page']")):
            self.user_goes_to_next_page(driver)
            listings = self.user_get_listings(driver)
            
            for listing in listings:
                info = self.user_will_get_info_from_listing(driver, listing)
                yield info


    def user_will_login(self, driver):
        username_input = driver.find_element_by_xpath("//input[@name = 'txtUserName']")
        username_input.send_keys(ENV.USERNAMES)
        password_input = driver.find_element_by_xpath("//input[@name = 'txtPassword']")
        password_input.send_keys(ENV.PASSWORDS)
        password_input.send_keys(Keys.ENTER)
        time.sleep(1)


    def user_search(self, driver):
        agent_tools = driver.find_element_by_xpath("//li[@id='menu5']/a").click()
        time_usage_approval = driver.find_element_by_xpath("//input[@id='popup_ok']").click()

        for_rent_btn = driver.find_element_by_xpath("//input[@id='cbForRent']")
        for_rent_btn.click()

        select_owner_btn = driver.find_element_by_xpath("//input[@id='cboOwnership_1']")
        select_owner_btn.click()
        #
        enter_posted_date_start = driver.find_element_by_xpath("//input[@id='txtDateFrom']").click()
        select_posted_year_start = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/div/div[2]/select").click()
        enter_posted_year_start = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/div/div[2]/select/option[10]").click()
        select_posted_month_start = driver.find_element_by_xpath("//button[@class='pika-next']").click()
        select_posted_month_start = driver.find_element_by_xpath("//button[@class='pika-next']").click()
        enter_posted_date_start = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/table/tbody/tr[2]/td[6]/button").click()

        #to 8th may 2019
        enter_posted_date_end = driver.find_element_by_xpath("//input[@id='txtDateTo']").click()
        select_posted_year_end = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/div/div[2]/select").click()
        enter_posted_year_end = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/div/div[2]/select/option[11]").click()
        select_posted_date_end = driver.find_element_by_xpath("//div[@class='pika-single is-bound']/div/table/tbody/tr[3]/td[1]/button").click()
    
        search_btn = driver.find_element_by_xpath("//input[@id='btnSearch']").click()
        time.sleep(1)
        driver.set_window_size(3000,5000)
        size_10 = driver.find_element_by_xpath("//div[@class='size']").click()
        time.sleep(1)

    def user_get_listings(self, driver):
        listings = driver.find_elements_by_xpath("//div[@id='grid']/div/table/tbody/tr")
        time.sleep(0.5)

        return listings

    def user_goes_to_next_page(self, driver):
        driver.find_element_by_xpath("//div[@title='Next Page']").click()
        time.sleep(1)

    def user_will_get_info_from_listing(self, driver, listing):
        details = listing.find_element_by_xpath(".//td[4]/a")
        details.click()
        
        driver.switch_to.frame(driver.find_element_by_xpath("//div[@id='jq-content']/div/iframe"))
        html = driver.page_source
        response_obj = Selector(text=html) 
        location = response_obj.xpath("//form[@name='form1']/table/tbody/tr[3]/td/table/tbody/tr/td[2]/text()").get()
        allowed_name = response_obj.xpath("//form[@name='form1']/table/tbody/tr[5]/td[1]/table/tbody/tr[1]/td[2]/text()").get()
        allowed_contact = response_obj.xpath("//form[@name='form1']/table/tbody/tr[5]/td[1]/table/tbody/tr[2]/td[2]/text()").get()
        date = response_obj.xpath("//form[@name='form1']/table/tbody/tr[5]/td[2]/table/tbody/tr[2]/td[2]/text()").get()
        property_type = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[2]/td[2]/text()").get()
        bedroom = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[2]/table/tbody/tr[1]/td[2]/text()").get()
        bathroom = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[2]/table/tbody/tr[2]/td[2]/text()").get()
        asking_price = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[4]/td[2]/text()").get()
        asking_psf = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[5]/td[2]/text()").get()
        build_up = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[6]/td[2]/text()").get()
        tenure = response_obj.xpath("//form[@name='form1']/table/tbody/tr[7]/td[1]/table/tbody/tr[7]/td[2]/text()").get()

        driver.switch_to.default_content()
        close_path_driver = driver.find_element_by_xpath("//div[@id='jq-img-close']")
        close_path_driver.click()

        return {
            'Location': location,
            'name' : allowed_name,
            'contact number': allowed_contact,
            'date posted' : date,
            'type' : property_type,
            'bedroom': bedroom,
            'bathroom' : bathroom,
            'asking price' : asking_price,
            'asking psf' : asking_psf,
            'build up' : build_up,
            'tenure' : tenure,
        }        
        


                
        

