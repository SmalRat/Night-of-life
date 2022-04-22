import game

rod = game.Rod()
duct_tape = game.DuctTape()
tool_types = [game.Rod, game.DuctTape]
tools_amount_num = 2

fixed_items = []
not_fixed_items = []

rooms_list = []
printers_list = []
current_room = None

backpack = []

#game_cycle = game.GameCycle(current_room, rooms_list, printers_list, backpack)

"""while True:
    try:
        game_cycle.cycle()
    except game.GameEnd:
        break"""

if __name__ == "__main__":
    print("Вітаю тебе у грі 'Нічна зміна'!")
    while True:
        try:
            print("Обери, наскільки довго буде тривати твоя гра:")
            print(" Швидка гра - 1 \n Нормальна протяжність - 2 \n Довга гра - 3")
            game_length = int(input(">> "))
            if game_length in (1, 2, 3):
                break
            else:
                raise TypeError
        except (TypeError, ValueError):
            print("Введи коректну відповідь!")
        except Exception as e:
            # should never work
            print(e)

    game_length_dictionary = {1: 180, 2: 360, 3: 540}
    game_rooms_amount_dictionary = {1: 2, 2: 4, 3: 5}
    game_generator = game.GameGenerator(game_rooms_amount_dictionary[game_length],
                                        tool_types, tools_amount_num, game_length)
    game_generator.generate_tools()
    for i in game_generator.rooms:
        i.get_details()
        print(i.get_items())

