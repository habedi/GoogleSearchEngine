import random

a = 0.1
b = 20


def generate_random_tses(n=100):
    if not isinstance(n, (float, int)):
        return []
    else:
        random.seed(a=None)
        ts_list = []
        for i in range(1, n):
            ts_list.append(round(random.uniform(a, b), 2))
        return ts_list
