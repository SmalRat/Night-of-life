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
    temper_names = {1: "Капризний", 2: "Жорстокий", 3: "Впертий", 4: "Мазохіст", 5: "Файний"}
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
    works = {1: (20, 3, "малі"),
             2: (55, 6, "малі"),
             3: (100, 12, "малі"),
             4: (190, 24, "малі"),
             5: (30, 1, "середні"),
             6: (55, 2, "середні"),
             7: (100, 4, "середні"),
             8: (195, 8, "середні"),
             9: (60, 1, "великі"),
             10: (110, 2, "великі"),
             11: (200, 4, "великі"),
             12: (380, 8, "великі")}
    work_statuses = {1: "Порожній",
                     2: "Всередині незавершена(зіпсута) робота",
                     3: "Працює",
                     4: "Всередині завершена робота"}

    def __init__(self, name):
        """Initialisation function"""
        self.name = name
        self.description = "Принтер"
        self.parts = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}
        for key in self.parts:
            self.parts[key] -= random.random()/2
        self.filament = 1 - random.random()/2
        self.temper = 1
        self.define_temper()
        self.set_conversation("Цей принтер " + Printer.temper_names[self.temper]
                              + " - " + Printer.temper_descriptions[self.temper] + ".")
        self.work_progress = 0
        self.status = 1
        self.work = random.choice([*Printer.works, 0])
        if self.work > 0:
            self.status = random.choice([3,4])
            if self.status == 3:
                self.work_progress = int(random.random()*Printer.works[self.work][0])
            else:
                self.work_progress = Printer.works[self.work][0]

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
        result = Printer.works[self.work]
        self.work = 0
        self.status = 1
        self.work_progress = 0
        return result

    def cycle_work_effects(self):
        """Implements time effect on printers work"""
        if self.status == 3:
            for part in Printer.temper_work_completion_effects[self.temper]:
                self.parts[part] -= Printer.temper_work_completion_effects[self.temper][part]*random.random()/100
            self.work_progress += 1
            if self.work_progress >= Printer.works[self.work][0]:
                self.status = 4
            else:
                for part in self.parts:
                    if self.parts[part] <= 0:
                        self.status = 2
                        self.work_progress = 0

    def interact(self, game_object):
        """Adds ability to interact with printers"""
        answer_map = {1: self.info, 2: self.retrieve, 3: self.start, 4: self.repair}
        while True:
            try:
                print("Як ви хочете взаємодіяти із принтером? \n \
1 - Стан принтера \n 2 - Вийняти виріб \n 3 - Запустити новий друк \n 4 - Ремонтувати \n 5 - Облишити принтер")
                answer = int(input(">> "))
                if answer in (1,2,3,4):
                    answer_map[answer](game_object)
                elif answer == 5:
                    break
                else:
                    raise TypeError
            except (ValueError, TypeError):
                print("Введіть прийнятну відповідь!")

    def parts_status(self):
        information = "\n\n Стан деталей: \n"
        for part in self.parts:
            information += Printer.parts_names[part] + ": "
            if self.parts[part] > 0.9:
                information += "дуже добрий \n"
            elif self.parts[part] > 0.65:
                information += "добрий \n"
            elif self.parts[part] > 0.4:
                information += "задовільний \n"
            elif self.parts[part] > 0.25:
                information += "незадовільний \n"
            elif self.parts[part] > 0.15:
                information += "поганий \n"
            elif self.parts[part] > 0:
                information += "дуже поганий \n"
            else:
                information += "зламаний \n"
        return information

    def info(self, game_object):
        """Grants info about printer"""
        information = "Принтер " + self.name + ". " + self.temper_names[self.temper]\
                      + " - " + self.temper_descriptions[self.temper] + ". \n"
        if self.status == 1:
            information += Printer.work_statuses[self.status] + "."
        else:
            information += Printer.work_statuses[self.status] + " - " + str(Printer.works[self.work][2])\
                           + " деталі " + str(Printer.works[self.work][1]) + " штук. "
            information += "Залишилось часу: " + str(Printer.works[self.work][0] - self.work_progress)
        information += self.parts_status()
        print(information)

    def retrieve(self, game_object):
        """Implements the possibility to retrieve works from printers"""
        if self.status == 4:
            print("Ви вийняли виріб : " + str(Printer.works[self.work][2])\
                           + " деталі " + str(Printer.works[self.work][1]) + " штук. ")
            work = self.work_completion()
            game_object.results[work[2]] += work[1]
            game_object.wait([None, 5])
        elif self.status == 3:
            print("Принтер все ще працює, ви не можете дістати виріб! \
Хочете завершити роботу і дістати неготову деталь? Так/Ні")
            answer = input(">> ")
            if answer in ("Так", "так"):
                self.work_completion()
                print("Ви витягли неготові деталі із принтера.")
                game_object.wait([None, 5])
        elif self.status == 2:
            self.work_completion()
            print("Ви витягли неготові деталі із принтера.")
            game_object.wait([None, 5])
        elif self.status == 1:
            print("Принтер порожній!")

    def start(self, game_object):
        """Implements the possibility to start works on printers"""
        for part in self.parts:
            if self.parts[part] <= 0:
                print("Принтер зламаний!")
                return
        if self.status != 1:
            print("Принтер не порожній, потрібно спершу вийняти деталі!")
            return
        print("Виберіть, яку роботу ви хочете тут запустити: ")
        for work in Printer.works:
            print(" " + str(work) + " - " + Printer.works[work][2] + " - " + str(Printer.works[work][1]) + " штук.")
        try:
            answer = int(input(">> "))
            if answer in range(1, 13):
                self.work = answer
                self.work_progress = 0
                self.status = 3
                game_object.wait([None, 5])
            else:
                raise TypeError
        except (ValueError, TypeError):
            print("Введіть прийнятну відповідь!")

    def repair(self, game_object, ):
        if self.status in (2, 4):
            print("Принтер непорожній, спочатку вийміть з нього вироби!")
            return
        if self.status == 3:
            print("Принтер працює, ви не можете ремонтувати його зараз!")
            return
        if self.status == 1:
            print(self.parts_status())
            while True:
                print("Чим ви бажаєте ремонтувати принтер?")
                for count, item in enumerate(game_object.backpack):
                    print(" " + str(count) + " - " + item.name)
                try:
                    answer = int(input(">> "))
                    if answer in range(1, len(game_object.backpack)+1):
                        pass
                        #game_object.wait([None, 5])
                    else:
                        raise TypeError
                except (ValueError, TypeError):
                    print("Введіть прийнятну відповідь!")



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


