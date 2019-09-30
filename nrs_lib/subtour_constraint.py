#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>

def _build_subtour_(out, arches, head, tail):
    for i, j in arches[1:]:
        if tail == i:
            out.append((i, j))
            tail = j
            if j == head:
                break
    return out, arches

def find_subtour(arches):
    first = arches[0]
    out = [first]
    head, tail = first
    if head != tail:
        out, arches = _build_subtour_(out, arches, head, tail)

    for i in out:
        arches.remove(i)

    return out

def check_subtour(tour):
    
    head, _ = tour[0]
 
    if head == 0:
        return False
    else:
        _, tail = tour[-1]
        return tail == head


def find_tours(arches):
    while arches:
        tmp = find_subtour(arches)
        if check_subtour(tmp):
            print(tmp)
            yield tmp
