"""Module with game classes"""


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
        self.character = None
        self.items = None

    def link_room(self, room, direction):
        """Links neighbour room to the current one and vice versa"""
        self.neighbours[direction] = room
        room.neighbours[Room.pairs[direction]] = self

    def set_character(self, character):
        """Sets character to the current room"""
        self.character = character

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

    def get_character(self):
        """Gets the character of the current room"""
        if self.character:
            return self.character

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


class Enemy:
    """Enemy object model"""
    defeated = 0

    def __init__(self, name, description):
        """Initialisation method"""
        self.name = name
        self.description = description
        self.replica = "No replica yet."
        self.weaknesses = ()

    def set_conversation(self, replica):
        """Sets replica to the character"""
        self.replica = replica

    def set_weakness(self, *weaknesses):
        """Sets weaknesses to the character"""
        self.weaknesses = tuple(weaknesses)

    def describe(self):
        """Returns the description of the character"""
        print("You see {} here. ".format(self.name) + self.description + "." + "\n")

    def talk(self):
        """Returns the replica of the character"""
        print(self.replica)

    def fight(self, weapon):
        """Checks, whether enemy is vulnerable to the given weapon"""
        if weapon in self.weaknesses:
            Enemy.defeated += 1
            return True
        return False

    def get_defeated(self):
        """Returns the value of slaughtered enemies"""
        return Enemy.defeated


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
