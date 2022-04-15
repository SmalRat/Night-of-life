"""Module with game classes"""


class SetDescrMixin:
    def set_description(self, description):
        self.description = description


class Room(SetDescrMixin):
    pairs = {"north": "south", "west": "east", "south": "north", "east": "west"}

    def __init__(self, name):
        self.name = name
        self.description = "No description yet."
        self.neighbours = {"north": None, "west": None, "south": None, "east": None}
        self.character = None
        self.items = None

    def link_room(self, room, direction):
        self.neighbours[direction] = room
        room.neighbours[Room.pairs[direction]] = self

    def set_character(self, character):
        self.character = character

    def set_item(self, *items):
        for item in items:
            if item:
                self.items = tuple(items)
                return
        self.items = None

    def get_details(self):
        print("You're currently at: " + str(self.name) + ". " + self.description + "\n")
        print("Adjoining rooms: " + ", ".join(("{}: {}".format(key, self.neighbours[key].name)
                                               if self.neighbours[key]
                                               else "{}: No room".format(key)
                                               for key in self.neighbours)) + "\n")

    def get_character(self):
        if self.character:
            return self.character

    def get_items(self):
        return self.items

    def move(self, direction):
        if self.neighbours[direction]:
            return self.neighbours[direction]
        else:
            print("There is no room in that direction!")
            return self


class Enemy:
    defeated = 0

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.replica = "No replica yet."
        self.weaknesses = ()

    def set_conversation(self, replica):
        self.replica = replica

    def set_weakness(self, *weaknesses):
        self.weaknesses = tuple(weaknesses)

    def describe(self):
        print("You see {} here. ".format(self.name) + self.description + "." + "\n")

    def talk(self):
        print(self.replica)

    def fight(self, weapon):
        if weapon in self.weaknesses:
            Enemy.defeated += 1
            return True
        return False

    def get_defeated(self):
        return Enemy.defeated


class Item(SetDescrMixin):
    def __init__(self, name):
        self.name = name
        self.description = "No description yet."

    def describe(self):
        print(self.name + ": " + self.description + ".")

    def get_name(self):
        return self.name
