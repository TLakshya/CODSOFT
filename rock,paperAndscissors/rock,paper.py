import random

gameelement = ["rock", "paper", "scissor"]
a = 1
while a:
    user_move = int(input("your choose?type 0 for Rock or 1 Paper Or 2 Sissors:"))
    print(f"User chose:{gameelement[user_move]}")
    com_choice = random.randint(0, 2)
    print(f"computer chose :{gameelement[com_choice]}")
    if user_move >= 3 or user_move < 0:
        print("you typed an invalid,you lose!")
    elif com_choice == user_move:
        print("its a draw! ")
    elif user_move == 0 and com_choice == 2:
        print("you win")
    elif user_move > com_choice:
        print("you win!")
    else:
        print("you lose|")
    a = input("do you want to play again(yes/no):")
    if a.lower() == "no":
        a = 0
