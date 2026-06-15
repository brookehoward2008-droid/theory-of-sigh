# Edit Plan — Brooke Howard Elevator Pitch Video

A Premiere-/Canva-ready plan to turn the uploaded talking-head clip + the full script
into a polished **45–70 second**, editorial, graphic-design-student portfolio piece.

- **Aesthetic:** professional, warm, artistic, sincere. Editorial layout (think a design
  magazine), not corporate stock. Lots of ivory negative space, quiet motion, one accent at a time.
- **Final spec:** 1920×1080, 30 fps, H.264 + AAC, under 500 MB (see `export_settings.md`).

---

## 1. Source assets (what you actually uploaded)

| File | Specs | Verdict |
|------|-------|---------|
| `ElevenLabs_video_Creatify Aurora_well lit art space_business pr.mp4` | **832×1088 (portrait), 31.36s, 25 fps, AAC mono, ~1.8 Mbps. No visible watermark.** Clean studio talking-head, warm neutral-gray background. | **PRIMARY base/talking-head.** Looks great. |
| (duplicate of the above) | byte-identical second copy | ignore |
| `…81dbbd0c…mp4` | 960×960 square, 31.16s, blurry casual selfie, different outfit/room | **Not used** (off-aesthetic, low quality). Could be the original source you fed into Creatify. |

> Watermark check: I sampled frames across the clip including all four corners and the
> bottom strip — **no Creatify/ElevenLabs watermark is baked in.** Nothing to cover or crop.
> The editorial frame below still gives you a clean bottom band if a future export adds one.

---

## 2. Two realities to handle (read this first)

**A) Duration.** Your full script is **164 words ≈ 68 seconds** of natural narration. The
uploaded clip is **only 31 seconds**, so it can hold only about the first third of the script.
To deliver the full-script 45–70s pitch, you need narration for the whole script. Pick one:

- **(Recommended) Re-generate the talking-head with the FULL script** in the same tool you
  used (Creatify / ElevenLabs avatar "Aurora"). Paste the exact script from this folder,
  export, and you'll get a ~60–68s clip in one consistent voice. Drop it in and everything
  here lines up. *This is the cleanest path and ~2 minutes of work.*
- **Record the full script yourself** (phone or webcam, quiet room) and use that as the talking head.
- **Hybrid "text-forward" cut:** keep the real 31s voice for the open, then carry the rest of
  the script as elegant on-screen typography + captions over B-roll with a soft music bed.
  (This is exactly what the included `rough_draft.mp4` previews — see §8.)

**B) Orientation.** The clip is **portrait** inside a **landscape** deliverable. We do **not**
crop her face. Instead we use an **editorial pillarbox**: the portrait sits as a framed panel
on an ivory canvas, with a typographic column beside it. This *is* the look — it reads as an
intentional design-magazine layout, not a mistake. (See §4.)

---

## 3. Sequence / structure (final, full-script version → ~1:08)

Timecodes are fitted to a natural ~150 wpm delivery so the whole script fits in 1:08. They
match `captions.srt` and `timeline.csv`. **Lock final timing to your re-recorded narration's
waveform in Premiere** (enable the audio waveform, then nudge clips to match). Order follows
your brief exactly.

| # | Time | Section | Visual | On-screen | Script (narration) |
|---|------|---------|--------|-----------|--------------------|
| 1 | 0:00–0:08 | Intro | Talking head in editorial frame | Lower third (name/title/college) | "Hello, my name is Brooke Howard… at Everett Community College." |
| 2 | 0:08–0:15 | Life experience | Warm study B-roll: sketchbook, hands, laptop, workspace | Kicker "LIFE EXPERIENCE" → chip *Life Experience* | "As a returning student, I bring both life experience and a fresh perspective…" |
| 3 | 0:15–0:25 | Design + technology | Web mockups, Adobe UI, type specimens, portfolio spreads | Chip *Design + Technology* | "My goal is to build a career where I can use design, technology, and creativity…" |
| 4 | 0:25–0:37 | Career experience | Customer-service / production-design / teamwork / print workflow | Kicker "CAREER EXPERIENCE" → chip *Communication* | "Throughout my career, I have worked in customer service, production design, and team-focused roles…" |
| 5 | 0:37–0:45 | Problem solving & pressure | Wireframes, revisions, layout grids, focused editing | Chip *Creative Problem Solving* | "Those experiences have helped me become a creative problem solver… under pressure." |
| 6a | 0:45–0:56 | Work ethic | Return to talking head | Chips *Work Ethic*, then *Willingness to Learn* | "What I would bring… a strong work ethic, a willingness to learn…" |
| 6b | 0:56–1:06 | Closing offer | Portfolio montage | (let the work breathe — minimal text) | "I would love the opportunity to learn more… entering the design field." |
| 6c | 1:06–1:08 | End card | Charcoal end card | "Thank you for your time." + name | "Thank you for your time." |

---

## 4. The editorial frame (portrait → landscape)

