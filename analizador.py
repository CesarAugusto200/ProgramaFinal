import ply.lex as lex
import ply.yacc as yacc

tokens = [
    'AS',
    'PA',
    'PC',
    'CM',
    # 'CC',
    'CO',
    'LA',
    'LC',
    'OR',
    # 'TP',
    # 'ST',
    # 'IT',
    'ID',
    'NUMBER',
    'SUM',
    'RES'
]

reserved = {
    'int': 'IT',
    'string': 'ST',
    'Fn': 'F',
    # 'contenido': 'C',
    'print': 'PRT',
    'if': 'I',
    'else': 'E',
    'while': 'W',
    'switch': 'SW',
    'case': 'CE',
    'default': 'DT',
    'break': 'BR',
    'rtn': 'RT',
}

tokens += list(reserved.values())

errores = []

# t_TP = r'int|string'
t_PA = r'\('
t_PC = r'\)'
t_LA = r'\{'
t_LC = r'\}'
t_CM = r'"'
# t_CC = r'"'
t_CO = r','
t_AS = r'=>'
t_OR = r'(>=|<=|==|!=|>|<)'
t_SUM = r'\++'
t_RES = r'\--'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # r'[a-zA-Z][a-zA-Z]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    mensaje_error = f"Carácter desconocido'{t.value[0]}'"
    errores.append(mensaje_error)
    t.lexer.skip(1)

lexer = lex.lex()


global nombrevar
global valorvar
global tipovar
global nombreint
global valorint
global tipoint
    
def p_PX(p):
    '''PX : variablestring 
        | variableint 
        | fnsinparam1 
        | fnsinparam2 
        | fnsinparam3
        | fnsinparam4
        | fncon1param1
        | fncon1param2
        | fncon2param1
        | while1 
        | while2 
        | if1 
        | if2 
        | ifelse1
        | ifelse2
        | switch'''

def p_variableaux(p):
    '''variableaux : ID AS ST PA CM ID CM PC'''
    global nombreaux
    global valoraux
    global tipoaux
    
    nombreaux = p[1]
    valoraux = p[6]
    tipoaux = p[3]
    aux = p[6]
    
    if isinstance(aux, str) and p[3] == 'string':
        print(f"Variable: {nombreaux} - valor: {aux}")
    else:
        print(f"Sintax error en: {nombreaux} - con valor {aux}")

def p_variablestring(p):
    '''variablestring : ID AS ST PA CM ID CM PC'''
    global nombrevar
    global valorvar
    global tipovar
    
    nombrevar = p[1]
    valorvar = p[6]
    tipovar = p[3]
    aux = p[6]
    
    if isinstance(aux, str) and p[3] == 'string':
        print(f"Variable: {nombrevar} - valor: {aux}")
    else:
        print(f"Sintax error en: {nombrevar} - con valor {aux}")

def p_variableint(p):
    '''variableint : ID AS IT PA NUMBER PC'''
    global nombreint
    global valorint
    global tipoint
    
    nombreint = p[1]
    valorint = p[5]
    tipoint = p[3]
    aux = p[5]
    if isinstance(aux, int) and p[3] == 'int':
        print(f"Variable: {nombreint} - valor: {aux}")
    else:
        print(f"Sintax error en: {nombreint} - con valor {aux}")
    
# CADENAS 
def p_fnsinparam1(p):
    '''fnsinparam1 : F AS ID PA PC LA PRT PA CM ID CM PC LC'''
    print(f"Fn: {p[10]}")
    

# VARIABLES ------------------
def p_fnsinparam2(p):
    '''fnsinparam2 : F AS ID PA PC LA variablestring PRT PA ID PC LC'''
    
    if nombrevar == p[10]:
        print(f"Fn2: {valorvar}")
    else:
        print(f"Error variable: {nombrevar} - desconocida {valorvar}")

def p_fnsinparam4(p):
    '''fnsinparam4 : F AS ID PA PC LA variableint PRT PA ID PC LC'''
    
    if nombreint == p[10]:
        print(f"Fn2: {valorint}")
    else:
        print(f"Error variable: {nombreint} - desconocida {valorint}")
        
# NUMEROS 
def p_fnsinparam3(p):
    '''fnsinparam3 : F AS ID PA PC LA PRT PA NUMBER PC LC'''
    print(f"Fn: {p[9]}")