class Rod(Item):
    """Rod object model"""
    generation_amount = 0.75

    def __init__(self):
        """Initialisation function"""
        super().__init__("Стержень")
        self.description = "Використовується для чищення забитого екструдеру"
        self.usage_time = 5


class Screwdriver(Item):
    """Screwdriver object model"""
    generation_amount = 0.50

    def __init__(self):
        """Initialisation function"""
        super().__init__("Викрутка")
        self.description = "Використовується для заміни ременя або ремонту системи подачі пластику"
        self.usage_time = 10


class Nozzle(Item):
    """Nozzle object model"""
    generation_amount = 0.30

    def __init__(self):
        """Initialisation function"""
        super().__init__("Сопло")
        self.description = "Нове сопло"
        self.usage_time = 10


class Extruder(Item):
    """Extruder object model"""
    generation_amount = 0.20

    def __init__(self):
        """Initialisation function"""
        super().__init__("Екструдер")
        self.description = "Справний екструдер"
        self.usage_time = 4


class Belt(Item):
    """Belt object model"""
    generation_amount = 0.20

    def __init__(self):
        """Initialisation function"""
        super().__init__("Ремінь")
        self.description = "Справний привідний ремінь"
        self.usage_time = 10


class ConsumableMixin:
    def describe(self):
        """Returns the description of the item"""
        print(self.name + ": " + self.description + ". " + "Стан: " + str(self.amount*100) + "%.")


class DuctTape(Item, ConsumableMixin):
    """Duct_tape object model"""
    generation_amount = 1.5

    def __init__(self):
        """Initialisation function"""
        super().__init__("Скотч")
        self.amount = 1
        self.description = "Використовується для відновлення цілісності покриття платформи"
        self.usage_time = 4


class Paper(Item, ConsumableMixin):
    """Paper object model"""
    generation_amount = 1

    def __init__(self):
        """Initialisation function"""
        super().__init__("Папір А4")
        self.amount = 1
        self.description = "Використовується для калібровки"
        self.usage_time = 7


