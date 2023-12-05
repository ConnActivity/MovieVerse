import downloader
import insert
import time

all_actor_ids = set()
all_actors = []
all_people_popularity = []

START = 1
PAGES = 500

start_time = time.time()

for i in range(START, PAGES + 1):
    print(f"Page {i} of {PAGES} started")
    for actor in downloader.get_popular_people(i).results:
        all_actor_ids.add(actor.id)
        all_actors.insert(i, actor)
    print(f"Page {i} of {PAGES} finished")

end_time = time.time()
print(f"Iterating through pages took {end_time - start_time} seconds to complete")


start_time = time.time()
print("Downloading popularity details")
for i, actor_ids in enumerate(all_actor_ids):
    try:
        all_people_popularity.append(downloader.get_person_details(actor_ids))
    except Exception as e:
        print(f"Could not load actor with id {actor_ids}")
        print(e)
    if i % 25 == 0:
        print(f"{i} of {len(all_actor_ids)} loaded from API")

end_time = time.time()
print(f"Downloading details took {end_time - start_time} seconds to complete")


start_time = time.time()
print("Inserting actors into database")
for i, actor in enumerate(all_actors):
    try:
        insert.insert_person(actor)
    except Exception as e:
        print(f"Could not insert actor with id {actor.id}")
        print(e)
    if i % 25 == 0:
        print(f"{i} of {len(all_actors)} inserted into database")

end_time = time.time()
print(f"Inserting actors took {end_time - start_time} seconds to complete")


start_time = time.time()
print("Inserting popularity into database")
for i, popularity in enumerate(all_people_popularity):
    try:
        insert.insert_person_popularity(person_id=popularity.id, popularity=popularity.popularity)
    except Exception as e:
        print(f"Could not insert popularity with id {popularity.id}")
        print(e)
    if i % 25 == 0:
        print(f"{i} of {len(all_people_popularity)} inserted into database")

end_time = time.time()
print(f"Inserting popularity took {end_time - start_time} seconds to complete")