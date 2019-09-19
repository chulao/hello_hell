defmodule Example do
  @moduledoc """
  ...
  """

  @doc """
  Prints a hello message

  ## Parameters

    - name: String that represents the name of the person.

  ## Examples

      iex> Example.hello("m4n3dw0lf")
      "Hello, m4n3dw0lf"

  """
  def hello(name) do
    "Hello, " <> name
  end
end
