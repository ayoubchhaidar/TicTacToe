import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from pynput import keyboard
# connexion au bd cloud "firebase"


def open_data():
    # cle de bd cloud de 'firebase'
    cred = credentials.Certificate(
        "tic-tac-toe-89fbf-firebase-adminsdk-wlthj-c8636a7b06.json")
    firebase_admin.initialize_app(cred, {
        # lien de base de donnée
        'databaseURL': 'https://tic-tac-toe-89fbf-default-rtdb.europe-west1.firebasedatabase.app/'
    })  
        

open_data()



# round='game/test'
# ready = db.reference(round)
# print(ready.get())




def print_board(board):
    row1 = '|{}|{}|{}|'.format(board[0], board[1], board[2])
    row2 = '|{}|{}|{}|'.format(board[3], board[4], board[5])
    row3 = '|{}|{}|{}|'.format(board[6], board[7], board[8])
    print()
    print(row1)
    print(row2)
    print(row3)
    print()

# function to check if there's a winner


def check_winner(board, player):
    if (board[0] == player and board[1] == player and board[2] == player) or \
       (board[3] == player and board[4] == player and board[5] == player) or \
       (board[6] == player and board[7] == player and board[8] == player) or \
       (board[0] == player and board[3] == player and board[6] == player) or \
       (board[1] == player and board[4] == player and board[7] == player) or \
       (board[2] == player and board[5] == player and board[8] == player) or \
       (board[0] == player and board[4] == player and board[8] == player) or \
       (board[2] == player and board[4] == player and board[6] == player):
        return True
    else:
        return False

# function to play the game


def play_game_x(ch):
    board = [' ' for x in range(9)]
    print("Welcome to Tic Tac Toe!")
    print_board(board)
    player = 'X'

    while True:
        if check_winner(board, 'O'):
                print("You Lost !")
                input("Press enter to return to main menu")
                break
        position = int(input("Enter a position (1-9) to place {}: " + player))
        if board[position-1] == ' ':
            board[position-1] = player
            
            ref = db.reference('game/')
            users_ref = ref.child(ch)
            #houni bech updati map bi map ili badltha x
            print_board(board)

            users_ref.update({
                'Map': board,
            })

            #houni ni9ol rahou round 2 ma3neha round mit3 o taw
            users_ref.update({
                'round': "2",
            })


            if check_winner(board, player):
                print("{} wins! Congratulations!".format(player))
                input("Press enter to return to main menu")
                break
            if check_winner(board, 'O'):
                print("You Lost !")
                input("Press enter to return to main menu")
                break

            if ' ' not in board:
                print("It's a tie!")
                input("Press enter to return to main menu")
                break
            print("waiting for o to play")

            #houni bech no93d nistna lin yiji dawri
            while True:
                #hetha lin li round 
                round='game/'+ch+'/round'
                #houni jebt donneé mit3 round ili hiya tikoun 1 -> x wala 2 -> o 
                ready = db.reference(round)
                #lina nitesti ken jé dawri wala le 
                if ready.get()=="1":
                    
                    round='game/'+ch+'/Map'
                    #w ken jé dawri bech ne5o map ili fi data base 
                    ready = db.reference(round)
                    #w ni7otha houni fi variable board
                    board=ready.get()
                    print_board(board)
                    # w lina yarja3 il fou9
                    break
        else:
            print("That position is already taken. Please choose another position.")


def play_game_o(ch):
    print("Welcome to Tic Tac Toe!")
    board = [' ' for x in range(9)]
    print_board(board)
    player = 'O'
    #houni nafss x mama juste fazet while true mit3 verification mi3 round tajra min louwel a5tr x yal3b louwel
    while True:
        print("waiting for o to play")
        while True:
                
                round='game/'+ch+'/round'
                ready = db.reference(round)
                if ready.get()=="2":
                    round='game/'+ch+'/Map'
                    ready = db.reference(round)
                    board=ready.get()
                    print_board(board)
                    break
        if check_winner(board, 'X'):
                print("You Lost !")
                input("Press enter to return to main menu")
                break                  
        position = int(
            input("Enter a position (1-9) to place {}: ".format(player)))
        if board[position-1] == ' ':
            board[position-1] = player
            print_board(board)
            ref = db.reference('game/')
            users_ref = ref.child(ch)
            users_ref.update({
                'Map': board,
            })
            users_ref.update({
                'round': "1",
            })
            if check_winner(board, player):
                print("{} wins! Congratulations!".format(player))
                input("Press enter to return to main menu")
                break
            if check_winner(board, 'X'):
                print("You Lost !")
                input("Press enter to return to main menu")
                break

            if ' ' not in board:
                print("It's a tie!")
                input("Press enter to return to main menu")
                break
            
            
        else:
            print("That position is already taken. Please choose another position.")

#hethi mezlt ma kemletch w ma 3aytlithch 
#fiha fazet join roomm

#lezm nizd fazet yida5el ismo o        
def MultiPlayer():

    while True:
        with keyboard.Events() as events:
            
            os.system("cls" if os.name == "nt" else "clear")
            print("+----------------------------------+")
            print("|                                  |")
            print("|                                  |")
            print("|           h : Host               |")
            print("|                                  |")
            print("|           j : Join Room          |")
            print("|                                  |")
            print("|                                  |")
            print("+----------------------------------+")
            event = events.get(1e6)
           
            if event.key == keyboard.KeyCode.from_char("h"):
                print(" rak host") 
                ch = input("Your name ")
                play_game_x(ch)
            if event.key == keyboard.KeyCode.from_char("j"):
                print("rak join")
                ch = input("Your name ")
                play_game_o(ch)


#MultiPlayer()
# round='game/gaith/Map'
# ready = db.reference(round)
# l=ready.get()
# print(l)

MultiPlayer()