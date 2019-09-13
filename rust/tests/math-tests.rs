extern crate hello;


#[cfg(test)]
mod test_math {
  use hello::common::math;

  #[test]
  fn test_equality() {
    assert_eq!(1, 1);
  }

  #[test]
  fn test_sum() {
    assert_eq!(math::sum(1, 2), 3);
  }

  #[test]
  fn test_sum_with_negative_value() {
    assert_eq!(math::sum(3, -5), -2);
  }  
}