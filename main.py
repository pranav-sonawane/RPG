from classes.game import Person, bcolors
from classes.magic import Spell
from  classes.inventory import Item
import  random


#Create Black Magic
fire = Spell("Fire", 25, 300, "black")
thunder = Spell("thunder", 25, 300, "black")
blizzard= Spell("blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 25, 620,"White")
cura = Spell("Cura", 32, 1500, "White")

# Create some Items
potion = Item("potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", " Deals 500 damage", 500)

player_spells =  [fire, thunder, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item" : hipotion, "quantity" : 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

#Instatiate People
player1 = Person("Valos:", 3260, 102, 220, 34, player_spells, player_items)
player2 = Person("Nick :", 4160, 118, 311, 34, player_spells, player_items)
player3 = Person("Robot:", 3089, 134, 208, 34, player_spells, player_items)

enemy = Person("Magus:", 1800, 701, 525, 25, [], [])

players = [player1, player2, player3]

running  = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS !" + bcolors.ENDC)

while running:
    print("=====================")

    print("\n\n")
    print("NAME                   HP                                 MP")
    for player in players:
        player.get_stats()

    print("\n")

    enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("    Choose Action: ")
        index = int(choice) - 1
      #  print("You Chose : ", player.get_spell_name(int()))

        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print("You attacked for", dmg, "points of damage.")
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose Magic: ")) - 1

            if magic_choice == -1:
                continue

            '''magic_dmg = player.generate_spell_damage(magic_choice)
            spell = player.get_spell_name(magic_choice)
            cost = player.get_spell_mp_cost(magic_choice)'''

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\ Not enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "White":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals for ", str(magic_dmg), "HP." +bcolors.ENDC)
            elif spell.type == "black":
             enemy.take_damage(magic_dmg)
             print(bcolors.OKBLUE + "\n" + spell.name + "deals", str(magic_dmg), "points of damage" + bcolors.ENDC)
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items [item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + "heals for", str(item.prop), "HP", bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " Fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage" + bcolors.ENDC)


    enemy_choice = 1
    target =  random.randrange(0,2)
    enemy_dmg = enemy.generate_damage()

    players[target].take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg)

    print("--------------------------")
    print("Enemy HP : ", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC)


    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "YOu WIN !" + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print((bcolors.FAIL + " Enemy defeated you !" + bcolors.ENDC))
        running = False