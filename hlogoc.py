import sys
from lark import Lark, tree, Token, Transformer, v_args

# Comprobación de los parámetros de entrada
if len(sys.argv) != 2:
    print(r'''
          // Wrong number of parameters!      \\
          \\ python hlogoc.py inputfile.hlogo //
          -------------------------------------
          \  ^__^
          \  (oo)\_______
             (__)\       )\/\\
                 ||----ww|
                 ||     ||
    ''')

# Definición de la gramática para el lenguaje High-LOGO
# La gramática se divide en varias partes:
# - `start`: Inicia con una o más instrucciones básicas
# - `basic_instruction`: Es una instrucción que puede ser un comando de movimiento (FD, BK, LT, RT, WIDTH) o un comando de lápiz (PU, PD)
# - `move_instruction`: Instrucción que mueve la tortuga (FD, BK, LT, RT, WIDTH)
# - `PEN`: Comando para levantar o bajar el lápiz (PU, PD)
# - `INTNUM`: Representa números enteros o decimales
# - `%ignore`: Ignora espacios en blanco y saltos de línea
high_logo_grammar = r"""
    start: (basic_instruction | function_def)+

    basic_instruction: move_instruction
                    | PEN
                    | conditional
                    | single_for
                    | double_for
                    | function_call

    function_def: DEF NAME LPAREN param_list? RPAREN block

    function_call: NAME LPAREN arg_list? RPAREN

    param_list: NAME (COMMA NAME)*

    arg_list: expression (COMMA expression)*

    expression: INTNUM | NAME

    conditional: IF boolean_expression block (ELSE block)?

    single_for: SINGLE_FOR VAR IN RANGE LPAREN range_args RPAREN block
    double_for: DOUBLE_FOR VAR COMMA VAR IN ZIP LPAREN range_expr COMMA range_expr RPAREN block

    range_expr: RANGE LPAREN range_args RPAREN

    range_args: INTNUM COMMA INTNUM COMMA INTNUM
              | INTNUM COMMA INTNUM
              | INTNUM

    boolean_expression: "(" boolean_term ")"

    boolean_term: comparison
                | NOT boolean_term
                | boolean_term AND boolean_term
                | boolean_term OR boolean_term
                | "(" boolean_term ")"

    comparison: INTNUM COMPARATOR INTNUM

    block: LBRACE basic_instruction* RBRACE

    move_instruction: MOVEMENT expression

    DEF: "def"
    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    SINGLE_FOR: "for"
    DOUBLE_FOR: "for"
    VAR: /[i-z]/
    IN: "in"
    ZIP: "zip"
    RANGE: "range"
    LPAREN: "("
    RPAREN: ")"
    COMMA: ","
    IF: "if"
    ELSE: "else"
    LBRACE: "{"
    RBRACE: "}"
    MOVEMENT: "FD" | "BK" | "LT" | "RT" | "WIDTH"
    PEN: "PU" | "PD"
    COMPARATOR: "==" | "!=" | "<" | ">" | "<=" | ">="
    NOT: "!"
    AND: "&&"
    OR: "||"
    INTNUM : /-?\d+(\.\d+)?([eE][+-]?\d+)?/

    COMMENT: /#[^\n]*/

    %ignore /[ \t\n\f\r]+/
    %ignore COMMENT
"""
# Diccionario que mapea los comandos High-LOGO a los métodos correspondientes de la tortuga en Python
command_map_move = {
    "FD": "forward",  # "FD" en High-LOGO se mapea a "forward" en Python
    "BK": "backward",  # "BK" en High-LOGO se mapea a "backward" en Python
    "LT": "left",  # "LT" en High-LOGO se mapea a "left" en Python
    "RT": "right",  # "RT" en High-LOGO se mapea a "right" en Python
    "WIDTH": "width"  # "WIDTH" en High-LOGO se mapea a "width" en Python
}

# Diccionario que mapea los comandos de lápiz High-LOGO a los métodos correspondientes de la tortuga en Python
command_map_pen = {
    "PU": "penup",  # "PU" en High-LOGO se mapea a "penup" en Python
    "PD": "pendown"  # "PD" en High-LOGO se mapea a "pendown" en Python
}

# Mapa de operadores de comparación
comparison_map = {
    "==": "==",
    "!=": "!=",
    "<": "<",
    ">": ">",
    "<=": "<=",
    ">=": ">=",
    "!": "not ",
}

def translate_boolean_expression(ast, out=''):
    """Traduce recursivamente expresiones booleanas a Python"""
    if isinstance(ast, Token):
        out+= comparison_map[ast.value] if True else ast.value
        return out

    if ast.data == "boolean_expression":
        return translate_boolean_expression(ast.children[0])

    elif ast.data == "boolean_term":
        if len(ast.children) == 1:
            if isinstance(ast.children[0], Token):
                return ast.children[0].value
            return translate_boolean_expression(ast.children[0])

        # Manejo de NOT
        if ast.children[0] == "!":
            for c in ast.children:
                out = translate_boolean_expression(c, out)

        # Manejo de AND
        elif len(ast.children) == 3 and ast.children[1].type == "AND":
            left = translate_boolean_expression(ast.children[0])
            right = translate_boolean_expression(ast.children[2])
            out += f"({left} and {right})"
            return out

        # Manejo de OR
        elif len(ast.children) == 3 and ast.children[1].type == "OR":
            left = translate_boolean_expression(ast.children[0])
            right = translate_boolean_expression(ast.children[2])
            out += f"({left} or {right})"
            return out

    elif ast.data == "comparison":
        left, op, right = ast.children
        out += f"{left.value} {comparison_map[op.value]} {right.value}"
        return out

    return out

