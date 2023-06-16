use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
#[pyfunction]
pub fn fibonacci(n: i32) -> PyResult<i64> {
    let mut f: Vec<i64> = vec![0, 1];

    for i in 2..n {
        f.push(f[(i - 1) as usize] + f[(i - 2) as usize]);
    }

    Ok(f[f.len() - 1])
}

/// A Python module implemented in Rust.
#[pymodule]
fn rustonacci(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fibonacci, m)?)?;
    Ok(())
}
