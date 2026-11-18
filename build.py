import random, math, html, sys
sys.path.insert(0, '.')
from pic import build

random.seed(1126)

def F(a, b):
    return f'<span class="fr"><span>{a}</span><span>{b}</span></span>'

M = '−'  # unicode minus

# ---------------- SVG helpers ----------------
def plane(xmin, xmax, ymin, ymax, px=220, curves=(), pts=(), labels=True):
    nx, ny = xmax - xmin, ymax - ymin
    s = px / max(nx, ny)
    w, h = nx * s, ny * s
    X = lambda x: (x - xmin) * s
    Y = lambda y: (ymax - y) * s
    o = [f'<svg class="plane" width="{w+12:.0f}" height="{h+12:.0f}" viewBox="-6 -6 {w+12:.0f} {h+12:.0f}">']
    for i in range(nx + 1):
        o.append(f'<line x1="{X(xmin+i):.1f}" y1="0" x2="{X(xmin+i):.1f}" y2="{h:.1f}" stroke="#ccc" stroke-width="0.6"/>')
    for j in range(ny + 1):
        o.append(f'<line x1="0" y1="{Y(ymin+j):.1f}" x2="{w:.1f}" y2="{Y(ymin+j):.1f}" stroke="#ccc" stroke-width="0.6"/>')
    o.append(f'<line x1="{X(0)}" y1="0" x2="{X(0)}" y2="{h}" stroke="#000" stroke-width="1.2"/>')
    o.append(f'<line x1="0" y1="{Y(0)}" x2="{w}" y2="{Y(0)}" stroke="#000" stroke-width="1.2"/>')
    for c in curves:
        d = ' '.join(f'{X(x):.1f},{Y(y):.1f}' for x, y in c)
        o.append(f'<polyline points="{d}" fill="none" stroke="#1a5fb4" stroke-width="2.2" stroke-linejoin="round"/>')
    for x, y in pts:
        o.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="3" fill="#1a5fb4"/>')
    o.append('</svg>')
    return ''.join(o)

def numline(lo=-10, hi=10, mark=None, w=300, labeled=False):
    n = hi - lo; s = (w - 20) / n
    X = lambda v: 10 + (v - lo) * s
    o = [f'<svg class="nl" width="{w}" height="38" viewBox="0 0 {w} 38">',
         f'<line x1="2" y1="14" x2="{w-2}" y2="14" stroke="#000" stroke-width="1.2"/>',
         f'<path d="M2 14 l7 -4 v8z M{w-2} 14 l-7 -4 v8z" fill="#000"/>']
    for v in range(lo, hi + 1):
        o.append(f'<line x1="{X(v):.1f}" y1="9" x2="{X(v):.1f}" y2="19" stroke="#000" stroke-width="1"/>')
        if labeled:
            o.append(f'<text x="{X(v):.1f}" y="32" font-size="10" text-anchor="middle">{str(v).replace("-", M)}</text>')
    if mark:
        for kind, a, b in mark:  # ('ray', start, direction) or ('seg', a, b)
            pass
    o.append('</svg>')
    return ''.join(o)

def numline_graph(lo, hi, segs, circles, w=300):
    """segs: list of (a,b) values, use None for arrow to end. circles: list of (v, filled)"""
    n = hi - lo; s = (w - 20) / n
    X = lambda v: 10 + (v - lo) * s
    base = numline(lo, hi, w=w, labeled=True)[:-6]
    o = [base]
    for a, b in segs:
        xa = 2 if a is None else X(a)
        xb = w - 2 if b is None else X(b)
        o.append(f'<line x1="{xa:.1f}" y1="14" x2="{xb:.1f}" y2="14" stroke="#1a5fb4" stroke-width="4"/>')
        if a is None: o.append(f'<path d="M0 14 l9 -6 v12z" fill="#1a5fb4"/>')
        if b is None: o.append(f'<path d="M{w} 14 l-9 -6 v12z" fill="#1a5fb4"/>')
    for v, filled in circles:
        o.append(f'<circle cx="{X(v):.1f}" cy="14" r="5" fill="{"#1a5fb4" if filled else "#fff"}" stroke="#1a5fb4" stroke-width="2"/>')
    o.append('</svg>')
    return ''.join(o)

