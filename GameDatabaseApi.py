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
                                    "time_to_beat", "cover", "screenshots"],
                         'expand': ['developers', 'genres']})

    for field in result.body:
        info.append(field)

    return info


