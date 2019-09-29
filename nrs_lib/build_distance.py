#! /usr/bin/python



def _zeros(size):
    out = [
            [0 for _ in range(size)] for _ in range(size)
        ]
    return out


def _enforce_self_dist(dist_matrix, scale):
    longest = max((max(row) for row in dist_matrix))
    longest *= scale
    for i in range(len(dist_matrix)):
        dist_matrix[i][i] = longest

    return dist_matrix

def build_distance(hub_distance, patient_distance, scale):
    out = _zeros(len(patient_distance) + 1)

    for i, d in enumerate(hub_distance, 1):
        out[0][i] = d
        out[i][0] = d

    for i, row in enumerate(patient_distance, 1):
        for j, d in enumerate(row, 1):
            out[i][j] = d


    return _enforce_self_dist(out, scale)