```
1920 × 1080 ivory canvas (#F5F1EA)
┌─────────────────────────────────────────────────────────┐
│                                                           │
│   ┌───────────────┐        BROOKE HOWARD                  │
│   │               │        Graphic & Web Design Student   │
│   │  portrait     │        ──────── (gold rule) ────────  │
│   │  talking      │        Everett Community College      │
│   │  head         │                                       │
│   │  (≈764×1000)  │        [ Life Experience ]  ← chip    │
│   │               │                                       │
│   └───────────────┘                                       │
│      framed panel             type / keyword column       │
└─────────────────────────────────────────────────────────┘
```

- Scale the portrait to ~1000px tall (keep aspect → ~764px wide). Center it vertically with ~40px margins.
- Place it left-of-center (x ≈ 170). Add a 2–3px charcoal hairline frame, optional soft drop shadow.
- Right column (x ≈ 1000) holds the lower third and the single keyword chip.
- For B-roll sections you can go full-bleed (B-roll fills the frame) with the kicker label top-left and a bottom caption — you don't need the portrait panel on B-roll shots.
- Keep ivory negative space generous. Quiet is the point.

---

## 5. Overlay & caption rules

- **Minimal text.** Never the whole script on screen. Big text = keywords only.
- Approved keywords (one at a time): *Life Experience · Design + Technology · Creative Problem Solving · Communication · Work Ethic · Willingness to Learn*.
- **Keyword chip** = Deep Charcoal box @ 72% + Warm Ivory text + optional 2px gold underline.
- **Captions** = same charcoal box @ 72%, ivory text, bottom-center, 1–2 short lines. Subtle, readable over any footage. Use `captions.srt`.
- Never show a kicker label and a keyword chip at the same time.
- Motion: fade + small rise (10–14px), 0.3–0.4s ease. No spins, no zooms, no corporate swooshes.

---

## 6. Music & audio

- Add a soft instrumental bed (warm piano / felt keys / light ambient) at **−24 to −20 LUFS**,
  ducking under narration to about −30 dB. Suggested searches in §`assets_needed.md`.
- Keep her voice the priority; music is atmosphere only. Fade music in over 1s, out over 1.5s.
- One gentle whoosh/paper transition is fine between sections — don't overdo SFX.

---

## 7. Watermark / cleanup

- No watermark exists on the primary clip → nothing to hide.
- If you re-generate and the new export *does* carry a corner mark: the editorial frame
  already covers/▸crops the panel edges; you can also scale the panel 102–105% or sit a thin
  ivory band over the bottom 40px. Don't crop her face to chase a mark — cover it with design.

---

## 8. What's in `rough_draft.mp4` (the included preview)

A real, watchable **~1:02** draft at 1920×1080 / 30 fps / H.264 / AAC that demonstrates the
whole system using **only today's 31s asset**:

- **0:00–0:31** — your real talking-head + audio, in the editorial ivory frame, with the
  lower third and two keyword chips. (No burned captions here yet because the exact word
  timing of the recorded audio isn't known to the tool — apply `captions.srt` and nudge to
  the waveform in Premiere.)
- **0:31–0:57** — text-forward section cards (Career / Problem Solving / Work Ethic) carrying
  the rest of the script as editorial type + keyword overlays, on palette backgrounds. Silent
  here = placeholder for your full narration or a music bed.
- **0:57–1:02** — charcoal "Thank you for your time." end card.

Treat it as an animatic / layout proof. The finished piece comes from §2-A + assembling per §3.

---

## 9. Assemble fast in Premiere Pro

1. New Project → New Sequence: 1920×1080, 30 fps (see `export_settings.md`).
2. Import the full-script talking-head (re-generated per §2-A), B-roll (`assets_needed.md`), and a music track.
3. Lay the talking head on V1; for portrait shots, scale to ~92% height and position per §4. Add the ivory background on V1-below (Color Matte `#F5F1EA`) and a frame (rectangle, 2px charcoal stroke).
4. Drop B-roll on V2 for sections 2–5; add a Color Matte or adjustment layer for cards.
5. File ▸ Import `captions.srt` (or Window ▸ Text ▸ Captions ▸ Import). Style: ivory text, charcoal box 72%, bottom-center. Nudge cues to the waveform.
6. Add lower third (§`lower_thirds.txt`) and keyword chips per §3; animate with fade+rise.
7. Add music, set levels (§6).
8. Color: a light warm LUT or a gentle curve lift; keep skin natural.
9. Export H.264 per `export_settings.md`.

## 9b. Assemble fast in Canva (alternative)

1. Create a 1920×1080 video design.
2. Upload the talking head + B-roll. Set an ivory page background; place the portrait as a framed element (add a thin line border).
3. Use Text for the lower third and keyword chips (charcoal rounded rectangle + ivory text).
4. Add the section cards as their own pages/scenes; use the palette from `color_palette.md`.
5. Add captions with Canva's text or the Captions app, styled ivory-on-charcoal.
6. Add a music track from Canva audio; lower its volume.
7. Share ▸ Download ▸ MP4 (1080p) — see `export_settings.md`.

---

## 10. Deliverables in this folder

- `edit_plan.md` (this file) · `timeline.csv` · `assets_needed.md` · `captions.srt`
- `lower_thirds.txt` · `color_palette.md` · `export_settings.md`
- `rough_draft.mp4` (preview) · `build_rough_draft.sh` (regenerates the preview with ffmpeg)
- `README.md` (index / quick start)
