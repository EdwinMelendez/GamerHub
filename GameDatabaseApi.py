from igdb_api_python.igdb import igdb as igdb

def get_key():
    file = open("user-key", "r")
    key = file.readline()
    file.close()
    return key

api_key = get_key()

igdb = igdb(api_key)


# todo: create query methods for searching keywords
# todo: create query methods for grabbing related info fields


def get_game_by_name(game_name):

    r = igdb.games({'search': game_name})

    return r

i = input('Enter Game name: ')

r = get_game_by_name(i)

for game in r.body:
    print("Found: " + game["name"] + "\n")

