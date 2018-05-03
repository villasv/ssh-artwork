from crypto import generate_key
from randomart import get_randomart

heavy_set = ['B', 'O', 'X', '@', '%', '&', '#', 'S', 'E']
light_set = ['.', 'o', '+', '=', '*', '/', '^']

def diff(a_art, b_art):
    def diff_coin_pair(pair):
        a, b = pair
        if a == b:
            return 0
        if (a == ' ' and b in heavy_set) or (a in heavy_set and b == ' '):
            return 100
        if (a == ' ' and b in light_set) or (a in light_set and b == ' '):
            return 50
        if (a in light_set and b in heavy_set) or (a in heavy_set and b in light_set):
            return 10
        return 1

    from operator import add
    from functools import reduce
    return  reduce(add, map(diff_coin_pair, zip(a_art, b_art)))

if __name__ == "__main__":
    with open('target.art') as f:
        target_art = f.read()
    print("Target Art:")
    print(target_art)
    print()

    import os
    _, _, art_files = next(os.walk('./keys'))
    approx_file = './keys/' + sorted(art_files)[-1]

    with open(approx_file) as f:
        approx_art = f.read()
    print("Approx Art:")
    print(approx_art)
    print()

    print("Current diff: {}".format(diff(target_art, approx_art)))
    print("Starting search...")

    private_key, public_key = generate_key()
    art = get_randomart(public_key)
    print(art)