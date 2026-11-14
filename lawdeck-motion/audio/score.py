"""Original score and sound design for the Lawdeck film, generated from code (no samples).

    python3 audio/score.py                -> audio/score.wav (93 s, 48 kHz stereo)

Warm pad chords, a soft felt-piano motif, paper whooshes at page moments,
a near-silence before the logo, and one resolving chord on the reveal.
"""
import numpy as np, wave, os

SR = 48000
DUR = 93.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)
T = np.arange(N) / SR

def env(t0, a, d, length):
    n = int(length * SR); t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / d)
    return int(t0 * SR), e

def add(sig, start, gain=1.0, pan=0.0):
    s = max(0, start); e = min(N, start + len(sig))
    if e <= s: return
    seg = sig[s - start:e - start] * gain
    L[s:e] += seg * np.sqrt(0.5 * (1 - pan)); R[s:e] += seg * np.sqrt(0.5 * (1 + pan))

def hz(m): return 440 * 2 ** ((m - 69) / 12)

def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)): acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y

# --- automation: overall intensity across the film --------------------------
def curve(points):
    xs, ys = zip(*points); return np.interp(T, xs, ys)
pad_level = curve([(0, 0), (3, .55), (6, .6), (11, .9), (13.6, .75), (64, .8), (66, 1), (73, .85), (79, .6), (80.6, 0), (81.6, 0), (82, 1), (93, .0)])
pulse_level = curve([(0, 0), (12.5, 0), (14.5, .7), (60, .8), (64, 1), (72.5, .9), (74, .45), (79, .35), (80.4, 0), (93, 0)])

# --- pads: detuned saws, softly filtered -------------------------------------
CHORDS = [  # (start, [midi notes])  ~ D major colours
    (0, [38, 50, 57, 62, 64, 69]),      # Dadd9
    (6.5, [35, 47, 54, 57, 62, 66]),    # Bm7
    (13.6, [38, 50, 57, 61, 64, 69]),   # Dmaj9
    (24, [35, 47, 54, 57, 61, 66]),     # Bm9
    (34, [31, 43, 50, 54, 59, 62]),     # Gmaj7
    (43, [33, 45, 52, 57, 59, 64]),     # Asus2
    (53, [38, 50, 57, 61, 64, 69]),     # Dmaj9
    (64, [31, 43, 50, 55, 59, 66]),     # Gmaj9
    (73, [35, 47, 54, 59, 62, 66]),     # Bm(add11)
    (82, [26, 38, 50, 57, 62, 64, 69, 73]),  # D, the resolve
]
pad = np.zeros(N)
for i, (t0, notes) in enumerate(CHORDS):
    t1 = CHORDS[i + 1][0] if i + 1 < len(CHORDS) else DUR
    s0, s1 = int(max(0, t0 - 1.2) * SR), int(min(DUR, t1 + 1.6) * SR)
    t = np.arange(s1 - s0) / SR
    x = np.zeros(s1 - s0)
    for m in notes:
        f = hz(m)
        for det in (-0.07, 0.0, 0.08):
            ph = rng.uniform(0, 2 * np.pi)
            x += (np.sin(2 * np.pi * f * (1 + det / 100) * t + ph) + 0.18 * np.sin(4 * np.pi * f * t + ph) + 0.06 * np.sin(6 * np.pi * f * t)) / len(notes)
    fade = np.minimum(1, np.minimum(t / 1.4, (t[-1] - t) / 1.6))
    pad[s0:s1] += x * fade
pad = lowpass(pad, 1400) * pad_level * 0.22
L += pad * 0.95; R += np.roll(pad, 240) * 0.95

# --- felt piano: sine partials with soft attack ------------------------------
def piano(m, t0, vel=0.5, length=3.2, pan=0.0):
    n = int(length * SR); t = np.arange(n) / SR; f = hz(m)
    x = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (1.1 + k * 0.9)) for k, a in ((1, 1), (2, .38), (3, .14), (4, .06)))
    x *= np.minimum(1, t / 0.012)
    add(x * vel * 0.16, int(t0 * SR), 1, pan)

