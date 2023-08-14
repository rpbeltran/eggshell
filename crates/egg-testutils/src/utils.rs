use crate::errors::*;

/// Compare vectors item by item.
/// Returns true iff the vectors are equal length and associated items are equal.
pub fn vecs_equal<T: std::cmp::PartialEq>(a: &Vec<T>, b: &Vec<T>) -> bool {
    (a.len() == b.len()) && (0..a.len()).all(|i| a[i] == b[i])
}

/// Compare vectors item by item.
/// Returns true iff the vectors are equal length and associated items are equal.
pub fn assert_vecs_equal<T: std::cmp::PartialEq + std::fmt::Debug>(
    a: &Vec<T>,
    b: &Vec<T>,
) -> Result<()> {
    if a.len() != b.len() {
        Err(Error::TestCaseFailedAssertionVecsEqual(format!(
            "a.len() != b.len(); {} != {}",
            a.len(),
            b.len()
        )))
    } else {
        for i in 0..a.len() {
            if a[i] != b[i] {
                return Err(Error::TestCaseFailedAssertionVecsEqual(format!(
                    "a[{i}] != b[{i}]; {:?} != {:?}, ",
                    a[i], b[i]
                )));
            }
        }
        Ok(())
    }
}
