from PIL import Image, ImageDraw, ImageFont
import os, shutil, sys, zipfile

HEIGHT = int(sys.argv[1]) if len(sys.argv) > 1 else 480
NAME = f'simple{sys.argv[2]}' if len(sys.argv) > 2 else 'simple'
CREATOR = 'yune'
CUSTOMOPTION = (
  ('TURNTABLE', ('LEFT', 'RIGHT')),
)
CUSTOMFILE = (
  ('FRAME', 'Frame', 'csv'),
  ('NOTE', 'Note', 'csv'),
  ('GAUGE', 'Gauge'),
  ('NUMBER SMALL', 'NumberSmall'),
  ('NUMBER BIG', 'NumberBig'),
  ('SHUTTER', 'Shutter'),
  ('OPTION', 'Option'),
  ('FINISH', 'Finish'),
  ('PROGRESS', 'Progress'),
  ('LINE', 'Line'),
  ('LOADING', 'Loading'),
  ('JUDGELINE', 'Judgeline'),
  ('JUDGE 0', 'Judge0'),
  ('JUDGE 1', 'Judge1'),
  ('JUDGE 2', 'Judge2'),
  ('JUDGE 3', 'Judge3'),
  ('JUDGE 4', 'Judge4'),
  ('JUDGE 5', 'Judge5'),
  ('RANK AAA', 'RankAAA'),
  ('RANK AA', 'RankAA'),
  ('RANK A', 'RankA'),
  ('RANK B', 'RankB'),
  ('RANK C', 'RankC'),
  ('RANK D', 'RankD'),
  ('RANK E', 'RankE'),
  ('RANK F', 'RankF'),
  ('DOT', 'Dot'),
  ('COLON', 'Colon'),
)

_ = lambda t: (
  (t * HEIGHT + t * HEIGHT // 480 % 2 + 239) // 480 if
  isinstance(t, int) else
  t * HEIGHT / 480
)

buffer = []

NUM = 900
OP = {}
for op, labels in CUSTOMOPTION:
  buffer.append(f'#CUSTOMOPTION,{op},{NUM},{",".join(labels)}\n')
  t = {}
  for label in labels:
    t[label] = NUM
    NUM += 1
  OP[op] = t
for op, path, *args in CUSTOMFILE:
  buffer.append(f'#CUSTOMFILE,{op},LR2files\\Theme\\{NAME}\\{path}\\*.{args[0] if args else "png"},default\n')
  if os.path.isdir(path): shutil.rmtree(path)
  os.mkdir(path)

buffer.append('#ENDOFHEADER\n')

buffer.append('#SCRATCHSIDE,0,0\n')
buffer.append('#STARTINPUT,0\n')
buffer.append('#LOADSTART,0\n')
buffer.append('#LOADEND,1000\n')
buffer.append('#PLAYSTART,1000\n')
buffer.append('#FADEOUT,200\n')
buffer.append('#CLOSE,200\n')

IMAGE = {}
N = 0
for op, path, *args in CUSTOMFILE:
  if args: continue
  IMAGE[op] = N
  buffer.append(f'#IMAGE,LR2files\\Theme\\{NAME}\\{path}\\*.png\n')
  N += 1
IMAGE['FRAME LEFT'] = N
N += 1
IMAGE['FRAME RIGHT'] = N
N += 1

buffer = ''.join(buffer)

def src(tag, num, img, x, y, w, h, dx, dy, *args):
  f.write(f'#SRC_{tag},{num},{img if isinstance(img, int) else IMAGE[img]},{x},{y},{w},{h},{dx},{dy}{"".join(f",{arg}" for arg in args)}\n')

def dst(tag, num, x, y, w, h, *args, time = 0, alpha = 255, blend = 0):
  f.write(f'#DST_{tag},{num},{time},{x},{y},{w},{h},0,{alpha},255,255,255,{blend},0,0,0{"".join(f",{arg}" for arg in args)}\n')

def lr2skin(b):
  f.write(f'#INFORMATION,{12 if b else 0},{NAME},{CREATOR}\n')
  f.write(buffer)

  f.write(f'#INCLUDE,LR2files\\Theme\\{NAME}\\Frame\\*.csv\n')

  src('LINE', 0, 'LINE', 0, 0, _(400), 1, 1, 1)
  dst('LINE', 0, _(120), _(480), _(400), 1)

  f.write(f'#INCLUDE,LR2files\\Theme\\{NAME}\\Note\\*.csv\n')

  src('SLIDER', 0, 'SHUTTER', 0, 0, 1, _(480), 1, 1, 0, 0, 2, _(480), 4, 1)
  dst('SLIDER', 0, _(120), _(-480), _(400), _(480))

  f.write('#IF,35\n') # ghost type a

  # target
  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 12, _(24) * 2, 12, 2, 0, 0, 108, 0, 5)
  dst('NUMBER', 0, _(284), _(48), _(12), _(24))

  f.write('#ENDIF\n')

  for i in range(6):
    src('NOWJUDGE_1P', i, f'JUDGE {i}', 0, 0, _(400), _(240), 1, 1, 0, 0, 1)
    dst('NOWJUDGE_1P', i, _(120), _(0), _(400), _(240))

  for i in range(3, 6):
    src('NOWCOMBO_1P', i, 'NUMBER BIG', 0, 0, _(24) * 10, _(48), 10, 1, 0, 0, 0, 1, 8)
    dst('NOWCOMBO_1P', i, _(188), _(216), _(24), _(48))

  src('IMAGE', 0, 'FINISH', 0, 0, _(400), _(240), 1, 1)
  dst('IMAGE', 0, _(120), _(240), _(400), _(240), 0, 143)

  src('JUDGELINE', 0, 'JUDGELINE', 0, 0, _(400), _(40), 1, 1)
  dst('JUDGELINE', 0, _(120), _(460), _(400), _(40))

  if b:
    for i in range(8):
      dst('NOTE', i + 10, 0, 0, 0, 0)

