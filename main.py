from fileinput import filename
from textwrap import indent
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
        self.data_for_write = {f"{self.nick}": {}}
        if self.req.status_code == 200:
            self.main_information(self.data_for_write)
            self.about_user(self.data_for_write)
            self.counters(self.data_for_write)
            self.posts(self.data_for_write)
            self.groups(self.data_for_write)
            Write(self.nick, self.data_for_write).write_to_json()


    def main_information(self, all_info):
        current_info = {}
        try:
            name = self.soup.find(class_="page_name").text.strip()
        except AttributeError:
            name = "Not found"
        finally:
            current_info.update(Name=str(name))

        try:
            status = self.soup.find(class_="page_current_info").\
                           find(class_="current_text").text
        except AttributeError:
            status = "Not found"
        finally:
            current_info.update(Status=str(status))

        try:
            last_seen = self.soup.find(class_="profile_online_lv").text
        except AttributeError:
            last_seen = "Not found"
        finally:
            current_info.update(LastSeen=str(last_seen))

        all_info[self.nick].update({"Main info": current_info})


    def about_user(self, all_info):
        current_info = {}

        try:
            labeled = self.soup.find_all("div", class_="labeled")
            data = []

            for l in labeled[2:]:
                data.append(l.find("a").text)

        except AttributeError:
            data = "Not found"
        finally:
            current_info.update(AboutUser=data)

        all_info[self.nick].update({"Data": current_info})

    
    def counters(self, all_info):
        current_info = {}
        try:
            page_counters = self.soup.find_all("a", class_="page_counter")
            data = {}
            for i in page_counters:
                label = i.find(class_="label").text.upper()
                count = i.find(class_="count").text.upper()
                data.update({label:count})
        except AttributeError:
            data = "Not found"
        finally:
            current_info.update(Data=data)

        all_info[self.nick].update({"Quantitative information": current_info})

    
    def posts(self, all_info):
        current_info = {}
        
        try:
            post_info = self.soup.find_all(class_="post_info")
            data = {}
            for post in post_info:
                text = post.find(class_="wall_post_text zoom_text").text
                likes = post.\
                find(class_="PostButtonReactions__title _counter_anim_container").text
                data.update({str(text): int(likes)})

        except AttributeError:
            data = "Not found"
        finally:
            current_info.update({"Posts": data})
        
        all_info[self.nick].update(current_info)


    def groups(self, all_info):
        current_info = {"Block": "Groups", "Data": {}}

        try:
            data = {"Groups": {}}
            amount = self.soup.find(class_="header_top clear_fix").\
                            find(class_="header_count fl_l").text
            data.update(Amount=int(amount))
            all_groups = self.soup.find_all(class_="group_name")

            for group in all_groups:
                title = group.find("a").text
                link = group.find("a").get("href")
                data["Groups"].update({str(title): str(link)})
        except AttributeError:
            data = "Not found"
        finally:
            current_info.update(data)
        
        all_info[self.nick].update({"Groups": current_info})


class Write:
    def __init__(self, user_nick, dict_for_write):
        self.user_nick = user_nick
        self.file_name = f"{self.user_nick}.json"
        self.file_path = f"data/{self.file_name}"
        self.dick_for_write = dict_for_write 

    def write_to_json(self):
        with open(self.file_path, "w") as file:
            json.dump(self.dick_for_write, file, indent=4)


    def print(self, file_name):
        with open(file_name, "rb") as f:
            data = json.load(f)
            print(data)


def get_data():
    get_nick = input("Введи ник или id: ")
    if len(get_nick) > 4:
        Parsing(get_nick)
    else:
        print("Слишком короткий ник!")
get_data()
