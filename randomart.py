# Derived from https://github.com/natmchugh/drunken-bishop
# Licensed under MIT
# Copyright (c) 2015 Nathaniel McHugh, 2018 Victor Villas

import base64
import hashlib
import math


def generate_key_art(public_key, digest="SHA256"):
    key_prefix, key_encoded = public_key.split(b" ", 2)
    key_decoded = base64.b64decode(key_encoded)
    hash_fn = {
        "SHA256": hashlib.sha256,
        "MD5": hashlib.md5,
    }[digest]
    key_type_name = {
        b"ssh-rsa": "RSA",
        b"ssh-dss": "DSA",
        b"ecdsa-sha2-nistp256": "ECDSA 256",
        b"ssh-ed25519": "ED25519 256",
    }[key_prefix]

    if key_prefix == b"ssh-rsa":
        key_type_name += " %s" % get_rsa_key_length(key_decoded)

    key_digest = hash_fn(key_decoded).hexdigest()
    hash_blocks = [int(key_digest[i : i + 8], 16) for i in range(0, len(key_digest), 8)]
    return str(Fingerprint(hash_blocks, key_type_name, digest))


def get_rsa_key_length(key):
    hex_str = key.encode("hex")
    start = 8
    typeLength = int(hex_str[0:start], 16)
    start += typeLength * 2
    lengthExponent = int(hex_str[start : start + 8], 16)
    start += 8 + 2 * lengthExponent
    lengthKey = int(hex_str[start : start + 8], 16)
    start += 8
    key = hex_str[start : start + 2 * lengthKey]
    n = int(key, 16)
    return int(math.log(n, 2)) + 1


class Bishop:
    def __init__(self, pos):
        self.pos = pos

    def coords(self):
        x = self.pos % 17
        y = int(math.floor(self.pos / 17))
        return [x, y]

    def type(self):
        [x, y] = self.coords()
        if y == 0:
            if x == 0:
                return "a"
            if x == 16:
                return "b"
            return "T"
        if x == 0:
            if y == 8:
                return "c"
            return "L"
        if x == 16:
            if y == 8:
                return "d"
            return "R"
        if y == 8:
            return "B"
        return "M"

    def move(self, step):
        w = 0
        squareType = self.type()
        # quite literally corner cases
        if "a" == squareType:
            w = {0: 18, 1: 17, 2: 1}.get(step, 0)
        if "b" == squareType:
            w = {0: 17, 1: 16, 3: 1}.get(step, 0)
        if "c" == squareType:
            w = {0: 1, 2: -16, 3: -17}.get(step, 0)
        if "d" == squareType:
            w = {1: -1, 2: -17, 3: -18}.get(step, 0)
        if "R" == squareType and step % 2 == 1:
            w = -1
        if "T" == squareType and step < 2:
            w = 17
        if "B" == squareType and step > 1:
            w = -17
        if "L" == squareType and step % 2 == 0:
            w = 1
        d = {
            0: -18,
            1: -16,
            2: 16,
            3: 18,
        }[step]
        self.pos += d + w

    def location(self):
        return self.pos


class Atrium:
    def __init__(self, bishop, key_type, digest):
        self.bishop = bishop
        self.counts = [0] * 153
        self.counts[76] = 15
        self.key_type = key_type
        self.digest = digest

    def move(self, step):
        self.bishop.move(step)
        if self.counts[self.bishop.location()] < 15:
            self.counts[self.bishop.location()] += 1

    def stop(self, step):
        self.bishop.move(step)
        self.counts[self.bishop.location()] = 16

    def coin(self, count):
        return {
            0: " ",
            1: ".",
            2: "o",
            3: "+",
            4: "=",
            5: "*",
            6: "B",
            7: "O",
            8: "X",
            9: "@",
            10: "%",
            11: "&",
            12: "#",
            13: "/",
            14: "^",
            15: "S",
            16: "E",
        }.get(count)

    def draw(self):
        type_str = "[" + self.key_type + "]-"
        output = "+" + type_str.center(17, "-") + "+\n"
        for idx, val in enumerate(self.counts):
            coin = self.coin(val)
            if idx % 17 == 0:
                output += "|"
            output += coin
            if (idx + 1) % 17 == 0:
                output += "|\n"
        hash_str = "[" + self.digest + "]"
        output += "+" + hash_str.center(17, "-") + "+"
        return output


class Fingerprint:
    def __init__(self, hash, key_type, digest):
        bishop = Bishop(76)
        self.atrium = Atrium(bishop, key_type, digest)
        moves = self.hash_to_moves(hash)
        lastmove = moves.pop()
        for move in moves:
            self.atrium.move(move)
        self.atrium.stop(lastmove)

    def __str__(self):
        return self.atrium.draw()

    def hash_to_moves(self, hash):
        moves = []
        for word in hash:
            for pair in (3, 2, 1, 0):
                shift = pair * 8
                byte = (word & (255 << shift)) >> shift
                for step in range(0, 8, 2):
                    mask = 3 << step
                    move = (byte & mask) >> step
                    moves.append(move)
        return moves
