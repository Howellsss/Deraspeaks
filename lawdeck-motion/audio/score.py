"""Original score and sound design for the Lawdeck film, generated from code (no samples).

    python3 audio/score.py                -> audio/score.wav (72 s, 48 kHz stereo)

The grid is ~113 bpm: a bar is 2.125 s, so every 8.5 s product scene is exactly four bars
and each scene change lands on a downbeat.
  0.0 - 3.7   cold open: three impacts with paper bursts, a reverse swell into the deck
  3.7 - 7.5   tension, ticking hats, riser; impact on "Meet Lawdeck"; drop at 7.5
  7.5 - 50    groove: kick, snap, hats, sub, plucked arp; it builds scene by scene
  50  - 56    feature ribbon: four on the floor, brightest point
  56  - 61.6  trust: drums out, a heartbeat under each line
  61.6- 64.6  riser, a beat of silence, then the logo hit and a D major resolve
"""
import numpy as np, wave, os

SR = 48000
DUR = 72.0
N = int(SR * DUR)
T = np.arange(N) / SR
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)

BAR = 2.125; BEAT = BAR / 4; GRID0 = 7.5
HITS = [0.35, 1.15, 1.95]; MEET = 5.6; SC0 = 7.5; SCL = 8.5
FT0 = SC0 + 5 * SCL; TR = FT0 + 6; TE = TR + 5.6; LOGO = TE + 3.0

def hz(m): return 440 * 2 ** ((m - 69) / 12)
def add(sig, t0, gain=1.0, pan=0.0):
    s = int(t0 * SR); e = min(N, s + len(sig))
    if s < 0: sig = sig[-s:]; s = 0
    if e <= s: return
    seg = sig[:e - s] * gain
    L[s:e] += seg * np.sqrt(0.5 * (1 - pan)); R[s:e] += seg * np.sqrt(0.5 * (1 + pan))
def lp(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y
def noise(sec): return rng.standard_normal(int(sec * SR))
def tt(sec): return np.arange(int(sec * SR)) / SR
def level(points, t): xs, ys = zip(*points); return float(np.interp(t, xs, ys))

# ---------------- instruments ----------------
def kick(t0, g=1.0):
    t = tt(0.45); f = 45 + 95 * np.exp(-t * 28)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5) + 0.25 * np.exp(-t * 120) * rng.standard_normal(len(t)) * 0.3
    add(x * 0.55 * g, t0)
def snap(t0, g=1.0, pan=0.0):
    n = noise(0.18); x = (lp(n, 3500) - lp(n, 900)) * 2.2
    t = tt(0.18); env = np.exp(-t * 26) + 0.5 * np.exp(-np.maximum(0, t - 0.012) * 30) * (t > 0.012)
    add(x * env * 0.22 * g, t0, 1, pan)
HAT = noise(0.06); HAT = (HAT - lp(HAT, 7000)) * np.exp(-tt(0.06) * 70)
def hat(t0, g=1.0, pan=0.0): add(HAT * 0.12 * g, t0, 1, pan)
def pluck(m, t0, g=1.0, pan=0.0, dec=5.0):
    t = tt(1.0); f = hz(m)
    x = (np.sin(2 * np.pi * f * t) + 0.45 * np.sin(4 * np.pi * f * t) * np.exp(-t * 9) + 0.2 * np.sin(6 * np.pi * f * t) * np.exp(-t * 14))
    add(x * np.exp(-t * dec) * np.minimum(1, t / 0.004) * 0.09 * g, t0, 1, pan)
def sub(m, t0, length, g=1.0):
    t = tt(length); x = np.sin(2 * np.pi * hz(m) * t) + 0.15 * np.sin(4 * np.pi * hz(m) * t)
    env = np.minimum(1, t / 0.01) * np.minimum(1, (length - t) / 0.03)
    duck = 1 - 0.75 * np.exp(-((t % BEAT) / 0.09))      # side-chain feel against the kick
    add(x * env * duck * 0.2 * g, t0)
