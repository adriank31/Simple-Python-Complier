**Lexer**:

Imports and Token Definitions: Import ply.lex and define tokens for numbers and arithmetic operators.

Token Rules: Define regular expressions for each token and a rule to handle numbers, converting them to integers.

Error Handling: Define how to handle illegal characters.

Build Lexer: Build the lexer using lex.lex().

**Parser**:

Imports and Parsing Rules: Import ply.yacc and define parsing rules for expressions, terms, and factors based on the grammar.

Error Handling: Define how to handle syntax errors.

Build Parser: Build the parser using yacc.yacc().

**LLVM IR Generation**:

Import llvmlite: Import ir and binding from llvmlite.

Generate LLVM IR: Define a function generate_code to generate LLVM IR code from the AST.

Compile Expressions: Define a helper function compile_expr to compile expressions in the AST to LLVM IR.

Compile to Executable: Define a function compile_to_executable to compile the AST to an executable file using gcc.

**Compilation to Executable**:
Generates an object file from the LLVM IR and uses gcc to produce an executable.
