from functools import lru_cache


@lru_cache()
def read_list_of_words():
    with open("words.txt") as file:
        lines = []
        count = 0
        for line in file:
            lines.append(line.strip().upper())
            count += 1
    return lines, count
