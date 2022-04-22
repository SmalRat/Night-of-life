import game
import time

tool_types = [game.Rod, game.DuctTape]

game_length_dictionary = {1: 180, 2: 360, 3: 540}
game_rooms_amount_dictionary = {1: 2, 2: 4, 3: 5}

fixed_items = []
not_fixed_items = []

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
                                        tool_types,
                                        game_length)
    game_cycle = game.GameCycle(game_generator.current_room,
                                game_generator.rooms,
                                game_generator.printers,
                                [])

    while game_cycle.time < game_length_dictionary[game_length]:
        try:
            game_cycle.action_menu()
        except game.GameEnd:
            break
