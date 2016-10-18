import socket
import time
import sys
import math


def euclideanDistance(x1, y1, x2, y2):
    distance = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
    return math.sqrt(distance)




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


def easy_refresh_pull(player, weplayer, x, y, easy_grid, easy_choice, moves, easy_pull, N):
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


def find_next_move(weplayer, N, easy_grid, easy_choice, moves, easy_pull):
    x = 0
    y = 0
    max = 0
    #print easy_pull
    for i in range(0, 25):
        for j in range(0, 25):
            a, b = real_index(i, j)
            if is_valid(a, b, moves):
                score = easy_refresh_pull(weplayer, weplayer, a, b, easy_grid, easy_choice, moves, easy_pull, N)
                if score > max:
                    print score, a, b
                    max = score
                    x = a
                    y = b

    cx,cy = center_index(x,y)
    for i in range(0, 40):
        for j in range(0, 40):
            a, b = small_real_index(cx,cy,i,j)
            if is_valid(a, b, moves):
                score = easy_refresh_pull(weplayer, weplayer, a, b, easy_grid, easy_choice, moves, easy_pull, N)
                if score > max:
                    print score, a, b
                    max = score
                    x = a
                    y = b

    return x, y


# update pull array for each element
def refresh_pull(player, x, y, grid, choice, easy_grid, easy_choice, pull, easy_pull):
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
def is_valid(x, y, moves):
    for move in moves:
        if euclideanDistance(x, y, move[0], move[1]) < 66:
            return False
    return True