import vk
import json
import os
import requests

from typing import List, Optional

from config import VK_TOKEN


class Parser:
    RESOLUTION_TYPES = ["w", "z", "y", "x"]
    api = vk.API(access_token=VK_TOKEN, v="5.131")

    def __init__(self, group_name: str, posts_count: int = 10) -> None:
        """
        Parser class
        Экземпляр класса с названием паблика Вконтакте и количеством постов, перебирает свежие посты и сохраняет их
        на диск

        :param group_name: (str) - название паблика ВКонтакте, который будет парсится
        :param posts_count: (int) - сколько парсим постов
        """
        self._group_name = group_name
        self._posts_count = posts_count
        self._posts: Optional[List[dict]] = None
        self._fresh_posts_ids: Optional[List] = None
        self._new_posts_ids: Optional[List] = None

    @property
    def posts(self) -> list:
        return self._posts

    @posts.setter
    def posts(self, new_posts) -> None:
        self._posts = new_posts

    @property
    def fresh_posts_ids(self) -> list:
        return self._fresh_posts_ids

    @fresh_posts_ids.setter
    def fresh_posts_ids(self, new_fresh_post_ids) -> None:
        self._fresh_posts_ids = new_fresh_post_ids

    @property
    def new_posts_id(self) -> list:
        return self._new_posts_ids

    @new_posts_id.setter
    def new_posts_id(self, value) -> None:
        self._new_posts_ids = value

    def get_posts(self, offset: int = 1) -> None:
        """
        Отправляем с помощью ВК-апи запрос на сервер, получаем от него ответ в виде json-файла
        :param offset: (int) - сколько пропускаем постов в группе перед парсингом
        :return: posts (List[dict]) -  данные со всех постов, которые спарсили
                 fresh_posts_ids (list) - файлы, готовящиеся поместится в текстовый файл для их сравнения
        """

        # отправляем запрос к апи и получаем результат
        result = self.api.wall.get(domain=self._group_name, count=self._posts_count, offset=offset)

        # создаём папку, где будем хранить полученные данные по группам
        if not os.path.exists(fr"groups/{self._group_name}"):
            os.mkdir(fr"groups/{self._group_name}")

        # скидываем полученный результат в json в папку группы с таким же названием для файла
        with open(fr"groups/{self._group_name}/{self._group_name}.json", "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4)

        # пока пустой список всех постов и все посты (по items из апи)
        self.fresh_posts_ids: List = []
        self.posts: [List[dict]] = result["items"]

        # наполняем список свежими постами
        for a_fresh_post_id in self.posts:
            if not a_fresh_post_id["marked_as_ads"] == 1:  # фильтр рекламных постов
                a_fresh_post_id = a_fresh_post_id["id"]
                self.fresh_posts_ids.append(a_fresh_post_id)

        print("Fresh posts! - ", self.fresh_posts_ids)

    def parse_posts(self) -> None:
        """Вытаскиваем ссылки на картинки из JSON-файла, выбираем наилучшее разрешение и скачиваем"""
        for post in self.posts:
            if post["id"] in self._new_posts_ids:  # фильтр рекламы  !!! В идеале - добавить данное условие сюда
                post_id = post["id"]
                print(f"Отправляем пост номер с ID: {post_id}")  # Пост id - собственно, уникальный ID каждого поста
                # начинаем вытаскивать вложения в посте
                try:
                    # проверяем, есть ли вообще вложения в посте
                    attachments = post["attachments"]

                    # проверка вложения на соответствие типу "фото"
                    file_counter = 0  # номер вложения (пометка для будущего сохранения)
                    for i_attachment in attachments:  # пошли циклом по всем вложениям

                        if i_attachment["type"] == "photo":
                            file_counter += 1
                            photo_sizes = i_attachment["photo"]["sizes"]
                            for size_type in self.RESOLUTION_TYPES:  # пошли циклом по резам ВК
                                size_found = False
                                for the_photo_size in photo_sizes:  # а теперь пошли циклом по резам самой картинки
                                    if the_photo_size.get("type") == size_type:
                                        if len(attachments) == 1:
                                            print(f"The size {size_type} is here!")
                                            self.download_image(the_photo_size["url"], post_id)
                                        else:
                                            print(f"The size {size_type} is here! {file_counter}-я КАРТИНКА")
                                            self.download_image(the_photo_size["url"], f"{post_id}-{file_counter}")
                                        print(the_photo_size["url"])
                                        print()
                                        size_found = True  # флаг для остановки
                                        break

                                if size_found:
                                    break
                            else:
                                print("No good quality or no photo at all")

                        elif i_attachment["type"] == "video":
                            file_counter += 1
                            print(f"Видео-пост и вложение в посте номер - {file_counter}")
                            video_access_key = i_attachment["video"]["access_key"]
                            video_owner_id = i_attachment["video"]["owner_id"]
                            video_post_id = i_attachment["video"]["id"]
                            print("Параметры видео:", video_owner_id, video_access_key, video_post_id)

                except (KeyError, IndexError):
                    print("Либо вложений нет, либо ненужный формат вложения (ссылка, видео, аудио)")

    def download_image(self, url: str, post_id: str) -> None:
        """Скачиваем конвертированную в байты пикчу с ВК"""
        image_result = requests.get(url=url)

        if not os.path.exists(fr"groups/{self._group_name}/images"):
            os.mkdir(fr"groups/{self._group_name}/images")

        with open(fr"groups/{self._group_name}/images/{post_id}.jpg", "wb") as image:
            image.write(image_result.content)

    def analyze_posts(self) -> None:
        """Сравнием полученные посты с теми, что мы уже сохраняли - старые или свежие """
        if not os.path.exists(fr"groups/{self._group_name}/exist_posts_{self._group_name}.txt"):
            print("Making new txt for 'fresh' posts")

            self._new_posts_ids = []
            with open(fr"groups/{self._group_name}/exist_posts_{self._group_name}.txt", "w") as file:
                for post_id in self.fresh_posts_ids:
                    file.write(f"{str(post_id)}\n")
                    self._new_posts_ids.append(post_id)

            self.parse_posts()

        else:
            with open(fr"groups/{self._group_name}/exist_posts_{self._group_name}.txt", "r+") as exist_posts:
                old_posts_set = set()
                for i_exist_post in exist_posts:
                    exist_post = int(i_exist_post.rstrip("\n"))
                    old_posts_set.add(exist_post)

                self._new_posts_ids = list(set(self.fresh_posts_ids).difference(old_posts_set))
                if self._new_posts_ids:
                    print(f"Bubba has new posts! - {self._new_posts_ids}")
                    exist_posts.seek(0)
                    for new_post_id in self.fresh_posts_ids:
                        exist_posts.write(f"{str(new_post_id)}\n")

                    self.parse_posts()

                else:
                    print("No new posts for now =/")

        return None

    def parsing(self):
        """Функция для запуска всего процесса парсинга"""
        self.get_posts()
        self.analyze_posts()

    def get_group_name(self):
        result = self.api.groups.getById(group_id=self._group_name)
        return result[0]["name"]


if __name__ == '__main__':
    # harry_parser = Parser("i_am_potterhead_hp", posts_count=6)
    # harry_parser.parsing()

    group_parser_yobangelion = Parser("yobangelion")
    group_parser_yobangelion.parsing()
    # group_name = Parser("dobriememes").get_group_name()


    # british_parser = Parser("pretty_british", posts_count=5)
    # british_parser.parsing()

    # good_parser = Parser("dobriememes")
    # good_parser.parsing()

    # news_parser = Parser("act54")
    # news_parser.paring()

    # for i_parser in ("yobangelion", "pretty_british", "dobriememes", "m_elizarov"):
    #     print(f"Сейчас рассматриваем паблик - {i_parser}")
    #     parser = Parser(i_parser, posts_count=15)
    #     parser.parsing()
    #     print(f"Закончили с группой - {i_parser}")
    #     print("="*55)
