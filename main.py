from bitcoinrequest import BitcoinRequest
import os
import random

GRID = [1, 2, 3, 4]

def draw_grid(prize_index, choice=None, show_prize=False):
    icon = "⬜️"
    prize_icon = "🟩"
    your_choice_icon = "🟨"

    map = ""

    if choice:
        choice = int(choice)

    for position in GRID:
        if show_prize and prize_index == position:
            map += "{} ".format(prize_icon)
            continue
        if choice == position:
            map += "{} ".format(your_choice_icon)
        else:
            map += "⬜️ "

    print("\n\n", map, "\n\n")

def move_player(player, move):
    x, y = player
    if move == "LEFT":
        x -= 1
    if move == "RIGHT":
        x += 1
    if move == "UP":
        y -= 1
    if move == "DOWN":
        y += 1
    return x, y

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_prize():
    return round(random.random() * 3) + 1, round(random.random() * 10, 7)

def game_loop():
    playing = True
    prize_index, amount = generate_prize()
    br = BitcoinRequest()

    host = {
        'label': "accountA",
        'address': "2MuAp5bLbAcZFhCPoCdV4EgpRZjo2AfFfwZ"
    }
    player = {
        'label': "accountB",
        'address': "2Mzg5iVVCP32UHxusjdQxetu2C3XS64f34e"
    }
    player['address'] = "2Mzg5iVVCP32UHxusjdQxetu2C3XS64f34e"
    balance = 0
    balance = br.post('getbalance', ["accountB"])['result']
    choices = ['1', '2', '3', '4']
    choice = None
    playing_status = 'selecting'

    while playing:
        clear_screen()
        print("Welcome to the Monty Hall!\n---")
        print("You need to point out which card do you think the prize hidden at.")
        print("Your wallet address is: {}".format(player['address']))
        print("This is your balance: ${}".format(balance))
        print("This is current random amount: ${}".format(amount))
        draw_grid(prize_index, choice, playing_status == 'confirmed')
        print("You can choose {}".format(", ".join(choices)))
        print("status {}".format(playing_status))
        print("Enter QUIT to quit")

        if playing_status == 'selecting':
            choice = input(">  ").upper()

        if choice == 'QUIT':
            clear_screen()
            print("See you next time!")
            break

        if choice in choices:

            if playing_status == 'selecting':
                playing_status = 'selected'
                continue

            if playing_status == 'selected':
                print("Your choice is: {}".format(choice))
                confirm = input("Do you confirm? (y/n)").lower()
                txid = None
                if confirm != "y":
                    game_loop()
                playing_status = 'confirmed'
                continue

            if playing_status == 'confirmed':
                print("Prize index is: {}".format(prize_index))
                print("---")
                if int(choice) == prize_index:
                    print("You Win!!")
                    txid = br.post('sendfrom', [host['label'], player['address'], amount])['result']
                if int(choice) != prize_index:
                    print("You Lose!!")
                    txid = br.post('sendfrom', [player['label'], host['address'], amount])['result']
                br.post('generate', [1])
                balance = br.post('getbalance', [player['label']])['result']
                print("Txid: {}".format(txid))
                print("This is your new balance: ${}".format(balance))
                playing = False

        else:
            input("Invalid input... press return to try again")

    else:
        play_again = input("Do you want to play again? (y/n)").lower()
        if play_again != "n":
            game_loop()

game_loop()