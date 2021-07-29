# Expression-puzzle-solver
Solve puzzle similar to the one described in introduction in Art of exploitation. Puzzle goes like this:
> Use each of the numbers 1, 3, 4, and 6 exactly once with any of the four basic math operations (addition, subtraction, multiplication, and division) to total 24. Each number must be used once and only once, and you may define the order of operations; for example, 3 * (4 + 6) + 1 = 31 is valid, however incorrect, since it doesn’t total 24.

To solve that particular puzzle:
```bash
$ python main.py 1 3 4 6 --target 24
24
  = (6 / (1 - (3 / 4)))
```

List all possible combinations sorted by result:
```bash
$ python main.py 1 2 3
-5
  = (1 - (2 * 3))
-4
  = ((1 - 3) - 2)
  = (1 - (2 + 3))
  = ((1 - 2) - 3)
  = ((1 - 3) * 2)
-3
  = ((1 - 2) * 3)
  = (3 / (1 - 2))
.....
```

Prohibit using operator (`sub`, `add`, `mul` or `div`):
```bash
$ python main.py 1 3 4 6 --no-sub --target 21
21
  = (6 + (3 * (1 + 4)))
```