def table(xs, ys):
    tx = ''.join(f'<td>{str(v).replace("-", M)}</td>' for v in xs)
    ty = ''.join(f'<td>{str(v).replace("-", M)}</td>' for v in ys)
    return f'<table class="xy"><tr><th><i>x</i></th>{tx}</tr><tr><th><i>y</i></th>{ty}</tr></table>'

def bakery_graph():
    W_, H_ = 260, 200; L, B = 40, 30
    gw, gh = W_ - L - 10, H_ - B - 10
    X = lambda x: L + x / 8 * gw
    Y = lambda y: 10 + (64 - y) / 64 * gh
    o = [f'<svg width="{W_}" height="{H_+14}" viewBox="0 0 {W_} {H_+14}" font-size="10">']
    for i in range(9):
        o.append(f'<line x1="{X(i):.1f}" y1="10" x2="{X(i):.1f}" y2="{Y(0):.1f}" stroke="#ccc"/>')
        o.append(f'<text x="{X(i):.1f}" y="{Y(0)+13:.1f}" text-anchor="middle">{i}</text>')
    for j in range(0, 65, 8):
        o.append(f'<line x1="{L}" y1="{Y(j):.1f}" x2="{X(8):.1f}" y2="{Y(j):.1f}" stroke="#ccc"/>')
        o.append(f'<text x="{L-5}" y="{Y(j)+3.5:.1f}" text-anchor="end">{j}</text>')
    o.append(f'<line x1="{L}" y1="10" x2="{L}" y2="{Y(0)}" stroke="#000" stroke-width="1.3"/>')
    o.append(f'<line x1="{L}" y1="{Y(0)}" x2="{X(8)}" y2="{Y(0)}" stroke="#000" stroke-width="1.3"/>')
    o.append(f'<line x1="{X(0)}" y1="{Y(64)}" x2="{X(8)}" y2="{Y(0)}" stroke="#1a5fb4" stroke-width="2.4"/>')
    o.append(f'<circle cx="{X(3)}" cy="{Y(40)}" r="3.5" fill="#1a5fb4"/>')
    o.append(f'<text x="{X(3)+6}" y="{Y(40)-5}" font-size="10" font-weight="bold">(3, 40)</text>')
    o.append(f'<text x="{L+gw/2}" y="{H_+12}" text-anchor="middle" font-size="11">Hours since opening</text>')
    o.append(f'<text x="11" y="{10+gh/2}" text-anchor="middle" font-size="11" transform="rotate(-90 11 {10+gh/2})">Pies left</text>')
    o.append('</svg>')
    return ''.join(o)

# ---------------- Questions ----------------
# each: (unit, prompt_html, extra_html, answer_html, [distractors], space)
Q = []
def q(unit, prompt, answer, distract, extra='', space=90, group=None):
    Q.append(dict(unit=unit, prompt=prompt, extra=extra, answer=answer, distract=distract, space=space, group=group))

fx = f'<i>f</i>(<i>x</i>) = 2<i>x</i> + 5'
gx = f'<i>g</i>(<i>x</i>) = {F(1,3)}<i>x</i> {M} 4'

# Unit 1
q(1, f'Simplify the expression: 3(<i>x</i> {M} 4) {M} 5<i>x</i> + 2', f'{M}2<i>x</i> {M} 10', [f'{M}2<i>x</i> {M} 2', f'8<i>x</i> {M} 10'])
q(1, f'Evaluate <i>g</i>(12).', f'<i>g</i>(12) = 0', [f'<i>g</i>(12) = 8'], group=f'Evaluate using {fx} and {gx}.')
q(1, f'Evaluate <i>g</i>(<i>f</i>(5)).', f'<i>g</i>(<i>f</i>(5)) = 1', [f'<i>g</i>(<i>f</i>(5)) = 15', f'<i>g</i>(<i>f</i>(5)) = {F(1,3)}'], group=f'Evaluate using {fx} and {gx}.')
q(1, f'Solve: <i>h</i> {M} 2 = 6<i>h</i> + 2<i>h</i> {M} 16', '<i>h</i> = 2', [f'<i>h</i> = {M}2'])
q(1, f'Solve: 48 = 4({M}3<i>r</i> {M} 6)', f'<i>r</i> = {M}6', ['<i>r</i> = 6', f'<i>r</i> = {M}2'])
q(1, f'Solve: 3(2<i>g</i> {M} 4) = 2(<i>g</i> + 8)', '<i>g</i> = 7', ['<i>g</i> = 3', '<i>g</i> = 5'])
q(1, 'Define the variable, write an equation, solve, and interpret your solution.<br>You had $25 saved for Black Friday shopping. After babysitting your cousins for 6 hours on Thanksgiving, you now have $97. What is your hourly wage?',
  '$12 per hour', ['$20.33 per hour', '$16.17 per hour'], space=120)
