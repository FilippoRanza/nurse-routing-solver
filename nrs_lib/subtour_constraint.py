#! /usr/bin/python3

# Copyright (c) 2019 Filippo Ranza <filipporanza@gmail.com>


def _is_tour_(tour):
    head, _ = tour[0]
    _, tail = tour[-1]
    return head == tail


def _build_subtour_(out, arches, head, tail):
    for i, j in arches:
        if tail == i:
            out.append((i, j))
            tail = j
            if j == head:
                break

    return out, arches, head, tail


def find_subtour(arches):
    first = arches[0]
    out = [first]
    head, tail = first

    while (not _is_tour_(out)) and arches:
        out, arches, head, tail = _build_subtour_(out, arches, head, tail)
        for i in out:
            try:
                arches.remove(i)
            except:
                pass

    for i in out:
        try:
            arches.remove(i)
        except:
            pass

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
            yield tmp
