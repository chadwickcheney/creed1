from . import debug
import time
import random
import traceback
from abc import ABCMeta, abstractmethod
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from . import webhelper

class Site:
    def __init__(self,driver,debug,tier,webster):
        self.driver=driver
        self.debug=debug
        self.tier=tier
        self.webster=webster
        self.webhelper = webhelper.WebHelper(self.driver)
        self.check_modal_dictionary={
                'controlledchaoshair':self.controlledchaoshair_modal_exists,
                'beardedgoat':self.beardedgoat_modal_exists,
            }

        #site tests
        self.test_dictionary={}

    #COMMENCE TEST
    def unit_test(self):
        print("web tests")
        tests = [self.check_modal_functionality,self.viewport_meta_tag_exists,self.facebook_pixel_exists,self.has_javascript_fallback]
        for test in tests:
            self.debug.press(feed='Running test {}'.format(test.__name__),tier=self.tier+1)
            try:
                self.test_dictionary.update({test.__name__:test()})
            except Exception as e:
                self.test_dictionary.update({test.__name__:str(e)})
        return self.test_dictionary

    def check_modal_functionality(self):
        return self.get_modal_response(self.webster.url)

    def viewport_meta_tag_exists(self):
        elements = self.driver.find_elements_by_xpath("//*[not(*)]")
        for element in elements:
            if 'meta name="viewport" content="width=device-width, initial-scale' in element.get_attribute('outerHTML'):
                return True
        return False

    def facebook_pixel_exists(self):
        elements = self.driver.find_elements_by_xpath("//*[not(*)]")
        for element in elements:
            if 'https://connect.facebook.net/' in str(element.get_attribute('outerHTML')):
                return True
        return False

    def has_javascript_fallback(self):
        for element in self.driver.find_elements_by_xpath('.//*'):
            if element.tag_name=='noscript':
                dictionary={"Found":True,"Text":element.text}
                return dictionary
        return False

    def get_modal_response(self,url):
        for key,value in self.check_modal_dictionary.items():
            if key in url:
                return value()

    def controlledchaoshair_modal_exists(self):
        dictionary={
                'email_location_method':self.driver.find_element_by_class_name,
                'email_element_identifier':'privy-email-input',
                'email_element_submit_method':self.driver.find_element_by_id,
                'email_element_submit_identifier':'privy-submit-btn',
                'modal_close_method':self.driver.find_element_by_class_name,
                'modal_close_identifier':'privy-dismiss-content',
            }
        controlledchaoshair=ControlledChaosHair(self.driver,self.webhelper,dictionary)
        return controlledchaoshair.response_dictionary

    def beardedgoat_modal_exists(self):
        dictionary={
                'email_location_method':self.driver.find_element_by_xpath,
                'email_element_identifier':'/html/body/div[3]/div/div/div/div/div/div[2]/div/div/input',
                'email_element_submit_method':self.driver.find_element_by_xpath,
                'email_element_submit_identifier':'/html/body/div[3]/div/div/div/div/div/div[3]/div/button',
                'modal_close_method':self.driver.find_element_by_xpath,
                'modal_close_identifier':'privy-dismiss-content',
                'pop_up':None,
            }
        beardedgoat=BeardedGoat(self.driver,self.webhelper,dictionary)
        return beardedgoat.response_dictionary

#MODAL ABSTRACT class
class AbstractModalFunctionality:
    def __init__(self,driver,webhelper,dictionary):
        self.driver=driver
        self.dictionary=dictionary
        self.webhelper=webhelper
        self.response_list=[
                self.activate,
                self.exists,
                self.email_keys,
                self.email_submit,
                self.close,
            ]
        self.response_dictionary={}
        attempt=0
        while true:
            attempt+=1
            try:
                self.act()
                break
            except NoSuchElementException:
                self.webhelper.check_pop_up(self.driver,self.dictionary)
            if attempt > 1:
                break

    @abstractmethod
    def act(self):
        for m in self.response_list:
            var = m()
            self.response_dictionary.update({m.__name__:var})
            if not var:
                break

    @abstractmethod
    def activate(self):
        time.sleep(2)
        return True

    @abstractmethod
    def exists(self):
        try:
            return bool(self.dictionary['email_location_method'](self.dictionary['email_element_identifier']))
        except:
            time.sleep(1)
            input('>>>')
            return False

    @abstractmethod
    def email_keys(self):
        self.dictionary['email_location_method'](self.dictionary['email_element_identifier']).send_keys('john@gmail.com')
        if self.dictionary['email_location_method'](self.dictionary['email_element_identifier']).get_attribute('value'):
            return True
        return False


    @abstractmethod
    def email_submit(self):
        e = self.dictionary['email_element_submit_method'](self.dictionary['email_element_submit_identifier']).click()
        if e:
            return True
        return False

    @abstractmethod
    def close(self):
        e = self.dictionary['modal_close_method'](self.dictionary['modal_close_identifier']).click()
        if e:
            return True
        return False


