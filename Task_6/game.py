"""Module with game classes"""
import random


class FriendlyFire(Exception):
    pass


class GameEnd(Exception):
    pass


class SetDescrMixin:
    """Mixin class with set_description method"""
    def set_description(self, description):
        self.description = description


class Room(SetDescrMixin):
    """Room object model"""
    pairs = {"north": "south", "west": "east", "south": "north", "east": "west"}

    def __init__(self, name):
        """Initialisation function"""
        self.name = name
        self.description = "No description yet."
        self.neighbours = {"north": None, "west": None, "south": None, "east": None}
        self.characters = None
        self.items = None

    def link_room(self, room, direction):
        """Links neighbour room to the current one and vice versa"""
        self.neighbours[direction] = room
        room.neighbours[Room.pairs[direction]] = self

    def set_characters(self, characters):
        """Sets characters to the current room"""
        self.characters = characters

    def set_item(self, *items):
        """Sets items to the current room"""
        for item in items:
            if item:
                self.items = list(items)
                return
        self.items = None

    def add_item(self, items):
        if self.items:
            try:
                check_iterator = iter(items)
                for item in items:
                    self.items.append(item)
            except TypeError:
                self.items.append(items)
        else:
            try:
                self.items = list(items)
            except TypeError:
                self.items = [items]

    def get_details(self):
        """Gets details of the current room"""
        print("-" * 100)
        print("You're currently at: " + str(self.name) + ". " + self.description + "\n")
        print("Adjoining rooms: " + ", ".join(("{}: {}".format(key, self.neighbours[key].name)
                                               if self.neighbours[key]
                                               else "{}: No room".format(key)
                                               for key in self.neighbours)) + "\n")
        print("-"*100)

    def get_characters(self):
        """Gets the characters of the current room"""
        if self.characters:
            return self.characters

    def get_items(self):
        """Gets items of the current room"""
        return self.items

    def move(self, direction):
        """Returns room in the given direction"""
        if self.neighbours[direction]:
            return self.neighbours[direction]
        else:
            print("There is no room in that direction!")
            return self


class Character:
    """Character object model"""
    def __init__(self, name, description):
        """Initialisation function"""
        self.name = name
        self.description = description
        self.replica = "No replica yet."

    def set_conversation(self, replica):
        """Sets replica to the character"""
        self.replica = replica

    def describe(self):
        """Returns the description of the character"""
        print("You see {} here. ".format(self.name) + self.description + "." + "\n")

    def talk(self):
        """Returns the replica of the character"""
        print(self.replica)


class Enemy(Character):
    """Enemy object model"""
    defeated = 0

    def __init__(self, name, description, death_phrase):
        """Initialisation method"""
        super().__init__(name, description)
        self.death_phrase = death_phrase
        self.weaknesses = ()

    def set_weakness(self, *weaknesses):
        """Sets weaknesses to the character"""
        self.weaknesses = tuple(weaknesses)

    def fight(self, weapon):
        """Checks, whether enemy is vulnerable to the given weapon"""
        if weapon in self.weaknesses:
            Enemy.defeated += 1
            return True
        return False

    def get_defeated(self):
        """Returns the value of slaughtered enemies"""
        return Enemy.defeated


class Friend(Character):
    """Friend object model"""
    defeated = 0

    def __init__(self, name, description, fight_phrase):
        """Initialisation method"""
        super().__init__(name, description)
        self.fight_phrase = fight_phrase

    def fight(self, weapon):
        """Fight with a friend?"""
        print(self.fight_phrase)
        raise FriendlyFire("You hit a friend!")


