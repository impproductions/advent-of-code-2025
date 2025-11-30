defmodule Solution do
  def part1(lines) do
    lines
  end

  def part2(lines) do
    lines
  end
end

lines =
  File.stream!("./example1.txt")
  |> Enum.map(fn a -> String.upcase(a) end)

IO.puts(Solution.part1(lines))
IO.puts(Solution.part2(lines))
