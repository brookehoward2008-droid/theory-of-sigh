# Export Settings — Canvas (LMS) Upload

Target spec from the assignment:
**MP4 · H.264 · 1920×1080 · 24 or 30 fps · AAC audio · under 500 MB.**

The settings below land well under 500 MB (a 60–70s 1080p clip is typically 30–120 MB)
while staying crisp. Use **30 fps** unless your source is 24 — mixing is fine, just pick one
project frame rate and stick to it. (The supplied source clip is 25 fps; the project and
export should be normalized to 30 fps.)

---

## Adobe Premiere Pro / Media Encoder

**Sequence settings**
- Editing Mode: Custom
- Frame size: 1920 × 1080 (16:9)
- Frame rate: 30 fps (or 24)
- Pixel Aspect Ratio: Square Pixels (1.0)
- Fields: No Fields (Progressive)
- Audio: 48000 Hz

**Export (File ▸ Export ▸ Media, or send to Media Encoder)**
- Format: **H.264**
- Preset: start from "Match Source – High bitrate", then adjust below
- Video:
  - Width/Height: 1920 × 1080
  - Frame Rate: 30
  - Field Order: Progressive
  - Aspect: Square Pixels (1.0)
  - Profile: High · Level: 4.2
  - Render at Maximum Depth: on (optional)
  - Bitrate Encoding: **VBR, 2 pass**
  - Target Bitrate: **10 Mbps** · Maximum Bitrate: **14 Mbps**
    (≈ 75–110 MB for ~70s — well under 500 MB. Bump target to 16/20 only if you want it sharper.)
- Audio:
  - Format: AAC · Codec: AAC
  - Sample Rate: 48000 Hz
  - Channels: Stereo
  - Bitrate: 256 kbps (192 is fine too)
- Multiplexer: MP4
- Use Maximum Render Quality: on
- Check **Estimated File Size** at the bottom — confirm it reads well under 500 MB before exporting.

---

## Canva (if you assemble there instead)

1. Design size: **1920 × 1080 px** (Custom size, or "Video" 16:9).
2. Share ▸ Download.
3. File type: **MP4 Video**.
4. Quality: **1080p** (Canva Pro lets you pick; 1080p is the target).
5. Leave compression default — Canva exports H.264/AAC MP4 automatically.
6. Frame rate: Canva exports at 30 fps by default. Good.
7. Download and confirm the file is < 500 MB (it will be).

---

## DaVinci Resolve (free alternative)

- Deliver page ▸ Custom.
- Format: MP4 · Codec: H.264 · Resolution: 1920×1080 · Frame rate: 30.
- Quality: Restrict to **10,000 Kb/s** (VBR) or "Automatic – Best".
- Audio: AAC · 256 kbps · 48 kHz · Stereo.

---

## Sanity checklist before uploading to Canvas

- [ ] Resolution reads 1920×1080 (File ▸ Properties / Get Info).
- [ ] Duration is between 0:45 and 1:10.
- [ ] Codec is H.264 / audio is AAC (QuickTime/VLC ▸ Tools ▸ Codec Info).
- [ ] Audio is audible and in sync (watch the last 5 seconds — exports sometimes clip the tail).
- [ ] File size < 500 MB.
- [ ] Filename has no spaces or odd characters, e.g. `Brooke_Howard_Elevator_Pitch.mp4`.

---

## Quick verify with ffmpeg/ffprobe (optional)

```bash
# Confirm container/codecs/resolution/fps/duration:
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1 Brooke_Howard_Elevator_Pitch.mp4

# Re-wrap/compress to guarantee the spec if an export ever comes out wrong:
ffmpeg -i input.mov -c:v libx264 -profile:v high -pix_fmt yuv420p -r 30 -vf scale=1920:1080 \
  -b:v 10M -maxrate 14M -bufsize 20M -c:a aac -b:a 256k -ar 48000 -ac 2 \
  -movflags +faststart Brooke_Howard_Elevator_Pitch.mp4
```
`-movflags +faststart` makes it stream/preview faster after upload — recommended.