def frame(b):
  f.write(f'#IMAGE,LR2files\\Theme\\{NAME}\\Frame\\{"mirror" if b else "default"}-left.png\n')
  f.write(f'#IMAGE,LR2files\\Theme\\{NAME}\\Frame\\{"mirror" if b else "default"}-right.png\n')

  src('IMAGE', 0, 'FRAME LEFT', 0, 0, _(120), _(480), 1, 1)
  dst('IMAGE', 0, _(0), _(0), _(120), _(480))

  src('IMAGE', 0, 'FRAME RIGHT', 0, 0, _(120), _(480), 1, 1)
  dst('IMAGE', 0, _(520), _(0), _(120), _(480))

  src('BARGRAPH', 0, 'LOADING', 0, 0, 1, 1, 1, 1, 0, 0, 2, 1)
  dst('BARGRAPH', 0, _(520 if b else 96), _(360), _(24), _(-360), 0, 0, 80)

  src('IMAGE', 0, 'LOADING', 0, 0, 1, 1, 1, 1)
  dst('IMAGE', 0, _(520 if b else 96), _(0), _(24), _(360), -1, 40, 81, blend = 1)
  dst('IMAGE', 0, _(520 if b else 96), _(0), _(24), _(360), time = 1000, alpha = 0)

  src('SLIDER', 0, 'PROGRESS', 0, 0, _(24), _(24), 1, 1, 0, 0, 2, _(336), 6, 1)
  dst('SLIDER', 0, _(520 if b else 96), _(0), _(24), _(24), 0, 0, 81)

  # remaining time
  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 163, 0, 2)
  dst('NUMBER', 0, _(556 if b else 24), _(324), _(12), _(24))
  src('IMAGE', 0, 'COLON', 0, 0, _(12), _(24), 1, 1)
  dst('IMAGE', 0, _(580 if b else 48), _(324), _(12), _(24))
  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 164, 0, 2)
  dst('NUMBER', 0, _(592 if b else 60), _(324), _(12), _(24))

  # rate
  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 102, 0, 2)
  dst('NUMBER', 0, _(556 if b else 24), _(24), _(12), _(24))
  src('IMAGE', 0, 'DOT', 0, 0, _(12), _(24), 1, 1)
  dst('IMAGE', 0, _(580 if b else 48), _(24), _(12), _(24))
  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 103, 0, 2)
  dst('NUMBER', 0, _(592 if b else 60), _(24), _(12), _(24))

  for i in range(5):
    # pg gr gd bd pr
    src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 110 + i, 0, 5)
    dst('NUMBER', 0, _(556 if b else 24), _(i * 24 + 48), _(12), _(24))

  # speed
  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 10, 0, 3)
  dst('NUMBER', 0, _(592 if b else 72), _(360), _(12), _(24))

  # bpm
  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 160, 0, 3)
  dst('NUMBER', 0, _(592 if b else 72), _(384), _(12), _(24))

  # random
  src('BUTTON', 0, 'OPTION', 0, 0, _(120), _(24) * 6, 1, 6, 0, 0, 42, 0, 0, 0)
  dst('BUTTON', 0, _(520 if b else 0), _(408), _(120), _(24))

  # gauge
  src('BUTTON', 0, 'OPTION', 0, _(24) * 6, _(120), _(24) * 6, 1, 6, 0, 0, 40, 0, 0, 0)
  dst('BUTTON', 0, _(520 if b else 0), _(432), _(120), _(24))

  for i in range(4):
    # judgerank
    src('IMAGE', 0, 'OPTION', 0, _(24) * (i + 12), _(120), _(24), 1, 1)
    dst('IMAGE', 0, _(520 if b else 0), _(456), _(120), _(24), 0, 0, 180 + i, -290)

  for i in range(5):
    # course
    src('IMAGE', 0, 'OPTION', 0, _(24) * (i + 16), _(120), _(24), 1, 1)
    dst('IMAGE', 0, _(520 if b else 0), _(456), _(120), _(24), 0, 0, 289 if i == 4 else 280 + i, 290)

  # rank
  for i, t in enumerate(('AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F')):
    src('IMAGE', 0, f'RANK {t}', 0, 0, _(120), _(120), 1, 1)
    dst('IMAGE', 0, _(0 if b else 520), _(0), _(120), _(120), 0, 0, 200 + i)

  # gauge
  src('NUMBER', 0, 'NUMBER BIG', 0, 0, _(24) * 10, _(48), 10, 1, 0, 0, 107, 2, 3)
  dst('NUMBER', 0, _(24 if b else 544), _(126), _(24), _(48))

  src('GROOVEGAUGE', 0, 'GAUGE', 0, 0, _(120), _(6) * 4, 1, 4, 0, 0, 0, _(-6))
  dst('GROOVEGAUGE', 0, _(0 if b else 520), _(474), _(120), _(6))

