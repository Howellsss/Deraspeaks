# Lawdeck brand film

A 93-second motion piece built with three.js. The camera moves through paper, the Lawdeck interface and type, from a single page to the Lawdeck mark.

| Time | Scene |
|---|---|
| 0–6s | One page rises into the light. *Every case begins with a question.* |
| 6–14s | Pages swirl (statutes, judgments, lecture notes, deadlines), then settle into one deck. |
| 14–24s | **01 Research.** Home screen: a question is typed into the composer, and the answer streams in with three cited authorities. |
| 24–34s | **02 Learn.** An MCQ answered correctly, the memory challenge, and My progress. |
| 34–43s | **03 Briefs.** Nash v Inman briefed as facts, issue, held and ratio, then *Save to Briefs* or *Quiz me*. |
| 43–53s | **04 Draft.** The Drafting catalogue, with a tenancy agreement drafted clause by clause. |
| 53–64s | **05 Campus chat** (dark theme). A class channel, where `@Lawdeck` summarises the lecture. |
| 64–73s | **Everything else.** Two moving rows of feature cards: Courses, MCQ, Briefs, Study Diary, Memory challenge, My progress, Projects, Documents, My uploads, Drafting catalogue, Campus chat, Search, Voice, Light and dark. |
| 73–80s | **Trust.** Cited, always. Your work, yours. You stay in control. |
| 80–93s | A page comes to camera and becomes the paper end card: mark, wordmark, tagline. |

The interface is drawn in code from the real app's layout and palette: sidebar, serif greeting, composer, chips and memory-challenge card. A placeholder student, "Tolu", is used instead of a real account.

## Preview

Serve this folder with any static server and open `index.html`. Space toggles play and pause; the scrubber seeks.

```bash
npx serve .
```

## Render to MP4

```bash
npm install
node render.mjs                      # out/lawdeck.mp4, 1920x1080 at 30fps (about 10 min)
node render.mjs --fps 60 --scale 2   # 3840x2160 at 60fps
node render.mjs --stills 3,20,68     # single frames for checking
```

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
