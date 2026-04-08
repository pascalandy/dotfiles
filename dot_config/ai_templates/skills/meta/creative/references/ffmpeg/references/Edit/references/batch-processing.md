# Batch Processing

Loop over a folder of files to apply the same ffmpeg operation.

## Convert all MP4s to WebM

```bash
for f in *.mp4; do
    ffmpeg -i "$f" -c:v libvpx-vp9 -crf 30 -c:a libopus "${f%.mp4}.webm"
done
```

The `${f%.mp4}` strips the `.mp4` extension; `.webm` replaces it.

## Extract audio from every video

```bash
for f in *.mp4; do
    ffmpeg -i "$f" -vn -c:a mp3 -b:a 192k "${f%.mp4}.mp3"
done
```

## Resize all images in a directory

```bash
for f in *.jpg; do
    ffmpeg -i "$f" -vf "scale=1280:-1" "resized_$f"
done
```

## Recursive (bash 4+ with globstar)

```bash
shopt -s globstar
for f in **/*.mov; do
    ffmpeg -i "$f" -c:v libx264 -crf 23 "${f%.mov}.mp4"
done
```

## Parallel processing with `xargs`

Use `-P` to control parallelism:

```bash
ls *.mp4 | xargs -P 4 -I {} ffmpeg -i {} -c:v libx264 -crf 23 {}.h264.mp4
```

`-P 4` runs 4 encodes in parallel. Tune to your core count.

## Parallel with GNU parallel (nicer)

```bash
parallel -j 4 'ffmpeg -i {} -c:v libx264 -crf 23 {.}.h264.mp4' ::: *.mp4
```

`{.}` is GNU parallel's "without extension" substitution.

## Recursive find + process

```bash
find . -name "*.mov" -print0 | while IFS= read -r -d '' f; do
    ffmpeg -i "$f" -c:v libx264 -crf 23 "${f%.mov}.mp4"
done
```

The `-print0` / `-d ''` handles filenames with spaces safely.

## Skip already-processed files

```bash
for f in *.mp4; do
    out="${f%.mp4}_720p.mp4"
    if [[ -f "$out" ]]; then
        echo "Skipping $f — output exists"
        continue
    fi
    ffmpeg -i "$f" -vf "scale=-2:720" -c:v libx264 -crf 23 "$out"
done
```

## Batch rename via ffprobe metadata

```bash
for f in *.mp4; do
    duration=$(ffprobe -v error -show_entries format=duration \
                -of default=noprint_wrappers=1:nokey=1 "$f")
    rounded=$(printf "%.0f" "$duration")
    mv "$f" "${rounded}s_${f}"
done
```

## Batch concat per directory

If you have subdirectories each containing clips to concatenate:

```bash
for dir in */; do
    cd "$dir"
    rm -f list.txt
    for f in *.mp4; do
        echo "file '$f'" >> list.txt
    done
    ffmpeg -f concat -safe 0 -i list.txt -c copy "../${dir%/}_merged.mp4"
    cd ..
done
```

## Error Handling in Loops

```bash
for f in *.mp4; do
    if ! ffmpeg -i "$f" -c:v libx264 -crf 23 "out/$f" 2>>errors.log; then
        echo "FAILED: $f" >> errors.log
    fi
done
```

Pipe ffmpeg stderr to a log so you can review failures after the batch completes.

## Progress Bar with `pv`

```bash
for f in *.mp4; do
    pv "$f" | ffmpeg -i pipe:0 -c:v libx264 -crf 23 "out/${f}"
done
```

`pv` shows progress through each input file.
