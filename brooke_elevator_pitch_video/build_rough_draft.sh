#!/usr/bin/env bash
# Build a rough-draft / animatic MP4 for Brooke Howard's elevator pitch.
# - 1920x1080, 30fps, H.264 (yuv420p) + AAC  -> meets the Canvas upload spec.
# - Uses the uploaded portrait talking-head in an editorial ivory frame for the open,
#   then editorial section cards carrying the rest of the script, then a thank-you end card.
#
# Usage:  ./build_rough_draft.sh [path/to/source_talking_head.mp4]
# Default source: ./source_video.mp4  (drop your clip there, or pass a path).
#
# Requires: ffmpeg (with libx264, libfreetype/drawtext).
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="${1:-$DIR/source_video.mp4}"
OUT="$DIR/rough_draft.mp4"
T="$DIR/.build_tmp"
mkdir -p "$T"

if [[ ! -f "$SRC" ]]; then
  echo "ERROR: source video not found at: $SRC"
  echo "Put your talking-head clip at $DIR/source_video.mp4 or pass it as an argument."
  exit 1
fi

# ---- Palette (0xRRGGBB) ----
IVORY=0xF5F1EA; CHARC=0x2C2C2C; TEAL=0x5D8A87; GOLD=0xC9A96E; ROSE=0xB98B82
INK=0x4A4A4A; CREAM=0xE9E3D6   # secondary text on dark

# ---- Fonts (fall back to DejaVu if the editorial serif isn't present) ----
SERIF_B=/mnt/skills/examples/canvas-design/canvas-fonts/CrimsonPro-Bold.ttf
SERIF_R=/mnt/skills/examples/canvas-design/canvas-fonts/CrimsonPro-Regular.ttf
SANS_R=/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf
SANS_B=/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf
[[ -f "$SERIF_B" ]] || SERIF_B=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
[[ -f "$SERIF_R" ]] || SERIF_R=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
[[ -f "$SANS_R"  ]] || SANS_R=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
[[ -f "$SANS_B"  ]] || SANS_B=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf

# ---- Text snippets (use textfiles to avoid shell/ffmpeg escaping) ----
printf '%s' "Brooke Howard"                                              > "$T/name.txt"
printf '%s' "Graphic & Web Design Student"                              > "$T/title.txt"
printf '%s' "Everett Community College"                                  > "$T/college.txt"
printf '%s' "Life Experience"                                           > "$T/kw_life.txt"
printf '%s' "Design + Technology"                                        > "$T/kw_design.txt"
printf '%s' "C A R E E R   E X P E R I E N C E"                          > "$T/lbl_career.txt"
printf '%s' "Communication"                                             > "$T/kw_comm.txt"
printf '%s' "Customer service  ·  Production design  ·  Team-focused roles" > "$T/sub_career.txt"
printf '%s' "P R O B L E M   S O L V I N G"                              > "$T/lbl_problem.txt"
printf '%s' "Creative Problem Solving"                                   > "$T/kw_solve.txt"
printf '%s' "Adaptable.  Collaborative.  Focused under pressure."        > "$T/sub_solve.txt"
printf '%s' "W H A T   I   B R I N G"                                    > "$T/lbl_bring.txt"
printf '%s' "Work Ethic"                                                > "$T/kw_ethic.txt"
printf '%s' "A strong work ethic, and a willingness to learn."          > "$T/sub_ethic.txt"
printf '%s' "Thank you for your time."                                   > "$T/thanks.txt"
printf '%s' "Brooke Howard  ·  Graphic & Web Design  ·  Everett Community College" > "$T/sub_end.txt"

VENC=(-c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -r 30)
AENC=(-c:a aac -b:a 192k -ar 44100 -ac 1)