with open('7.lr2skin', 'w') as f:
  lr2skin(False)
with open('7b.lr2skin', 'w') as f:
  lr2skin(True)
with open('Frame/default.csv', 'w') as f:
  frame(False)
with open('Frame/mirror.csv', 'w') as f:
  frame(True)

def noteset(dh, sh, name):
  global f
  def note(imgs, keys, b, dh, sh, k):
    for y in imgs:
      f.write(f'#IMAGE,LR2files\\Theme\\{NAME}\\Note\\{y}.png\n')
    for i, j in enumerate(keys): src('NOTE', i, N + j, 0, 0, _(50), sh, 1, 1)
    for i, j in enumerate(keys): src('LN_START', i, N + j + k, 0, 0, _(50), sh, 1, 1)
    for i, j in enumerate(keys): src('LN_BODY', i, N + j + k * 2, 0, 0, _(50), 1, 1, 1)
    for i, j in enumerate(keys): src('LN_END', i, N + j + k * 3, 0, 0, _(50), sh, 1, 1)
    f.write(f'#IF,{OP["TURNTABLE"]["LEFT"]}\n')
    for i in range(8): dst('NOTE', -i & 7 if b else i, _(120 + i * 50), _(480) - (dh >> 1), _(50), dh)
    f.write('#ENDIF\n')
    f.write(f'#IF,{OP["TURNTABLE"]["RIGHT"]}\n')
    for i in range(8): dst('NOTE', 7 - i if b else i + 1 & 7, _(120 + i * 50), _(480) - (dh >> 1), _(50), dh)
    f.write('#ENDIF\n')

  sprite = (name, ) if sh == 1 else (name, f'{name}LNStart', 'default', f'{name}LNEnd')
  color = ('red', 'white', 'blue', 'orange')

  x = [f'{s}-{c}' for s in sprite for c in color[:-1]]
  y = (0, 1, 2, 1, 2, 1, 2, 1)
  with open(f'Note/{name}.csv', 'w') as f:
    note(x, y, False, dh, sh, (sh != 1) * 3)
  with open(f'Note/{name}Mirror.csv', 'w') as f:
    note(x, y, True, dh, sh, (sh != 1) * 3)

  x = [f'{s}-{c}' for s in sprite for c in color]
  y = (0, 1, 2, 1, 3, 1, 2, 1)
  with open(f'Note/{name}2.csv', 'w') as f:
    note(x, y, False, dh, sh, (sh != 1) * 4)
  with open(f'Note/{name}2Mirror.csv', 'w') as f:
    note(x, y, True, dh, sh, (sh != 1) * 4)

  x = [f'{s}-{c}' for s in sprite for c in color[:-1]]
  y = (0, 1, 1, 1, 2, 1, 1, 1)
  with open(f'Note/{name}3.csv', 'w') as f:
    note(x, y, False, dh, sh, (sh != 1) * 3)
  with open(f'Note/{name}3Mirror.csv', 'w') as f:
    note(x, y, True, dh, sh, (sh != 1) * 3)

