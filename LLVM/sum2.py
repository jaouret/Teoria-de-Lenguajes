from llvmlite import ir

double = ir.DoubleType()
fnty = ir.FunctionType(double, (double, double))
module = ir.Module(name=__file__)
func = ir.Function(module, fnty, name="fpadd")
block = func.append_basic_block(name="entry")
builder = ir.IRBuilder(block)
a, b = func.args
result = builder.fadd(a, b, name="res")
builder.ret(result)
print(module)
