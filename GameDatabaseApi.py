from igdb_api_python.igdb import igdb as igdb

def get_key():
    filename = '/Users/DarthVader/Desktop/GamerHub/game_key'
    file = open(filename, "r")
    key = file.readline()
    file.close()
    return key


api_key = get_key()

igdb = igdb(api_key)


def get_platforms(platform_name):

    result = igdb.platforms({'search': platform_name,
                             'fields': ["games", "name"]})
    return result

def get_platform_games(plat_name):

    platform = get_platforms(plat_name)

    for plat in platform.body:
        if plat['name'] == plat_name:
            game_names = {}
            game_names.update(plat['games'])
            return game_names


def add_platform_filter(game_name, platform_name):

    result = igdb.games({'search': game_name,
                         'fields': ['name']})
    filter = igdb.platforms({'search': platform_name,
                             'filter': ['name']})




def generate_search_list(game_name):

    result = igdb.games({'search': game_name,
                         'fields': ["name"],
                         'limit': 5})
    return result


def single_search(game_name):

    info = []
    result = igdb.games({'search': game_name,
                         'fields': ["name", "summary", "storyline", "rating",
                                    "time_to_beat"],
                         'expand': ['developers', 'genres']})

    for field in result.body:
        info.append(field)

    return info


# todo: create query methods for searching keywords
# todo: create query methods for grabbing related info fields


# how to use generate search list
#
# i = input('Enter Game name: ')
#
# r = generate_search_list(i)
#
# for n in r.body:
#      print(n['name'])

# how to use single search


# i = input('Enter Game name: ')
#
# r = single_search(i)
# for n in r.body:
#     info = {}
#     if n['name'] == i:
#         info.update(n)
#         for val in info.values():
#             print(val)

# i = input('enter game system name: ')
#
# r = get_platform_games(i)
#
# print(r.items())




# todo: template inheritance

# todo: filters, search ratings, prices