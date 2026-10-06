import sys
import time
sys.setrecursionlimit(40000)
      


####################### УМНОЖЕНИЕ, ДЕЛЕНИЕ #######################
def search_mul_div(simbols, keys, indx, len_, leading_simbols, used_digits):
    global op1, op2, ans, act
    
    if indx == len_:
        op1_val = 0
        for i in reversed(op1): 
            op1_val = op1_val * 10 + simbols[i]
            
        op2_val = 0
        for i in reversed(op2): 
            op2_val = op2_val * 10 + simbols[i]
            
        ans_val = 0
        for i in reversed(ans): 
            ans_val = ans_val * 10 + simbols[i]

        if act == "*" and op1_val * op2_val == ans_val: return True
        if act == "/" and op2_val != 0 and op1_val % op2_val == 0 and op1_val // op2_val == ans_val: return True
        return False

    current_simbol = keys[indx]

    for j in range(0, 10):
        if j == 0 and current_simbol in leading_simbols:
            continue
        
        if not(used_digits & (1 << j)):
            simbols[current_simbol] = j

            if simbols[op1[0]] != -1 and simbols[op2[0]] != -1 and simbols[ans[0]] != -1:
                if (simbols[op1[0]] * simbols[op2[0]]) % 10 != simbols[ans[0]]:
                    simbols[current_simbol] = -1
                    continue

            if search_mul_div(simbols, keys, indx + 1, len_, leading_simbols, (used_digits | (1 << j))):
                return True

            simbols[current_simbol] = -1


    return False
####################### УМНОЖЕНИЕ, ДЕЛЕНИЕ #######################


####################### СЛОЖЕНИЕ, ВЫЧИТАНИЕ #######################
def search_add_sub(simbols, keys, indx, len_, leading_simbols, used_digits, weights, score):
    
    if indx == len_:
        return score == 0

    current_simbol = keys[indx]

    max_remaining_potential = sum(abs(weights[keys[k]]) * 9 for k in range(indx + 1, len_)) # верхняя примерная граница потенциала неназначенных букв, кроме keys[indx]

    for j in range(0, 10):
        if j == 0 and current_simbol in leading_simbols:
            continue
        
        if not (used_digits & (1 << j)):

            ## score + j * weights[current_simbol] - score, который будет, если назначить текущему символу в соответсвие цифру j
            if abs(score + j * weights[current_simbol]) > max_remaining_potential:
                continue
            
            simbols[current_simbol] = j



            if search_add_sub(simbols, keys, indx + 1, len_, leading_simbols, (used_digits | (1 << j)), weights, score + j * weights[current_simbol]):
                return True

            simbols[current_simbol] = -1

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
    parts = [p for p in parts if p]

    simbols = {char: -1 for char in ''.join(parts)}
    
    keys = list(simbols.keys())

    op1 = parts[0][::-1]
    op2 = parts[1][::-1]
    ans = parts[-1][::-1]

    leading_simbols = {op1[-1], op2[-1], ans[-1]} ## set

    found = None

    if act == '*' or act == '/':
        tail_simbols = {op1[0], op2[0], ans[0]}
        keys.sort(key=lambda char: char in tail_simbols, reverse=True)
        keys.sort(key=lambda char: char in leading_simbols, reverse=True)
        found = search_mul_div(simbols, keys, 0, len(simbols), leading_simbols, 0)## used_digits - маска

        
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

        keys.sort(key=lambda char: abs(weights.get(char, 0)), reverse=True) ## сортируем в порядке убывания модулей весов
        keys.sort(key=lambda char: char in leading_simbols, reverse=True)
                
        found = search_add_sub(simbols, keys, 0, len(simbols), leading_simbols, 0, weights, 0)## used_digits - маска


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
    #inp = "CROSS + ROADS = DANGER"
    inp = "NWAQ * NVI = VSBQNSV"
    
    ###########################
    start = time.process_time()
    ###########################

    search(inp)

    stop = time.process_time()
    print(stop-start)

main()