q(1, 'Solve: |<i>x</i> + 3| = 7', f'<i>x</i> = 4 and <i>x</i> = {M}10', [f'<i>x</i> = 4 and <i>x</i> = {M}4', f'<i>x</i> = 10 and <i>x</i> = {M}4'])
q(1, f'Solve: 3|5<i>u</i> {M} 2| = {M}9', 'No solution', [f'<i>u</i> = 1 and <i>u</i> = {M}{F(1,5)}'])
q(1, f'Solve: {M}4|2<i>v</i> + 6| + 3 = {M}37', f'<i>v</i> = 2 and <i>v</i> = {M}8', [f'<i>v</i> = 2 and <i>v</i> = {M}2'])
q(1, f'Solve the equation for <i>y</i>: 6<i>x</i> {M} 3<i>y</i> = 12', f'<i>y</i> = 2<i>x</i> {M} 4', [f'<i>y</i> = {M}2<i>x</i> + 4', '<i>y</i> = 2<i>x</i> + 4'])
q(1, 'The time <i>t</i> (in minutes) to roast a turkey can be estimated by <i>t</i> = 15<i>w</i> + 30, where <i>w</i> is the weight of the turkey in pounds.<br>a) Solve the equation for <i>w</i>.<br>b) A turkey roasted for 210 minutes. Use part (a) to find its weight.',
  '12 pounds', ['16 pounds', '14 pounds'], space=120)

# Unit 2
q(2, "Write the sentence as an inequality: Grandma's table can seat no more than 12 guests.", '<i>x</i> ≤ 12', ['<i>x</i> &lt; 12', '<i>x</i> ≥ 12'], space=45)
q(2, 'Write the sentence as an inequality: The difference between a number and 7 is at least 20.', f'<i>x</i> {M} 7 ≥ 20', [f'7 {M} <i>x</i> ≥ 20', f'<i>x</i> {M} 7 &gt; 20'], space=45)
NL = numline()
q(2, 'Solve and graph: 22 &lt; <i>r</i> ' + M + ' 8', '<i>r</i> &gt; 30', ['<i>r</i> &gt; 14', '<i>r</i> &lt; 30'], extra=NL, space=55)
q(2, f'Solve and graph: {F("<i>x</i>", 4)} ≥ 5', '<i>x</i> ≥ 20', ['<i>x</i> ≥ 1.25', '<i>x</i> ≤ 20'], extra=NL, space=55)
q(2, f'Solve and graph: {M}13 {M} <i>x</i> ≥ {M}4', f'<i>x</i> ≤ {M}9', [f'<i>x</i> ≥ {M}9', '<i>x</i> ≤ 9'], extra=NL, space=55)
q(2, 'Write an inequality for the graph:', f'<i>x</i> &gt; {M}3', [f'<i>x</i> ≥ {M}3', f'<i>x</i> &lt; {M}3'],
  extra=numline_graph(-6, 6, [(-3, None)], [(-3, False)]), space=20)
