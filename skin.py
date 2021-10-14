from PIL import Image, ImageDraw, ImageFont
import os, shutil, sys, zipfile

# For SD, use height = 480 and offset = 0

if len(sys.argv) != 4:
  print(f'Usage: {sys.argv[0]} height offset name')
  exit()

HEIGHT = int(sys.argv[1])
OFFSET = int(sys.argv[2])
NAME = f'simple{sys.argv[3]}'
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

_x = lambda t: (
  (t * HEIGHT + t * HEIGHT // 480 % 2 + 239) // 480 + OFFSET if
  type(t) is int else
  t * HEIGHT / 480 + OFFSET
)
_y = lambda t: (
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
buffer.append(f'#INCLUDE,LR2files\\Theme\\{NAME}\\7.csv\n')
buffer = ''.join(buffer)

with open('7.lr2skin', 'w') as f:
  f.write(f'#INFORMATION,0,{NAME},{CREATOR}\n')
  f.write(buffer)
with open('7gb.lr2skin', 'w') as f:
  f.write(f'#INFORMATION,12,{NAME},{CREATOR}\n')
  f.write(buffer)

def src(tag, num, img, x, y, w, h, dx, dy, *args):
  f.write(f'#SRC_{tag},{num},{img if type(img) is int else IMAGE[img]},{x},{y},{w},{h},{dx},{dy}{"".join(f",{arg}" for arg in args)}\n')

def dst(tag, num, x, y, w, h, *args, time = 0, alpha = 255, blend = 0):
  f.write(f'#DST_{tag},{num},{time},{x},{y},{w},{h},0,{alpha},255,255,255,{blend},0,0,0{"".join(f",{arg}" for arg in args)}\n')

IMAGE = {}
N = 0
with open('7.csv', 'w') as f:
  f.write('#SCRATCHSIDE,0,0\n')
  f.write('#STARTINPUT,0\n')
  f.write('#LOADSTART,0\n')
  f.write('#LOADEND,1000\n')
  f.write('#PLAYSTART,1000\n')
  f.write('#FADEOUT,100\n')
  f.write('#CLOSE,100\n')
  for op, path, *args in CUSTOMFILE:
    if args: continue
    IMAGE[op] = N
    f.write(f'#IMAGE,LR2files\\Theme\\{NAME}\\{path}\\*.png\n')
    N += 1

  src('LINE', 0, 'LINE', 0, 0, _y(400), _y(50), 1, 1)
  dst('LINE', 0, _x(120), _y(455), _y(400), _y(50))

  f.write(f'#INCLUDE,LR2files\\Theme\\{NAME}\\Note\\*.csv\n')

  src('SLIDER', 0, 'SHUTTER', 0, 0, 1, _y(480), 1, 1, 0, 0, 2, _y(480), 4, 1)
  dst('SLIDER', 0, _x(120), _y(-480), _y(400), _y(480))

  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _y(12) * 12, _y(24) * 2, 12, 2, 0, 0, 108, 0, 5)
  dst('NUMBER', 0, _x(284), _y(48), _y(12), _y(24))

  for i in range(6):
    src('NOWJUDGE_1P', i, f'JUDGE {i}', 0, 0, _y(400), _y(240), 1, 1, 0, 0, 1)
    dst('NOWJUDGE_1P', i, _x(120), _y(0), _y(400), _y(240))

  for i in range(3, 6):
    src('NOWCOMBO_1P', i, 'NUMBER BIG', 0, 0, _y(24) * 10, _y(48), 10, 1, 0, 0, 0, 1, 8)
    dst('NOWCOMBO_1P', i, _y(188), _y(216), _y(24), _y(48))

  src('IMAGE', 0, 'FRAME LEFT', 0, 0, _y(120), _y(480), 1, 1)
  dst('IMAGE', 0, _x(0), _y(0), _y(120), _y(480))

  src('BARGRAPH', 0, 'LOADING', 0, 0, 1, 1, 1, 1, 0, 0, 2, 1)
  dst('BARGRAPH', 0, _x(96), _y(360), _y(24), _y(-360), 0, 0, 80)

  src('IMAGE', 0, 'LOADING', 0, 0, 1, 1, 1, 1)
  dst('IMAGE', 0, _x(96), _y(0), _y(24), _y(360), -1, 40, 81, blend = 1)
  dst('IMAGE', 0, _x(96), _y(0), _y(24), _y(360), time = 1000, alpha = 0)

  src('SLIDER', 0, 'PROGRESS', 0, 0, _y(24), _y(24), 1, 1, 0, 0, 2, _y(336), 6, 1)
  dst('SLIDER', 0, _x(96), _y(0), _y(24), _y(24), 0, 0, 81)

  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _y(12) * 11, _y(24), 11, 1, 0, 0, 102, 0, 2)
  dst('NUMBER', 0, _x(24), _y(24), _y(12), _y(24))
  src('IMAGE', 0, 'DOT', 0, 0, _y(12), _y(24), 1, 1)
  dst('IMAGE', 0, _x(48), _y(24), _y(12), _y(24))
  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _y(12) * 11, _y(24), 11, 1, 0, 0, 103, 0, 2)
  dst('NUMBER', 0, _x(60), _y(24), _y(12), _y(24))

  for i in range(5):
    src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _y(12) * 11, _y(24), 11, 1, 0, 0, 110 + i, 0, 5)
    dst('NUMBER', 0, _x(24), _y(i * 24 + 48), _y(12), _y(24))

  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _y(12) * 11, _y(24), 11, 1, 0, 0, 163, 0, 2)
  dst('NUMBER', 0, _x(24), _y(324), _y(12), _y(24))
  src('IMAGE', 0, 'COLON', 0, 0, _y(12), _y(24), 1, 1)
  dst('IMAGE', 0, _x(48), _y(324), _y(12), _y(24))
  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _y(12) * 11, _y(24), 11, 1, 0, 0, 164, 0, 2)
  dst('NUMBER', 0, _x(60), _y(324), _y(12), _y(24))

  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _y(12) * 11, _y(24), 11, 1, 0, 0, 10, 0, 3)
  dst('NUMBER', 0, _x(72), _y(360), _y(12), _y(24))

  src('NUMBER', 0, 'NUMBER SMALL', 0, 0, _y(12) * 11, _y(24), 11, 1, 0, 0, 160, 0, 3)
  dst('NUMBER', 0, _x(72), _y(384), _y(12), _y(24))

  src('BUTTON', 0, 'OPTION', 0, 0, _y(120), _y(24) * 6, 1, 6, 0, 0, 42, 0, 0, 0)
  dst('BUTTON', 0, _x(0), _y(408), _y(120), _y(24))

  src('BUTTON', 0, 'OPTION', 0, _y(24) * 6, _y(120), _y(24) * 6, 1, 6, 0, 0, 40, 0, 0, 0)
  dst('BUTTON', 0, _x(0), _y(432), _y(120), _y(24))

  for i in range(4):
    src('IMAGE', 0, 'OPTION', 0, _y(24) * (i + 12), _y(120), _y(24), 1, 1)
    dst('IMAGE', 0, _x(0), _y(456), _y(120), _y(24), 0, 0, 180 + i)

  src('IMAGE', 0, 'FRAME RIGHT', 0, 0, _y(120), _y(480), 1, 1)
  dst('IMAGE', 0, _x(520), _y(0), _y(120), _y(480))

  for i, t in enumerate(('AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F')):
    src('IMAGE', 0, f'RANK {t}', 0, 0, _y(120), _y(120), 1, 1)
    dst('IMAGE', 0, _x(520), _y(0), _y(120), _y(120), 0, 0, 200 + i)

  src('NUMBER', 0, 'NUMBER BIG', 0, 0, _y(24) * 10, _y(48), 10, 1, 0, 0, 107, 2, 3)
  dst('NUMBER', 0, _x(544), _y(126), _y(24), _y(48))

  src('GROOVEGAUGE', 0, 'GAUGE', 0, 0, _y(120), _y(6) * 4, 1, 4, 0, 0, 0, _y(-6))
  dst('GROOVEGAUGE', 0, _x(520), _y(474), _y(120), _y(6))

