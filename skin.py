from PIL import Image, ImageDraw, ImageFont
import os, shutil, sys, zipfile

HEIGHT = int(sys.argv[1]) if len(sys.argv) > 1 else 480
NAME = f'simple{sys.argv[2]}' if len(sys.argv) > 2 else 'simple'
CREATOR = 'yune'
CUSTOMOPTION = (
  ('TURNTABLE', ('LEFT', 'RIGHT')),
)
CUSTOMFILE = (
  ('NOTE', 'Note', 'csv'),
  ('GAUGE', 'Gauge'),
  ('NUMBER SMALL', 'NumberSmall'),
  ('NUMBER BIG', 'NumberBig'),
  ('SHUTTER', 'Shutter'),
  ('OPTION', 'Option'),
  ('FINISH', 'Finish'),
  ('FRAME LEFT', 'FrameLeft'),
  ('FRAME RIGHT', 'FrameRight'),
  ('PROGRESS', 'Progress'),
  ('LOADING', 'Loading'),
  ('LINE', 'Line'),
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
  type(t) is int else
  t * HEIGHT / 480
)

buffer = []

i = 900
OP = {}
for op, labels in CUSTOMOPTION:
  buffer.append(f'#CUSTOMOPTION,{op},{i},{",".join(labels)}\n')
  t = {}
  for label in labels:
    t[label] = i
    i += 1
  OP[op] = t
for op, path, *args in CUSTOMFILE:
  buffer.append(f'#CUSTOMFILE,{op},LR2files\\Theme\\{NAME}\\{path}\\*.{args[0] if len(args) > 0 else "png"},default\n')
  if os.path.isdir(path): shutil.rmtree(path)
  os.mkdir(path)

buffer.append('#ENDOFHEADER\n')

IMAGE = {}
N = 0
for op, path, *args in CUSTOMFILE:
  if args: continue
  IMAGE[op] = N
  buffer.append(f'#IMAGE,LR2files\\Theme\\{NAME}\\{path}\\*.png\n')
  N += 1

buffer.append('#SCRATCHSIDE,0,0\n')
buffer.append('#STARTINPUT,0\n')
buffer.append('#LOADSTART,0\n')
buffer.append('#LOADEND,1000\n')
buffer.append('#PLAYSTART,1000\n')
buffer.append('#FADEOUT,100\n')
buffer.append('#CLOSE,100\n')

buffer = ''.join(buffer)

def src(tag, num, img, x, y, w, h, dx, dy, *args):
  f.write(f'#SRC_{tag},{num},{img if type(img) is int else IMAGE[img]},{x},{y},{w},{h},{dx},{dy}{"".join(f",{arg}" for arg in args)}\n')

def dst(tag, num, x, y, w, h, *args, time = 0, alpha = 255, blend = 0):
  f.write(f'#DST_{tag},{num},{time},{x},{y},{w},{h},0,{alpha},255,255,255,{blend},0,0,0{"".join(f",{arg}" for arg in args)}\n')

