import search
import time


def print_solution(letters, inp):
    for char in inp:
        if char.isalpha():
            print(letters[char], end="")
        else:
            print(char, end="")
    print() # Перенос строки в конце


def main():
    with open("test.txt", "r") as file:
        lines = file.readlines()

    for i in lines:
        if i[0]=='#':
            continue
        rebus = i.strip()
        if not rebus:
            continue


        ###########################
        start = time.process_time()
        ###########################
        result = search.search(rebus)
        
        if result:
            letters, rpn, original_names = result
            print_solution(letters, rebus)            
        else:
            print("no solution")

        ###########################
        stop = time.process_time()
        print(stop-start)
        ###########################
            
main()