MOTIF = [74, 69, 66, 69, 76, 74, 69, 62]   # a quiet, open phrase
piano(74, 1.0, .45, 5); piano(69, 2.6, .35, 5)
beat = 60 / 76
for k, (t0, notes) in enumerate(CHORDS[2:9]):
    t1 = CHORDS[k + 3][0]
    tt = t0; j = 0
    while tt < t1 - 0.2 and tt < 80:
        lvl = float(np.interp(tt, T[::480], pulse_level[::480]))
        if lvl > 0.05:
            m = MOTIF[j % len(MOTIF)] + (0 if notes[3] % 12 in (1, 2, 6, 9) else -2 if j % 3 == 0 else 0)
            piano(m, tt, 0.42 * lvl, pan=0.25 * np.sin(j))
            if j % 4 == 0: piano(notes[1] + 12, tt, 0.3 * lvl, 4, pan=-0.2)
        tt += beat * (2 if j % 4 != 3 else 1); j += 1

# --- soft low pulse -----------------------------------------------------------
for k in range(int(DUR / beat)):
    tt = k * beat
    if k % 2: continue
    lvl = float(np.interp(tt, T[::480], pulse_level[::480]))
    if lvl < 0.05: continue
    n = int(0.5 * SR); t = np.arange(n) / SR
    chord = max([c for c in CHORDS if c[0] <= tt], key=lambda c: c[0])[1]
    x = np.sin(2 * np.pi * hz(chord[0] + 12) * t) * np.exp(-t * 7) * np.minimum(1, t / 0.01)
    add(x * 0.11 * lvl, int(tt * SR))

# --- paper whooshes: band-limited noise swells --------------------------------
def whoosh(t0, length=1.2, gain=0.12, pan=0.0, bright=2500):
    n = int(length * SR); t = np.arange(n) / SR
    x = lowpass(rng.standard_normal(n), bright) - lowpass(rng.standard_normal(n), 250) * 0.5
    e = np.sin(np.pi * np.clip(t / length, 0, 1)) ** 2
    add(x * e * gain, int(t0 * SR), 1, pan)

for t0, p in ((0.4, 0), (6.2, -.3), (7.0, .4), (7.9, -.5), (8.8, .3), (9.6, -.2), (10.6, .5), (11.4, -.4)):
    whoosh(t0, 1.4, 0.10, p)
for t0 in (13.4, 23.8, 33.8, 42.8, 52.8):      # each interface window arrives
    whoosh(t0, 1.1, 0.07, 0.5, 1800)
for k in range(7):                              # feature cards fly in
    whoosh(64.2 + k * 0.14, 0.9, 0.035, (-1) ** k * 0.6, 3200)
whoosh(78.8, 2.2, 0.12, 0, 2200)                # pages gather
whoosh(80.0, 1.8, 0.10, 0, 1500)                # page comes to camera

# --- logo hit: low bloom under the resolving chord ----------------------------
n = int(8 * SR); t = np.arange(n) / SR
boom = np.sin(2 * np.pi * 36.7 * t * (1 + 0.15 * np.exp(-t * 6))) * np.exp(-t * 0.9) * np.minimum(1, t / 0.02)
add(boom * 0.35, int(82.0 * SR))
for m, d in ((74, 0), (78, .05), (81, .1), (86, .16)):
    piano(m, 82.0 + d, .55, 9)

# --- gentle room: two short delays --------------------------------------------
for dly, g in ((0.113, .18), (0.191, .12)):
    k = int(dly * SR)
    L[k:] += R[:-k] * g; R[k:] += L[:-k] * g

# --- master ---------------------------------------------------------------------
out = np.stack([L, R], 1)
out *= np.minimum(1, np.minimum(T / 0.3, (DUR - T) / 2.5))[:, None]
out = np.tanh(out * 1.6) / 1.6
out /= np.max(np.abs(out)) / 0.7     # leave headroom for the voice
path = os.path.join(os.path.dirname(__file__), 'score.wav')
with wave.open(path, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype('<i2').tobytes())
print('wrote', path)
