# Example

- Testing: `mix test`

- Using with Elixir Interactive shell **IEx**

  - `iex -S mix`

  - Getting help about lib/example.ex:

    ```
    iex> h Example.hello
    ```

  - Running the function
    ```
    iex> Example.hello("m4n3dw0lf")
    ```

### Generating HTML Docs

- Install dependencies declared on mix.exs `mix deps.get`

- Generate docs `mix docs`

- Output will be on `doc/index.html`