class Printer(Enemy):
    parts_names = {1: "Поверхня",
                   2: "Калібрація",
                   3: "Екструдер",
                   4: "Сопло",
                   5: "Ремінь",
                   6: "Подача пластику"}
    temper_names = {1: "капризний", 2: "жорстокий", 3: "впертий", 4: "мазохіст", 5: "файний"}
    temper_descriptions = {1: "часто потребує перекалібровки",
                           2: "при знятті деталей завжди пошкоджує поверхню",
                           3: "постійно забивається",
                           4: "любить чинити собі шкоду",
                           5: "дуже добре працює(таке буває?)"}
    temper_work_completion_effects = {1: {1: 0.3, 2: 0.9, 3: 0.2, 4: 0.1, 5: 0.01, 6: 0.1},
                                      2: {1: 1, 2: 0.3, 3: 0.7, 4: 0.1, 5: 0.01, 6: 0.1},
                                      3: {1: 0.3, 2: 0.2, 3: 0.2, 4: 0.15, 5: 0.01, 6: 0.3},
                                      4: {1: 0.3, 2: 0.3, 3: 0.5, 4: 0.8, 5: 0.4, 6: 0.15},
                                      5: {1: 0.2, 2: 0.1, 3: 0.05, 4: 0.01, 5: 0.001, 6: 0.01}}

    def __init__(self, name):
        """Initialisation function"""
        self.name = name
        self.description = "Принтер"
        self.parts = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}
        for key in self.parts:
            self.parts[key] -= random.random()/2
        self.temper = 1
        self.define_temper()
        self.set_conversation("Цей принтер " + Printer.temper_names[self.temper]
                              + " - " + Printer.temper_descriptions[self.temper] + ".")

    def define_temper(self):
        """Defines temper(tendencies) of this printer"""
        random_value = 10 * random.random()
        if 0 <= random_value <= 2:
            self.temper = 1
        elif 2 < random_value <= 6:
            self.temper = 2
        elif 6 < random_value <= 8:
            self.temper = 3
        elif 8 < random_value <= 9:
            self.temper = 4
        elif 9 < random_value <= 10:
            self.temper = 5

    def work_completion(self):
        """Applies consequences of work completion"""
        for part in Printer.temper_work_completion_effects[self.temper]:
            self.parts[part] -= Printer.temper_work_completion_effects[self.temper][part]

    def cycle_work_effects(self):
        for part in Printer.temper_work_completion_effects[self.temper]:
            self.parts[part] -= Printer.temper_work_completion_effects[self.temper][part]*random.random()/100


class Item(SetDescrMixin):
    """Item object model"""
    def __init__(self, name):
        """Initialisation method"""
        self.name = name
        self.description = "No description yet."

    def describe(self):
        """Returns the description of the item"""
        print(self.name + ": " + self.description + ".")

    def get_name(self):
        """Returns the name of the item"""
        return self.name


class ConsumableMixin:
    def describe(self):
        """Returns the description of the item"""
        print(self.name + ": " + self.description + ". " + "Стан: " + str(self.amount*100) + "%.")


class Rod(Item):
    """Rod object model"""
    generation_amount = 1

    def __init__(self):
        """Initialisation function"""
        super().__init__("Стержень")
        self.description = "Використовується для чищення забитого екструдеру"


class DuctTape(Item, ConsumableMixin):
    """Duct_tape object model"""
    generation_amount = 2

    def __init__(self):
        """Initialisation function"""
        super().__init__("Скотч")
        self.amount = 1
        self.description = "Використовується для відновлення цілісності покриття платформи"


class Paper(Item, ConsumableMixin):
    """Paper object model"""
    generation_amount = 1

    def __init__(self):
        """Initialisation function"""
        super().__init__("Папір А4")
        self.amount = 1
        self.description = "Використовується для калібровки"


class GameGenerator:
    """Game generator - generates rooms, items in rooms and characters"""
    def __init__(self, rooms_num, tool_types, game_length):
        """Initialisation function"""
        self.rooms_num = rooms_num
        self.tool_types = tool_types
        self.game_length = game_length

        self.rooms = []
        self.printers = []

        self.generate_rooms()
        self.generate_tools()

        self.current_room = random.choice(self.rooms)

    def generate_rooms(self):
        """Randomly generates needed amount of rooms and links them in one tree"""
        rooms = []
        for i in range(self.rooms_num):
            while True:
                name = str(random.randint(1, 99)).zfill(3)
                if name not in rooms:
                    self.rooms.append(self.generate_room(name))
                    rooms.append(name)
                    break
                else:
                    pass
        main_room = random.choice(self.rooms)
        linked_rooms = [main_room]
        for room in self.rooms:
            if not room in linked_rooms:
                while True:
                    linking_room = random.choice(linked_rooms)
                    linking_side = random.choice(("west", "east", "north", "south"))
                    if not linking_room.neighbours[linking_side]:
                        room.link_room(linking_room, Room.pairs[linking_side])
                        linked_rooms.append(room)
                        break

    def generate_room(self, room_name):
        """Generates a room with a random amount of printers"""
        room = Room(room_name)
        printers = []
        printers_num = random.randint(2, 8)
        for i in range(printers_num):
            printers.append(self.generate_printer())
        room.set_characters(printers)
        return room

    def generate_printer(self):
        """Generates printer with a random name"""
        while True:
            name = str(random.randint(1, 99))
            if name not in [printer.name for printer in self.printers]:
                printer = Printer(name)
                return printer
            else:
                pass

    def generate_tools(self):
        """Generates tools and randomly puts them in rooms"""
        tools = []
        for tool_type in self.tool_types:
            for counter in range(tool_type.generation_amount*self.game_length):
                tools.append(tool_type())
        for tool in tools:
            random.choice(self.rooms).add_item(tool)


