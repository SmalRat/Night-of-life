import game

kitchen = game.Room("Kitchen")
kitchen.set_description("A dank and dirty room buzzing with flies.")

dining_hall = game.Room("Dining Hall")
dining_hall.set_description("A large room with ornate golden decorations on each wall.")

ballroom = game.Room("Ballroom")
ballroom.set_description("A vast room with a shiny wooden floor. Huge candlesticks guard the entrance.")

kitchen.link_room(dining_hall, "south")
dining_hall.link_room(kitchen, "north")
dining_hall.link_room(ballroom, "west")
ballroom.link_room(dining_hall, "east")

dave = game.Enemy("Dave", "A smelly zombie", "ddd")
dave.set_conversation("What's up, dude! I'm hungry.")
dave.set_weakness("cheese")
dining_hall.set_characters([dave])

tabitha = game.Enemy("Tabitha", "An enormous spider with countless eyes and furry legs.", "fff")
tabitha.set_conversation("Sssss....I'm so bored...")
tabitha.set_weakness("book")
ballroom.set_characters([tabitha])

cheese = game.Item("cheese")
cheese.set_description("A large and smelly block of cheese")
ballroom.set_item(cheese)

book = game.Item("book")
book.set_description("A really good book entitled 'Knitting for dummies'")
dining_hall.set_item(book)

current_room = kitchen
backpack = []

game_cycle = game.GameCycle(current_room, backpack)

while True:
    try:
        game_cycle.cycle()
    except game.GameEnd:
        break



