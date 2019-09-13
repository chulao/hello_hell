/*
 * Rust hello world
 */
mod common;


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
  let total = common::math::sum(4, value);

  // Print a hello
  println!("Give hello {} for {} times", name, total);
}