q(2, f'Solve and graph: {M}2 {M} 4<i>r</i> ≥ 30', f'<i>r</i> ≤ {M}8', [f'<i>r</i> ≥ {M}8', f'<i>r</i> ≤ {M}7'], extra=NL, space=55)
q(2, 'Solve and graph: 5<i>n</i> + 14 &gt; 2 + 8<i>n</i>', '<i>n</i> &lt; 4', ['<i>n</i> &gt; 4', f'<i>n</i> &lt; {M}4'], extra=NL, space=55)
q(2, f'Solve and graph: {M}3(<i>x</i> {M} 1) ≥ 23 + 2<i>x</i>', f'<i>x</i> ≤ {M}4', [f'<i>x</i> ≥ {M}4', f'<i>x</i> ≤ {M}5.2'], extra=NL, space=60)
q(2, 'Define the variable, write the inequality, solve, and interpret the solution.<br>Pumpkin pies cost $8.50 each. What is the maximum number of pies you can buy with $40?',
  'You can buy at most 4 pies', ['You can buy at most 5 pies', 'You can buy at least 5 pies'], space=110)
q(2, f'Solve and graph: {M}4 &lt; 6 + <i>n</i> &lt; 11', f'{M}10 &lt; <i>n</i> &lt; 5', ['2 &lt; <i>n</i> &lt; 17', f'{M}10 &lt; <i>n</i> &lt; 17'], extra=NL, space=55)
q(2, f'Solve and graph: 5<i>v</i> {M} 3 ≥ 27 or {M}2<i>v</i> + 1 &gt; 9', f'<i>v</i> &lt; {M}4 or <i>v</i> ≥ 6', [f'<i>v</i> &gt; {M}4 or <i>v</i> ≥ 6', f'<i>v</i> &lt; {M}5 or <i>v</i> ≥ 6'], extra=NL, space=60)

# Unit 3
sideways = [(y*y - 4, y) for y in [i/10 for i in range(-30, 31)]]
q(3, 'Is the graph a function or not a function? Explain how you know.', 'Not a function; it fails the vertical line test',
  ['Function; it passes the vertical line test'], extra=plane(-6, 6, -6, 6, px=150, curves=[sideways]), space=25)
q(3, 'What is the domain of this table?', f'{{{M}5, 0, 2, 4}}', ['{1, 3, 6, 7, 9}', f'{{{M}5, 4}}'],
  extra=table([-5, 0, 2, 4, 4], [3, 7, 1, 9, 6]), space=35)
q(3, f'Calculate the slope: (5, {M}6) and (3, 2)', f'<i>m</i> = {M}4', ['<i>m</i> = 4', f'<i>m</i> = {M}{F(1,4)}'], space=60)
q(3, f'Calculate the slope: ({M}2, 5) and ({M}2, 1)', '<i>m</i> = undefined', ['<i>m</i> = 0'], space=60)
BK = 'The graph shows the number of pies left at a bakery on the day before Thanksgiving, <i>x</i> hours after it opens.'
q(3, 'Identify <u>and</u> interpret the slope.', f'<i>m</i> = {M}8; the bakery sells 8 pies each hour', ['<i>m</i> = 8; the bakery bakes 8 pies each hour', f'<i>m</i> = {M}8; the bakery started with 8 pies'], group=BK, space=55)
q(3, 'Identify <u>and</u> interpret the <i>y</i>-intercept.', '(0, 64); the bakery started the day with 64 pies', ['(0, 64); the bakery sells 64 pies each hour', '(8, 0); the bakery started the day with 8 pies'], group=BK, space=55)
q(3, 'Interpret the point (3, 40).', 'After 3 hours, 40 pies are left', ['After 40 hours, 3 pies are left'], group=BK, space=55)
q(3, 'Convert to slope-intercept form: 4<i>x</i> + 3<i>y</i> = 24', f'<i>y</i> = {M}{F(4,3)}<i>x</i> + 8', [f'<i>y</i> = {F(4,3)}<i>x</i> + 8', f'<i>y</i> = {M}{F(4,3)}<i>x</i> + 24', f'<i>y</i> = {M}4<i>x</i> + 24'], space=60)
q(3, f'Graph <i>y</i> + 2 = {M}{F(1,3)}(<i>x</i> {M} 9). Where does your line cross the <i>y</i>-axis?', '(0, 1)', ['(0, 5)', f'(0, {M}5)'],
  extra=plane(-10, 10, -10, 10, px=170), space=10)
q(3, 'Does this table represent a linear function? Explain.', 'Not linear; the rate of change is not constant', ['Linear; the rate of change is constant'],
  extra=table([0, 1, 2, 3], [2, 5, 8, 12]), space=35)
