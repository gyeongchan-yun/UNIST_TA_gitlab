import sys
import os
from random import randint


def generate_task2_test(dir_path):
    pass


def generate_task3_test(dir_path):
    word_num_map = {'apple': 10, 
                'orange': 9, 
                'strawberry': 8, 
                'pineapple': 7, 
                'banana': 6,
                'melone': 5,
                'pear': 4,
                }
    word_map = ['apple', 
                 'orange', 
                 'strawberry', 
                 'pineapple', 
                 'banana', 
                 'melone', 
                 'pear',
                ]
    total_word_num = sum(word_num_map.values())

    with open(os.path.join(dir_path, "task3-input.txt"), "w") as f:
        num_word_written = 0
        while True:
            if num_word_written == total_word_num:
                break

            idx = randint(0, len(word_map)-1)
            if word_num_map[word_map[idx]] != 0:
                f.write(word_map[idx]+'\n')
                word_num_map[word_map[idx]] -= 1
                num_word_written += 1       


def main():
    if len(sys.argv) < 2:
        print("USAGE: python test_file_generator.py [dir_path]")
        exit(0)

    dir_path = sys.argv[1]
    if not os.path.isdir(dir_path):
        print("The directory doesn't exist.")
        exit(0)

    generate_task2_test(dir_path)
    generate_task3_test(dir_path)


if __name__ == "__main__":
    main() 
