---
name: ffmpeg
description: Unified video and audio toolkit covering AI-generated video production, one-shot operations, content analysis, and full ffmpeg editing. USE WHEN video, audio, ffmpeg, ffprobe, mp4, mov, mkv, webm, mp3, wav, cut, trim, slice, merge, concat, join, thumbnail, screenshot, gif, extract audio, watermark, speed change, slow motion, fast motion, transcode, convert format, H.264, H.265, HEVC, VP9, AV1, HLS, DASH, stream, LUT, .cube, color grade, brightness contrast saturation, chroma key, green screen, picture in picture, PiP, stacking, hstack, vstack, xstack, xfade, dissolve, transition, drawtext, title, subtitles, SRT, ASS, burn subs, loudnorm, normalize audio, denoise, fade in out, volume, reverse, frame rate, minterpolate, slideshow, NVENC, QSV, VideoToolbox, VAAPI, hardware accel, GPU encode, batch process, ffprobe, probe metadata, analyse video, summarise recording, what happens in video, timestamped summary, frame extraction, scene detection, create video, explainer video, product demo, marketing video, AI voiceover, TTS, talking head, narrator, Remotion, FLUX, SadTalker, LTX-2, Qwen3-TTS, ACE-Step, acemusic, Modal, RunPod, music generation, image generation, video generation, chain video, scene images.
---

# FFmpeg

## Routing

| Request Pattern | Route To |
|---|---|
| create video from brief, explainer video, product demo, marketing video, AI voiceover, TTS, talking head, narrator, Remotion, FLUX image gen, SadTalker, LTX-2, Qwen3-TTS, ACE-Step, acemusic, music generation, scene images, chain video, Modal, RunPod | `Create/SKILL.md` |
| cut, trim, slice video, merge clips, concatenate (simple), extract audio track, thumbnail, screenshot frame, gif, convert format (one-shot), change speed, add watermark | `Quick/SKILL.md` |
| analyse video, summarise recording, what happens in video, describe video content, timestamped summary, frame extraction for vision, scene detection for understanding | `Analyse/SKILL.md` |
| transcode, convert codec, H.264, H.265, HEVC, VP9, AV1, HLS, DASH, streaming, LUT, .cube, haldclut, color grade, eq brightness contrast saturation, hue shift, chroma key, green screen, colorkey, picture in picture, PiP, stacking (hstack/vstack/xstack), xfade, transition, drawtext, title, subtitles, SRT, ASS, burn subs, loudnorm, normalize audio, denoise, afftdn, fade, volume, amix, reverse, frame rate, minterpolate, slideshow, NVENC, QSV, VideoToolbox, VAAPI, hardware accel, batch process loop, ffprobe, preset profile, web-optimized, social-vertical | `Edit/SKILL.md` |

## Routing Notes

- **Quick vs Edit**: Quick = single-purpose wrapper script with positional flags (`cut.sh -i in.mp4 -s 00:01:00 -e 00:02:00 -o out.mp4`). Edit = raw ffmpeg command construction, multi-filter graphs, streaming setups, preset profiles. If the user says "just cut" or "quick trim", use Quick. If they want anything involving codecs, filters, LUTs, or chained operations, use Edit.
- **Create vs Edit**: Create generates new media from text (AI models on cloud GPU). Edit manipulates existing media. If the user has files and wants to change them, use Edit.
- **Analyse vs Quick thumbnail**: Quick's `thumb.sh` grabs one frame at a specific timestamp. Analyse extracts many frames and reasons about them to produce a narrative summary. If the user wants to *understand* what's in the video, use Analyse.
