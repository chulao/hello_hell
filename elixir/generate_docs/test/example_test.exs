defmodule ExampleTest do
  use ExUnit.Case
  doctest Example

  test "greets the world" do
    assert Example.hello("m4n3dw0lf") == "Hello, m4n3dw0lf"
  end
end