echo "==> SEG 1: editorial talking head (real audio)"
D1=31.36
ffmpeg -y -v error -i "$SRC" -f lavfi -i "color=c=$IVORY:s=1920x1080:r=30" -filter_complex "
  [0:v]scale=-2:1000,setsar=1,fps=30[tv];
  [1:v]drawbox=x=158:y=38:w=768:h=1004:color=$CHARC:t=4[bg];
  [bg][tv]overlay=x=160:y=40[c];
  [c]drawtext=fontfile=$SERIF_B:textfile=$T/name.txt:fontcolor=$CHARC:fontsize=78:x=1000:y=360,
     drawtext=fontfile=$SANS_R:textfile=$T/title.txt:fontcolor=$INK:fontsize=37:x=1002:y=458,
     drawbox=x=1004:y=520:w=360:h=3:color=$GOLD:t=fill,
     drawtext=fontfile=$SANS_R:textfile=$T/college.txt:fontcolor=$INK:fontsize=33:x=1004:y=548,
     drawbox=enable='between(t,12,18.5)':x=1002:y=648:w=470:h=88:color=$CHARC@0.72:t=fill,
     drawtext=enable='between(t,12,18.5)':fontfile=$SANS_B:textfile=$T/kw_life.txt:fontcolor=$IVORY:fontsize=46:x=1030:y=672,
     drawbox=enable='between(t,22,30.5)':x=1002:y=648:w=560:h=88:color=$CHARC@0.72:t=fill,
     drawtext=enable='between(t,22,30.5)':fontfile=$SANS_B:textfile=$T/kw_design.txt:fontcolor=$IVORY:fontsize=46:x=1030:y=672,
     setsar=1[outv]
" -map "[outv]" -map 0:a -t $D1 "${VENC[@]}" "${AENC[@]}" "$T/seg1.mp4"

# ---- Card helper: $1 dur $2 bg $3 lblfile $4 lblcolor $5 kwfile $6 kwcolor $7 subfile $8 subcolor $9 kwfont $10 out
make_card () {
  local DUR="$1" BG="$2" LBL="$3" LBLC="$4" KW="$5" KWC="$6" SUB="$7" SUBC="$8" KWFONT="$9" OUTF="${10}"
  ffmpeg -y -v error -f lavfi -i "color=c=$BG:s=1920x1080:r=30" \
    -f lavfi -i "anullsrc=r=44100:cl=mono" -filter_complex "
    [0:v]drawtext=fontfile=$SANS_R:textfile=$LBL:fontcolor=$LBLC:fontsize=34:x=(w-text_w)/2:y=372,
         drawtext=fontfile=$KWFONT:textfile=$KW:fontcolor=$KWC:fontsize=104:x=(w-text_w)/2:y=448,
         drawbox=x=(iw-220)/2:y=602:w=220:h=3:color=$GOLD:t=fill,
         drawtext=fontfile=$SANS_R:textfile=$SUB:fontcolor=$SUBC:fontsize=38:x=(w-text_w)/2:y=648,
         setsar=1[outv]
  " -map "[outv]" -map 1:a -t "$DUR" "${VENC[@]}" "${AENC[@]}" "$OUTF"
}

echo "==> SEG 2: Career card"
make_card 8  "$IVORY" "$T/lbl_career.txt"  "$TEAL"  "$T/kw_comm.txt"  "$CHARC" "$T/sub_career.txt" "$INK"   "$SERIF_B" "$T/seg2.mp4"
echo "==> SEG 3: Problem-solving card"
make_card 7  "$CHARC" "$T/lbl_problem.txt" "$GOLD"  "$T/kw_solve.txt" "$IVORY" "$T/sub_solve.txt"  "$CREAM" "$SERIF_B" "$T/seg3.mp4"
echo "==> SEG 4: Work-ethic card"
make_card 8  "$TEAL"  "$T/lbl_bring.txt"   "$IVORY" "$T/kw_ethic.txt" "$IVORY" "$T/sub_ethic.txt"  "$IVORY" "$SERIF_B" "$T/seg4.mp4"

echo "==> SEG 5: End card"
ffmpeg -y -v error -f lavfi -i "color=c=$CHARC:s=1920x1080:r=30" \
  -f lavfi -i "anullsrc=r=44100:cl=mono" -filter_complex "
  [0:v]drawtext=fontfile=$SERIF_R:textfile=$T/thanks.txt:fontcolor=$IVORY:fontsize=96:x=(w-text_w)/2:y=452,
       drawbox=x=(iw-260)/2:y=596:w=260:h=3:color=$GOLD:t=fill,
       drawtext=fontfile=$SANS_R:textfile=$T/sub_end.txt:fontcolor=$CREAM:fontsize=34:x=(w-text_w)/2:y=638,
       setsar=1[outv]
" -map "[outv]" -map 1:a -t 5 "${VENC[@]}" "${AENC[@]}" "$T/seg5.mp4"

echo "==> CONCAT -> $OUT"
ffmpeg -y -v error \
  -i "$T/seg1.mp4" -i "$T/seg2.mp4" -i "$T/seg3.mp4" -i "$T/seg4.mp4" -i "$T/seg5.mp4" \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a][4:v][4:a]concat=n=5:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$OUT"

echo "==> DONE"
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1 "$OUT"
