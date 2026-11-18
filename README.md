# Gobble Up Algebra!

A Thanksgiving "Solve & Color" mystery-picture review for Algebra 1B, Units 1–3.

Students solve 36 problems (12 per unit), look up each answer in the Answer Bank to get a
2-character code, and color every grid square with that code. A turkey with a fanned tail,
two pumpkins, and grass appears when the answers are correct. Wrong-answer codes sit in the
white background, so mistakes show up as stray colored squares.

- **Unit 1:** simplifying, function evaluation and composition, multi-step equations,
  absolute value equations, solving for a variable, literal equations
- **Unit 2:** writing, solving, and graphing inequalities, including compound inequalities
- **Unit 3:** functions, domain, slope, interpreting slope/intercepts, forms of lines,
  absolute value graphs

## Files

| File | What it is |
| --- | --- |
| `Gobble_Up_Algebra_Units1-3_Review.pdf` | Printable activity (student pages, answer bank, grid, teacher key) |
| `game.html` | The same activity as HTML |
| `build.py` | Generates `game.html`: questions, answers, distractors, colors, codes |
| `pic.py` | The pixel-art picture design |
| `render.js` | Converts `game.html` to PDF with Playwright |

## Rebuilding after edits

Edit the questions in `build.py`, then run:

```bash
python3 build.py
```

```bash
node render.js "$PWD/game.html" "$PWD/Gobble_Up_Algebra_Units1-3_Review.pdf"
```

Requires Python 3 and Node.js with Playwright (Chromium).
