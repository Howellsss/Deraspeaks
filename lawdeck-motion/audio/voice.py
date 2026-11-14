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
 ("What if your study partner never slept?", 0.9),
 ("Never tired of your questions. There from your very first lecture, all the way to your final exam.", 0.92),
 ("Meet Lawdeck. Your AI law school companion.", 0.9),
 ("Built on five pillars.", 0.9),
 ("Research.", 0.88), ("Learn.", 0.88), ("Draft.", 0.88), ("Remember.", 0.88), ("Communicate.", 0.88),
 ("Research. Ask anything, in plain language, and get answers cited to the cases and statutes behind them.", 0.94),
 ("Learn. Work through your courses and MCQs, with explanations that make each principle click.", 0.94),
 ("Draft. Start from a catalogue of templates, and build your first draft on your own research.", 0.94),
 ("Remember. Memory challenges bring back what you studied, right before you would forget it. So exam preparation starts on day one, not the week before.", 0.94),
 ("Communicate. Bring your whole class together in Campus chat, with Lawdeck right there in the thread.", 0.94),
 ("And your Study Diary, your progress, briefs, projects and uploads. All in one place.", 0.94),
 ("Every answer is cited. Your work stays private. And you stay in control.", 0.92),
 ("From day one, to exam day.", 0.88),
 ("Lawdeck. Your law school companion.", 0.86),
]
os.makedirs(out, exist_ok=True)
for i, (text, sp) in enumerate(LINES, 1):
    s, sr = k.create(text.replace('Lawdeck', 'Law-deck'), voice=voice, speed=sp, lang='en-us')
    sf.write(os.path.join(out, f'{i:02d}.wav'), s, sr)
    print(f'{i:02d} {len(s)/sr:5.2f}s  {text}')
