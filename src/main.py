import os
import sys
import json
import random
import time
from Weapon import Weapon
from Player import Player


welcome_text = """
Hi, welcome to rps101.
Possible moves:
"""
welcome_text_cont = """

You can also type "random" for a random move or "exit" to exit the game.
"""


def clear_screen():

    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux (here, os.name is 'posix')
    else:
        _ = os.system('clear')

    return


def get_application_path():
    """Gets the path of the python file"""
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return application_path


def load_json_file():
    """loads the json file"""

    application_path = get_application_path()

    path = os.path.join(application_path, "rps101_data.json")
    with open(path) as f:
        json_load = json.load(f)
    return json_load


def get_weapon_objects(json_load):
    """creates weapon objects by iterating over the json load
    and making an object of each dictionary
    """
    weapon_object_list = []
    for weapon_dict in json_load:
        weapon = Weapon(**weapon_dict)
        weapon_object_list.append(weapon)
    return weapon_object_list


def display_available_weapons(weapon_object_list):
    """Prints a list of weapons, 10 per line, seperated by a |"""
    weapons_on_line = 0
    for weapon in weapon_object_list:
        if weapons_on_line < 10:
            print(weapon.title, end=" | ")
            weapons_on_line += 1
        else:
            print(weapon.title)
            weapons_on_line = 0


def get_player_weapon(weapon_object_list, player):
    """Gets input from the user and matches that input to a weapon object,
    also handles exiting the program
    """

    player_input = input(f"Player {player.number}'s move >> ").lower()

    if player_input == "exit":
        print("Bye!")
        time.sleep(0.5)
        raise SystemExit("Exiting...")

    elif player_input == "random":
        player.weapon = random.choice(weapon_object_list)

    else:
        for weapon in weapon_object_list:
            if weapon.title == player_input:
                player.weapon = weapon
    return


def get_winner(player_one, player_two):
    """Searches through each player's weapon's comparison dictionary to match
    the other players weapon id to their weapon id, then prints the comparison.
    Also updates player scores, clears player weapons and returns the winning
    player.
    """

    if player_one.weapon is None or player_two.weapon is None:
        return None

    winner = None

    for comparison in player_one.weapon.compares:
        if int(comparison["other_gesture_id"]) == player_two.weapon.id:
            print(player_one.weapon.title, comparison["verb"][0],
                  player_two.weapon.title)
            player_one.wins += 1
            winner = player_one

    for comparison in player_two.weapon.compares:
        if int(comparison["other_gesture_id"]) == player_one.weapon.id:
            print(player_two.weapon.title, comparison["verb"][0],
                  player_one.weapon.title)
            player_two.wins += 1
            winner = player_two

    if player_one.weapon == player_two.weapon:
        print("It's a tie! The scores stay the same.")
        return None

    player_one.weapon = None
    player_two.weapon = None

    return winner


def game_loop(weapon_object_list, player_one, player_two):
    """Gets new weapons for each player, prints the winner and the scores then
    loops again
    """
    print()
    print()

    get_player_weapon(weapon_object_list, player_one)
    get_player_weapon(weapon_object_list, player_two)
    print()

    winner = get_winner(player_one, player_two)
    if winner is not None:
        print(f"Player {winner.number} wins!")
    else:
        print("Someone entered an invalid input, the scores stay the same")
    print()

    print("Player 1's score:", player_one.wins)
    print("Player 2's score:", player_two.wins)
    print()

    input("-- Press enter to play again --")
    clear_screen()

    print("Possible moves:")
    print()
    display_available_weapons(weapon_object_list)

    return


if __name__ == "__main__":
    json_load = load_json_file()
    weapon_object_list = get_weapon_objects(json_load)
    print(welcome_text)
    display_available_weapons(weapon_object_list)
    print(welcome_text_cont)
    p1 = Player(1)
    p2 = Player(2)
    while True:
        game_loop(weapon_object_list, p1, p2)