absg = [(-3, -3), (1, 5), (5, -3)]
AB = 'Use the absolute value graph to answer the questions.'
q(3, 'What is the vertex?', '(1, 5)', [f'({M}1, 5)', '(5, 1)'], group=AB, extra=plane(-6, 6, -6, 6, px=150, curves=[absg], pts=[(1, 5)]), space=10)
q(3, 'What is the range?', '<i>y</i> ≤ 5', ['<i>y</i> ≥ 5', 'All real numbers'], group=AB, space=30)

assert len(Q) == 36, len(Q)

# ---------------- colors / codes ----------------
COLORS = {'R': ('Red', '#c0392b'), 'O': ('Orange', '#e67e22'), 'Y': ('Yellow', '#f4d03f'),
          'B': ('Brown', '#6e3b1e'), 'T': ('Tan / Light Brown', '#d2a679'), 'K': ('Black', '#111111'),
          'G': ('Green', '#3f8f3a')}
pool = ['K'] + ['T']*3 + ['Y']*4 + ['G']*6 + ['R']*7 + ['O']*8 + ['B']*7
random.shuffle(pool)
for qq, c in zip(Q, pool):
    qq['color'] = c

letters = 'ABCDEFGHJKLMNPRSTUVWXYZ'
allcodes = [l + d for l in letters for d in '23456789']
random.shuffle(allcodes)
ci = iter(allcodes)
for qq in Q:
    qq['code'] = next(ci)
    qq['dcodes'] = [next(ci) for _ in qq['distract']]

# grid
grid = build()[2:]  # trim 2 empty rows
H_, W_ = len(grid), len(grid[0])
codes = [[None]*W_ for _ in range(H_)]
for col in COLORS:
    cells = [(r, c) for r in range(H_) for c in range(W_) if grid[r][c] == col]
    qs = [qq for qq in Q if qq['color'] == col]
    random.shuffle(cells)
    for i, (r, c) in enumerate(cells):
        codes[r][c] = qs[i % len(qs)]['code']
bg = [(r, c) for r in range(H_) for c in range(W_) if grid[r][c] == '.']
dlist = [dc for qq in Q for dc in qq['dcodes']]
random.shuffle(bg)
for i, (r, c) in enumerate(bg):
    codes[r][c] = dlist[i % len(dlist)]
print('cells', H_, W_, 'bg', len(bg), 'distractors', len(dlist))
for col in COLORS:
    print(col, sum(1 for qq in Q if qq['color'] == col), sum(1 for row in grid for x in row if x == col))

