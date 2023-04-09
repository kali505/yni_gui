use pyo3::prelude::*;

#[pyfunction]
pub fn to_base_str(_py: Python, src: String, base: u32) -> PyResult<String> {
    Ok(libyni::to_base_str(src.as_str(), base))
}

#[pymodule]
pub fn pyyni(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(to_base_str, m)?)?;
    Ok(())
}
