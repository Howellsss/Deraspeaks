# Lawdeck film: voice-over script (72-second cut)

Delivery: confident and warm, with energy. Think of a premium tech launch rather than a lecture. The first three lines are short and hit with the music. After "Meet Lawdeck" the pace is brisk, and the trust lines are slow and deliberate. The last two lines are calm.

| # | Cue | Scene | Line |
|---|---|---|---|
| 01 | 0:00.35 | Impact, pages burst | Too many cases. |
| 02 | 0:01.15 | Impact | Too many pages. |
| 03 | 0:01.95 | Impact | Not enough time. |
| 04 | 0:03.75 | Pages become one deck | What if all of it lived in one place? |
| 05 | 0:05.65 | Impact, title | Meet Lawdeck. |
| 06 | 0:08.3 | Ask. / Research | Ask anything, and get answers cited to the cases and statutes behind them. |
| 07 | 0:16.8 | Learn. / MCQ | Learn with courses and MCQs. Keep it with memory challenges that bring topics back before you forget. |
| 08 | 0:25.3 | Brief. / Briefs | Brief any case in moments: facts, issue, held, ratio. |
| 09 | 0:33.8 | Draft. / Drafting catalogue | Draft from a catalogue of templates, built on your own research. |
| 10 | 0:42.3 | Connect. / Campus chat | And bring your whole class together in Campus chat, with Lawdeck in the thread. |
| 11 | 0:50.3 | Feature ribbon | Study Diary. Progress. Projects. Uploads. Voice. Day or night. |
| 12 | 0:56.4 | Trust | Every answer, cited. |
| 13 | 0:58.2 | Trust | Your work, private. |
| 14 | 0:59.9 | Trust | You, in control. |
| 15 | 1:04.8 | Logo hit | Lawdeck. |
| 16 | 1:06.3 | Tagline | Research. Learn. Draft. |

About 120 words.

## Recording and mixing

Record each line as its own WAV file (48 kHz, quiet room, a little silence either side), named `01.wav` to `16.wav` in this folder. Then run:

```bash
bash audio/mix.sh
```

The script trims leading silence, places each line on its cue, ducks the music under the voice, and writes `out/lawdeck-final.mp4`.
