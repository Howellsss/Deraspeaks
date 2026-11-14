# Lawdeck brand film

A 75-second motion piece built with three.js. The camera moves through paper, interface and type, from a single page to the Lawdeck mark.

| Time | Scene |
|---|---|
| 0–6s | One page rises into the light. *Every case begins with a question.* |
| 6–14s | Pages swirl (statutes, judgments, lecture notes, deadlines), then settle into one deck. |
| 14–24s | **01 Research.** A question is typed, the answer streams in, and three cited authorities appear. |
| 24–34s | **02 Learn.** A lesson card, a quick check answered correctly, and module progress. |
| 34–44s | **03 Draft.** A tenancy agreement is drafted clause by clause, with a review rail and export. |
| 44–55s | **04 Campus Chat.** A class channel; `@Lawdeck` summarises the lecture inside the thread. |
| 55–62s | **Trust.** Cited, always. Your work, yours. You stay in control. |
| 62–75s | A page comes to camera and becomes the paper end card: mark, wordmark, tagline. |

## Preview

Serve this folder with any static server and open `index.html`. Space toggles play and pause; the scrubber seeks.

```bash
npx serve .
```

## Render to MP4

```bash
npm install
node render.mjs                      # out/lawdeck.mp4, 1920x1080 at 30fps
node render.mjs --fps 60 --scale 2   # 3840x2160 at 60fps
node render.mjs --stills 3,20,68     # single frames for checking
```

## Using real screen recordings

The four interface scenes are drawn in code. To replace any of them with a real Lawdeck recording, put the clip in `clips/` and pass it in. It plays inside the same floating window, from the start of that scene.

```bash
node render.mjs --query "research=clips/research.mp4&learn=clips/learn.mp4&draft=clips/draft.mp4&chat=clips/chat.mp4"
```

The same parameters work in the browser preview, for example `index.html?chat=clips/chat.mp4`. Record at 16:10 if you can (the window is 1600×1000), with about 10 seconds per scene.

## Before publishing, check

- The trust lines ("Your notes, drafts and chats stay private to you") must match Lawdeck's actual privacy practice.
- The legal example (minors and necessaries; Nash v Inman [1908] 2 KB 1; Sale of Goods Act 1979, s 3; Chapple v Cooper (1844) 13 M & W 252) is English common law. Swap it if your audience is in another jurisdiction.
- The logo assets in `assets/` were extracted from the supplied logo image. Replace them with the vector originals for a sharper 4K render.
