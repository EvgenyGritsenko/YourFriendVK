import requests
from bs4 import BeautifulSoup
import json





class Parsing:
    """Выполняет запрос и парсит всю нужную информацию"""
    def __init__(self, user_nick):
        self.nick = user_nick
        self.fake_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        self.req = requests.get(f"https://vk.com/{self.nick}",
                                headers={
                                    "User-Agent": self.fake_user_agent,
                                })
        self.soup = BeautifulSoup(self.req.content, "lxml")
        if self.req.status_code == 200:
            self.start()


    def start(self):
        """Запускает все нужные методы"""
        self.main_information()
        self.about_user()
        self.counters()
        self.posts()
        self.groups()


    def main_information(self):
        name = self.soup.find(class_="page_name").text.strip()
        print(name)
        status = self.soup.find(class_="page_current_info").\
                           find(class_="current_text").text
        print(status)
        last_seen = self.soup.find(class_="profile_online_lv").text
        print(last_seen)

    
    def about_user(self):
        labeled = self.soup.find_all("div", class_="labeled")
        data = []

        for l in labeled[2:]:
            data.append(l.find("a").text)

        print(data)

    
    def counters(self):
        page_counters = self.soup.find_all("a", class_="page_counter")

        for i in page_counters:
            label = i.find(class_="label").text.upper()
            count = i.find(class_="count").text.upper()
            print(label, count)

    
    def posts(self):
        print("----------")
        
        post_info = self.soup.find_all(class_="post_info")
        
        for post in post_info:
            text = post.find(class_="wall_post_text zoom_text").text
            likes = post.\
            find(class_="PostButtonReactions__title _counter_anim_container").text
            print(text, likes)           

    
    def groups(self):
        print("---groups---")
        amount = self.soup.find(class_="header_top clear_fix").\
                           find(class_="header_count fl_l").text
        print(amount)
        all_groups = self.soup.find_all(class_="group_name")

        for group in all_groups:
            title = group.find("a").text
            link = group.find("a").get("href")
            print(title, link)


def get_data():
    get_nick = input("Введи ник или id: ")
    if len(get_nick) > 4:
        Parsing(get_nick)
    else:
        print("Слишком короткий ник!")
get_data()