def image(name):
  f.write(f'#IMAGE,LR2files\\Theme\\{NAME}\\Note\\{name}.png\n')

a = (0, 1, 2, 1, 2, 1, 2, 1)
with open('Note/default.csv', 'w') as f:
  for y in ('Red', 'White', 'Blue'):
    image(f'default{y}')
  for i in range(8): src('NOTE', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  for i in range(8): src('LN_START', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  for i in range(8): src('LN_BODY', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  for i in range(8): src('LN_END', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  f.write(f'#IF,{OP["TURNTABLE"]["LEFT"]}\n')
  for i in range(8): dst('NOTE', i, _x(120 + i * 50), _y(472), _y(50), _y(16))
  f.write(f'#ENDIF\n')
  f.write(f'#IF,{OP["TURNTABLE"]["RIGHT"]}\n')
  for i in range(8): dst('NOTE', i + 1 & 7, _x(120 + i * 50), _y(472), _y(50), _y(16))
  f.write(f'#ENDIF\n')

with open('Note/defaultMirror.csv', 'w') as f:
  for y in ('Red', 'White', 'Blue'):
    image(f'default{y}')
  for i in range(8): src('NOTE', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  for i in range(8): src('LN_START', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  for i in range(8): src('LN_BODY', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  for i in range(8): src('LN_END', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  f.write(f'#IF,{OP["TURNTABLE"]["LEFT"]}\n')
  for i in range(8): dst('NOTE', -i & 7, _x(120 + i * 50), _y(472), _y(50), _y(16))
  f.write(f'#ENDIF\n')
  f.write(f'#IF,{OP["TURNTABLE"]["RIGHT"]}\n')
  for i in range(8): dst('NOTE', 7 - i, _x(120 + i * 50), _y(472), _y(50), _y(16))
  f.write(f'#ENDIF\n')

with open('Note/diamond.csv', 'w') as f:
  def image(name):
    f.write(f'#IMAGE,LR2files\\Theme\\{NAME}\\Note\\{name}.png\n')
  for x in ('diamondNote', 'diamondLNStart', 'default', 'diamondLNEnd'):
    for y in ('Red', 'White', 'Blue'):
      image(f'{x}{y}')
  for i in range(8): src('NOTE', i, N + a[i], 0, 0, _y(50), _y(50), 1, 1)
  for i in range(8): src('LN_START', i, N + a[i] + 3, 0, 0, _y(50), _y(50), 1, 1)
  for i in range(8): src('LN_BODY', i, N + a[i] + 6, 0, 0, _y(50), 1, 1, 1)
  for i in range(8): src('LN_END', i, N + a[i] + 9, 0, 0, _y(50), _y(50), 1, 1)
  f.write(f'#IF,{OP["TURNTABLE"]["LEFT"]}\n')
  for i in range(8): dst('NOTE', i, _x(120 + i * 50), _y(465), _y(50), _y(50))
  f.write(f'#ENDIF\n')
  f.write(f'#IF,{OP["TURNTABLE"]["RIGHT"]}\n')
  for i in range(8): dst('NOTE', i + 1 & 7, _x(120 + i * 50), _y(465), _y(50), _y(50))
  f.write(f'#ENDIF\n')

a = (0, 1, 2, 1, 3, 1, 2, 1)
with open('Note/default2.csv', 'w') as f:
  for y in ('Red', 'White', 'Blue', 'Orange'):
    image(f'default{y}')
  for i in range(8): src('NOTE', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  for i in range(8): src('LN_START', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  for i in range(8): src('LN_BODY', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  for i in range(8): src('LN_END', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  f.write(f'#IF,{OP["TURNTABLE"]["LEFT"]}\n')
  for i in range(8): dst('NOTE', i, _x(120 + i * 50), _y(472), _y(50), _y(16))
  f.write(f'#ENDIF\n')
  f.write(f'#IF,{OP["TURNTABLE"]["RIGHT"]}\n')
  for i in range(8): dst('NOTE', i + 1 & 7, _x(120 + i * 50), _y(472), _y(50), _y(16))
  f.write(f'#ENDIF\n')

with open('Note/default2Mirror.csv', 'w') as f:
  for y in ('Red', 'White', 'Blue', 'Orange'):
    image(f'default{y}')
  for i in range(8): src('NOTE', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  for i in range(8): src('LN_START', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  for i in range(8): src('LN_BODY', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  for i in range(8): src('LN_END', i, N + a[i], 0, 0, _y(50), 1, 1, 1)
  f.write(f'#IF,{OP["TURNTABLE"]["LEFT"]}\n')
  for i in range(8): dst('NOTE', -i & 7, _x(120 + i * 50), _y(472), _y(50), _y(16))
  f.write(f'#ENDIF\n')
  f.write(f'#IF,{OP["TURNTABLE"]["RIGHT"]}\n')
  for i in range(8): dst('NOTE', 7 - i, _x(120 + i * 50), _y(472), _y(50), _y(16))
  f.write(f'#ENDIF\n')

im = Image.new('RGBA', (_y(120), _y(480)), (0, 0, 0, 0))
pi = im.load()
for i in range(_y(480)): pi[(_y(120) - 1, i)] = (255, 255, 255, 255)
for i in range(_y(360)): pi[(_y(96), i)] = (255, 255, 255, 255)
for i in range(360, 480, 24):
  for j in range(_y(120)):
    pi[(j, _y(i))] = (255, 255, 255, 255)
font = ImageFont.truetype('./Lato/Lato-Regular.ttf', _y(16))
draw = ImageDraw.Draw(im)
txt = ['SPEED', 'B  P  M']
for i in range(len(txt)):
  w, h = draw.textsize(txt[i], font = font)
  draw.text(((_y(60) - w) / 2, (_y(48 * i + 740.) - h) / 2), txt[i], (255, 255, 255), font = font)
im.save('FrameLeft/default.png', optimize = True)

im = Image.new('RGBA', (_y(120), _y(480)), (0, 0, 0, 0))
pi = im.load()
for i in range(_y(480)): pi[(0, i)] = (255, 255, 255, 255)
im.save('FrameRight/default.png', optimize = True)

im = Image.new('RGBA', (1, _y(480)), (0, 0, 0, 255))
pi = im.load()
pi[(0, _y(480) - 1)] = (255, 255, 255, 255)
im.save('Shutter/default.png', optimize = True)

im = Image.new('RGBA', (_y(120), _y(24) * 16), (0, 0, 0, 0))
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
  draw.text(((_y(120) - w) / 2, _y(24) * i + (_y(20.) - h) / 2), txt[i], (255, 255, 255), font = font)
im.save('Option/default.png', optimize = True)

im = Image.new('RGBA', (_y(24), _y(24)), (0, 0, 0, 0))
pi = im.load()
for i in range(_y(6), _y(18)):
  for j in range(_y(6), _y(18)):
    pi[(i, j)] = (255, 255, 255, 255)
im.save('Progress/default.png', optimize = True)

im = Image.new('RGBA', (1, 1), (170, 170, 170, 255))
im.save('Loading/default.png', optimize = True)

im = Image.new('RGBA', (_y(400), _y(50)), (0, 0, 0, 0))
pi = im.load()
for i in range(_y(400)):
  pi[(i, _y(25))] = (170, 170, 170, 255)
im.save('Line/default.png', optimize = True)

for n, c in (
  ('Red', (255, 0, 0)),
  ('Blue', (0, 128, 255)),
  ('White', (255, 255, 255)),
  ('Orange', (255, 128, 0)),
):
  im = Image.new('RGBA', (_y(50), 1), (0, 0, 0, 0))
  pi = im.load()
  for i in range(_y(1), _y(49)):
    pi[(i, 0)] = (*c, 255)
  im.save(f'Note/default{n}.png', optimize = True)
  im = Image.new('RGBA', (_y(50), _y(50)), (0, 0, 0, 0))
  pi = im.load()
  for i in range(_y(50)):
    for j in range(_y(50)):
      t = (abs(i + i - _y(50) + 1) + abs(j + j - _y(50) + 1) < _y(48.)) * 255
      pi[(i, j)] = (*c, t)
  im.save(f'Note/diamondNote{n}.png', optimize = True)
  im = Image.new('RGBA', (_y(50), _y(50)), (0, 0, 0, 0))
  pi = im.load()
  for i in range(_y(50)):
    for j in range(_y(50)):
      t = (abs(i + i - _y(50) + 1) + max(0, j + j - _y(50) + 1) < _y(48.)) * 255
      if t > 255: t = 255
      pi[(i, j)] = (*c, t)
  im.save(f'Note/diamondLNStart{n}.png', optimize = True)
  im = Image.new('RGBA', (_y(50), _y(50)), (0, 0, 0, 0))
  pi = im.load()
  for i in range(_y(50)):
    for j in range(_y(50)):
      t = (abs(i + i - _y(50) + 1) + max(0, _y(50) - j - j - 1) < _y(48.)) * 255
      pi[(i, j)] = (*c, t)
  im.save(f'Note/diamondLNEnd{n}.png', optimize = True)

im = Image.new('RGBA', (_y(120), _y(6) * 4), (0, 0, 0, 0))
pi = im.load()
c = [(255, 255, 255, 255), (0, 0, 255, 255), (0, 0, 0, 0), (0, 0, 85, 255)]
for i in range(_y(30), _y(90)):
  for j in range(_y(6) * 4):
    pi[(i, j)] = c[j // _y(6)]
im.save('Gauge/default.png', optimize = True)

font = ImageFont.truetype('./Lato/Lato-Regular.ttf', _y(16))
im = Image.new('RGBA', (_y(12), _y(24)), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
w, h = draw.textsize('.', font = font)
draw.text(((_y(12) - w) / 2, (_y(20.) - h) / 2), '.', (255, 255, 255), font = font)
im.save('Dot/default.png', optimize = True)

im = Image.new('RGBA', (_y(12), _y(24)), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
w, h = draw.textsize(':', font = font)
draw.text(((_y(12) - w) / 2, (_y(20.) - h) / 2), ':', (255, 255, 255), font = font)
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
font = ImageFont.truetype('./Lato/Lato-Bold.ttf', _y(32))
im = Image.new('RGBA', (len(s) * _y(24), _y(48)), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
for i in range(len(s)):
  w, h = draw.textsize(s[i], font = font)
  draw.text((i * _y(24) + (_y(24) - w) / 2, (_y(40.) - h) / 2), s[i], (255, 255, 255), font = font)
pi = im.load()
w, h = im.size
d = blur(pi, w, h, _y(2))
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
font = ImageFont.truetype('./Lato/Lato-Regular.ttf', _y(16))
im = Image.new('RGBA', (len(s[0]) * _y(12), _y(24) * 2), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
for j in range(len(s)):
  for i in range(len(s[j])):
    w, h = draw.textsize(s[j][i], font = font)
    draw.text((i * _y(12) + (_y(12) - w) / 2, j * _y(24) + (_y(20.) - h) / 2), s[j][i], c[j], font = font)
pi = im.load()
w, h = im.size
d = blur(pi, w, h, _y(1))
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
font = ImageFont.truetype('./Kaushan_Script/KaushanScript-Regular.ttf', _y(80))
for x, y in zip(s, c):
  im = Image.new('RGBA', (_y(120), _y(120)), (0, 0, 0, 0))
  draw = ImageDraw.Draw(im)
  w, h = draw.textsize(x[0], font = font)
  draw.text(((_y(120) - w) / 2, (_y(96.) - h) / 2), x[0], y[0], font = font)
  pi = im.load()
  w, h = im.size
  d = blur(pi, w, h, _y(4))
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
      dx = (k + k - len(x) + 1) * _y(12)
      dy = (k + k - len(x) + 1) * _y(6)
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
font = ImageFont.truetype('./Lato/Lato-Bold.ttf', _y(32))
for T in range(len(s)):
  im = Image.new('RGBA', (_y(400), _y(240)), (0, 0, 0, 0))
  draw = ImageDraw.Draw(im)
  w, h = draw.textsize(s[T], font = font)
  draw.text(((_y(400) - w) / 2, (_y(240) - h) / 2), s[T], c[T], font = font)
  pi = im.load()
  w, h = im.size
  d = blur(pi, w, h, _y(2))
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
zf.write('7.csv')
zf.write('7.lr2skin')
zf.write('7gb.lr2skin')
zf.close()
