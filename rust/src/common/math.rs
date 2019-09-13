/// A Math module

extern crate log;

use self::log::{trace};

/// Sum two numbers
///
/// ```
/// let result = hello::common::math::sum(2, 3);
/// assert_eq!(result, 5);
/// ```
pub fn sum(x: i32, y: i32) -> i32 {
  trace!("sum {} with {}", x, y);
  x + y
}