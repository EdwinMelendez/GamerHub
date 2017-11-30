from igdb_api_python.igdb import igdb as igdb

def get_key():
    filename = '/Users/DarthVader/Desktop/GamerHub/game_key'
    file = open(filename, "r")
    key = file.readline()
    file.close()
    return key

api_key = get_key()

igdb = igdb(api_key)




def generate_search_list(game_name):

    result = igdb.games({'search': game_name,
                         'limit': 5})

    return result


def single_search(game_name):

    info = []
    result = igdb.games({'search': game_name,
                         'fields': ["name", "summary", "storyline", "rating",
                                    "time_to_beat", "genres"],
                         'expand': ['developers']})

    for field in result.body:
        info.append(field)

    return result


# todo: create query methods for searching keywords
# todo: create query methods for grabbing related info fields


# i = input('Enter Game name: ')
#
# r = single_search(i)
#
#
# for n in r.body:
#     info = {}
#     if n['name'] == i:
#         info.update(n)
#         for val in info.values():
#             print(val)



