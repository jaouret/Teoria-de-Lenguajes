import llvmlite.ir as ir
import llvmlite.binding as llvm

# Crear un módulo LLVM y una función principal
module = ir.Module(name="simple_module")
func_type = ir.FunctionType(ir.IntType(32), [])
main_func = ir.Function(module, func_type, name="main")

# Crear un bloque básico de código
block = main_func.append_basic_block(name="entry")
builder = ir.IRBuilder(block)

# Función recursiva para generar código desde el AST
def generate_code(node):
    if isinstance(node, int):
        return ir.Constant(ir.IntType(32), node)
    elif node[0] == '+':
        lhs = generate_code(node[1])
        rhs = generate_code(node[2])
        return builder.add(lhs, rhs)
    elif node[0] == '*':
        lhs = generate_code(node[1])
        rhs = generate_code(node[2])
        return builder.mul(lhs, rhs)

# Generar el código para el AST
result = generate_code(ast)
builder.ret(result)

# Imprimir el código IR
print(module)