def impact(t0, g=1.0, low=36.0):
    t = tt(3.0); f = low * (1 + 0.6 * np.exp(-t * 9))
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6)
    crack = lp(noise(3.0), 2200) * np.exp(-t * 9) * 1.4
    add((boom * 0.6 + crack * 0.25) * g, t0)
def whoosh(t0, length=0.9, g=1.0, pan=0.0, bright=2600, rev=False):
    t = tt(length); n = noise(length); x = lp(n, bright) - lp(n, 300) * 0.6
    e = (t / length) ** 2.5 if rev else np.sin(np.pi * np.clip(t / length, 0, 1)) ** 2
    add(x * e * 0.16 * g, t0, 1, pan)
def riser(t0, t1, g=1.0):
    length = t1 - t0; t = tt(length); n = noise(length); k = (t / length)
    x = lp(n, 700) * (1 - k) + (n - lp(n, 1500)) * k * 0.8
    tone = np.sin(2 * np.pi * np.cumsum(220 + 660 * k ** 2) / SR) * 0.15
    add((x * 0.12 + tone) * k ** 2.2 * g, t0)
def pad(notes, t0, length, g=1.0, bright=1300):
    t = tt(length + 1.5); x = np.zeros(len(t))
    for m in notes:
        for det in (-0.08, 0.0, 0.09):
            ph = rng.uniform(0, 6.28)
            x += np.sin(2 * np.pi * hz(m) * (1 + det / 100) * t + ph) + 0.2 * np.sin(4 * np.pi * hz(m) * t + ph)
    x /= len(notes) * 3
    env = np.minimum(1, t / 0.6) * np.minimum(1, np.maximum(0, (length + 1.5 - t)) / 1.5)
    x = lp(x * env, bright)
    add(x * 0.5 * g, t0, 1, -0.3); add(np.roll(x, 300) * 0.5 * g, t0, 1, 0.3)
def piano(m, t0, g=1.0, length=4.0, pan=0.0):
    t = tt(length); f = hz(m)
    x = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (0.9 + k * 0.8)) for k, a in ((1, 1), (2, .4), (3, .15), (4, .07)))
    add(x * np.minimum(1, t / 0.01) * 0.13 * g, t0, 1, pan)

# D minor, with a lift to D major at the very end
PROG = [[38, 50, 53, 57, 64], [34, 46, 50, 53, 57], [41, 53, 57, 60, 64], [36, 48, 52, 55, 62]]  # Dm9 Bbmaj7 F C
ARP = [0, 2, 3, 4, 3, 2, 1, 2]

# ---------------- cold open ----------------
for h, low in zip(HITS, (34, 32, 30)):
    impact(h, 1.0, low)
    whoosh(h - 0.05, 0.8, 1.2, 0, 3200)
    for m in (26, 38, 45): piano(m, h, 0.9, 3)
whoosh(2.6, 1.15, 1.3, 0, 2400, rev=True)              # implosion into the deck
impact(3.72, 0.45, 40)
pad([38, 50, 53, 57, 62], 3.7, 2.1, 0.7, 900)
for k in range(int((MEET - 3.9) / (BEAT / 2))):         # ticking hats, accelerating feel
    hat(3.9 + k * BEAT / 2, 0.5 + 0.5 * k / 14, 0.4 * (-1) ** k)
riser(4.1, MEET, 0.9)
impact(MEET, 1.1, 36)
pad([38, 50, 57, 62, 65, 69], MEET, 1.9, 0.9, 1800)
riser(MEET + 0.15, SC0, 1.1)
for k in range(8): snap(SC0 - BEAT * 2 + k * BEAT / 4, 0.25 + 0.5 * k / 8)   # snare roll into the drop

