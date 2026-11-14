"""Original score and sound design for the Lawdeck film, generated from code (no samples).

    python3 audio/score.py                -> audio/score.wav (98 s, 48 kHz stereo)

  0    - 25.5  slow open: pads and a quiet piano under "What if your study partner never slept?",
               a warm swell on "Meet Lawdeck", a rising note on each of the five pillars, a riser
  25.5 - 72.25 the beat drops (~113 bpm): one scene per pillar, each change on a downbeat
  72.25- 78.6  everything else: four on the floor, brightest point
  78.6 - 87    trust and "From day one, to exam day": drums out, heartbeat, warm chords
  87   - 98    riser, a beat of silence, the logo hit and a D major resolve
"""
import numpy as np, wave, os

SR = 48000
DUR = 98.0
N = int(SR * DUR)
T = np.arange(N) / SR
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)

BAR = 2.125; BEAT = BAR / 4
MEET = 12.4; FIVE = 16.6; PILL = [18.9, 20.0, 21.1, 22.2, 23.3]
SC0 = 25.5; LENS = [b * BAR for b in (4, 4, 4, 6, 4)]
STARTS = [SC0 + sum(LENS[:i]) for i in range(5)]
FT0 = STARTS[4] + LENS[4]; TR = FT0 + 3 * BAR; DAY = TR + 6.0; TE = DAY + 2.4; LOGO = TE + 3.0

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

# ---------------- slow open ----------------
OPEN = [(0.0, [38, 50, 57, 62, 64]), (4.4, [34, 46, 53, 57, 62]), (8.4, [41, 53, 57, 60, 64]), (12.4, [38, 50, 57, 62, 66, 69]), (16.6, [34, 46, 50, 57, 62]), (20.6, [36, 48, 55, 60, 64])]
for i, (t0, notes) in enumerate(OPEN):
    t1 = OPEN[i + 1][0] if i + 1 < len(OPEN) else SC0
    pad(notes, max(0, t0 - 0.6), t1 - t0 + 0.6, 0.55 if t0 < 12 else 0.7, 900 if t0 < 12 else 1500)
for t0, m in ((1.2, 69), (2.4, 64), (4.6, 69), (5.8, 65), (7.9, 72), (9.2, 69), (10.4, 67)):
    piano(m, t0, 0.55, 4, 0.2)
whoosh(4.3, 2.6, 0.7, -0.3, 1800)                      # pages leave the first page
whoosh(10.2, 2.2, 0.8, 0.3, 2000, rev=True)            # and gather into one deck
impact(MEET, 0.7, 38)
for m, d in ((62, 0), (66, .05), (69, .1), (74, .16)): piano(m, MEET + d, 0.8, 5)
for k in range(int((SC0 - FIVE) / (BEAT / 2))):        # quiet ticking from "five pillars"
    hat(FIVE + k * BEAT / 2, 0.25 + 0.5 * k / 32, 0.4 * (-1) ** k)
for k, (t0, m) in enumerate(zip(PILL, (62, 65, 69, 72, 74))):   # a rising note on each pillar
    pluck(m + 12, t0, 1.6, 0.4 * (k - 2) / 2, 3.5); piano(m, t0, 0.7, 3); kick(t0, 0.35)
riser(SC0 - 2.0, SC0, 1.0)
for k in range(8): snap(SC0 - BEAT * 2 + k * BEAT / 4, 0.2 + 0.45 * k / 8)

# ---------------- groove: five pillars and everything else ----------------
intensity = [(SC0, .72), (STARTS[2], .82), (STARTS[4], .92), (FT0, 1.0), (TR, 1.0)]
bar_i = 0; t = SC0
while t < TR - 0.01:
    lvl = level(intensity, t); chord = PROG[bar_i % 4]
    sub(chord[0], t, BAR, lvl)
    pad(chord[1:], t, BAR, 0.45 * lvl, 1000 + 900 * lvl)
    four = t >= STARTS[3]
    for b in range(4):
        tb = t + b * BEAT
        if b in (0, 2) or four: kick(tb, lvl)
        if b in (1, 3): snap(tb, lvl * 0.9, 0.1)
        hat(tb + BEAT / 2, lvl, 0.35)
        if t >= STARTS[2]: hat(tb + BEAT / 4, lvl * 0.45, -0.35); hat(tb + 3 * BEAT / 4, lvl * 0.45, -0.35)
    for k in range(8):
        n = chord[1 + ARP[k] % 4] + 12 + (12 if t >= FT0 and k % 2 else 0)
        pluck(n, t + k * BEAT / 2, lvl, 0.5 * np.sin(k), 6 if t < FT0 else 4.5)
    bar_i += 1; t += BAR

for k, s0 in enumerate(STARTS):
    impact(s0, 1.0 if k == 0 else 0.55, 40)
    whoosh(s0 + 0.5, 0.7, 0.9, 0.6, 2800)
    whoosh(s0 + LENS[k] - 0.55, 0.6, 1.1, -0.6, 3600, rev=True)
for k in range(7): whoosh(FT0 - 0.1 + k * 0.08, 0.5, 0.35, (-1) ** k * 0.7, 4000)

# ---------------- trust, then "From day one, to exam day" ----------------
impact(TR, 0.6, 38)
pad([34, 46, 50, 53, 57, 62], TR, 2.0, 0.8, 1200)
pad([41, 53, 57, 60, 64], TR + 1.9, 1.8, 0.8, 1200)
pad([36, 48, 55, 60, 62, 64], TR + 3.5, 2.6, 0.8, 1300)
for h, m in ((TR + 0.3, 74), (TR + 2.0, 72), (TR + 3.6, 69)):
    kick(h, 0.8); kick(h + 0.28, 0.45); piano(m, h, 0.8, 3, 0.2)
pad([31, 43, 50, 55, 59, 62, 66], DAY, 2.6, 1.0, 1800)       # a warm G major lift
for m, d in ((67, 0), (71, .08), (74, .16)): piano(m, DAY + d, 0.8, 4)

# ---------------- close ----------------
whoosh(TE - 0.2, 1.4, 1.2, 0, 2400)                    # pages gather
riser(TE + 0.5, LOGO - 0.45, 1.2)
whoosh(TE + 0.8, 2.0, 0.9, 0, 1600)                    # the page comes to camera
impact(LOGO, 1.3, 33)
pad([26, 38, 50, 54, 57, 62, 66, 69], LOGO, 7.0, 1.2, 2200)
for m, d in ((62, 0), (66, .06), (69, .12), (74, .2), (78, .3)): piano(m, LOGO + d, 1.0, 7)

# ---------------- room, silence before the logo, master ----------------
for dly, g in ((0.107, .16), (0.173, .11), (0.29, .07)):
    k = int(dly * SR); l2 = L.copy()
    L[k:] += R[:-k] * g; R[k:] += l2[:-k] * g
gap = np.ones(N); a, b = int((LOGO - 0.42) * SR), int((LOGO - 0.02) * SR)
gap[a:b] = np.linspace(1, 0, b - a) ** 0.5; gap[b:int(LOGO * SR)] = 0
L *= gap; R *= gap
out = np.stack([L, R], 1)
out *= np.minimum(1, np.minimum(T / 0.6, (DUR - T) / 2.5))[:, None]
out = np.tanh(out * 1.5) / 1.5
out /= np.max(np.abs(out)) / 0.89
path = os.path.join(os.path.dirname(__file__), 'score.wav')
with wave.open(path, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype('<i2').tobytes())
print('wrote', path)