class ControlledChaosHair(AbstractModalFunctionality):
    def __init__(self,driver,webhelper,dictionary):
        self.driver=driver
        self.dictionary=dictionary
        self.response_dictionary={}
        self.response_list=[
                self.activate,
                self.exists,
                self.email_keys,
                self.email_submit,
                self.close,
            ]
        self.act()

    def act(self):
        return super().act()

    def activate(self):
        return super().activate()

    def exists(self):
        return super().exists()

    def email_keys(self):
        return super().email_keys()

    def email_submit(self):
        return super().email_submit()

    def close(self):
        return super().close()

class BeardedGoat(AbstractModalFunctionality):
    def __init__(self,driver,webhelper,dictionary):
        self.driver=driver
        self.dictionary=dictionary
        self.webhelper=webhelper
        self.response_dictionary={}
        self.response_list=[
                self.activate,
                self.exists,
                self.email_keys,
                self.email_submit,
                self.close,
            ]
        self.act()

    def act(self):
        return super().act()

    def activate(self):
        email_element=False
        time.sleep(4)
        elements = self.driver.find_elements_by_xpath('.//*')
        for element in elements:
            try:
                time.sleep(int(random.randint(0,10)/100))
                self.driver.execute_script("return arguments[0].scrollIntoView(true);", element)
            except StaleElementReferenceException as Exception:
                pass

        self.driver.execute_script("return arguments[0].scrollIntoView(true);", self.driver.find_element_by_tag_name('body'))
        time.sleep(4)
        try:
            email_element = bool(self.dictionary['email_location_method'](self.dictionary['email_element_identifier']))
        except:
            try:
                elements = self.driver.find_elements_by_class_name('col')
                for element in elements:
                    try:
                        hover = ActionChains(self.driver).move_to_element(element)
                        hover.perform()
                    except:
                        pass
                email_element = bool(self.dictionary['email_location_method'](self.dictionary['email_element_identifier']))
            except:
                email_element=False
        return email_element

    def exists(self):
        return super().exists()

    def email_keys(self):
        return super().email_keys()

    def email_submit(self):
        return super().email_submit()

    def close(self):
        return super().close()











'''class ControlledChaosHair:
    def __init__(self,driver):
        self.driver=driver
        self.dictionary={
                'email_location_method':self.driver.find_element_by_class_name,
                'email_element_identifier':'privy-email-input',
                'email_element_submit_method':self.driver.find_element_by_id,
                'email_element_submit_identifier':'privy-submit-btn',
                'modal_close_method':self.driver.find_element_by_class_name,
                'modal_close_identifier':'privy-dismiss-content',
            }

        self.response_list=[
                self.activate,
                self.exists,
                self.email_keys,
                self.email_submit,
                self.close,
            ]

        self.response_dictionary={}

        self.act()

    def act(self):
        for m in self.response_list:
            var = m()
            self.response_dictionary.update({m.__name__:var})
            if not var:
                break

    def activate(self):
        time.sleep(2)
        return True

    def exists(self):
        return bool(self.dictionary['email_location_method'](self.dictionary['email_element_identifier']))

    def email_keys(self):
        self.dictionary['email_location_method'](self.dictionary['email_element_identifier']).send_keys('john@gmail.com')
        if self.dictionary['email_location_method'](self.dictionary['email_element_identifier']).get_attribute('value'):
            return True
        return False


    def email_submit(self):
        e = self.dictionary['email_element_submit_method'](self.dictionary['email_element_submit_identifier']).click()
        if e:
            return True
        return False

    def close(self):
        e = self.dictionary['modal_close_method'](self.dictionary['modal_close_identifier']).click()
        if e:
            return True
        return False


class BeardedGoat:
    def __init__(self,driver):
        self.driver=driver
        self.dictionary={
                'email_location_method':self.driver.find_element_by_xpath,
                'email_element_identifier':'/html/body/div[3]/div/div/div/div/div/div[2]/div/div/input',
                'email_element_submit_method':self.driver.find_element_by_xpath,
                'email_element_submit_identifier':'/html/body/div[3]/div/div/div/div/div/div[3]/div/button',
                'modal_close_method':self.driver.find_element_by_xpath,
                'modal_close_identifier':'privy-dismiss-content',
            }

        self.response_list=[
                self.activate,
                self.exists,
                self.email_keys,
                self.email_submit,
                self.close,
            ]

        self.response_dictionary={}

        self.act()

        def act(self):
        for m in self.response_list:
            var = m()
            self.response_dictionary.update({m.__name__:var})
            if not var:
                break

        def activate(self):
            time.sleep(2)
            return True

        def exists(self):
            return bool(self.dictionary['email_location_method'](self.dictionary['email_element_identifier']))

        def email_keys(self):
            self.dictionary['email_location_method'](self.dictionary['email_element_identifier']).send_keys('john@gmail.com')
            if self.dictionary['email_location_method'](self.dictionary['email_element_identifier']).get_attribute('value'):
                return True
            return False


        def email_submit(self):
            e = self.dictionary['email_element_submit_method'](self.dictionary['email_element_submit_identifier']).click()
            if e:
                return True
            return False

        def close(self):
            e = self.dictionary['modal_close_method'](self.dictionary['modal_close_identifier']).click()
            if e:
                return True
            return False'''