# ---------------- HTML ----------------
CSS = '''
@page { size: letter; margin: 0.45in 0.5in; }
* { box-sizing: border-box; }
body { font-family: "DejaVu Sans", "Liberation Sans", sans-serif; font-size: 10.5pt; color: #222; margin: 0; }
i { font-family: "DejaVu Serif", serif; }
.fr { display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; font-size: 0.85em; margin: 0 1px; line-height: 1.05; }
.fr > span:first-child { border-bottom: 1px solid currentColor; padding: 0 2px; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
header.top { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 3px solid #b5541c; padding-bottom: 4px; margin-bottom: 8px; }
header.top h1 { font-size: 19pt; margin: 0; color: #7a2e0e; font-family: "DejaVu Serif", serif; }
header.top .sub { font-size: 9.5pt; color: #555; }
.name { font-size: 10pt; }
.dir { background: #fdf2e4; border: 1.5px solid #e0a35c; border-radius: 8px; padding: 8px 12px; margin-bottom: 10px; font-size: 10pt; }
.dir ol { margin: 4px 0 0 0; padding-left: 20px; }
h2.unit { font-size: 12.5pt; margin: 6px 0 6px; color: #fff; background: #b5541c; padding: 3px 10px; border-radius: 5px; }
.grp { font-weight: bold; margin: 4px 0 4px; font-size: 10pt; }
.qs { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 14px; }
.qbox { border: 1px solid #bbb; border-radius: 6px; padding: 6px 8px 4px; break-inside: avoid; display: flex; flex-direction: column; }
.qbox.wide { grid-column: span 2; }
.qhead { display: flex; justify-content: space-between; align-items: center; margin-bottom: 3px; }
.qnum { font-weight: bold; background: #7a2e0e; color: #fff; border-radius: 4px; padding: 0 6px; font-size: 10pt; }
.color { font-size: 8.5pt; font-weight: bold; display: flex; align-items: center; gap: 4px; }
.sw { display: inline-block; width: 13px; height: 13px; border: 1px solid #333; border-radius: 2px; }
.extra { margin: 4px 0; }
.ans { margin-top: auto; font-size: 8.5pt; display: flex; gap: 10px; padding-top: 4px; }
.ans span.blank { border-bottom: 1px solid #333; flex: 1; }
.ans span.codeblank { border: 1px solid #333; width: 38px; height: 16px; display: inline-block; }
table.xy { border-collapse: collapse; font-size: 10pt; }
table.xy td, table.xy th { border: 1px solid #555; padding: 2px 9px; text-align: center; }
table.xy th { background: #f3e3cf; }
.bank h3 { margin: 3px 0 1px; font-size: 11pt; color: #7a2e0e; }
.bankgrid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 14px; }
.bi { display: flex; gap: 8px; border-bottom: 1px dotted #bbb; padding: 0.8px 0; font-size: 8.4pt; break-inside: avoid; align-items: center; }
.bi b { font-family: "DejaVu Sans Mono", monospace; width: 26px; flex: none; color: #7a2e0e; }
table.grid { border-collapse: collapse; margin: 0 auto; }
table.grid td { border: 0.8px solid #888; width: 0.3in; height: 0.3in; text-align: center; font-size: 7.5pt; font-family: "DejaVu Sans Mono", monospace; padding: 0; }
.key table { border-collapse: collapse; width: 100%; font-size: 8pt; }
.key td, .key th { border: 1px solid #aaa; padding: 1px 4px; }
.key th { background: #f3e3cf; text-align: left; }
.small { font-size: 8.5pt; color: #555; }
'''

def qbox(n, qq, wide=False):
    nm, hexc = COLORS[qq['color']]
    extra = f'<div class="extra">{qq["extra"]}</div>' if qq['extra'] else ''
    return (f'<div class="qbox{" wide" if wide else ""}"><div class="qhead"><span class="qnum">{n}</span>'
            f'<span class="color"><span class="sw" style="background:{hexc}"></span>Color: {nm}</span></div>'
            f'<div>{qq["prompt"]}</div>{extra}<div style="height:{qq["space"]}px"></div>'
            f'<div class="ans">Answer:<span class="blank"></span>Code: <span class="codeblank"></span></div></div>')

UNITS = {1: 'Unit 1 · Equations, Functions & Absolute Value Equations',
         2: 'Unit 2 · Inequalities',
         3: 'Unit 3 · Functions, Slope & Graphing'}

def header(title, sub):
    return (f'<header class="top"><div><h1>{title}</h1><div class="sub">{sub}</div></div>'
            f'<div class="name">Name: ______________________ &nbsp;Block: ____</div></header>')

pages = []
# page 1: directions + questions. Build question sections in sequence with manual page breaks.
DIR = ('<div class="dir"><b>🦃 Directions — Gobble Up the Review!</b><ol>'
       '<li>Solve each problem. <b>Show all required work</b> in the box.</li>'
       '<li>Find your answer in the <b>Answer Bank</b>. Write the 2-character <b>code</b> next to your answer.</li>'
       '<li>On the <b>Mystery Picture</b> grid, color <u>every</u> square with that code using the color listed on the problem.</li>'
       '<li>Can\'t find your answer in the bank? Check your work — it\'s not right yet! Squares whose codes you never get stay <b>white</b>.</li>'
       '</ol><div class="small" style="margin-top:4px">You will need: red, orange, yellow, brown, tan/light brown, black, and green colored pencils.</div></div>')