def p_fncon1param1(p):
    '''fncon1param1 : variablestring F AS ID PA ST ID PC LA PRT PA ID PC LC'''
    
    param = p[7]
    print_param = p[12]
    tipo_variable = p[6]
    
    if tipo_variable == tipovar:
        if param == print_param == nombrevar:
            print(valorvar)
        else:
            print(f"Error: Variable no coincide con parametro: {param}")
    else:
        print(f"Tipo valor de variable: {tipovar} no coincide con parametro {tipo_variable}")

def p_fncon1param2(p):
    '''fncon1param2 : variableint F AS ID PA IT ID PC LA PRT PA ID PC LC'''

    param = p[7]
    print_param = p[12]
    tipo_variable = p[6]
    
    if tipo_variable == tipoint:
        if param == print_param == nombreint:
            print(valorint)
        else:
            print(f"Error: Variable no coincide con parametro: {param}")
    else:
        print(f"Tipo valor de variable: {tipoint} no coincide con parametro {tipo_variable}")

def p_fncon2param1(p):
    '''fncon2param1 : variableint variablestring F AS ID PA IT ID CO ST ID PC LA PRT PA ID PC PRT PA ID PC LC'''
    
    tipo_param1 = p[7]
    param1 = p[8]
    tipo_param2 = p[10]
    param2 = p[11]
    print_param1 = p[16]
    print_param2 = p[20]

    if tipoint == tipo_param1 and tipovar == tipo_param2:
        if param1 == nombreint == print_param1 and param2 == nombrevar == print_param2:
            print(valorint)
            print(valorvar)
        else:
            print(f"Error Variables -> {nombreint, nombrevar} No coinciden con parametros: {param1, param2}")
    else:
        print(f"Error: Tipo de parametro no coincide con: {param1, param2}")



def p_while1(p):
    '''while1 : variableint W PA ID OR NUMBER PC AS LA ID SUM PRT PA CM ID CM PC LC'''
    
    variable_name = p[4]  # El ID de la variable usada en la condición
    operator = p[5]       # Operador de comparación
    comparison_value = p[6]  # Valor para comparación
    increment_variable = p[10] # La variable a incrementar
    
    # Asegurar que la variable de incremento y la variable en la condición son la misma
    if variable_name != increment_variable != nombreint:
        print(f"Error: variable de control del bucle '{variable_name}' y variable de incremento '{increment_variable}' no coinciden")
        return
    
    tabla_operadores = {
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '==': lambda x, y: x == y,
        '<=': lambda x, y: x <= y,
        '>=': lambda x, y: x >= y,
        '!=': lambda x, y: x != y,
    }
    
    variable_value = valorint
    condition_result = tabla_operadores[operator](variable_value, comparison_value)

    while condition_result:
        variable_value += 1
        print(p[15])
        condition_result = tabla_operadores[operator](variable_value, comparison_value)

def p_while2(p):
    '''while2 : variableint variablestring W PA ID OR NUMBER PC AS LA ID SUM PRT PA ID PC LC'''
    variable_name = p[5]
    operador = p[6]
    valor_comparacion = p[7]
    variable_incremento = p[11]
    
    tabla_operadores = {
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '==': lambda x, y: x == y,
        '<=': lambda x, y: x <= y,
        '>=': lambda x, y: x >= y,
        '!=': lambda x, y: x != y,
    }
    
    if variable_name != variable_incremento != nombreint:
        print(f"Error: variable de control del bucle '{variable_name}' y variable de incremento '{variable_incremento}' no coinciden")
        return

    variable_value = valorint
    condicion_result = tabla_operadores[operador](variable_value, valor_comparacion)    
    
    while condicion_result:
        variable_value += 1
        print(valorvar)
        condicion_result = tabla_operadores[operador](variable_value, valor_comparacion)

def p_if1(p):
    '''if1 : variableint I PA ID OR NUMBER PC AS LA PRT PA CM ID CM PC LC'''

    variable_comparacion = p[4]
    operador = p[5]
    valor_comparacion = p[6]

    tabla_operadores = {
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '==': lambda x, y: x == y,
        '<=': lambda x, y: x <= y,
        '>=': lambda x, y: x >= y,
        '!=': lambda x, y: x != y,
    }
    
    valorif = valorint
    condicion_if = tabla_operadores[operador](valorif, valor_comparacion)
    
    if nombreint == variable_comparacion:
        if condicion_if:
            print(p[13])
    else:
        print(f"Error variable:{variable_comparacion} o {nombreint} no coinciden")
    
    
