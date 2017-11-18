import private
from collections import defaultdict
import vk_api

vk = vk_api.VkApi(login=private.login, password=private.password)   # This is authorization to vk.com using my login
vk.auth()                                                           # and password which exist in the different module


def format_output(cities, friends_amount):
    sorted_cities = sorted([(value, key) for (key, value) in cities.items()])
    if len(sorted_cities) >= 3:
        sorted_cities = sorted_cities[-3:]
        return "{} - {:.2f}%, {} - {:.2f}%, {} - {:.2f}%".format(sorted_cities[2][1],
                                                                 sorted_cities[2][0] / friends_amount * 100,
                                                                 sorted_cities[1][1],
                                                                 sorted_cities[1][0] / friends_amount * 100,
                                                                 sorted_cities[0][1],
                                                                 sorted_cities[0][0] / friends_amount * 100)
    if len(sorted_cities) == 0:
        return "Person has no friends"
    if len(sorted_cities) == 1:
        return "{} - 100%".format(sorted_cities[0][1])
    if len(sorted_cities) == 2:
        return "{} - {:.2f}%, {} - {:.2f}%".format(sorted_cities[1][1], sorted_cities[1][0] / friends_amount * 100,
                                                   sorted_cities[0][1], sorted_cities[0][0] / friends_amount * 100)


def over_5000_friends(user_id, friends_amount):
    cities = defaultdict(int)
    response = vk.method('friends.get', {'user_id': user_id, 'fields': 'city', 'offset': 0})
    offset = 5000
    while response['items']:
        for person in response['items']:
            if 'city' in person.keys():
                city = person['city']['title']
                cities[city] += 1
        response = vk.method('friends.get', {'user_id': user_id, 'fields': 'city', 'offset': offset})
        offset += 5000
    return format_output(cities, friends_amount)


def guess_city(user_id):
    response = vk.method('friends.get', {'user_id': user_id, 'fields': 'city'})
    cities = defaultdict(int)
    friends_amount = response['count']
    if friends_amount == 5000 and vk.method('friends.get', {'user_id': user_id, 'fields': 'city', 'offset': 5000})['items']:
        return over_5000_friends(user_id, friends_amount)
    for person in response['items']:
        if 'city' in person.keys():
            city = person['city']['title']
            cities[city] += 1
    return format_output(cities, friends_amount)

guessed_cities = guess_city(103524554)
print(guessed_cities)