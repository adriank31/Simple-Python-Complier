# Step 2: Lexer using `ply`
import ply.lex as lex

# List of token names. This is always required
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN'
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Step 3: Parser using `ply`
import ply.yacc as yacc

# Parsing rules

# The grammar for our language
def p_expr(p):
    '''expr : expr PLUS term
            | expr MINUS term'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expr_term(p):
    'expr : term'
    p[0] = p[1]

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor(p):
    '''factor : NUMBER
              | LPAREN expr RPAREN'''
    if len(p) == 2:
        p[0] = ('number', p[1])
    else:
        p[0] = p[2]

def p_error(p):
    print("Syntax error")

# Build the parser
parser = yacc.yacc()

# Step 5-7: Intermediate Representation, Optimization, and Code Generation using `llvmlite`
from llvmlite import ir, binding

# Generate LLVM IR code from AST
def generate_code(ast):
    module = ir.Module(name="my_module")
    func_type = ir.FunctionType(ir.IntType(32), [])
    func = ir.Function(module, func_type, name="main")
    block = func.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    def compile_expr(expr):
        if expr[0] == 'number':
            return ir.Constant(ir.IntType(32), expr[1])
        elif expr[0] == 'binop':
            left = compile_expr(expr[2])
            right = compile_expr(expr[3])
            if expr[1] == '+':
                return builder.add(left, right, name="addtmp")
            elif expr[1] == '-':
                return builder.sub(left, right, name="subtmp")
            elif expr[1] == '*':
                return builder.mul(left, right, name="multmp")
            elif expr[1] == '/':
                return builder.sdiv(left, right, name="divtmp")

    result = compile_expr(ast)
    builder.ret(result)

    return module

# Initialize LLVM
binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()

# Compile AST to executable
def compile_to_executable(ast, output_filename):
    module = generate_code(ast)
    llvm_ir = str(module)

    target = binding.Target.from_default_triple()
    target_machine = target.create_target_machine()
    with open(output_filename + ".o", 'wb') as obj_file:
        obj_file.write(target_machine.emit_object(module))
    
    import subprocess
    subprocess.call(["gcc", output_filename + ".o", "-o", output_filename])

# Example usage
code = "3 + 4 * (2 - 1)"
ast = parser.parse(code)
compile_to_executable(ast, "output")

# You can run the output executable by calling `./output` on a Unix-like system