class GameCycle:
    """Class with functions usable for game cycle"""
    def __init__(self, current_room, rooms_list, printers_list, backpack):
        self.current_room = current_room
        self.backpack = backpack
        self.rooms_list = rooms_list
        self.printers_list = printers_list
        self.time = 0

    def get_answer(self):
        raw_answer = input(">> ")
        answer = raw_answer.split()
        if len(answer) > 0:
            if answer[0] in ("north", "south", "east", "west"):
                return self.move, answer[0]
            elif answer[0] == "talk":
                return self.talk, answer
            elif answer[0] == "fight":
                return self.fight, answer
            elif answer[0] == "take":
                return self.take, answer
            elif answer[0] == "wait":
                return self.wait, answer
            else:
                print("Я не знаю, що означає: " + raw_answer + ".")

        else:
            return None

    def move(self, direction):
        self.current_room = self.current_room.move(direction)

    def talk(self, answer):
        if len(answer) == 1:
            if len(self.current_room.get_characters()) == 1:
                self.current_room.get_characters()[0].talk()
            elif len(self.current_room.get_characters()) == 0:
                print("Тут немає персонажів!")
            else:
                print("Оберіть конкретного персонажа, з яким будете говорити: talk <персонаж>")
        elif len(answer) == 2:
            for character in self.current_room.get_characters():
                if answer[1] == character.name:
                    character.talk()
                    return
            print("Тут немає такого персонажа!")
        else:
            print("Неправильний формат відповіді!")

    def fight(self, answer):
        def fight_additional(inhabitant):
            print("Чим ви будете битися?")
            fight_with = input()

            # Do I have this item?
            if fight_with in self.backpack:
                try:
                    if inhabitant.fight(fight_with) == True:
                        # What happens if you win?
                        print(inhabitant.death_phrase)
                        self.current_room.characters.\
                            pop(self.current_room.characters.index(inhabitant))
                        if inhabitant.get_defeated() == 2:
                            print("Ура, ви перемогли!")
                            raise GameEnd("Перемога!")
                    else:
                        print("Ой лишенько, ви програли!")
                        print("Кінець гри")
                        raise GameEnd("Поразка!")
                except FriendlyFire:
                    pass
            else:
                print("Ви не маєте такого предмета: " + fight_with)
        if len(answer) == 1:
            if len(self.current_room.get_characters()) == 1:
                fight_additional(self.current_room.get_characters()[0])
            elif len(self.current_room.get_characters()) == 0:
                print("Тут немає персонажів!")
            else:
                print("Оберіть конкретного персонажа, з яким будете битись: talk <персонаж>")
        elif len(answer) == 2:
            for character in self.current_room.get_characters():
                if answer[1] == character.name:
                    fight_additional(character)
                    return
            print("Тут немає такого персонажа!")
        else:
            print("Неправильний формат відповіді!")

    def take(self, answer):
        items = self.current_room.get_items()
        if items is not None:
            for item in items:
                print("Ви поклали " + item.get_name() + " в сумку.")
                self.backpack.append(item.get_name())
            self.current_room.set_item(None)
        else:
            print("Тут немає ніяких предметів!")

    def wait(self, answer):
        try:
            time = int(answer[1])
            self.cycle(time)

        except (TypeError, ValueError):
            print("Введіть коректне значення (час у хвилинах, ціле значення).")
        except IndexError:
            print("Введіть час у хвилинах, протягом якого чекати.")

    def action_menu(self):

        print("\n")
        self.current_room.get_details()

        inhabitants = self.current_room.get_characters()
        if inhabitants is not None:
            print("Тут є такі персонажі: " + ", ".join((inhabitant.name for inhabitant in inhabitants)) + ".")
            for inhabitant in inhabitants:
                if inhabitant:
                    inhabitant.describe()

        items = self.current_room.get_items()
        if items is not None:
            print("Тут є такі предмети: " + ", ".join((item.name for item in items)) + ".")
            for item in items:
                if item:
                    item.describe()

        answer = self.get_answer()
        if answer:
            answer[0](answer[1])

    def cycle(self, time):
        for time_count in range(time):
            for room in self.rooms_list:
                for printer in room.get_characters():
                    printer.cycle_work_effects()
            self.time += 1
