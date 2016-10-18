import time
import sys
import math
import socket
import waGreedy

HOST = 'localhost'
PORT = 9000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# N == number of stones for the game
N = int(sys.argv[1])

easy_grid = [[0] * 50 for item in range(0, 50)]
easy_pull = [[{1: 0, 2: 0} for j in range(0, 50)] for i in range(0, 50)]
easy_choice = [[0] * 50 for item in range(0, 50)]

grid = [[0] * 1000 for item in range(0, 1000)]
pull = [[{1: 0, 2: 0} for j in range(0,1000)] for i in range(0, 1000)]
choice = [[0] * 1000 for item in range(0, 1000)]
moves = []
weplayer = 1

def main():

    while 1:
        serverResponse = s.recv(1024)
        data = serverResponse.split()

        # Check if the game has ended
        if int(data[0]) == 1:
            count1 = 0
            count2 = 0
            for i in range(0, 1000):
                for j in range(0, 1000):
                    if choice[i][j] == 1:
                        count1 += 1
                    else:
                        count2 += 1
            break

        # Construct the grid by placing all the moves so far
        numberOfMoves = int(data[1])

        player = 0
        global weplayer
        for item in range(numberOfMoves - 1, numberOfMoves):
            i = int(data[2 + item * 3])
            j = int(data[2 + item * 3 + 1])
            player = int(data[2 + item * 3 + 2])
            if player > 0:
                moves.append((i, j, player))
                waGreedy.refresh_pull(player, i, j, grid, choice, easy_grid, easy_choice, pull, easy_pull)
                weplayer = 3 - player

        print "weplayer", weplayer
        # Make a random valid move. Your algorithm goes here instead of the
        # following randomized move selection
        validMoveFound = False
        nextI = 0
        nextJ = 0

        while not validMoveFound:
            if len(moves) == 0:
                nextI, nextJ = 250, 250
                break
            moveI, moveJ = waGreedy.find_next_move(weplayer, N, easy_grid, easy_choice, moves, easy_pull)

            validMoveFound = waGreedy.is_valid(moveI, moveJ, moves)

            if validMoveFound:
                nextI = moveI
                nextJ = moveJ

        waGreedy.refresh_pull(weplayer, nextI, nextJ, grid, choice, easy_grid, easy_choice, pull, easy_pull)

        moves.append((nextI, nextJ, 3-player))
        print nextI, nextJ
        s.sendall("{} {}".format(nextI, nextJ))

    s.close()

if __name__ == "__main__":
    main()