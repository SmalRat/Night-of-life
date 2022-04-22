import game
import time

game_length_dictionary = {1: 180, 2: 360, 3: 540}
game_rooms_amount_dictionary = {1: 2, 2: 4, 3: 5}

fixed_items = [game.Rod, game.DuctTape, game.Screwdriver, game.Paper,
               game.Glue, game.FilamentABS, game.FilamentPLA, game.FilamentPETG]
not_fixed_items = [game.Nozzle, game.Extruder, game.Belt]

rooms_list = []
printers_list = []
current_room = None

backpack = []


def print_decorator():
    func = print
    def new_print(text):
        func(text)
        time.sleep(0.1)
    return new_print


print = print_decorator()


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

    game_generator = game.GameGenerator(game_rooms_amount_dictionary[game_length],
                                        fixed_items,
                                        not_fixed_items,
                                        game_length)
    game_cycle = game.GameCycle(game_generator.current_room,
                                game_generator.rooms,
                                game_generator.printers,
                                [])
    print("-" * 100)
    for room in game_generator.rooms:
        for printer in room.get_characters():
            print(printer.work)
    while game_cycle.time < game_length_dictionary[game_length]:
        try:
            game_cycle.action_menu()
        except game.GameEnd:
            break
