#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>


def find_subtour(arches):
    first = arches[0]
    out = [first]
    head, tail = first
    for i, j in arches:
        if tail == i:
            out.append((i, j))
            tail = j
        elif j == head:
            out.append((i, j))
            break

    for i in out:
        arches.remove(i)

    return out

def check_subtour(tour):
    head = tour[0]
    i, _ = head
    return i != 0

def find_tours(arches):
    while arches:
        tmp = find_subtour(arches)
        if check_subtour(tmp):
            yield tmp