def lr2skin(b):
  f.write(f'#INFORMATION,{12 if b else 0},{NAME},{CREATOR}\n')
  f.write(buffer)
  
  src('LINE', 0, 'LINE', 0, 0, _(400), _(50), 1, 1)
  dst('LINE', 0, _(120), _(455), _(400), _(50))

  f.write(f'#INCLUDE,LR2files\\Theme\\{NAME}\\Note\\*.csv\n')

  src('SLIDER', 0, 'SHUTTER', 0, 0, 1, _(480), 1, 1, 0, 0, 2, _(480), 4, 1)
  dst('SLIDER', 0, _(120), _(-480), _(400), _(480))

  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 12, _(24) * 2, 12, 2, 0, 0, 108, 0, 5)
  dst('NUMBER', 0, _(284), _(48), _(12), _(24))

  for i in range(6):
    src('NOWJUDGE_1P', i, f'JUDGE {i}', 0, 0, _(400), _(240), 1, 1, 0, 0, 1)
    dst('NOWJUDGE_1P', i, _(120), _(0), _(400), _(240))

  for i in range(3, 6):
    src('NOWCOMBO_1P', i, 'NUMBER BIG', 0, 0, _(24) * 10, _(48), 10, 1, 0, 0, 0, 1, 8)
    dst('NOWCOMBO_1P', i, _(188), _(216), _(24), _(48))

  src('IMAGE', 0, 'FINISH', 0, 0, _(400), _(240), 1, 1)
  dst('IMAGE', 0, _(120), _(240), _(400), _(240), 0, 143)

  src('IMAGE', 0, 'FRAME LEFT', 0, 0, _(120), _(480), 1, 1)
  dst('IMAGE', 0, _(0), _(0), _(120), _(480))

  src('BARGRAPH', 0, 'LOADING', 0, 0, 1, 1, 1, 1, 0, 0, 2, 1)
  dst('BARGRAPH', 0, _(96), _(360), _(24), _(-360), 0, 0, 80)

  src('IMAGE', 0, 'LOADING', 0, 0, 1, 1, 1, 1)
  dst('IMAGE', 0, _(96), _(0), _(24), _(360), -1, 40, 81, blend = 1)
  dst('IMAGE', 0, _(96), _(0), _(24), _(360), time = 1000, alpha = 0)

  src('SLIDER', 0, 'PROGRESS', 0, 0, _(24), _(24), 1, 1, 0, 0, 2, _(336), 6, 1)
  dst('SLIDER', 0, _(96), _(0), _(24), _(24), 0, 0, 81)

  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 102, 0, 2)
  dst('NUMBER', 0, _(24), _(24), _(12), _(24))
  src('IMAGE', 0, 'DOT', 0, 0, _(12), _(24), 1, 1)
  dst('IMAGE', 0, _(48), _(24), _(12), _(24))
  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 103, 0, 2)
  dst('NUMBER', 0, _(60), _(24), _(12), _(24))

  for i in range(5):
    src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 110 + i, 0, 5)
    dst('NUMBER', 0, _(24), _(i * 24 + 48), _(12), _(24))

  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 163, 0, 2)
  dst('NUMBER', 0, _(24), _(324), _(12), _(24))
  src('IMAGE', 0, 'COLON', 0, 0, _(12), _(24), 1, 1)
  dst('IMAGE', 0, _(48), _(324), _(12), _(24))
  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 164, 0, 2)
  dst('NUMBER', 0, _(60), _(324), _(12), _(24))

  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 10, 0, 3)
  dst('NUMBER', 0, _(72), _(360), _(12), _(24))

  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _(12) * 11, _(24), 11, 1, 0, 0, 160, 0, 3)
  dst('NUMBER', 0, _(72), _(384), _(12), _(24))

  src('BUTTON', 0, 'OPTION', 0, 0, _(120), _(24) * 6, 1, 6, 0, 0, 42, 0, 0, 0)
  dst('BUTTON', 0, _(0), _(408), _(120), _(24))

  src('BUTTON', 0, 'OPTION', 0, _(24) * 6, _(120), _(24) * 6, 1, 6, 0, 0, 40, 0, 0, 0)
  dst('BUTTON', 0, _(0), _(432), _(120), _(24))

  for i in range(4):
    src('IMAGE', 0, 'OPTION', 0, _(24) * (i + 12), _(120), _(24), 1, 1)
    dst('IMAGE', 0, _(0), _(456), _(120), _(24), 0, 0, 180 + i)

  src('IMAGE', 0, 'FRAME RIGHT', 0, 0, _(120), _(480), 1, 1)
  dst('IMAGE', 0, _(520), _(0), _(120), _(480))

  for i, t in enumerate(('AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F')):
    src('IMAGE', 0, f'RANK {t}', 0, 0, _(120), _(120), 1, 1)
    dst('IMAGE', 0, _(520), _(0), _(120), _(120), 0, 0, 200 + i)

  src('NUMBER', 0, 'NUMBER BIG', 0, 0, _(24) * 10, _(48), 10, 1, 0, 0, 107, 2, 3)
  dst('NUMBER', 0, _(544), _(126), _(24), _(48))

  src('GROOVEGAUGE', 0, 'GAUGE', 0, 0, _(120), _(6) * 4, 1, 4, 0, 0, 0, _(-6))
  dst('GROOVEGAUGE', 0, _(520), _(474), _(120), _(6))

  if b:
    for i in range(8):
      dst('NOTE', i + 10, 0, 0, 0, 0)

with open('7.lr2skin', 'w') as f:
  lr2skin(False)
with open('7b.lr2skin', 'w') as f:
  lr2skin(True)

def image(name):
  f.write(f'#IMAGE,LR2files\\Theme\\{NAME}\\Note\\{name}.png\n')

