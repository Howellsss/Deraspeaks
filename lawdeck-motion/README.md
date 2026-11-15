# Lawdeck brand film

A 98-second motion piece built with three.js, introducing Lawdeck as an AI law school study companion built on five pillars: Research, Learn, Draft, Remember and Communicate. It has an American male voice-over and is cut to an original score.

| Time | Scene |
|---|---|
| 0–12s | **Hook, slow.** A single page in the light: "What if your study partner never slept?" Pages drift past for "from your very first lecture to your final exam". |
| 12–25s | The pages gather into one deck: "Meet Lawdeck. Your AI law school study companion." Then "Built on five pillars", with the five words landing one by one. |
| 25.5s | The beat drops (~113 bpm). Each pillar scene is a whole number of bars. |
| 25.5–34s | **Research.** The home-screen composer, then a cited answer. The camera pushes into the sources. |
| 34–42.5s | **Learn.** An MCQ answered correctly, with progress. |
| 42.5–51s | **Draft.** Drafting catalogue, with a tenancy agreement drafted clause by clause. |
| 51–64s | **Remember.** The "Before you move on…" memory challenge answered, beside the week's Study Diary: "exam preparation starts on day one". |
| 64–72s | **Communicate.** Campus chat (dark theme), with `@Lawdeck` in the thread. |
| 72–78.6s | Everything else, in one place: 14 feature cards. |
| 78.6–87s | Trust (Every answer, cited. Your work, private. You, in control.), then "From day one, to exam day." |
| 87–98s | A page comes to camera, then the logo, "Your AI law school study companion." and the five pillars. |

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
node render.mjs                      # out/lawdeck.mp4, 1920x1080 at 30fps (about 45 min)
node render.mjs --fps 60 --scale 2   # 3840x2160 at 60fps
node render.mjs --stills 3,20,68     # single frames for checking
```

## Sound

- `audio/score.py` generates the original score and sound design (no samples): `python3 audio/score.py`, which writes `audio/score.wav`.
- `audio/voiceover.md` is the voice-over script, with a cue time for each line.
- `audio/mix.sh` places the recorded lines (`audio/01.wav` to `18.wav`) on their cues, ducks the music under the voice, and writes `out/lawdeck-final.mp4`.

## Using real screen recordings

The five interface scenes are drawn in code. To replace any of them with a real Lawdeck recording, put the clip in `clips/` and pass it in. It plays inside the same floating window, from the start of that scene.

```bash
node render.mjs --query "research=clips/research.mp4&learn=clips/learn.mp4&remember=clips/remember.mp4&draft=clips/draft.mp4&chat=clips/chat.mp4"
```

The same parameters work in the browser preview, for example `index.html?chat=clips/chat.mp4`. Record at 16:10 if you can (the window is 1600×1000), with about 10 seconds per scene.

## Before publishing, check

- The one-line feature descriptions in the feature ribbon (`FEATURES` in `index.html`) and the trust lines are written from the feature names. Confirm that each matches what the product does.

- In particular, the trust lines ("Your notes, drafts and chats stay private to you") must match Lawdeck's actual privacy practice.
- The legal example (minors and necessaries; Nash v Inman [1908] 2 KB 1; Sale of Goods Act 1979, s 3; Chapple v Cooper (1844) 13 M & W 252) is English common law. Swap it if your audience is in another jurisdiction.
- The logo assets in `assets/` were extracted from the supplied logo image. Replace them with the vector originals for a sharper 4K render.
