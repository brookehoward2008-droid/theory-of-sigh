# Brooke Howard — Elevator Pitch Video (project folder)

Everything you need to assemble a polished **45–70 second**, editorial graphic-design
portfolio pitch in Premiere Pro or Canva, plus a ready-to-watch rough draft.

## Start here
1. Read **`edit_plan.md`** — the master plan (creative direction, structure, the two things to know).
2. Watch **`rough_draft.mp4`** — a ~1:00 animatic showing the look, framing, and pacing.
3. Build the final using **`timeline.csv`**, **`captions.srt`**, **`lower_thirds.txt`**, **`color_palette.md`**, **`assets_needed.md`**, and **`export_settings.md`**.

## Files
| File | What it is |
|------|-----------|
| `edit_plan.md` | Master edit plan + Premiere/Canva assembly steps |
| `timeline.csv` | Shot-by-shot timeline (open in Excel/Sheets) |
| `assets_needed.md` | B-roll, overlays, fonts, and music to gather (with search terms + free sources) |
| `captions.srt` | Full-script captions for the ~1:08 final cut |
| `lower_thirds.txt` | Name/title text + keyword chips + end-card copy |
| `color_palette.md` | Exact hex/RGB + where each color goes |
| `export_settings.md` | Premiere / Canva / Resolve settings for the Canvas upload |
| `rough_draft.mp4` | Rendered preview (1920×1080, 30fps, H.264/AAC) |
| `build_rough_draft.sh` | Regenerates the preview with ffmpeg |
| `source_video.mp4` | Your talking-head clip (local only — not committed) |

## The one decision that unlocks the full-length final
Your uploaded clip is **31 seconds** but the full script needs **~68 seconds** of narration.
To get a fully-voiced 45–70s pitch, **re-generate (or re-record) the talking-head with the
full script** — then it drops straight into this plan. See `edit_plan.md` §2 for the options.
The rough draft here uses the 31s clip for the open and carries the rest of the script as
editorial cards so you can see the whole thing today.

## Re-render the preview
```bash
./build_rough_draft.sh                 # uses ./source_video.mp4
./build_rough_draft.sh /path/to/clip.mp4
```
Requires ffmpeg.
