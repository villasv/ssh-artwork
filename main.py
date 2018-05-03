from crypto import generate_key
from randomart import get_randomart


def diff(a_art, b_art):
    heavy_set = ['B', 'O', 'X', '@', '%', '&', '#', 'S', 'E']
    light_set = ['.', 'o', '+', '=', '*', '/', '^']

    def diff_coin_pair(pair):
        a, b = pair
        if a == b:
            return 0
        if (a == ' ' and b in heavy_set) or (a in heavy_set and b == ' '):
            return 100
        if (a == ' ' and b in light_set) or (a in light_set and b == ' '):
            return 25
        if (a in light_set and b in heavy_set) or (a in heavy_set and b in light_set):
            return 10
        return 1

    from operator import add
    from functools import reduce
    return  reduce(add, map(diff_coin_pair, zip(a_art, b_art)))


def search(_):
    with open('target.art') as f:
        target_art = f.read()

    import os
    _, _, art_files = next(os.walk('./keys'))
    approx_file = './keys/' + sorted(art_files)[-1]

    with open(approx_file) as f:
        approx_art = f.read()

    approx_diff = diff(target_art, approx_art)

    private_key, public_key = generate_key()
    newest_art = get_randomart(public_key)
    newest_diff = diff(target_art, newest_art)

    if newest_diff < approx_diff:
        print("New approximation found! Diff = {}".format(newest_diff))
        print(newest_art)
        index = int(approx_file[7:-4])
        approx_file = "./keys/{}.art".format(index+1)
        with open(approx_file, 'w') as f:
            approx_art = f.write(newest_art)
        with open(approx_file[:-3] + '.key', 'w') as f:
            approx_art = f.write(private_key)
    

from multiprocessing import Pool
from tqdm import tqdm

if __name__ == "__main__":
    attempts = 1000
    with Pool(processes=10) as p:
        r = list(tqdm(p.imap(search, range(attempts)), total=attempts))
