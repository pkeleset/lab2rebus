import sys
import time
sys.setrecursionlimit(40000)

op1 = act = op2 = ans = None      


####################### УМНОЖЕНИЕ, ДЕЛЕНИЕ #######################
def search_mul_div(simbols, keys, indx, len_, leading_simbols, used_digits):
    
    if indx == len_:
        op1_val = sum([simbols[op1[i]] * (10**i) for i in range(len(op1))])
        op2_val = sum([simbols[op2[i]] * (10**i) for i in range(len(op2))])
        ans_val = sum([simbols[ans[i]] * (10**i) for i in range(len(ans))])

        if act == "*" and op1_val * op2_val == ans_val: return True
        if act == "/" and op2_val != 0 and op1_val % op2_val == 0 and op1_val // op2_val == ans_val: return True
        return False

    current_simbol = keys[indx]

    for j in range(0, 10):
        if j == 0 and current_simbol in leading_simbols:
            continue
        
        if not(used_digits[j]):
            simbols[current_simbol] = j
            used_digits[j] = True

            if search_mul_div(simbols, keys, indx + 1, len_, leading_simbols, used_digits):
                return True

            simbols[current_simbol] = -1
            used_digits[j] = False

    return False
####################### УМНОЖЕНИЕ, ДЕЛЕНИЕ #######################


####################### СЛОЖЕНИЕ, ВЫЧИТАНИЕ #######################
def search_add_sub(simbols, keys, indx, len_, leading_simbols, used_digits, weights, score):
    
    if indx == len_:
        return score == 0

    current_simbol = keys[indx]

    for j in range(0, 10):
        if j == 0 and current_simbol in leading_simbols:
            continue
        
        if not used_digits[j]:
            simbols[current_simbol] = j
            used_digits[j] = True

            if search_add_sub(simbols, keys, indx + 1, len_, leading_simbols, used_digits, weights, score + j * weights[current_simbol]):
                return True

            simbols[current_simbol] = -1
            used_digits[j] = False

    return False
####################### СЛОЖЕНИЕ, ВЫЧИТАНИЕ #######################


#######################               #######################
####################### РАСПРЕДЕЛЕНИЕ #######################
#######################               #######################
def search(inp):
    
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

    leading_simbols = {op1[-1], op2[-1], ans[-1]} ## set



    found = None

    if act == '*' or act == '/':
        found = search_mul_div(simbols, keys, 0, len(simbols), leading_simbols, [False] * 10)
    else: ## act == '+' or act == '-'
        weights={}
        
        for i in range(0, len(op1)):
            if op1[i] in weights:
                weights[op1[i]]+=10**i
            else:
                weights[op1[i]]=10**i

        for i in range(0, len(op2)):
            if op2[i] in weights:
                if act=='+': weights[op2[i]]+=10**i
                else: weights[op2[i]]-=10**i
            else:
                if act=='+': weights[op2[i]]=10**i
                else: weights[op2[i]] = -1 * 10**i ## act=='-'

        for i in range(0, len(ans)):
            if ans[i] in weights:
                weights[ans[i]] -= 10**i
            else:
                weights[ans[i]] = -1 * 10**i
                
        found = search_add_sub(simbols, keys, 0, len(simbols), leading_simbols, [False] * 10, weights, 0)


    if found:
        for i in op1[::-1]: print(simbols[i], end="")
        print(' ' + act + ' ', end="")
        for i in op2[::-1]: print(simbols[i], end="")
        print(' = ', end="")
        for i in ans[::-1]: print(simbols[i], end="")
        print()
    else:
        print("no solution")


#######################               #######################
####################### РАСПРЕДЕЛЕНИЕ #######################
#######################               #######################


def main():
    inp = "CROSS + ROADS = DANGER"
    
    ###########################
    start = time.process_time()
    ###########################

    search(inp)

    stop = time.process_time()
    print(stop-start)

main()
