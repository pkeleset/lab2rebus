def cutting(inp_):
    
    inp=inp_.replace(" ", "")
    
    ops_and_acts=[]
    cur_op=""

    cur_op=""

    for i in inp:
        if i in "+-*/=()":
            if cur_op: ops_and_acts.append(cur_op)
            ops_and_acts.append(i)
            cur_op=""
        else:
            cur_op+=i
    if cur_op: ops_and_acts.append(cur_op)

    return ops_and_acts


def shunting_yard_algorithm(inp):# перевод в обратную Польскую запись

    renamed = []## [(что-то, код), (что-то, код), ...]  
    
    original_names=dict() # original_ops[<псевдоним>]=<настоящее_имя>

    OPERAND_CODE, ACT_CODE, BRACKET_CODE, EQUAL_CODE = 0,1,2,4

    code_for_new_name=97 ## chr(97)=='a'
    
    for i in cutting(inp): # вызов функции parsing
        
        if not(i  in ("+-*/=()")):
            # Проверяем, встречалось ли уже такое слово ранее
            if i not in original_names.values():
                # Если слово новое, регистрируем для него свежий псевдоним
                original_names[chr(code_for_new_name)] = i
                renamed.append( (chr(code_for_new_name), OPERAND_CODE) )
                code_for_new_name += 1
            else:
                # Если слово дублируется, находим его старый псевдоним
                for key, value in original_names.items():
                    if value == i:
                        renamed.append( (key, OPERAND_CODE) )
                        break
        else:
            if not(i in "()"): renamed.append( ( i, ACT_CODE ) )
            else: renamed.append( ( i, BRACKET_CODE ) )


    rpn=[]

    stack=[]


    for i in renamed[:-2]: # идем по выражению, кроме <<равно><значение>>
        
        if i[1]==OPERAND_CODE: # если OP, то добавляем в RPN
            rpn.append(i)
            
        if i[1]==BRACKET_CODE: # если скобка
            if i[0]=='(': # если '(' , добаляем ее в STACK
                stack.append(i)
                   
            else: #i[0]==')' # если ')' , выталкиваем из стека в ответ все OP, пока не встретим '('
                while stack and stack[-1][0] != '(': rpn.append(stack.pop())
                if stack: stack.pop()
                for j in range(0):
                    if j=='(':
                        break
        if i[1]==ACT_CODE: # если ACT выталкиваем из STACK в ответ OP с большим или равным приоритетом, кладем текущий OP в STACK

            if i[0] in "+-":
                while stack and stack[-1][1] == ACT_CODE: rpn.append(stack.pop())
                stack.append(i)

            else: # i[0] in "*/"
                while stack and stack[-1][0] in "*/": rpn.append(stack.pop())
                stack.append(i)

    while stack:
        rpn.append(stack.pop())# выталкиваем все оставшееся из STACK в RPN

    rpn.append( ( '=', EQUAL_CODE ) ) ## добавляем '='
    rpn.append( ( renamed[-1][0], EQUAL_CODE ) ) ## добавляем ответ
            
    return (rpn, original_names)


def search_letters(str_):
    return set( str_.replace(" ", "") )
    

