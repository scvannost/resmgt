from resmgt.db import Building, Database, load_dotenv_config, User, Villager
from resmgt.game import Game
from resmgt.sprite import RectangleSprite


db = Database()
db.connect(**load_dotenv_config(), create_db_if_not_exist=True)
db.create_all_tables()

try:
    db.open_session()
    u = User(name="scvannost", email="scvannost@gmail.com")
    db.add(u)

    b1, b2 = Building(), Building()
    v1, v2 = Villager(), Villager()
    db.add_all([b1, b2, v1, v2])

    v1.work_id = b1.id
    v2.house_id = b1.id
    v2.work_id = b2.id
    db.merge(v1)
except Exception as e:
    print(e.__traceback__)
    print(e)
else:
    print(b1)
    print()
    print("workers:")
    for w in b1.workers:
        print(w)
    print()
    print("residents:")
    for r in b1.residents:
        print(r)
finally:
    db.drop_all_tables()
    db.drop_database(**load_dotenv_config())
    db.disconnect()

# set up and run a default game
# by default, __init__() calls start() and run() calls quit()
Game(other_sprites=[RectangleSprite()]).run()