# Layout plan: list of pages, each a list of question indices (0-based)
layout = [
    [0, 1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10, 11],
    [12, 13, 14, 15, 16, 17, 18, 19],
    [20, 21, 22, 23],
    [24, 25, 26, 27, 32, 33],
    [28, 29, 30, 31, 34, 35],
]
wide_set = {6, 11, 21}
for pi, idxs in enumerate(layout):
    body = [header('Gobble Up Algebra!', 'Algebra 1B · Units 1–3 Thanksgiving Review · Solve &amp; Color Mystery Picture')] if pi == 0 else []
    if pi == 0:
        body.append(DIR)
    last_unit = None if pi == 0 else Q[layout[pi-1][-1]]['unit']
    cur = []
    last_group = None
    def flush():
        if cur:
            body.append('<div class="qs">' + ''.join(cur) + '</div>')
            cur.clear()
    for i in idxs:
        qq = Q[i]
        if qq['unit'] != last_unit:
            flush()
            body.append(f'<h2 class="unit">{UNITS[qq["unit"]]}</h2>')
            last_unit = qq['unit']
        if qq['group'] != last_group:
            if qq['group']:
                flush()
                body.append(f'<div class="grp">{qq["group"]}</div>')
                if qq['group'] == BK:
                    body.append(f'<div style="text-align:center">{bakery_graph()}</div>')
            elif last_group:
                flush()
            last_group = qq['group']
        cur.append(qbox(i + 1, qq, wide=i in wide_set))
    flush()
    pages.append('<div class="page">' + ''.join(body) + '</div>')

# Answer bank
bank = [header('Answer Bank', 'Not every answer here is correct!')]
for u in (1, 2, 3):
    items = []
    for qq in Q:
        if qq['unit'] != u: continue
        items.append((qq['code'], qq['answer']))
        items += list(zip(qq['dcodes'], qq['distract']))
    items.sort()
    bank.append(f'<div class="bank"><h3>{UNITS[u]}</h3><div class="bankgrid">' +
                ''.join(f'<div class="bi"><b>{c}</b><span>{a}</span></div>' for c, a in items) + '</div></div>')
pages.append('<div class="page">' + ''.join(bank) + '</div>')

# Grid page
def grid_html(colored=False):
    rows = []
    for r in range(H_):
        tds = []
        for c in range(W_):
            if colored and grid[r][c] != '.':
                hexc = COLORS[grid[r][c]][1]
                fg = '#fff' if grid[r][c] in 'BKRG' else '#000'
                tds.append(f'<td style="background:{hexc};color:{fg}">{codes[r][c]}</td>')
            else:
                tds.append(f'<td>{codes[r][c]}</td>')
        rows.append('<tr>' + ''.join(tds) + '</tr>')
    return '<table class="grid">' + ''.join(rows) + '</table>'

pages.append('<div class="page">' + header('Mystery Picture', 'Color each square using the code and color from your problems. What Thanksgiving picture appears?')
             + '<div style="margin-top:14px">' + grid_html() + '</div></div>')

# Teacher key
key = ['<header class="top"><div><h1>Teacher Answer Key</h1><div class="sub">Gobble Up Algebra! · Units 1–3 Review</div></div></header>',
       '<div class="key"><table><tr><th>#</th><th>Unit</th><th>Correct answer</th><th>Code</th><th>Color</th><th>Distractor codes (likely error)</th></tr>']
for i, qq in enumerate(Q):
    nm, hexc = COLORS[qq['color']]
    ds = '; '.join(f'<b>{c}</b>: {a}' for c, a in zip(qq['dcodes'], qq['distract']))
    key.append(f'<tr><td>{i+1}</td><td>{qq["unit"]}</td><td>{qq["answer"]}</td><td><b>{qq["code"]}</b></td>'
               f'<td><span class="sw" style="background:{hexc}"></span> {nm}</td><td class="small">{ds}</td></tr>')
key.append('</table></div>')
pages.append('<div class="page">' + ''.join(key) + '</div>')
pages.append('<div class="page"><header class="top"><div><h1>Teacher Key · Completed Picture</h1>'
             '<div class="sub">Any colored square outside the turkey/pumpkins/grass shows a distractor code — check the key to see which problem went wrong.</div></div></header>'
             '<div style="margin-top:14px">' + grid_html(True) + '</div></div>')

out = f'<!doctype html><html><head><meta charset="utf-8"><title>Gobble Up Algebra</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
open('game.html', 'w').write(out)
print('written')
