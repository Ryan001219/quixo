import random
import math
import pandas as pd

def checktheblock(board,index,turn): # checking if the block can touch or not
    if board[index] == turn or board[index] == 0: # if the block is my own block or empty block, i can touch
        return True
    else:
        return False
    
def check_move(board,turn,index,push_from):
    dim = int(math.sqrt(len(board)))
    if index == 0: # top left corner
        if push_from == "B" or push_from == "R": # top left corner cannot push from T or L
             return checktheblock(board,index,turn)
        else:
             return False
    elif index == dim-1: # top right corner
        if push_from == "B" or push_from == "L": # top right corner cannot push from T or R
             return checktheblock(board,index,turn)
        else:
             return False
    elif index == dim*(dim-1): # bottom left corner
        if push_from == "T" or push_from == "R": # bottom left corner cannot push from B or L
             return checktheblock(board,index,turn)
        else:
             return False
    elif index == dim**2-1: # bottom right corner
        if push_from == "T" or push_from == "L": # bottom right corner cannot push from B or R
             return checktheblock(board,index,turn)
        else:
             return False
    elif index in range(1,dim-1): # top row excluding corners
        if push_from == "B" or push_from == "L" or push_from == "R": # cannot push from T
             return checktheblock(board,index,turn)
        else:
             return False
    elif index in range(dim**2-dim+1,dim**2-1): # bottom row excluding corners
        if push_from == "T" or push_from == "L" or push_from == "R": # cannot push from B
             return checktheblock(board,index,turn)
        else:
             return False
    elif index % dim == 0: # most left column excluding corners
        if push_from == "T" or push_from == "B" or push_from == "R": # cannot push from L
             return checktheblock(board,index,turn)
        else:
             return False
    elif (index+1) % dim == 0: # most right column excluding corners
        if push_from == "T" or push_from == "B" or push_from == "L": # cannot push from R
             return checktheblock(board,index,turn)
        else:
             return False
    else: # invalid index which are the blocks in the middle
        return False

