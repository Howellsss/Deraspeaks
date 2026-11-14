# Lawdeck brand film

A 72-second motion piece built with three.js and cut to an original ~113 bpm score. Every 8.5-second product scene is exactly four bars, so each scene change lands on a downbeat.

| Time | Scene |
|---|---|
| 0–3s | **Hook.** "Too many cases. Too many pages. Not enough time." Each line slams in on an impact, with a burst of paper. |
| 3–7.5s | The pages implode into one deck: "What if all of it lived in one place?" Then a flash and a hit on **"Meet Lawdeck."** The beat drops. |
| 7.5–16s | **Ask.** Research: the home-screen composer, then a cited answer. The camera pushes into the sources. |
| 16–24.5s | **Learn.** MCQ answered correctly, memory challenge, My progress. The camera pushes into the correct answer. |
| 24.5–33s | **Brief.** Nash v Inman as facts, issue, held and ratio. |
| 33–41.5s | **Draft.** Drafting catalogue, with a tenancy agreement drafted clause by clause. |
| 41.5–50s | **Connect.** Campus chat (dark theme), with `@Lawdeck` in the thread. |
| 50–56s | **Everything else.** Two rows of 14 feature cards fly in. |
| 56–61.6s | **Trust**, one line at a time: Every answer, cited. Your work, private. You, in control. |
| 61.6–72s | The pages gather, a page comes to camera, a beat of silence, then the logo lands on the hit. |

Every scene has a one-word title punch, a whip transition with motion blur, flashes and camera shake on the impacts.

The interface is drawn in code from the real app's layout and palette: sidebar, serif greeting, composer, chips and memory-challenge card. A placeholder student, "Tolu", is used instead of a real account.

## Preview

Serve this folder with any static server and open `index.html`. Space toggles play and pause; the scrubber seeks.

```bash
npx serve .
```

## Render to MP4

```bash
npm install
node render.mjs                      # out/lawdeck.mp4, 1920x1080 at 30fps (about 30 min)
node render.mjs --fps 60 --scale 2   # 3840x2160 at 60fps
node render.mjs --stills 3,20,68     # single frames for checking
```

## Sound

- `audio/score.py` generates the original score and sound design (no samples): `python3 audio/score.py`, which writes `audio/score.wav`.
- `audio/voiceover.md` is the voice-over script, with a cue time for each line.
- `audio/mix.sh` places the recorded lines (`audio/01.wav` to `16.wav`) on their cues, ducks the music under the voice, and writes `out/lawdeck-final.mp4`.

## Using real screen recordings

The five interface scenes are drawn in code. To replace any of them with a real Lawdeck recording, put the clip in `clips/` and pass it in. It plays inside the same floating window, from the start of that scene.

```bash
node render.mjs --query "research=clips/research.mp4&learn=clips/learn.mp4&brief=clips/brief.mp4&draft=clips/draft.mp4&chat=clips/chat.mp4"
```

The same parameters work in the browser preview, for example `index.html?chat=clips/chat.mp4`. Record at 16:10 if you can (the window is 1600×1000), with about 10 seconds per scene.

## Before publishing, check

- The one-line feature descriptions in the feature ribbon (`FEATURES` in `index.html`) and the trust lines are written from the feature names. Confirm that each matches what the product does.

- In particular, the trust lines ("Your notes, drafts and chats stay private to you") must match Lawdeck's actual privacy practice.
- The legal example (minors and necessaries; Nash v Inman [1908] 2 KB 1; Sale of Goods Act 1979, s 3; Chapple v Cooper (1844) 13 M & W 252) is English common law. Swap it if your audience is in another jurisdiction.
- The logo assets in `assets/` were extracted from the supplied logo image. Replace them with the vector originals for a sharper 4K render.
