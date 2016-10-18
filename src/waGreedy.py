import socket
import time
import sys
import math


def euclideanDistance(x1, y1, x2, y2):
    distance = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
    return math.sqrt(distance)

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


def real_index(i,j):
    return i * 40 + 20, j * 40 + 20

def small_real_index(x,y,i,j):
    return x * 40 + i, y * 40 + j

def center_index(i,j):
    return i / 40, j / 40


'''
def init_distance():
    for i in range(0, 8):
        for j in range(0, 8):
            a,b = real_index(i,j)
            for x in range(0, 1000):
                for y in range(0, 1000):
                    distance[(a,b,x,y)] = euclideanDistance(a,b,x,y)
'''


def easy_refresh_pull(player, x, y):
    x1, y1 = center_index(x, y)
    easy_grid[x1][y1] = player
    easy_choice[x1][y1] = player

    count = 0
    for a in range(0, 25):
        for b in range(0, 25):
            i, j = real_index(a, b)
            if easy_grid[a][b] == 0:
                score = 1.0 / ((i-x)*(i-x) + (j-y)*(j-y))
                easy_pull[a][b][player] += score * (40*40)
                if easy_pull[a][b][player] > easy_pull[a][b][3 - player]:
                    if weplayer == 2:
                        if len(moves) > N * 2 / 3:
                            count += 1
                        elif len(moves) > N / 3:
                            count += (easy_pull[a][b][player] - easy_pull[a][b][3 - player])
                        else:
                            count += 1.0 * (easy_pull[a][b][player] / easy_pull[a][b][3 - player])
                    else:
                        if len(moves) > N * 2/ 3:
                            count += 1
                        else:
                            count += (easy_pull[a][b][player] - easy_pull[a][b][3 - player])
                easy_pull[a][b][player] -= score * (40*40)

    easy_grid[x1][y1] = 0
    easy_choice[x1][y1] = 0
    return count


def find_next_move():
    x = 0
    y = 0
    max = 0
    #print easy_pull
    for i in range(0, 25):
        for j in range(0, 25):
            a, b = real_index(i, j)
            if is_valid(a, b):
                score = easy_refresh_pull(weplayer, a, b)
                if score > max:
                    print score, a, b
                    max = score
                    x = a
                    y = b

    cx,cy = center_index(x,y)
    for i in range(0, 40):
        for j in range(0, 40):
            a, b = small_real_index(cx,cy,i,j)
            if is_valid(a, b):
                score = easy_refresh_pull(weplayer, a, b)
                if score > max:
                    print score, a, b
                    max = score
                    x = a
                    y = b

    return x, y


# update pull array for each element
def refresh_pull(player, x, y):
    grid[x][y] = player
    choice[x][y] = player

    # update score for easy one
    a, b = center_index(x, y)
    easy_grid[a][b] = player
    easy_choice[a][b] = player

    count = 0
    for i in range(0, 1000):
        for j in range(0, 1000):
            if grid[i][j] == 0:
                score = 1.0 / ((i-x)*(i-x) + (j-y)*(j-y))
                pull[i][j][player] += score
                a, b = center_index(i, j)
                easy_pull[a][b][player] += score
            if pull[i][j][player] > pull[i][j][3 - player]:
                choice[i][j] = player
            if easy_pull[a][b][player] > easy_pull[a][b][3 - player]:
                easy_choice[a][b] = player
            if choice[i][j] == player:
                count += 1
    return count


# Judge whether a new point is valid
def is_valid(x, y):
    for move in moves:
        if euclideanDistance(x, y, move[0], move[1]) < 66:
            return False
    return True

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
                refresh_pull(player, i, j)
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
            moveI, moveJ = find_next_move()

            validMoveFound = is_valid(moveI, moveJ)

            if validMoveFound:
                nextI = moveI
                nextJ = moveJ

        refresh_pull(weplayer, nextI, nextJ)

        moves.append((nextI, nextJ, 3-player))
        s.sendall("{} {}".format(nextI, nextJ))

    s.close()

if __name__ == "__main__":
    main()