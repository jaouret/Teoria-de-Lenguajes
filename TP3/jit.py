# Configurar el entorno de LLVM para JIT
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

# Crear un motor de ejecución JIT
target = llvm.Target.from_default_triple()
target_machine = target.create_target_machine()
backing_mod = llvm.parse_assembly(str(module))
engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

# Ejecutar la función principal
engine.finalize_object()
main_func_ptr = engine.get_function_address("main")

import ctypes
# Convertir a una función ejecutable en Python
cfunc = ctypes.CFUNCTYPE(ctypes.c_int32)(main_func_ptr)

# Ejecutar y obtener el resultado
result = cfunc()
print("Resultado de la ejecución:", result)
