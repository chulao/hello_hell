/*
 * Rust hello world
 */

// Sum two numbers
fn sum(x: i32, y: i32) -> i32 {
  x + y
}


// Main function
fn main() {
  // Inline Function
  fn pow (i: i32) -> i32 { i*2 }

  // Closure
  let add = |i: i32| -> i32 { i+1 };
  let two = || 2;

  // Define the name
  let name = "world";
  let value = pow(add(two()));
  let total = sum(4, value);

  // Print a hello
  println!("Give hello {} for {} times", name, total);
}


#[cfg(test)]
mod tests {
  // Note this useful idiom: importing names from outer (for mod tests) scope.
  use super::*;

  #[test]
  fn test_sum() {
    assert_eq!(sum(1, 2), 3);
  }

  #[test]
  fn test_sum_with_negative_value() {
    assert_eq!(sum(3, -5), -2);
  }  
}