a = (0, 1, 2, 1, 2, 1, 2, 1)
with open('Note/default.csv', 'w') as f:
  for y in ('Red', 'White', 'Blue'):
    image(f'default{y}')
  for i in range(8): src('NOTE', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  for i in range(8): src('LN_START', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  for i in range(8): src('LN_BODY', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  for i in range(8): src('LN_END', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  f.write(f'#IF,{OP["TURNTABLE"]["LEFT"]}\n')
  for i in range(8): dst('NOTE', i, _(120 + i * 50), _(472), _(50), _(16))
  f.write(f'#ENDIF\n')
  f.write(f'#IF,{OP["TURNTABLE"]["RIGHT"]}\n')
  for i in range(8): dst('NOTE', i + 1 & 7, _(120 + i * 50), _(472), _(50), _(16))
  f.write(f'#ENDIF\n')

with open('Note/defaultMirror.csv', 'w') as f:
  for y in ('Red', 'White', 'Blue'):
    image(f'default{y}')
  for i in range(8): src('NOTE', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  for i in range(8): src('LN_START', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  for i in range(8): src('LN_BODY', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  for i in range(8): src('LN_END', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  f.write(f'#IF,{OP["TURNTABLE"]["LEFT"]}\n')
  for i in range(8): dst('NOTE', -i & 7, _(120 + i * 50), _(472), _(50), _(16))
  f.write(f'#ENDIF\n')
  f.write(f'#IF,{OP["TURNTABLE"]["RIGHT"]}\n')
  for i in range(8): dst('NOTE', 7 - i, _(120 + i * 50), _(472), _(50), _(16))
  f.write(f'#ENDIF\n')

with open('Note/diamond.csv', 'w') as f:
  def image(name):
    f.write(f'#IMAGE,LR2files\\Theme\\{NAME}\\Note\\{name}.png\n')
  for x in ('diamondNote', 'diamondLNStart', 'default', 'diamondLNEnd'):
    for y in ('Red', 'White', 'Blue'):
      image(f'{x}{y}')
  for i in range(8): src('NOTE', i, N + a[i], 0, 0, _(50), _(50), 1, 1)
  for i in range(8): src('LN_START', i, N + a[i] + 3, 0, 0, _(50), _(50), 1, 1)
  for i in range(8): src('LN_BODY', i, N + a[i] + 6, 0, 0, _(50), 1, 1, 1)
  for i in range(8): src('LN_END', i, N + a[i] + 9, 0, 0, _(50), _(50), 1, 1)
  f.write(f'#IF,{OP["TURNTABLE"]["LEFT"]}\n')
  for i in range(8): dst('NOTE', i, _(120 + i * 50), _(465), _(50), _(50))
  f.write(f'#ENDIF\n')
  f.write(f'#IF,{OP["TURNTABLE"]["RIGHT"]}\n')
  for i in range(8): dst('NOTE', i + 1 & 7, _(120 + i * 50), _(465), _(50), _(50))
  f.write(f'#ENDIF\n')

a = (0, 1, 2, 1, 3, 1, 2, 1)
with open('Note/default2.csv', 'w') as f:
  for y in ('Red', 'White', 'Blue', 'Orange'):
    image(f'default{y}')
  for i in range(8): src('NOTE', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  for i in range(8): src('LN_START', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  for i in range(8): src('LN_BODY', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  for i in range(8): src('LN_END', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  f.write(f'#IF,{OP["TURNTABLE"]["LEFT"]}\n')
  for i in range(8): dst('NOTE', i, _(120 + i * 50), _(472), _(50), _(16))
  f.write(f'#ENDIF\n')
  f.write(f'#IF,{OP["TURNTABLE"]["RIGHT"]}\n')
  for i in range(8): dst('NOTE', i + 1 & 7, _(120 + i * 50), _(472), _(50), _(16))
  f.write(f'#ENDIF\n')

with open('Note/default2Mirror.csv', 'w') as f:
  for y in ('Red', 'White', 'Blue', 'Orange'):
    image(f'default{y}')
  for i in range(8): src('NOTE', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  for i in range(8): src('LN_START', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  for i in range(8): src('LN_BODY', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  for i in range(8): src('LN_END', i, N + a[i], 0, 0, _(50), 1, 1, 1)
  f.write(f'#IF,{OP["TURNTABLE"]["LEFT"]}\n')
  for i in range(8): dst('NOTE', -i & 7, _(120 + i * 50), _(472), _(50), _(16))
  f.write(f'#ENDIF\n')
  f.write(f'#IF,{OP["TURNTABLE"]["RIGHT"]}\n')
  for i in range(8): dst('NOTE', 7 - i, _(120 + i * 50), _(472), _(50), _(16))
  f.write(f'#ENDIF\n')

im = Image.new('RGBA', (_(120), _(480)), (0, 0, 0, 0))
pi = im.load()
for i in range(_(480)): pi[(_(120) - 1, i)] = (255, 255, 255, 255)
for i in range(_(360)): pi[(_(96), i)] = (255, 255, 255, 255)
for i in range(360, 480, 24):
  for j in range(_(120)):
    pi[(j, _(i))] = (255, 255, 255, 255)
font = ImageFont.truetype('./Lato/Lato-Regular.ttf', _(16))
draw = ImageDraw.Draw(im)
txt = ['SPEED', 'B  P  M']
for i in range(len(txt)):
  w, h = draw.textsize(txt[i], font = font)
  draw.text(((_(60) - w) / 2, (_(48 * i + 740.) - h) / 2), txt[i], (255, 255, 255), font = font)
im.save('FrameLeft/default.png', optimize = True)

im = Image.new('RGBA', (_(120), _(480)), (0, 0, 0, 0))
pi = im.load()
for i in range(_(480)): pi[(0, i)] = (255, 255, 255, 255)
im.save('FrameRight/default.png', optimize = True)

im = Image.new('RGBA', (1, _(480)), (0, 0, 0, 255))
pi = im.load()
pi[(0, _(480) - 1)] = (255, 255, 255, 255)
im.save('Shutter/default.png', optimize = True)

im = Image.new('RGBA', (_(120), _(24) * 16), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
txt = [
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
]
for i in range(len(txt)):
  w, h = draw.textsize(txt[i], font = font)
  draw.text(((_(120) - w) / 2, _(24) * i + (_(20.) - h) / 2), txt[i], (255, 255, 255), font = font)
im.save('Option/default.png', optimize = True)

im = Image.new('RGBA', (_(24), _(24)), (0, 0, 0, 0))
pi = im.load()
for i in range(_(6), _(18)):
  for j in range(_(6), _(18)):
    pi[(i, j)] = (255, 255, 255, 255)
im.save('Progress/default.png', optimize = True)

im = Image.new('RGBA', (1, 1), (170, 170, 170, 255))
im.save('Loading/default.png', optimize = True)

im = Image.new('RGBA', (_(400), _(50)), (0, 0, 0, 0))
pi = im.load()
for i in range(_(400)):
  pi[(i, _(25))] = (170, 170, 170, 255)
im.save('Line/default.png', optimize = True)

for n, c in (
  ('Red', (255, 0, 0)),
  ('Blue', (0, 128, 255)),
  ('White', (255, 255, 255)),
  ('Orange', (255, 128, 0)),
):
  im = Image.new('RGBA', (_(50), 1), (0, 0, 0, 0))
  pi = im.load()
  for i in range(_(1), _(49)):
    pi[(i, 0)] = (*c, 255)
  im.save(f'Note/default{n}.png', optimize = True)
  im = Image.new('RGBA', (_(50), _(50)), (0, 0, 0, 0))
  pi = im.load()
  for i in range(_(50)):
    for j in range(_(50)):
      t = (abs(i + i - _(50) + 1) + abs(j + j - _(50) + 1) < _(48.)) * 255
      pi[(i, j)] = (*c, t)
  im.save(f'Note/diamondNote{n}.png', optimize = True)
  im = Image.new('RGBA', (_(50), _(50)), (0, 0, 0, 0))
  pi = im.load()
  for i in range(_(50)):
    for j in range(_(50)):
      t = (abs(i + i - _(50) + 1) + max(0, j + j - _(50) + 1) < _(48.)) * 255
      if t > 255: t = 255
      pi[(i, j)] = (*c, t)
  im.save(f'Note/diamondLNStart{n}.png', optimize = True)
  im = Image.new('RGBA', (_(50), _(50)), (0, 0, 0, 0))
  pi = im.load()
  for i in range(_(50)):
    for j in range(_(50)):
      t = (abs(i + i - _(50) + 1) + max(0, _(50) - j - j - 1) < _(48.)) * 255
      pi[(i, j)] = (*c, t)
  im.save(f'Note/diamondLNEnd{n}.png', optimize = True)

im = Image.new('RGBA', (_(120), _(6) * 4), (0, 0, 0, 0))
pi = im.load()
c = [(255, 255, 255, 255), (0, 0, 255, 255), (0, 0, 0, 0), (0, 0, 85, 255)]
for i in range(_(30), _(90)):
  for j in range(_(6) * 4):
    pi[(i, j)] = c[j // _(6)]
im.save('Gauge/default.png', optimize = True)

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
d = blur(pi, w, h, _(1))
for i in range(w):
  for j in range(h):
    if not d[i][j]: continue
    r, g, b, a = pi[(i, j)]
    aa = (255 - a) * d[i][j] / 255
    r, g, b = inner((r, g, b), a, (0, 0, 0), aa)
    a += aa
    pi[(i, j)] = toInt((r, g, b, a))
im.save('NumberSmall/default.png', optimize = True)

s = ['AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F']
c = [
  ((221, 238, 255), (255, 255, 255)),
  ((255, 255, 0), (255, 255, 255)),
  ((0, 255, 0), (255, 255, 255)),
  ((0, 0, 255), (255, 255, 255)),
  ((85, 85, 85), (255, 255, 255)),
  ((85, 85, 85), (255, 255, 255)),
  ((85, 85, 85), (255, 255, 255)),
  ((85, 85, 85), (255, 255, 255)),
]
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

s = ['POOR', 'POOR', 'BAD', 'GOOD', 'GREAT', 'GREAT']
c = [(0, 0, 255), (255, 0, 0), (85, 85, 85), (0, 255, 0), (255, 255, 0), (255, 255, 255)]
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