# ---------------- groove: product scenes and feature ribbon ----------------
intensity = [(SC0, .72), (SC0 + 2 * SCL, .82), (SC0 + 4 * SCL, .92), (FT0, 1.0), (TR, 1.0)]
bar_i = 0; t = SC0
while t < TR - 0.01:
    lvl = level(intensity, t); chord = PROG[bar_i % 4]
    sub(chord[0] - 12 + 12, t, BAR, lvl)
    pad(chord[1:], t, BAR, 0.45 * lvl, 1000 + 900 * lvl)
    four = t >= FT0 or (t >= SC0 + 3 * SCL)
    for b in range(4):
        tb = t + b * BEAT
        if b in (0, 2) or four: kick(tb, lvl)
        if b in (1, 3): snap(tb, lvl * 0.9, 0.1)
        hat(tb + BEAT / 2, lvl, 0.35)
        if t >= SC0 + 2 * SCL: hat(tb + BEAT / 4, lvl * 0.45, -0.35); hat(tb + 3 * BEAT / 4, lvl * 0.45, -0.35)
    for k in range(8):
        n = chord[1 + ARP[k] % 4] + 12 + (12 if t >= FT0 and k % 2 else 0)
        pluck(n, t + k * BEAT / 2, lvl, 0.5 * np.sin(k), 6 if t < FT0 else 4.5)
    bar_i += 1; t += BAR

for k in range(5):                                     # every scene: punch on the downbeat, whip at the end
    s0 = SC0 + k * SCL
    impact(s0, 0.55 if k else 1.0, 40)
    whoosh(s0 + 0.5, 0.7, 0.9, 0.6, 2800)
    whoosh(s0 + SCL - 0.55, 0.6, 1.1, -0.6, 3600, rev=True)
for k in range(7): whoosh(FT0 - 0.1 + k * 0.08, 0.5, 0.35, (-1) ** k * 0.7, 4000)

# ---------------- trust: drums out, a heartbeat under each line ----------------
impact(TR, 0.6, 38)
pad([34, 46, 50, 53, 57, 62], TR, 2.0, 0.8, 1200)
pad([41, 53, 57, 60, 64], TR + 1.9, 1.8, 0.8, 1200)
pad([36, 48, 55, 60, 62, 64], TR + 3.6, 2.4, 0.8, 1300)
for h in (TR + 0.4, TR + 2.2, TR + 3.9):
    kick(h, 0.8); kick(h + 0.28, 0.45)
    piano(74 if h < TR + 1 else 72 if h < TR + 3 else 69, h, 0.8, 3, 0.2)

# ---------------- close ----------------
whoosh(TE - 0.2, 1.4, 1.2, 0, 2400)                    # pages gather
riser(TE + 0.5, LOGO - 0.45, 1.2)
whoosh(TE + 0.8, 2.0, 0.9, 0, 1600)                    # the page comes to camera
impact(LOGO, 1.3, 33)
pad([26, 38, 50, 54, 57, 62, 66, 69], LOGO, 6.5, 1.2, 2200)
for m, d in ((62, 0), (66, .06), (69, .12), (74, .2), (78, .3)): piano(m, LOGO + d, 1.0, 7)

# ---------------- room, silence before the logo, master ----------------
for dly, g in ((0.107, .16), (0.173, .11), (0.29, .07)):
    k = int(dly * SR); l2 = L.copy()
    L[k:] += R[:-k] * g; R[k:] += l2[:-k] * g
gap = np.ones(N); a, b = int((LOGO - 0.42) * SR), int((LOGO - 0.02) * SR)
gap[a:b] = np.linspace(1, 0, b - a) ** 0.5; gap[b:int(LOGO * SR)] = 0
L *= gap; R *= gap
out = np.stack([L, R], 1)
out *= np.minimum(1, np.minimum(T / 0.02, (DUR - T) / 2.0))[:, None]
out = np.tanh(out * 1.5) / 1.5
out /= np.max(np.abs(out)) / 0.89
path = os.path.join(os.path.dirname(__file__), 'score.wav')
with wave.open(path, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype('<i2').tobytes())
print('wrote', path)