def translate_range_args(args,out = ""):
    """Traduce los argumentos de range a una cadena Python"""
    if isinstance(args, Token):
        return args.value

    if args.data == "range_args":
        for c in args.children:
            out += translate_range_args(c,out)
        return out

# Función para traducir el árbol de sintaxis (AST) generado por el parser
def translate_program(ast, out, indent_level=0):
    indent = "    " * indent_level

    if ast.data == "start":
        out.write("import turtle\n")
        out.write("t = turtle.Turtle()\n\n")

        # Primero procesamos todas las definiciones de funciones
        for c in ast.children:
            if isinstance(c, tree.Tree) and c.data == "function_def":
                translate_program(c, out)

        # Luego procesamos el resto de instrucciones
        for c in ast.children:
            if not (isinstance(c, tree.Tree) and c.data == "function_def"):
                translate_program(c, out)

        out.write("\nturtle.mainloop()\n")

    elif ast.data == "function_def":
        name = ast.children[1].value
        params = []
        if len(ast.children) > 4:
            param_list = ast.children[3]
            if param_list.data == "param_list":
                params = [param.value for param in param_list.children if param.type == "NAME"]

        out.write(f"{indent}def {name}({', '.join(params)}):\n")

        block_node = ast.children[-1]
        for instruction in block_node.children:
            if not isinstance(instruction, Token):
                translate_program(instruction, out, indent_level + 1)
        out.write("\n")

    elif ast.data == "function_call":
        name = ast.children[0].value
        args = []
        if len(ast.children) > 2:
            arg_list = ast.children[2].children
            for arg in arg_list:
                if not isinstance(arg, Token):
                    args.append(arg.children[0].value)
        out.write(f"{indent}{name}({','.join(args)})\n")

    elif ast.data == "basic_instruction":
        if isinstance(ast.children[0], Token):
            out.write(f"{indent}t.{command_map_pen[ast.children[0].value]}()\n")
        else:
            for c in ast.children:
                translate_program(c, out, indent_level)

    elif ast.data == "conditional":
        condition = translate_boolean_expression(ast.children[1])
        out.write(f"{indent}if {condition}:\n")
        translate_program(ast.children[2], out, indent_level + 1)
        if len(ast.children) > 3:
            out.write(f"{indent}else:\n")
            translate_program(ast.children[4], out, indent_level + 1)

    elif ast.data == "single_for":
        var = ast.children[1].value
        range_args = translate_range_args(ast.children[5])
        out.write(f"{indent}for {var} in range({range_args}):\n")
        translate_program(ast.children[7], out, indent_level + 1)

    elif ast.data == "double_for":
        var1 = ast.children[1].value
        var2 = ast.children[3].value
        range_args1 = translate_range_args(ast.children[7].children[2])
        range_args2 = translate_range_args(ast.children[9].children[2])
        out.write(f"{indent}for {var1},{var2} in zip(range({range_args1}), range({range_args2})):\n")
        translate_program(ast.children[11], out, indent_level + 1)

    elif ast.data == "block":
        for instruction in ast.children:
            if not isinstance(instruction, Token):
                translate_program(instruction, out, indent_level)

    elif ast.data == "move_instruction":
        left, right = ast.children
        if isinstance(right, Token):
            value = right.value
        else:
            value = right.children[0].value
        out.write(f"{indent}t.{command_map_move[left.value]}({value})\n")

    else:
        print(f"No implementation for the node: {ast}")
# Verifica que se haya pasado el archivo de entrada como argumento
input_file = sys.argv[1] #sys.argv[1]
output_file = f'{sys.argv[1]}.py' # El archivo de salida tendrá la extensión .py

# Crear el parser usando la gramática definida
parser = Lark(high_logo_grammar)

# Abre el archivo de entrada para leer el código High-LOGO
with open(input_file) as inputFile:
    # Abre el archivo de salida para escribir el código Python generado
    with open(output_file, 'w') as out:
        # Analiza el código High-LOGO y genera el árbol de sintaxis abstracta (AST)
        ast = parser.parse(inputFile.read())
        print(ast.pretty())  # Imprime el árbol de sintaxis abstracta (AST)
        tree.pydot__tree_to_png(ast, "tree.png") # Genera una imagen del árbol de sintaxis abstracta (AST)
        tree.pydot__tree_to_dot(ast, "tree.dot", rankdir="TD") # Genera un archivo DOT del árbol de sintaxis abstracta (AST)
        # Llama a la función que traduce el AST y escribe el código Python en el archivo de salida
        translate_program(ast, out)
