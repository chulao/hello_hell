/*
 * Rust hello world
 */

extern crate log;
extern crate simple_logger;

use log::{info};

mod common;


// Main function
fn main() {
  simple_logger::init().unwrap();

  info!("Initiating main function");

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