class Glue(Item, ConsumableMixin):
    """Glue object model"""
    generation_amount = 1

    def __init__(self):
        """Initialisation function"""
        super().__init__("Клей")
        self.amount = 1
        self.description = "Використовується для ремонту системи подачі пластику"
        self.usage_time = 10


class FilamentABS(Item, ConsumableMixin):
    """ABS filament object model"""
    generation_amount = 2

    def __init__(self):
        """Initialisation function"""
        super().__init__("Котушка ABS")
        self.amount = 1
        self.description = "Використовується для заміни пластику ABS"
        self.usage_time = 5


class FilamentPLA(Item, ConsumableMixin):
    """PLA filament object model"""
    generation_amount = 3

    def __init__(self):
        """Initialisation function"""
        super().__init__("Котушка PLA")
        self.amount = 1
        self.description = "Використовується для заміни пластику PLA"
        self.usage_time = 5


class FilamentPETG(Item, ConsumableMixin):
    """PETG filament object model"""
    generation_amount = 1

    def __init__(self):
        """Initialisation function"""
        super().__init__("Котушка PETG")
        self.amount = 1
        self.description = "Використовується для заміни пластику PETG"
        self.usage_time = 5


class GameGenerator:
    """Game generator - generates rooms, items in rooms and characters"""
    def __init__(self, rooms_num, necessary_tool_types, optional_tool_types, game_length):
        """Initialisation function"""
        self.rooms_num = rooms_num
        self.necessary_tool_types = necessary_tool_types
        self.game_length = game_length
        self.optional_tool_types = optional_tool_types

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
        for tool_type in self.necessary_tool_types:
            for counter in range(max(1, int(tool_type.generation_amount*self.game_length))):
                tools.append(tool_type())
        for tool_type in self.optional_tool_types:
            random_value = random.random()
            if random_value < tool_type.generation_amount*self.game_length:
                for counter in range(max(1, int(tool_type.generation_amount*self.game_length))):
                    tools.append(tool_type())
        for tool in tools:
            random.choice(self.rooms).add_item(tool)


class GameCycle:
    """Class with functions usable for game cycle"""
    def __init__(self, current_room, rooms_list, printers_list, backpack, game_length):
        """Initialisation function"""
        self.current_room = current_room
        self.backpack = backpack
        self.rooms_list = rooms_list
        self.printers_list = printers_list
        self.game_length = game_length
        self.time = 0
        self.results = {"великі": 0, "середні": 0, "малі": 0}

    def get_answer(self):
        """Gets an answer from the player"""
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
        """Adds ability to move from one room to another"""
        self.current_room = self.current_room.move(direction)

    def talk(self, answer):
        """Adds ability to talk with characters"""
        if len(answer) == 1:
            if len(self.current_room.get_characters()) == 1:
                self.current_room.get_characters()[0].interact(self)
            elif len(self.current_room.get_characters()) == 0:
                print("Тут немає персонажів!")
            else:
                print("Оберіть конкретного персонажа, з яким будете говорити: talk <персонаж>")
        elif len(answer) == 2:
            for character in self.current_room.get_characters():
                if answer[1] == character.name:
                    character.interact(self)
                    return
            print("Тут немає такого персонажа!")
        else:
            print("Неправильний формат відповіді!")

    def fight(self, answer):
        """Implements 'fight'"""
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
        """Implements ability to take items"""
        items = self.current_room.get_items()
        if items is not None:
            for item in items:
                print("Ви поклали " + item.get_name() + " в сумку.")
                self.backpack.append(item.get_name())
            self.current_room.set_item(None)
        else:
            print("Тут немає ніяких предметів!")

    def wait(self, answer):
        """Allows to wait for some time"""
        try:
            time = int(answer[1])
            self.cycle(time)

        except (TypeError, ValueError):
            print("Введіть коректне значення (час у хвилинах, ціле значення).")
        except IndexError:
            print("Введіть час у хвилинах, протягом якого чекати.")

    def action_menu(self):
        """Implements action choice menu"""
        print("\n")
        print("Пройшло: " + str(self.time) + "хвилин.")
        print("До кінця зміни залишилося " + str(self.game_length - self.time) + " хвилин.")
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
        """Implements time and changes it brings in the game"""
        for time_count in range(time):
            if self.time >= self.game_length:
                raise GameEnd
            for room in self.rooms_list:
                for printer in room.get_characters():
                    printer.cycle_work_effects()
            self.time += 1
