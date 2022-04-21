"""Module with game classes"""


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
                self.items = tuple(items)
                return
        self.items = None

    def get_details(self):
        """Gets details of the current room"""
        print("You're currently at: " + str(self.name) + ". " + self.description + "\n")
        print("Adjoining rooms: " + ", ".join(("{}: {}".format(key, self.neighbours[key].name)
                                               if self.neighbours[key]
                                               else "{}: No room".format(key)
                                               for key in self.neighbours)) + "\n")

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


class GameCycle:
    """Class with functions usable for game cycle"""
    def __init__(self, current_room, backpack):
        self.current_room = current_room
        self.backpack = backpack

    def get_answer(self):
        raw_answer = input("> ")
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

    def cycle(self):

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
