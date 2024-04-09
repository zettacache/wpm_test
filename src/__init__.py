import sys
from wpm_test import WpmTester


def main(word_list: str, amount: int):
    world_list_contents = None

    try:
        with open(word_list) as f:
            world_list_contents = f.read().split("\n")
    except IOError:
        print("Invalid word list.")
        return

    wpm_tester = WpmTester(world_list_contents, amount)
    wpm_tester.start()


if __name__ == "__main__":
    word_list_path = sys.argv[1]
    amount_of_words = sys.argv[2]

    try:
        amount_of_words = int(amount_of_words)
    except ValueError:
        print("Invalid word amount.")
        amount_of_words = -1

    if amount_of_words >= 1:
        main(word_list_path, amount_of_words)
