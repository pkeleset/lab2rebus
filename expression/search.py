import parsing

def search(inp):
    letters = {i: -1 for i in inp if i.isalpha()}
    if len(letters) > 10:
        return None
    
    left_part = inp.split('=')[0]
    left_keys = {ch for ch in left_part if ch.isalpha()}
    left_len = len(left_keys)

    rpn, original_names = parsing.shunting_yard_algorithm(inp)
    leading_letters = set([value[0] for value in original_names.values() if len(value) > 1])

    keys = letters.keys()

    total_weights = {i: 0 for i in keys}
    
    total_weights = {i: 0 for i in keys}
    letter_word_weights = {i: [] for i in keys}
    
    for k, v in original_names.items():
        rev_v = list(reversed(v))
        w = 1

        word_letter_weights = {}
        for i in range(0, len(v)):
            char = rev_v[i]
            word_letter_weights[char] = word_letter_weights.get(char, 0) + w
            total_weights[char] += w
            w *= 10

        for char, weight in word_letter_weights.items():
            letter_word_weights[char].append((k, weight))

    scores = {i: 0 for i in original_names.keys()}

    keys = sorted(keys, key=total_weights.get, reverse=True)
    keys = sorted(keys, key=lambda x: x not in left_keys)  # буквы левой части вперёд

    can_be = {i: [1, 2, 3, 4, 5, 6, 7, 8, 9] if i in leading_letters
              else [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] for i in keys}

    ans = original_names[rpn[-1][0]]  # rpn[-1] - это (псевдоним, код)

    return enumeration(letters, list(keys), 0, left_len, rpn, original_names, [False] * 10,
                       letter_word_weights, can_be, scores, ans)
    


def enumeration(letters, keys, indx, left_len, rpn, original_names, used_digits,
                letter_word_weights, can_be, scores, ans):

    if indx == left_len:  # условие выхода - присвоены все буквы левой части
        if eval_rpn(rpn, scores, ans, letters, used_digits):
            return (letters, rpn, original_names)
        return None

    current_letter = keys[indx]

    for j in can_be[current_letter]:
        if used_digits[j]: continue

        letters[current_letter] = j
        used_digits[j] = True

        for word_alias, weight in letter_word_weights[current_letter]:
            scores[word_alias] += j * weight

        res = enumeration(letters, keys, indx + 1, left_len, rpn, original_names, used_digits,
                          letter_word_weights, can_be, scores, ans)
        if res:
            return res

        # Откат (Backtracking)
        for word_alias, weight in letter_word_weights[current_letter]:
            scores[word_alias] -= j * weight

        letters[current_letter] = -1
        used_digits[j] = False

    return None





def eval_rpn(rpn, scores, ans, letters, used_digits):
    stack = []

    OPERAND_CODE, ACT_CODE, BRACKET_CODE, EQUAL_CODE = 0, 1, 2, 4

    for i in rpn[:-2]:

        if i[1] == OPERAND_CODE: # если OP - берем готовое число из scores и кладем в STACK
            stack.append(scores[i[0]])

        elif i[1] == ACT_CODE: # если ACT - берем 2 операнды из STACK
            if len(stack) < 2: return False # на всякий случай защита стека
            op2 = stack.pop()
            op1 = stack.pop()

            if i[0] == '+': cur_res = op1 + op2
            elif i[0] == '-': cur_res = op1 - op2
            elif i[0] == '*': cur_res = op1 * op2
            elif i[0] == '/':
                if op2 == 0: return False
                cur_res = op1 // op2

            stack.append(cur_res) # кладем результат в STACK

    if len(stack) != 1:
        return False

    # проверяем может ли быть равна правая часть левой
    return can_be_ans(stack[0], ans, letters, used_digits)





def can_be_ans(left, ans, letters, used_digits_):
    if left < 0:
        return False

    left_str = str(left)
    if len(left_str) != len(ans):
        return False

    new_notes = dict()
    used_digits = used_digits_.copy()

    for digit_char, letter in zip(left_str, ans):
        digit = int(digit_char)
        
        current_assigned_digit = letters[letter]

        if current_assigned_digit != -1: # буква уже была определена в левой части уравнения
            
            if current_assigned_digit != digit: # проверяем, совпадает ли её старое значение с текущей цифрой ответа
                return False

        elif letter in new_notes:# буква новая для левой части, но уже встречалась ранее 
            if new_notes[letter] != digit: # проверяем, совпадает ли сохраненное для неё значение
                return False

        else:# абсолютно новая буква, у которой ещё нет закрепленной цифры
            if used_digits[digit]: # проверяем, не занята ли уже эта цифра кем-то другим
                return False
            
            new_notes[letter] = digit
            used_digits[digit] = True

    letters.update(new_notes)
    
    for i in range(10):
        used_digits_[i] = used_digits[i]

    return True

                

