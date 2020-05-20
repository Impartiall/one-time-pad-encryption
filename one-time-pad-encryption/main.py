import requests
from lxml import html
import random
import fire


CHARS = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
    "K": 10,
    "L": 11,
    "M": 12,
    "N": 13,
    "O": 14,
    "P": 15,
    "Q": 16,
    "R": 17,
    "S": 18,
    "T": 19,
    "U": 20,
    "V": 21,
    "W": 22,
    "X": 23,
    "Y": 24,
    "Z": 25,
    "_": 26,
    ".": 27,
}

INVERTED_CHARS = {CHARS[key]: key for key in CHARS}

MODULO = len(CHARS)


def modular_sum(a: str, b: str, mode: str) -> str:
    # Convert strings to ints
    a = CHARS[a]
    b = CHARS[b] if mode == "+" else -CHARS[b]

    n = (a + b) % MODULO

    # Return string from int n
    return INVERTED_CHARS[n]


def normalize_string(s: str) -> str:
    """
    Remove capitalize and remove whitespace from a string.
    Raises an exception for any char in the modified string that is not an accepted char.
    """
    out_string = ""

    for c in s.upper():
        if c in " \n\t":
            continue
        elif c not in CHARS:
            raise ValueError(
                f"The given string '{s}' contains an unrecognized char '{c}'."
            )
        else:
            out_string += c

    return out_string


def get_true_random_seed():
    """
    Use random.org to generate a truly random seed between with bounds +/- 1,000,000,000
    """
    page = requests.get(
        "https://www.random.org/integers/?num=1&min=-1000000000&max=1000000000&col=1&base=10&format=html&rnd=new"
    )
    tree = html.fromstring(page.content)

    seed = tree.xpath('//*[@id="invisible"]/pre/text()')[0].strip("\n")

    return int(seed.strip("\n"))


class OTPTools:
    # TODO: check if length of key and input are compatible
    def encrypt(self, s: str, key: str) -> str:
        """
        Encrypt a given string using OTP encryption.

        s -- the input string
        key -- the OTP key
        """

        s = normalize_string(s)
        key = normalize_string(key)

        if len(s) > len(key):
            raise ValueError("Input string cannot be longer than the key.")

        return "".join(modular_sum(c, key[i], "+") for i, c in enumerate(s))

    def decrypt(self, s: str, key: str) -> str:
        """
        Encrypt a given string using OTP encryption.

        s -- the input string
        key -- the OTP key
        """

        s = normalize_string(s)
        key = normalize_string(key)

        if len(s) > len(key):
            raise ValueError("Input string cannot be longer than the key.")

        return "".join(modular_sum(c, key[i], "-") for i, c in enumerate(s))

    def generate(self, keys: int, key_length: int = 80, filename: str = ""):
        """
        Generate a OTP with a given number of keys of a certain length.

        keys -- the number of keys to be generated
        key_length -- the length of each key (default 100)
        """
        if keys < 1:
            raise ValueError("Number of keys must be greater than zero.")

        out_string = ""

        for i in range(keys):
            random.seed(get_true_random_seed())

            if keys > 1:
                out_string += f"-- OTP KEY {i + 1} --\n\n"

            for j in range(key_length):
                group = "".join(random.choices("".join(CHARS.keys()), k=5))
                out_string += group + " "

            out_string += "\n\n"

        if filename:
            with open(filename, "w") as f:
                f.write(out_string)

        else:
            print(out_string)


if __name__ == "__main__":
    fire.Fire(OTPTools)
