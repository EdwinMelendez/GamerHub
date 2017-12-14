import GameDatabaseApi
import Models

'''A few methods for testing different aspects of project'''


'''how to use generate search list'''

i = input('Enter Game name: ')

r = GameDatabaseApi.generate_search_list(i)

for n in r.body:
     print(n['name'])


'''how to use single search'''


i = input('Enter Game name: ')

r = GameDatabaseApi.single_search(i)
for n in r.body:
    info = {}
    if n['name'] == i:
        info.update(n)
        for val in info.values():
            print(val)

i = input('enter game system name: ')

r = GameDatabaseApi.get_platform_games(i)

print(r.items())


'''testing database'''

new_user = Models.User("tastybob", "password123", "tastybob@aol.com")
Models.db.add(new_user)
Models.db.commit()

