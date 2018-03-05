#!/usr/bin/python

from copy import deepcopy
SIZE = 9

m = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

#m = [
#    [0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0],
#    [0, 0, 0, 0, 0, 0, 0, 0, 0]
#    ]
#m = [
#    [0, 7, 0, 0, 1, 0, 0, 9, 0],
#    [9, 0, 0, 8, 0, 0, 0, 0, 7],
#    [0, 0, 3, 0, 0, 0, 0, 0, 6],
#    [0, 4, 0, 0, 0, 1, 5, 0, 0],
#    [0, 3, 0, 0, 0, 0, 0, 1, 0],
#    [0, 0, 2, 7, 0, 0, 0, 6, 0],
#    [5, 0, 0, 0, 0, 0, 6, 0, 0],
#    [6, 0, 0, 0, 0, 5, 0, 0, 2],
#    [0, 8, 0, 0, 2, 0, 0, 7, 0]
#    ]

def construct_matrix(m):
    matrix = [[[] for i in xrange(SIZE)] for j in xrange(SIZE)]
    for x in xrange(SIZE):
        for y in xrange(SIZE):
            matrix[x][y] = Node(x, y, x % 3 * 3 + y % 3, m[x][y])
    return matrix

class Node:
    row_n = None
    column_n = None
    matrix_n = None
    value = None

    def __init__(self, row_n, column_n, matrix_n, value):
        self.row_n = row_n
        self.column_n = column_n
        self.matrix_n = matrix_n
        self.value = value

def dump_matrix(m):
    print 'dump'
    for x in m:
        for y in x:
            print str(y.value) + ' ',
        print '\n'

def collect_occupied_node(matrix):
    row_exist_number = [[] for x in xrange(SIZE)]
    column_exist_number = [[] for x in xrange(SIZE)]
    matrix_exist_number = [[] for x in xrange(SIZE)]
    first_zero = None
    for i in xrange(SIZE):
        for j in xrange(SIZE):
            if matrix[i][j].value == 0 and type(first_zero) != int:
                #node = Node(i, j, i / 3 * 3 + j / 3, matrix[i][j].value)
                first_zero = i * SIZE + j
            else:
                if not matrix[i][j].value in row_exist_number[i]:
                    row_exist_number[i].append(matrix[i][j].value)
                if not matrix[i][j].value in column_exist_number[j]:
                    column_exist_number[j].append(matrix[i][j].value)
                # matrix number j / 3 + i / 3 * 3
                matrix_number = j / 3 + i / 3 * 3
                if not matrix[i][j].value in \
                        matrix_exist_number[matrix_number]:
                    matrix_exist_number[matrix_number].append(matrix[i][j].value)
    return (row_exist_number, column_exist_number, matrix_exist_number, first_zero)

def find_next_zero(matrix, last_zero):
    start_i = last_zero / SIZE
    for i in range(start_i, SIZE):
        for j in range(0, SIZE):
            if matrix[i][j].value == 0:
                return i * SIZE + j

    return None


def check(matrix, row_exist_number = [], column_exist_number = [] \
        , matrix_exist_number = [], first_zero = None):
    #if not node:
    #    print 'found'
    #    dump_matrix(matrix)
    #    return

    #dump_matrix(matrix)
    empty_i = first_zero / SIZE
    empty_j = first_zero % SIZE
    # matrix_number represent which sub matrix this empty space belongs
    matrix_number = empty_i / 3 * 3 + empty_j / 3
    for v in range(1, SIZE+1):
        if not v in row_exist_number[empty_i] \
                and not v in column_exist_number[empty_j] \
                and not v in matrix_exist_number[matrix_number]:
                    node = Node(empty_i, empty_j, matrix_number, v)
                    new_matrix = deepcopy(matrix)
                    new_matrix[node.row_n][node.column_n] = node
                    new_row_exist_number = deepcopy(row_exist_number)
                    new_column_exist_number = deepcopy(column_exist_number)
                    new_matrix_exist_number = deepcopy(matrix_exist_number)
                    new_row_exist_number[empty_i].append(v)
                    new_column_exist_number[empty_j].append(v)
                    new_matrix_exist_number[matrix_number].append(v)
                    new_first_zero = find_next_zero(new_matrix, first_zero)
                    if not new_first_zero:
                        dump_matrix(new_matrix)
                        break
                    else:
                        check(new_matrix, new_row_exist_number, new_column_exist_number, \
                                new_matrix_exist_number, new_first_zero)

if __name__ == '__main__':
    matrix = construct_matrix(m)
    row_exist_number, column_exist_number, matrix_exist_number, first_zero = collect_occupied_node(matrix)
    check(matrix ,row_exist_number, column_exist_number, matrix_exist_number, first_zero)
