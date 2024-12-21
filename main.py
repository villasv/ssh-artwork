from pathlib import Path
from operator import add
from functools import reduce
from multiprocessing import Pool
from tqdm import tqdm
from crypto import generate_key
from randomart import generate_key_art

HEAVY_SET = {"B", "O", "X", "@", "%", "&", "#", "/", "^", "S", "E"}
LIGHT_SET = {".", "o", "+", "=", "*"}


def diff(a_art: str, b_art: str) -> int:
    def diff_coin_pair(pair: tuple) -> int:
        a, b = pair
        if a == b:
            return 0
        if (a in LIGHT_SET and b in LIGHT_SET) or (a in HEAVY_SET and b in HEAVY_SET):
            return 1
        if (a in LIGHT_SET and b in HEAVY_SET) or (a in HEAVY_SET and b in LIGHT_SET):
            return 2
        if (a == " " and b in LIGHT_SET) or (a in LIGHT_SET and b == " "):
            return 50
        if (a == " " and b in HEAVY_SET) or (a in HEAVY_SET and b == " "):
            return 100

        raise ValueError(f"Unexpected character pair: '{a}'<>'{b}'")

    return reduce(add, map(diff_coin_pair, zip(a_art, b_art)))


arts_dir = Path("./arts")
keys_dir = Path("./keys")
keys_dir.mkdir(exist_ok=True, parents=True)


def search(_):
    target_art = (arts_dir / "target.art").read_text()
    art_files = sorted(arts_dir.glob("*.art"))
    best_diff = int(art_files[0].stem)

    private_key, public_key = generate_key()
    new_art = generate_key_art(public_key)
    new_diff = diff(target_art, new_art)

    if new_diff > 2000:  # lame art threshold, don't bother saving
        return

    if new_diff < best_diff:
        print(f"New approximation found! Diff = {new_diff}")
        print(new_art)
        newest_art_file = f"{new_diff}.art"
        Path(arts_dir / newest_art_file).write_text(new_art)

        private_key_file = keys_dir / "id_ed25519"
        private_key_file.write_text(private_key.decode())
        public_key_file = keys_dir / "id_ed25519.pub"
        public_key_file.write_text(public_key.decode())


if __name__ == "__main__":
    attempts = 50_000_000
    with Pool(processes=20) as p:
        list(tqdm(p.imap(search, range(attempts)), total=attempts))
