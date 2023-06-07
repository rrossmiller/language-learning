from wasmer import engine, wasi, Store, Module, ImportObject, Instance
from wasmer_compiler_cranelift import Compiler

def hello_world():
    store = Store()

    # Let's compile the module to be able to execute it!
    module = Module(store, """
    (module
      (type (func (param i32 i32) (result i32)))
      (func (export "sum") (type 0) (param i32) (param i32) (result i32)
        local.get 0
        local.get 1
        i32.add))
    """)
    
    # Now the module is compiled, we can instantiate it.
    instance = Instance(module)
    
    # Call the exported `sum` function.
    result = instance.exports.sum(5, 37)
    
    print(result) # 42!

def wasi():
    # Let's get the `wasi.wasm` bytes!
    wasm_bytes = open(  'wasi.wasm', 'rb').read()
    
    # Create a store.
    store = Store(engine.Universal(Compiler))
    
    # Let's compile the Wasm module, as usual.
    module = Module(store, wasm_bytes)
    
    # Here we go.
    #
    # First, let's extract the WASI version from the module. Why? Because
    # WASI already exists in multiple versions, and it doesn't work the
    # same way. So, to ensure compatibility, we need to know the version.
    wasi_version = wasi.get_version(module, strict=True)
    
    # Second, create a `wasi.Environment`. It contains everything related
    # to WASI. To build such an environment, we must use the
    # `wasi.StateBuilder`.
    #
    # In this case, we specify the program name is `wasi_test_program`. We
    # also specify the program is invoked with the `--test` argument, in
    # addition to two environment variable: `COLOR` and
    # `APP_SHOULD_LOG`. Finally, we map the `the_host_current_dir` to the
    # current directory. There it is:
    wasi_env = \
        wasi.StateBuilder('wasi_test_program'). \
            argument('--test'). \
            environment('COLOR', 'true'). \
            environment('APP_SHOULD_LOG', 'false'). \
            map_directory('the_host_current_dir', '.'). \
            finalize()
    
    # From the WASI environment, we generate a custom import object. Why?
    # Because WASI is, from the user perspective, a bunch of
    # imports. Consequently `generate_import_object`… generates a
    # pre-configured import object.
    #
    # Do you remember when we said WASI has multiple versions? Well, we
    # need the WASI version here!
    import_object = wasi_env.generate_import_object(store, wasi_version)
    
    # Now we can instantiate the module.
    instance = Instance(module, import_object)
    
    # The entry point for a WASI WebAssembly module is a function named
    # `_start`. Let's call it and see what happens!
    instance.exports._start()
if __name__ == "__main__":
    hello_world()
