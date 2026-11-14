"""Generates the voice-over lines with Kokoro-82M (Apache-2.0).

    pip install kokoro-onnx soundfile
    # put model.onnx and af_heart.bin (plus any other voices) from
    # huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX in $KOKORO_DIR
    python audio/voice.py af_heart audio      -> audio/01.wav ... 16.wav
    bash audio/mix.sh                         -> out/lawdeck-final.mp4
"""
import sys, numpy as np, soundfile as sf, os
from kokoro_onnx import Kokoro
D = os.path.dirname(os.path.abspath(__file__)); M = os.environ.get('KOKORO_DIR', os.path.join(D, 'models'))
voices = {v: np.fromfile(os.path.join(M, v + '.bin'), dtype=np.float32).reshape(-1, 1, 256) for v in [f[:-4] for f in os.listdir(M) if f.endswith('.bin')]}
np.savez(os.path.join(M, 'voices.npz'), **voices)
k = Kokoro(os.path.join(M, 'model.onnx'), os.path.join(M, 'voices.npz'))
voice, out = sys.argv[1], sys.argv[2]
LINES = [
 ("Too many cases.", 1.22), ("Too many pages.", 1.22), ("Not enough time.", 1.22),
 ("What if all of it lived in one place?", 1.0), ("Meet Lawdeck.", 0.95),
 ("Ask anything, and get answers cited to the cases and statutes behind them.", 1.05),
 ("Learn with courses and MCQs. Keep it with memory challenges that bring topics back before you forget.", 1.08),
 ("Brief any case in moments: facts, issue, held, ratio.", 1.0),
 ("Draft from a catalogue of templates, built on your own research.", 1.0),
 ("And bring your whole class together in Campus chat, with Lawdeck in the thread.", 1.05),
 ("Study Diary. Progress. Projects. Uploads. Voice. Day or night.", 1.05),
 ("Every answer, cited.", 0.95), ("Your work, private.", 0.95), ("You, in control.", 0.95),
 ("Lawdeck.", 0.9), ("Research. Learn. Draft.", 0.9),
]
os.makedirs(out, exist_ok=True)
for i, (text, sp) in enumerate(LINES, 1):
    s, sr = k.create(text, voice=voice, speed=sp, lang='en-us')
    sf.write(os.path.join(out, f'{i:02d}.wav'), s, sr)
    print(f'{i:02d} {len(s)/sr:5.2f}s  {text}')