noteset(_(16), 1, 'default')
noteset(_(50), _(50), 'circle')

for n, c in (
  ('red', (255, 0, 0)),
  ('blue', (0, 128, 255)),
  ('white', (255, 255, 255)),
  ('orange', (255, 128, 0)),
):
  def render(name, w, h, cal):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    pi = im.load()
    for i in range(w):
      for j in range(h):
        r = g = b = a = 0
        for k in range(16):
          for l in range(16):
            _r, _g, _b, _a = cal(i << 5 | k << 1 | 1, j << 5 | l << 1 | 1)
            r += _r * _a
            g += _g * _a
            b += _b * _a
            a += _a
        pi[(i, j)] = ((r + r + a) // (a + a), (g + g + a) // (a + a), (b + b + a) // (a + a), a + 128 >> 8) if a else (0, 0, 0, 0)
    im.save(f'Note/{name}-{n}.png', optimize = True)
  render('default', _(50), 1, lambda x, y: (*c, 255 if abs(x - _(800)) < _(768) else 0))
  render('circle', _(50), _(50), lambda x, y: (*c, 255 if (x - _(800)) ** 2 + (y - _(800)) ** 2 < _(768) ** 2 else 0))
  render('circleLNStart', _(50), _(50), lambda x, y: (*c, 255 if (x - _(800)) ** 2 + max(0, y - _(800)) ** 2 < _(768) ** 2 else 0))
  render('circleLNEnd', _(50), _(50), lambda x, y: (*c, 255 if (x - _(800)) ** 2 + max(0, _(800) - y) ** 2 < _(768) ** 2 else 0))

im = Image.new('RGBA', (_(120), _(480)), (0, 0, 0, 0))
pi = im.load()
for i in range(_(480)): pi[(_(120) - 1, i)] = (255, 255, 255, 255)
for i in range(_(360)): pi[(_(96), i)] = (255, 255, 255, 255)
for i in range(360, 480, 24):
  for j in range(_(120)):
    pi[(j, _(i))] = (255, 255, 255, 255)
font = ImageFont.truetype('./Lato/Lato-Regular.ttf', _(16))
draw = ImageDraw.Draw(im)
txt = ('SPEED', 'B  P  M')
for i, t in enumerate(txt):
  w, h = draw.textsize(t, font = font)
  draw.text(((_(60) - w) / 2, (_(48 * i + 740.) - h) / 2), t, (255, 255, 255), font = font)
im.save('Frame/default-left.png', optimize = True)

im = Image.new('RGBA', (_(120), _(480)), (0, 0, 0, 0))
pi = im.load()
for i in range(_(480)): pi[(_(120) - 1, i)] = (255, 255, 255, 255)
for i in range(_(480)): pi[(0, i)] = (255, 255, 255, 255)
for i in range(_(360)): pi[(_(24), i)] = (255, 255, 255, 255)
for i in range(360, 480, 24):
  for j in range(_(120)):
    pi[(j, _(i))] = (255, 255, 255, 255)
font = ImageFont.truetype('./Lato/Lato-Regular.ttf', _(16))
draw = ImageDraw.Draw(im)
txt = ('SPEED', 'B  P  M')
for i, t in enumerate(txt):
  w, h = draw.textsize(t, font = font)
  draw.text(((_(60) - w) / 2, (_(48 * i + 740.) - h) / 2), t, (255, 255, 255), font = font)
im.save('Frame/mirror-right.png', optimize = True)

im = Image.new('RGBA', (_(120), _(480)), (0, 0, 0, 0))
pi = im.load()
for i in range(_(480)): pi[(0, i)] = (255, 255, 255, 255)
im.save('Frame/default-right.png', optimize = True)

im = Image.new('RGBA', (_(120), _(480)), (0, 0, 0, 0))
pi = im.load()
for i in range(_(480)): pi[(_(120) - 1, i)] = (255, 255, 255, 255)
im.save('Frame/mirror-left.png', optimize = True)

im = Image.new('RGBA', (1, _(480)), (0, 0, 0, 255))
pi = im.load()
pi[(0, _(480) - 1)] = (255, 255, 255, 255)
im.save('Shutter/default.png', optimize = True)

im = Image.new('RGBA', (_(120), _(24) * 21), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
txt = (
  'OFF',
  'MIRROR',
  'RANDOM',
  'S-RANDOM',
  'SCATTER',
  'CONVERGE',
  'GROOVE',
  'SURVIVAL',
  'DEATH',
  'EASY',
  'P-ATTACK',
  'G-ATTACK',
  'VERYHARD',
  'HARD',
  'NORMAL',
  'EASY',
  'STAGE 1',
  'STAGE 2',
  'STAGE 3',
  'STAGE 4',
  'STAGE FINAL',
)
for i, t in enumerate(txt):
  w, h = draw.textsize(t, font = font)
  draw.text(((_(120) - w) / 2, _(24) * i + (_(20.) - h) / 2), t, (255, 255, 255), font = font)
im.save('Option/default.png', optimize = True)

im = Image.new('RGBA', (_(24), _(24)), (0, 0, 0, 0))
pi = im.load()
for i in range(_(6), _(18)):
  for j in range(_(6), _(18)):
    pi[(i, j)] = (255, 255, 255, 255)
im.save('Progress/default.png', optimize = True)

im = Image.new('RGBA', (1, 1), (170, 170, 170, 255))
im.save('Loading/default.png', optimize = True)

im = Image.new('RGBA', (_(400), 1), (0, 0, 0, 0))
im.save('Line/transparent.png', optimize = True)
pi = im.load()
for i in range(_(400)):
  pi[(i, 0)] = (170, 170, 170, 255)
im.save('Line/default.png', optimize = True)

im = Image.new('RGBA', (_(120), _(6) * 4), (0, 0, 0, 0))
im.save('Gauge/transparent.png', optimize = True)
pi = im.load()
c = [(255, 255, 255, 255), (0, 0, 255, 255), (0, 0, 0, 0), (0, 0, 85, 255)]
for i in range(_(30), _(90)):
  for j in range(_(6) * 4):
    pi[(i, j)] = c[j // _(6)]
im.save('Gauge/default.png', optimize = True)

im = Image.new('RGBA', (_(400), _(40)), (0, 0, 0, 0))
im.save('Judgeline/transparent.png', optimize = True)
pi = im.load()
for i in range(_(400)):
  for j in range(_(16), _(24)):
    pi[(i, j)] = (255, 255, 255, 255)
im.save('Judgeline/default.png', optimize = True)

im = Image.new('RGBA', (_(400), _(40)), (0, 0, 0, 0))
pi = im.load()
for i in range(_(400)):
  for j in range(_(10), _(30)):
    t = abs(j - _(20) + .5) / _(10)
    tt = min(1, t * 4)
    pi[(i, j)] = (int(255 * (1 - tt / 2) + .5), int(255 * (1 - tt / 8) + .5), 255, int(255 * (1 - t) + .5))
im.save('Judgeline/R.png', optimize = True)

font = ImageFont.truetype('./Lato/Lato-Regular.ttf', _(16))

im = Image.new('RGBA', (_(400), _(240)), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
w, h = draw.textsize('FINISH', font = font)
draw.text(((_(400) - w) / 2, (_(240) - h) / 2), 'FINISH', (255, 255, 255), font = font)
im.save('Finish/default.png', optimize = True)

im = Image.new('RGBA', (_(12), _(24)), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
w, h = draw.textsize('.', font = font)
draw.text(((_(12) - w) / 2, (_(20.) - h) / 2), '.', (255, 255, 255), font = font)
im.save('Dot/default.png', optimize = True)

im = Image.new('RGBA', (_(12), _(24)), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
w, h = draw.textsize(':', font = font)
draw.text(((_(12) - w) / 2, (_(20.) - h) / 2), ':', (255, 255, 255), font = font)
im.save('Colon/default.png', optimize = True)

def blur(pi, w, h, z):
  c = [1]
  for i in range(z):
    c = [(j > 1 and c[j - 2]) + (j and j - 1 < len(c) and c[j - 1]) * 2 + (j < len(c) and c[j]) for j in range(i + i + 3)]
  d = [[0] * h for _ in range(w)]
  for i in range(w):
    for j in range(h):
      t = 0
      for k in range(max(-z, -i), min(z + 1, w - i)):
        for l in range(max(-z, -j), min(z + 1, h - j)):
          t += c[k + z] * c[l + z] * pi[(i + k, j + l)][-1]
      d[i][j] = t / (1 << (z << 2))
  return d

def inner(y0, a0, y1, a1):
  return ((t0 * a0 + t1 * a1) / (a0 + a1) for t0, t1 in zip(y0, y1))

def toInt(y):
  return tuple(int(t + .5) for t in y)

s = '0123456789'
font = ImageFont.truetype('./Lato/Lato-Bold.ttf', _(32))
im = Image.new('RGBA', (len(s) * _(24), _(48)), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
for i in range(len(s)):
  w, h = draw.textsize(s[i], font = font)
  draw.text((i * _(24) + (_(24) - w) / 2, (_(40.) - h) / 2), s[i], (255, 255, 255), font = font)
pi = im.load()
w, h = im.size
d = blur(pi, w, h, _(2))
for i in range(w):
  for j in range(h):
    if not d[i][j]: continue
    r, g, b, a = pi[(i, j)]
    aa = (255 - a) * d[i][j] / 255
    r, g, b = inner((r, g, b), a, (0, 0, 0), aa)
    a += aa
    pi[(i, j)] = toInt((r, g, b, a))
im.save('NumberBig/default.png', optimize = True)

s = ['01234567890+', '01234567890-']
c = [(255, 255, 255), (255, 0, 0)]
font = ImageFont.truetype('./Lato/Lato-Regular.ttf', _(16))
im = Image.new('RGBA', (len(s[0]) * _(12), _(24) * 2), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
for j in range(len(s)):
  for i in range(len(s[j])):
    w, h = draw.textsize(s[j][i], font = font)
    draw.text((i * _(12) + (_(12) - w) / 2, j * _(24) + (_(20.) - h) / 2), s[j][i], c[j], font = font)
pi = im.load()
w, h = im.size
d = blur(pi, w, h, _(2))
for i in range(w):
  for j in range(h):
    if not d[i][j]: continue
    r, g, b, a = pi[(i, j)]
    aa = (255 - a) * d[i][j] / 255
    r, g, b = inner((r, g, b), a, (0, 0, 0), aa)
    a += aa
    pi[(i, j)] = toInt((r, g, b, a))
im.save('NumberSmall/default.png', optimize = True)

s = ('AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F')
c = (
  ((221, 238, 255), (255, 255, 255)),
  ((255, 255, 0), (255, 255, 255)),
  ((0, 255, 0), (255, 255, 255)),
  ((0, 0, 255), (255, 255, 255)),
  ((85, 85, 85), (255, 255, 255)),
  ((85, 85, 85), (255, 255, 255)),
  ((85, 85, 85), (255, 255, 255)),
  ((85, 85, 85), (255, 255, 255)),
)
font = ImageFont.truetype('./Kaushan_Script/KaushanScript-Regular.ttf', _(80))
for x, y in zip(s, c):
  im = Image.new('RGBA', (_(120), _(120)), (0, 0, 0, 0))
  draw = ImageDraw.Draw(im)
  w, h = draw.textsize(x[0], font = font)
  draw.text(((_(120) - w) / 2, (_(96.) - h) / 2), x[0], y[0], font = font)
  pi = im.load()
  w, h = im.size
  d = blur(pi, w, h, _(4))
  dd = [[] for _ in range(h)]
  mx = 0
  for i in range(w):
    for j in range(h):
      r, g, b, a = pi[(i, j)]
      if d[i][j]:
        aa = (255 - a) * d[i][j] / 255
        r, g, b = inner((r, g, b), a, y[0], aa)
        a += aa
      if a > d[i][j]:
        tt = a - d[i][j]
        mx = max(tt, mx)
        tt *= 1.5
        aa = (255 - tt) * a / 255
        r, g, b = inner((r, g, b), aa, y[1], tt)
        a = aa + tt
      r, g, b = inner((r, g, b), j + h + .5, y[1], h - j - .5)
      dd[i].append((r, g, b, a))
  if len(x) > 1:
    im2 = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    dd2 = [[(0, 0, 0, 0)] * w for _ in range(h)]
    for k in range(len(x)):
      dx = (k + k - len(x) + 1) * _(12)
      dy = (k + k - len(x) + 1) * _(6)
      for i in range(max(-dx, 0), min(w - dx, w)):
        for j in range(max(-dy, 0), min(h - dy, h)):
          r1, g1, b1, a1 = dd[i][j]
          if not a1: continue
          r2, g2, b2, a2 = dd2[i + dx][j + dy]
          a2 *= (255 - a1) / 255
          r, g, b = inner((r1, g1, b1), a1, (r2, g2, b2), a2)
          a = a1 + a2
          dd2[i + dx][j + dy] = (r, g, b, a)
    dd = dd2
  for i in range(w):
    for j in range(h):
      pi[(i, j)] = toInt(dd[i][j])
  im.save(f'Rank{x}/default.png', optimize = True)

s = ('POOR', 'POOR', 'BAD', 'GOOD', 'GREAT', 'GREAT')
c = ((0, 0, 255), (255, 0, 0), (85, 85, 85), (0, 255, 0), (255, 255, 0), (255, 255, 255))
font = ImageFont.truetype('./Lato/Lato-Bold.ttf', _(32))
for T in range(len(s)):
  im = Image.new('RGBA', (_(400), _(240)), (0, 0, 0, 0))
  draw = ImageDraw.Draw(im)
  w, h = draw.textsize(s[T], font = font)
  draw.text(((_(400) - w) / 2, (_(240) - h) / 2), s[T], c[T], font = font)
  pi = im.load()
  w, h = im.size
  d = blur(pi, w, h, _(2))
  for i in range(w):
    for j in range(h):
      if not d[i][j]: continue
      r, g, b, a = pi[(i, j)]
      aa = (255 - a) * d[i][j] / 255
      r, g, b = inner((r, g, b), a, (0, 0, 0), aa)
      a += aa
      pi[(i, j)] = toInt((r, g, b, a))
  im.save(f'Judge{T}/default.png', optimize = True)

zf = zipfile.ZipFile(f'{NAME}.zip', 'w')
for _, path, *_ in CUSTOMFILE:
  for file in os.listdir(path):
    zf.write(f'{path}/{file}')
zf.write('7.lr2skin')
zf.write('7b.lr2skin')
zf.write('decide.lr2skin')
zf.close()
