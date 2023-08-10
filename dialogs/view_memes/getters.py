import os
import time

from typing import Generator

from vk import exceptions
from parser import Parser


from aiogram_dialog import DialogManager


# async def groups_getter(**kwargs):
#     """Возвращает названия всех занесённых групп (prod.: всех групп, что лежат уже спарсенные в папке)"""
#     # по умолчанию возвращает генератор
#     channels_tuple = tuple((os.listdir(path=r"C:\Me\Coding_Python\Projects\vk_memes\groups")))
#
#     channels_dict = {
#         "channels": channels_tuple
#     }
#
#     return channels_dict
#
#
#
# # !!!ACHTUNG!!!
# # Тестовая функция, парсим название самого паблика для красивого вывыода
# # В дальнейшем будем использовать при занесении паблика сразу в БД, пока что тестим
def nonsync_groups_getter(**kwargs):
    """Возвращает названия всех занесённых групп (prod.: всех групп, что лежат уже спарсенные в папке)"""
    # по умолчанию возвращает генератор
    channels_tuple = tuple((os.listdir(path=r"C:\Me\Coding_Python\Projects\vk_memes\groups")))
    print(channels_tuple)
    # ('act54', 'dobriememes', 'i_am_potterhead_hp', 'm_elizarov', 'pretty_british', 'walker.py', 'yobangelion')

    right_list = list()
    for i_group in channels_tuple:
        try:
            group_name = Parser(i_group).get_group_name()
            print(group_name)
            right_list.append(group_name)
        except exceptions.VkAPIError:
            time.sleep(1)

    enum_right_list = tuple(enumerate(right_list))
    print(enum_right_list)

    channels_dict = {
        "channels": right_list
    }

    print("old channels_dict:", channels_dict)

    channels_dict = {
        "channels": enum_right_list
    }

    print("enumerated channels_dict:", channels_dict)

    # print(channels_dict)
    # return channels_dict


# nonsync_groups_getter()
# А теперь попробуем перевести эту функцию на рельсы геттера


async def test_groups_getter(**kwargs) -> dict:
    """Вытаскиваем фото из папок по "официальным" названиям пабликов (не id)"""
    channels_tuple = tuple((os.listdir(path=r"C:\Me\Coding_Python\Projects\vk_memes\groups")))

    right_list = list()
    # Парсим "человеческое" название паблика (не id), для этого каждый раз делаем запрос по api
    # В будущем - перевести это действие при добавлении паблика в базу данных, чтобы не заниматься каждый раз
    # При открытии меню
    for i_group in channels_tuple:
        try:
            group_name = Parser(i_group).get_group_name()
            right_list.append(group_name)
        except exceptions.VkAPIError:
            time.sleep(1)

    channels_dict = {
        "channels": right_list
    }
    print(channels_dict)
    # {'channels': ['АСТ-54', 'Добрые мемы : )', 'Я поттероман Гарри Поттер Фантастические твари', 'Михаил Елизаров', 'БРИТИШ ЮМОР', 'Rebuild of Yobangelion']}

    return channels_dict


async def test_groups_getter_2(**kwargs) -> dict:
    """Currently working with this one """
    # Что нужно? Вытащим кортеж вида (id, название) - чтобы можно было осуществлять навигацию по папкам
    channels_tuple = tuple((os.listdir(path=r"C:\Me\Coding_Python\Projects\vk_memes\groups")))

    right_list = list()

    for group_id in channels_tuple:
        try:
            group_name = Parser(group_id).get_group_name()
            right_list.append((group_id, group_name))   # Добавляем кортеж из group_id & названия паблика
        except exceptions.VkAPIError:
            time.sleep(1)

    channels_dict = {
        "channels": right_list
    }
    print(channels_dict)
    # {'channels': ['АСТ-54', 'Добрые мемы : )', 'Я поттероман Гарри Поттер Фантастические твари', 'Михаил Елизаров', 'БРИТИШ ЮМОР', 'Rebuild of Yobangelion']}

    return channels_dict


async def test_groups_getter_3_by_db(**kwargs) -> dict:
    """Вытаскиваем фото из папок по "официальным" названиям пабликов (не id)"""
    # ---какая-то магия с дб, и вытащили данный кортеж---
    channels_tuple = (("yoba", "Rebuild"), ("m_elizarov", "Мыхайло"), ("act24", "Новосиб-сила"))

    channels_dict = {
        "channels": channels_tuple
    }

    return channels_dict


# ГЕТТЕРЫ ДЛЯ МЕМОВ

async def get_list_memes(dialog_manager: DialogManager, **kwargs) -> dict:
    group_id = dialog_manager.dialog_data.get("group_id")
    memes_list = list(os.listdir(
        path=r"C:\Me\Coding_Python\Projects\vk_memes\groups\{group_id}\images".format(group_id=group_id)))

    memes_dict = {
        "list": memes_list
    }

    return memes_dict


# async def get_meme(dialog_manager: DialogManager, **kwargs) -> dict: