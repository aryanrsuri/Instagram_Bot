from selenium import webdriver
from time import sleep
from password import pw

class Instabot:

    def __init__(self, username, passphrase):
        self.driver = webdriver.Chrome()
        self.driver.get("https://instagram.com")
        self.username = username
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]")\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(passphrase)
        self.driver.find_element_by_xpath("//button[@type='submit']")\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(),'Not Now')]")\
            .click()
        sleep(2)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(self.username))\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href, '/following')]")\
            .click()
        following = self._get_names()
        sleep(1)
        self.driver.find_element_by_xpath("//a[contains(@href, '/followers')]")\
            .click()
        followers = self._get_names()
        sleep(1)
        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)
        file = open("not_following_back.txt", "w+")
        file.write(not_following_back.__str__())

    def _get_names(self):
        sleep(2)
        suggestions = self.driver.find_element_by_xpath("//h4[contains(text(), 'Suggestions')]");
        self.driver.execute_script('arguments[0].scrollIntoView()', suggestions)
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_height, height = 0, 1
        while last_height != height:
            last_height = height
            sleep(1)
            height = self.driver.execute_script("""
                        arguments[0].scrollTo(0, arguments[0].scrollHeight);
                        return arguments[0].scrollHeight;
                        """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button')\
            .click()
        return names


my_bot = Instabot('aryansur.i', pw)
my_bot.get_unfollowers()