def apply_move(board,turn,index,push_from):
    board_temp = board[:] # create a temporary board
    dim = int(math.sqrt(len(board))) # using the length of board to calcuate the dimension
    row = (index//dim) + 1 # using the index to calculate the row 
    column = int(index%dim) + 1 # using the index to calculate the column
    if push_from == "R": # push from right
        board_temp.pop(index) # removing element from that index
        board_temp.insert((row*dim)-1, turn) # adding element 'turn' at the back of that row
    elif push_from == "L":# push from left
        board_temp.pop(index) # removing element from that index
        board_temp.insert((row-1)*dim, turn) # adding element 'turn' at the front of that row
    elif push_from == 'B':# push from bottom
        templist = board_temp[column-1::dim] # make a list to store all the entries on that column
        templist.pop(row-1) # removing element from that index
        templist.append(turn) # add the element 'turn' at the back of the list
        counter = 0 
        for i in templist: # replace the whole column by the list
            board_temp[counter*dim + column-1] = i
            counter += 1
    else: # push from top
        templist = board_temp[column-1::dim] # make a list to store all the entries on that column
        templist.pop(row-1) # removing element from that index
        templist.insert(0,turn) # add the element 'turn' at the front of the list
        counter = 0
        for i in templist: # replace the whole column by the list
            board_temp[counter*dim + column-1] = i
            counter += 1
    return board_temp

def check_victory(board,who_played): 
    dim = int(math.sqrt(len(board))) # using the length of board to calcuate the dimension
    win = [] # make a list to store all the winning situation currently
    if board[0:dim**2:dim+1].count(1) == dim: # top left to bottom right (diagonal)
        win.append(1) # if all the diagonal entries are 1, add 1 to the win list to record player 1 form a line
    if board[0:dim**2:dim+1].count(2) == dim: # top left to bottom right (diagonal)
        win.append(2) # if all the diagonal entries are 2, add 2 to the win list to record player 2 form a line
    if board[dim-1:dim*(dim-1)+1:dim-1].count(1) == dim: # top right to bottom left (diagonal)
        win.append(1) # same as above
    if board[dim-1:dim*(dim-1)+1:dim-1].count(2) == dim: # top right to bottom left (diagonal)
        win.append(2) # same as above
    for i in range(0,dim): # checking every column
        column_count_1 = 0 # count how many 1 in that column
        column_count_2 = 0 # count how many 2 in that column
        for r in board[i::dim]:
            if r == 1:
                column_count_1 += 1 # if got 1, count + 1
            if r == 2:
                column_count_2 += 1 # if got 2, count + 1
        if column_count_1 == dim: # if the whole column are all 1
            win.append(1) # add 1 to the win list to record player 1 form a line
        if column_count_2 == dim: # if the whole column are all 2
            win.append(2) # add 2 to the win list to record player 2 form a line
    for i in range(0,dim): # checking every row
        row_count_1 = 0 # count how many 1 in that row
        row_count_2 = 0 # count how many 2 in that row
        for r in board[i*dim:(i+1)*dim]:
            if r == 1:
                row_count_1 += 1 # if got 1, count + 1
            if r == 2:
                row_count_2 += 1 # if got 2, count + 1
        if row_count_1 == dim: # if the whole row are all 1
            win.append(1) # similar idea as above
        if row_count_2 == dim: # if the whole row are all 2
            win.append(2) # similar idea as above
    if len(win) == 0: # the win list has no entry, no one formed a line
        return 0 # no one wins
    elif who_played == 1:
        return max(win) # player 1's turn, if the win list got 2 then 2 will win, else 1 win
    elif who_played == 2:
        return min(win) # player 2's turn, if the win list got 1 then 1 will win, else 2 win

def computer_move(board,turn,level):
    dim = int(math.sqrt(len(board)))
    top_row = [i for i in range(0,dim)] 
    bottom_row = [i for i in range(dim*(dim-1),dim**2)]
    left_column = [i for i in  range(dim,dim*(dim-1),dim)]
    right_column = [i for i in range(2*dim-1,dim**2-1,dim)]
    index_choices = top_row
    index_choices.extend(bottom_row)
    index_choices.extend(left_column)
    index_choices.extend(right_column) # it will include all the outer blocks' indeces
    direction_choices = ['T','B','L','R'] # all four directions
    if turn == 1: # if computer is player 1
        player_turn = 2 # then player is player 2
    elif turn == 2: # if computer is player 2
        player_turn = 1 # then player is player 1
    random_moves = [] # a list to store all the possible moves computer can make and play one of them
    
    if level == 1: # player choose to play level 1
        while True:           
            index = random.choice(index_choices) # randomly pick 1 index
            push_from = random.choice(direction_choices) # randomly pick 1 direction
            if check_move(board,turn,index,push_from) == False:
                continue # regenerate a valid move
            elif check_move(board,turn,index,push_from) == True: 
                return(index,push_from) # it is a valid move, play it
            
    elif level == 2: # player choose to play level 2
        for i in index_choices: 
            for d in direction_choices: # exhausting all the moves and check if there is a direct win move
                if check_move(board,turn,i,d) == True: # valid move
                    imaginary_board = board[:]
                    imaginary_board = apply_move(board,turn,i,d)
                    if check_victory(imaginary_board,turn) == turn: # there is a direct win move
                        return(i,d) # play it and computer wins
        # if no direct win move, we will check for any direct lose move
        for i in index_choices: 
            for d in direction_choices: # exhausting all the moves by computer
                if check_move(board,turn,i,d) == True:
                    imaginary_board = board[:]
                    imaginary_board = apply_move(board,turn,i,d)
                    if check_victory(imaginary_board,turn) == player_turn:
                        continue # this is a direct lose move, we continue to another move
                    else: # this is not a direct lose, but we consider the player's move
                        count = 0
                        for i2 in index_choices: 
                            for d2 in direction_choices: # exhausting the moves and check the player's direct win
                                if check_move(imaginary_board,player_turn,i2,d2) == True: # valid move
                                    imaginary_board_2 = imaginary_board[:]
                                    imaginary_board_2 = apply_move(imaginary_board,player_turn,i2,d2)
                                    if check_victory(imaginary_board_2,player_turn) == player_turn: # if player have direct win  
                                        count += 1
                        if count > 0: # if the move will cause the player win, skip the move
                            continue
                        elif count == 0: # if the move won't cause player win, this is a good move
                            random_moves.append((i,d)) # add this move to the list
                                
        while len(random_moves) > 0: # there are moves that the player won't win anyway, play randomly
            return(random.choice(random_moves))
        
        while True: # no move that player will not win, so just play any valid move        
            index = random.choice(index_choices) 
            push_from = random.choice(direction_choices) 
            if check_move(board,turn,index,push_from) == False: # invalid move, regenerate
                continue 
            elif check_move(board,turn,index,push_from) == True: # valid move
                return(index,push_from) 

def display_board(board):
    dim = int(math.sqrt(len(board)))
    new_list=[] # a list to store the entries in the board
    for i in range(0,dim):
        i = board[i*dim:(i+1)*dim]
        new_list.append(i)
    db = pd.DataFrame(new_list, index=[dim for dim in range(1,dim+1)], columns=[dim for dim in range(1,dim+1)])
    print(db) # print the board
    pass

def menu():
    while True: # to ask user which mode he wants to play
       mode = input("Welcome to QUIXO game.\nTo play the mode 'Player vs Player', reply 'pvp'.\n\
To play the mode 'Player vs Computer', reply 'pvc'.\nYou want to play: ")
       if mode == 'pvp': # player versus player
           while True: # ask player choose the dimension of the board
               dim = input("The default board size is 5x5, if you want to change the dimension, \
please reply the dimension you want.\n\
(For example, if you want a 6x6 board, reply '6')\n\
Otherwise, please reply '5': ") 
               if dim.isdigit() == False:
                   print("\nInvalid input! Please input a positive integer!")
               else: # a valid dimension
                   dim = int(dim)
                   break
           break
       elif mode == 'pvc': # player versus computer
           while True: # first ask the user to choose difficulty
               level = input("Please choose the difficulty level of the computer (1 or 2): ")
               if level.isdigit() == False:
                   print("\nInvalid input! Please input 1 or 2!")
               elif int(level) == 1 or int(level) == 2:
                   level = int(level)
                   while True: # then ask the user to choose dimension
                       dim = input("The default board size is 5x5, if you want to change the dimension, \
please reply the dimension you want.\n\
(For example, if you want a 6x6 board, reply '6')\n\
Otherwise, please reply '5': ")
                       if dim.isdigit() == False:
                           print("\nInvalid input! Please input a positive integer!")
                       else:
                           dim = int(dim)
                           break
                   break
               else:
                    print("\nInvalid input! Please input 1 or 2!")
           break
       else: # invalid input
          print("\nInvalid input! Please write 'pvp' or 'pvc'!")
          
    # initialize settings
    board = [0 for i in range(dim**2)] # create a board full of 0s
    turn = 1 # player 1 move first, no matter is computer or player
    print("\nThe index of the block will be from 1 to",dim**2,".""\n\
(Example: the index of the block in row 1 column 5 is 5 and for row 2 column 1 is",dim+1,")") # way to calculate index
    while mode == 'pvp': # the pvp game starts here
       print("")
       display_board(board) # display the board
       print("\nNow is player",turn,"'s turn.") # telling them whose turn it is
       print("\nIf you wish to quit the game, please input ####. If not,") # user can quit immediately
       while True: # ask the user to input the row the block
           row = input("Please indicate the row of the block you wish to move: ")
           if row == "####":
               print("You've decided to quit the game. See you next time!")
               return False
           elif row.isdigit() == False:
               print("\nPlease insert an positive integer!")
           elif int(row) < 1 or int(row) > dim:
               print("\nPlease choose within the board!")
           else:
               row = int(row)
               break
        
       while True: # ask the user to input the column of the block
           column = input("Please indicate the column of the block you wish to move: ")
           if column.isdigit() == False:
               print("\nPlease insert an positive integer!")
           elif int(column) < 1 or int(column) > dim:
               print("\nPlease choose within the board!")
           else:
               column = int(column)
               break
         
       index = (row-1)*dim + (column-1) # calculate the index
       
       while True: # ask the user to input the direction they want to push
           push_from = input("Push from top - T\nPush from bottom - B\nPush from left - L\n\
Push from right - R\nPlease indicate the direction you want to push from: ")
           if push_from == 'T' or push_from == 'B' or push_from == 'L' or push_from == 'R':
               break
           else:
               print("\nPlease input 'T', 'B', 'L' or 'R'!")
               
       if check_move(board,turn,index,push_from) == False: # if it is an invalid move, ask user to input again
           print("\nIt is an invalid move! Please try again!")
           continue

       board = apply_move(board,turn,index,push_from) # apply the move on the board
       if check_victory(board,turn) == 1: # if player 1 wins
           display_board(board)
           print("\nCongratulation to Player 1! You've won the game!")
           return False
       elif check_victory(board,turn) == 2: # if player 2 wins
           display_board(board)
           print("\nCongratulation to Player 2! You've won the game!")
           return False
       else: # no winner currently
           pass
       
       if turn == 1: # swapping turns from 1 to 2 or 2 to 1
           turn = 2
       elif turn == 2:
           turn = 1
    
    while True: # ask user to choose to be player 1 or 2 when they choose pvc
        player_turn = input("If you want to be player 1, reply 1, if you want to be player 2, reply 2: ")
        if player_turn.isdigit() == False:
            print("\nInvalid input! Please input 1 or 2!")
        elif int(player_turn) == 1 or int(player_turn) == 2:
            player_turn = int(player_turn)
            break
        else:
            print("\nInvalid input! Please input 1 or 2!")
        
    if player_turn == 1: # if player choose to be player 1
        computer_turn = 2 # then computer is player 2 
    elif player_turn == 2: # the other way round
        computer_turn = 1
        
    while mode == 'pvc': # the pvc game starts here
        if turn == player_turn: # player's turn
            print("")
            display_board(board)
            print("\nNow is your turn.")
            print("\nIf you wish to quit the game, please input ####. If not,")
            while True: # ask the user to input the row the block
                row = input("Please indicate the row of the block you wish to move: ")
                if row == "####":
                    print("You've decide to quit the game. See you next time!")
                    return False
                elif row.isdigit() == False:
                    print("\nPlease insert an positive integer!")
                elif int(row) < 1 or int(row) > dim:
                    print("\nPlease choose within the board!")
                else:
                    row = int(row)
                    break
          
            while True: # ask the user to input the column of the block
                column = input("Please indicate the column of the block you wish to move: ")
                if column.isdigit() == False:
                    print("\nPlease insert an positive integer!")
                elif int(column) < 1 or int(column) > dim:
                    print("\nPlease choose within the board!")
                else:
                    column = int(column)
                    break
         
            index = (row-1)*dim + (column-1) # calculate the index
    
            while True: # ask the user to input the direction they want to push
                push_from = input("Push from top - T\nPush from bottom - B\nPush from left - L\n\
Push from right - R\nPlease indicate the direction you want to push from: ")
                if push_from == 'T' or push_from == 'B' or push_from == 'L' or push_from == 'R':
                    break
                else:
                    print("\nPlease input 'T', 'B', 'L' or 'R'!")
               
            if check_move(board,turn,index,push_from) == False: # invalid move, try again
                print("\nIt is an invalid move! Please try again!")
                continue

            board = apply_move(board,turn,index,push_from) # apply the move on the board
            if check_victory(board,player_turn) == player_turn: # if player plays and win
                display_board(board)
                print("\nCongratulation! You've beat the computer and won the game!")
                return False
            elif check_victory(board,player_turn) == computer_turn: # if player plays and lose
                display_board(board)
                print("\nToo bad! You've lost the game. Please try harder next time.")
                return False
            else: # no winner currently
                pass
            
            turn = computer_turn # change to computer's turn   
    
        elif turn == computer_turn: # computer's turn
            (index,push_from) = computer_move(board,turn,level) # computer's move
            board = apply_move(board,turn,index,push_from) # apply the move on the board
            print("\nComputer pushes the block",index+1,"in the direction of",push_from)
            # the code above shows the user which move the computer played
            if check_victory(board,computer_turn) == player_turn: # if computer plays and lose, player win
                display_board(board)
                print("\nCongratulation! You've beat the computer and won the game!")
                return False
            elif check_victory(board,computer_turn) == computer_turn: # if computer plays and win, player lose
                display_board(board)
                print("\nToo bad! You've lost the game. Please try harder next time.")
                return False
            else: # no winner currently
                pass
        
            turn = player_turn # change to player's turn

if __name__ == "__main__":
    menu()