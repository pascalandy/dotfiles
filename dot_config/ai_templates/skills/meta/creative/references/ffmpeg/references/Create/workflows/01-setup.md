# 01 — Setup

Verify the toolkit is installed, dependencies are present, and Modal endpoints are configured. Skip directly to Step 4 "Quick Test" if `verify_setup.py` reports everything `[x]`.

## Step 1: Check Current State

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/verify_setup.py
```

If everything shows `[x]`, jump to **Step 4 Quick Test**. Otherwise continue.

## Step 2: Install Python Dependencies

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
pip3 install --break-system-packages -r tools/requirements.txt
```

`--break-system-packages` is needed on Debian/Ubuntu with managed Python (PEP 668). Safe inside containers.

## Step 3: Configure Cloud GPU Endpoints

The toolkit needs cloud GPU endpoint URLs in `.env`.

```bash
cat ~/.openclaw/workspace/claude-code-video-toolkit/.env | grep MODAL
```

If Modal endpoints are configured, jump to Step 4. Otherwise set up Modal:

```bash
pip3 install --break-system-packages modal
python3 -m modal setup   # Opens browser for authentication

cd ~/.openclaw/workspace/claude-code-video-toolkit
modal deploy docker/modal-qwen3-tts/app.py
modal deploy docker/modal-flux2/app.py
modal deploy docker/modal-music-gen/app.py
modal deploy docker/modal-sadtalker/app.py
modal deploy docker/modal-image-edit/app.py
modal deploy docker/modal-upscale/app.py
modal deploy docker/modal-propainter/app.py
modal deploy docker/modal-ltx2/app.py
```

**LTX-2 prerequisite:** Before deploying LTX-2, create a HuggingFace secret and accept the [Gemma 3 license](https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized):

```bash
modal secret create huggingface-token HF_TOKEN=hf_your_read_access_token
```

Capture each deploy's endpoint URL and add to `.env`:

```
ACEMUSIC_API_KEY=...                          # Free key from acemusic.ai/api-key
MODAL_QWEN3_TTS_ENDPOINT_URL=https://...modal.run
MODAL_FLUX2_ENDPOINT_URL=https://...modal.run
MODAL_MUSIC_GEN_ENDPOINT_URL=https://...modal.run
MODAL_SADTALKER_ENDPOINT_URL=https://...modal.run
MODAL_IMAGE_EDIT_ENDPOINT_URL=https://...modal.run
MODAL_UPSCALE_ENDPOINT_URL=https://...modal.run
MODAL_DEWATERMARK_ENDPOINT_URL=https://...modal.run
MODAL_LTX2_ENDPOINT_URL=https://...modal.run
```

Optional but recommended — Cloudflare R2 for reliable file transfer:

```
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=video-toolkit
```

## Step 4: Verify and Quick Test

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/verify_setup.py
```

All tools should show `[x]`. Run a quick test:

```bash
cd ~/.openclaw/workspace/claude-code-video-toolkit
python3 tools/qwen3_tts.py --text "Hello, this is a test." --speaker Ryan --tone warm --output /tmp/video-toolkit-test.mp3 --cloud modal
```

Valid .mp3 output = setup complete. If it fails, check:

- `.env` has the correct `MODAL_QWEN3_TTS_ENDPOINT_URL`
- Run `python3 tools/verify_setup.py --json` and check `modal_tools` for missing endpoints

## Cost Baseline

Modal includes $30/month free compute. A typical 60s video costs $1-3. See `../references/cost-estimates.md` for per-tool breakdown.
