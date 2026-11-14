// Renders index.html to an MP4, frame by frame, so every frame is exact.
//   node render.mjs                       -> out/lawdeck.mp4 (1920x1080, 30fps)
//   node render.mjs --fps 60 --scale 2    -> 4K60
//   node render.mjs --stills 3,18,50      -> out/still-3.jpg ... (quick checks)
//   node render.mjs --query "research=clips/research.mp4&chat=clips/chat.mp4"
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > -1 ? process.argv[i + 1] : d; };
const FPS = +arg('fps', 30), SCALE = +arg('scale', 1), STILLS = arg('stills', ''), QUERY = arg('query', '');
const FROM = +arg('from', 0), TO = arg('to', null);
fs.mkdirSync(path.join(ROOT, 'out'), { recursive: true });

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.png': 'image/png', '.jpg': 'image/jpeg', '.mp4': 'video/mp4', '.webm': 'video/webm', '.mov': 'video/quicktime', '.css': 'text/css' };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  const stat = fs.statSync(p), type = TYPES[path.extname(p)] || 'application/octet-stream';
  const range = req.headers.range;
  if (range) { // video seeking needs range requests
    const [s, e] = range.replace('bytes=', '').split('-'); const start = +s, end = e ? +e : stat.size - 1;
    res.writeHead(206, { 'Content-Type': type, 'Content-Range': `bytes ${start}-${end}/${stat.size}`, 'Accept-Ranges': 'bytes', 'Content-Length': end - start + 1 });
    return fs.createReadStream(p, { start, end }).pipe(res);
  }
  res.writeHead(200, { 'Content-Type': type, 'Content-Length': stat.size, 'Accept-Ranges': 'bytes' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const port = server.address().port;

const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: SCALE });
page.on('pageerror', e => console.error('page error:', e.message));
// Serve three.js from node_modules (the CDN is what the published page uses).
await page.route('https://cdn.jsdelivr.net/npm/three@*/**', r => {
  const rel = new URL(r.request().url()).pathname.replace(/^\/npm\/three@[^/]+\//, '');
  r.fulfill({ path: path.join(ROOT, 'node_modules/three', rel), contentType: 'text/javascript' });
});
await page.goto(`http://localhost:${port}/index.html?render=1${QUERY ? '&' + QUERY : ''}`);
await page.waitForFunction('window.__ready === true', null, { timeout: 60000 });
const DUR = await page.evaluate('window.__DUR');

const shot = () => page.locator('#stage').screenshot({ type: 'jpeg', quality: 94 });

if (STILLS) {
  for (const s of STILLS.split(',').map(Number)) {
    await page.evaluate(t => window.renderFrame(t), s);
    fs.writeFileSync(path.join(ROOT, `out/still-${s}.jpg`), await shot());
    console.log('still', s);
  }
} else {
  const end = TO ? +TO : DUR, frames = Math.round((end - FROM) * FPS);
  const out = path.join(ROOT, arg('out', 'out/lawdeck.mp4'));
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = 0; f < frames; f++) {
    await page.evaluate(t => window.renderFrame(t), FROM + f / FPS);
    const buf = await shot();
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % FPS === 0) process.stdout.write(`\r${(f / FPS).toFixed(0)}s / ${(frames / FPS).toFixed(0)}s  (${((Date.now() - t0) / 1000).toFixed(0)}s elapsed)`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  console.log('\nwrote', out);
}
await browser.close(); server.close();
