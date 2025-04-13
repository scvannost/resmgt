from resmgt.db.database import Building, User, Villager, load_dotenv_config
from resmgt.game import Game
from resmgt.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from resmgt.sprite import RectangleSprite, VillagerIconSprite

player = VillagerIconSprite(location=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
game = Game(player_sprite=player, other_sprites=[RectangleSprite()])

try:
    game.db.open_session()
    u = User(name="scvannost", email="scvannost@gmail.com")
    game.db.add(u)

    b1, b2 = Building(), Building()
    v1, v2 = game.db.session.get(Villager, 1), Villager()
    game.db.add_all([b1, b2, v2])

    v1.work_id = b1.id
    v2.house_id = b1.id
    v2.work_id = b2.id
    game.db.merge(v1)

    # set up and run a default game
    # by default, __init__() calls start() and run() calls quit()
    game.run()
    print(game.player.location, (v1.x, v1.y))
except Exception as e:
    game.db.session.rollback()
    print(e.with_traceback(e.__traceback__))
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
    game.db.drop_all_tables()
    game.db.drop_database(**load_dotenv_config())
    game.db.disconnect()
