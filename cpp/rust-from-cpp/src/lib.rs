#[no_mangle]
pub extern "C" fn rust_function() -> i32 {
    42
}

#[no_mangle]
pub extern "C" fn greater_than_5(x: f32) -> bool {
    x > 5.0
}
