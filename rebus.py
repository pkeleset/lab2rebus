import sys
import time
sys.setrecursionlimit(40000)

op1 = op2 = ans = act = None

def search(simbols, keys, indx, len_):
    if indx == len_ and simbols[op1[-1]] != 0 and simbols[op2[-1]] != 0 and simbols[ans[-1]] != 0:
        op1_val = sum([simbols[op1[i]] * (10**i) for i in range(len(op1))])
        op2_val = sum([simbols[op2[i]] * (10**i) for i in range(len(op2))])
        ans_val = sum([simbols[ans[i]] * (10**i) for i in range(len(ans))])

        if act == "+" and op1_val + op2_val == ans_val: return True
        if act == "-" and op1_val - op2_val == ans_val: return True
        if act == "*" and op1_val * op2_val == ans_val: return True
        if act == "/" and op2_val != 0 and op1_val % op2_val == 0 and op1_val // op2_val == ans_val: return True
        return False

    if indx == len_:
        return False

    current_letter = keys[indx]

    for j in range(0, 10):
        if j not in simbols.values():
            simbols[current_letter] = j

            if search(simbols, keys, indx + 1, len_):
                return True

            simbols[current_letter] = -1

    return False


def main():
    #inp = input().strip()
    inp = "CROSS + ROADS = DANGER"
    
    ###########################
    start = time.process_time()
    ###########################
    
    global op1, op2, ans, act

    inp = inp.replace(' ', '')

    for ch in inp:
        if ch in '+-*/':
            act = ch
            break

    for ch in '+-*/=':
        inp = inp.replace(ch, '_')

    parts = inp.split('_')

    simbols = {char: -1 for char in ''.join(parts)}
    keys = list(simbols.keys())

    op1 = parts[0][::-1]
    op2 = parts[1][::-1]
    ans = parts[-1][::-1]

    found = search(simbols, keys, 0, len(simbols))

    if found:
        for i in op1[::-1]: print(simbols[i], end="")
        print(' ' + act + ' ', end="")
        for i in op2[::-1]: print(simbols[i], end="")
        print(' = ', end="")
        for i in ans[::-1]: print(simbols[i], end="")
        print()
    else:
        print("no solution")

    stop = time.process_time()
    print(stop-start)
main()