def p_if2(p):
    '''if2 : variableint variablestring I PA ID OR NUMBER PC AS LA PRT PA ID PC LC'''
    
    variable_comparacion = p[5]
    operador = p[6]
    valor_comparacion = p[7]
    
    tabla_operadores = {
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '==': lambda x, y: x == y,
        '<=': lambda x, y: x <= y,
        '>=': lambda x, y: x >= y,
        '!=': lambda x, y: x != y,
    }
    
    valorif = valorint
    
    condicion = tabla_operadores[operador](valorif, valor_comparacion)
    if nombreint == variable_comparacion:
        if condicion:
            if nombrevar == p[13]:
                print(valorvar)
            else:
                print(f"Variable {nombrevar} no coincide con {p[13]}")
    else:
        print(f"Error variable:{variable_comparacion} o {nombreint} no coinciden")

def p_ifelse1(p):
    '''ifelse1 : variableint I PA ID OR NUMBER PC AS LA PRT PA CM ID CM PC LC E AS LA PRT PA CM ID CM PC LC'''

    variable_comparacion = p[4]
    operador = p[5]
    valor_comparacion = p[6]

    tabla_operadores = {
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '==': lambda x, y: x == y,
        '<=': lambda x, y: x <= y,
        '>=': lambda x, y: x >= y,
        '!=': lambda x, y: x != y,
    }  
    
    valorifelse = valorint
    
    condicion = tabla_operadores[operador](valorifelse, valor_comparacion)
    
    if nombreint == variable_comparacion:
        if condicion:
            print(p[13])
        else:
            print(p[23])
    else:
        print(f"Error variable:{variable_comparacion} o {nombreint} no coinciden")

def p_ifelse2(p):
    '''ifelse2 : variableaux variablestring variableint I PA ID OR NUMBER PC AS LA PRT PA ID PC LC E AS LA PRT PA ID PC LC'''
    
    variable_comparacion = p[6]
    operador = p[7]
    valor_comparacion = p[8]
    
    tabla_operadores = {
        '>': lambda x, y: x > y,
        '<': lambda x, y: x < y,
        '==': lambda x, y: x == y,
        '<=': lambda x, y: x <= y,
        '>=': lambda x, y: x >= y,
        '!=': lambda x, y: x != y,
    }  
    
    valorifelse = valorint
    
    condicion = tabla_operadores[operador](valorifelse, valor_comparacion)
    
    if nombreint == variable_comparacion:
        if condicion:
            if nombrevar == p[14]:
                print(valorvar)
            else:
                print(f"Variable {nombrevar} no coincide con {p[14]}")
        else:
            if nombreaux == p[22]:
                print(valoraux)
            else:
                print(f"Variable {nombreaux} no coincide con {p[22]}")
    else:
        print(f"Error variable:{variable_comparacion} o {nombreint} no coinciden")
    
def p_switch(p):
    '''switch : variableint SW PA ID PC AS LA CE NUMBER AS LA PRT PA CM ID CM PC BR LC CE NUMBER AS LA PRT PA CM ID CM PC BR LC DT AS LA PRT PA CM ID CM PC LC LC'''
    
    switch_variable = p[4]
    case1_value = p[9]
    case1_print = p[15]
    case2_value = p[21]
    case2_print = p[27]
    default_print = p[38]   

    if switch_variable == nombreint:
        variable_value = valorint
        
        if variable_value == case1_value:
            print(case1_print)
        elif variable_value == case2_value:
            print(case2_print)
        else:
            print(default_print)
    else:
        print(f"Error: variable '{switch_variable}' no definida")
    
def p_error(p):
    if p:
        errores.append(f"Error de sintaxis en '{p.value}'")
    else:
        errores.append("Error de sintaxis al final de la entrada")

parser = yacc.yacc()

def analizar(texto):
    # limpiar la lista de errores antes de cada análisis
    errores.clear()
    lexer.input(texto)
    tokens = []
    for token in lexer:
        tokens.append((token.type, token.value))
    parser.parse(texto)
    # Retorna la lista de errores para que pueda ser usada por la interfaz gráfica
    return errores, tokens