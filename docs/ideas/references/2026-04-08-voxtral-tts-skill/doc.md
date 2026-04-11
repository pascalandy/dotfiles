Voxtral official doc:
https://docs.mistral.ai/capabilities/audio/text_to_speech

---
id: text_to_speech
title: Text to Speech
sidebar_position: 2
---

# Text to Speech

**Voxtral TTS** is Mistral's text-to-speech model with zero-shot voice cloning. It generates natural, expressive speech from text using a short audio prompt.

## Key Features

- **Zero-shot voice cloning**: Clone any voice from as little as 2–3 seconds of audio, capturing emotion, speaking style, and accent.
- **Voice-as-an-instruction**: The model follows the intonation, rhythm, and emotional rendering of the voice prompt — no prosody or emotion tags needed.
- **Multilingual support**: English, French, Spanish, Portuguese, Italian, Dutch, German, Hindi, Arabic. Supports cross-lingual voice cloning and code-mixing.
- **Streaming**: Low model latency (~90ms processing time). End-to-end API time-to-first-audio varies by format (~0.8s for `pcm`, ~3s for `mp3`), suitable for real-time voice agent applications.

<SectionTab as="h1" sectionId="tts-services">Text to Speech Services</SectionTab>

Explore our comprehensive TTS services to bring your applications to life with natural-sounding speech:
    - [Voices](text_to_speech/voices): Create and manage reusable voice profiles for consistent branding and personalization.
    - [Speech Generation](text_to_speech/speech): Generate speech using either saved voices or one-off reference audio clips with support for both basic and streaming delivery.

---
id: tts_voices
title: Voices
sidebar_position: 1
---

# Voices

Save audio samples as reusable voices. Once created, a voice can be referenced by `voice_id` in any [speech generation](../speech) request, avoiding the need to pass `ref_audio` each time.

:::warning
**Voice cloning usage policy**: By using this model and its voice cloning feature, you agree to comply with all applicable laws and our usage policy. You are not authorized to use this model for any unlawful purpose, including to impersonate others, clone voices without explicit consent, or engage in fraud, deception, misinformation, disinformation, harm, or the generation of unlawful, harmful, libelous, abusive, harassing, discriminatory, hateful, or privacy-invasive content. You must disclose AI-generated or partially AI-generated content where required by law. We disclaim all liability for non-compliant use.
:::

<ExplorerTabs id="tts-voices">
  <ExplorerTab value="create" label="Create">
    Create a voice by providing a name and a base64-encoded audio sample. The audio sample is used for voice cloning and can be retrieved later via `get_sample_audio`.

<Tabs groupId="code">
  <TabItem value="python" label="python">
    <Tabs groupId="sdk-version">
      <TabItem value="v1" label="V1" default>

```python
import base64
from pathlib import Path
from mistralai import Mistral

client = Mistral(api_key="your-api-key")

sample_audio_b64 = base64.b64encode(Path("sample.mp3").read_bytes()).decode()

voice = client.audio.voices.create(
    name="my-voice",
    sample_audio=sample_audio_b64,
    sample_filename="sample.mp3",
    languages=["en", "fr"],
    gender="female",
)

print(f"Created voice: {voice.id}")
print(f"Name: {voice.name}")
print(f"Languages: {voice.languages}")
```

      </TabItem>
      <TabItem value="v2" label="V2">

```python
import base64
from pathlib import Path
from mistralai.client import Mistral

client = Mistral(api_key="your-api-key")

sample_audio_b64 = base64.b64encode(Path("sample.mp3").read_bytes()).decode()

voice = client.audio.voices.create(
    name="my-voice",
    sample_audio=sample_audio_b64,
    sample_filename="sample.mp3",
    languages=["en", "fr"],
    gender="female",
)

print(f"Created voice: {voice.id}")
print(f"Name: {voice.name}")
print(f"Languages: {voice.languages}")
```

      </TabItem>
    </Tabs>
  </TabItem>
  <TabItem value="typescript" label="typescript">

```typescript

const client = new Mistral({ apiKey: "your-api-key" });

const sampleAudio = readFileSync("sample.mp3").toString("base64");

const voice = await client.audio.voices.create({
  name: "my-voice",
  sampleAudio: sampleAudio,
  sampleFilename: "sample.mp3",
  languages: ["en", "fr"],
  gender: "female",
});

console.log(`Created voice: ${voice.id}`);
console.log(`Name: ${voice.name}`);
console.log(`Languages: ${voice.languages}`);
```

  </TabItem>
  <TabItem value="curl" label="curl">

```bash
SAMPLE_AUDIO=$(base64 -i sample.mp3)

curl -X POST "https://api.mistral.ai/v1/audio/voices" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"my-voice\",
    \"sample_audio\": \"$SAMPLE_AUDIO\",
    \"sample_filename\": \"sample.mp3\",
    \"languages\": [\"en\", \"fr\"],
    \"gender\": \"female\"
  }"
```

  </TabItem>
  <TabItem value="output" label="output">

```json
{
  "id": "a3e8f2b1-4c9d-4a6b-8e2f-1c3d5e7a9b0c",
  "name": "my-voice",
  "slug": null,
  "languages": ["en", "fr"],
  "gender": "male",
  "age": null,
  "tags": null,
  "created_at": "2026-03-20T18:34:32.118943Z"
}
```

  </TabItem>
</Tabs>

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Display name for the voice |
| `sample_audio` | string | Yes | Base64-encoded audio file |
| `sample_filename` | string | No | Original filename (used for format detection) |
| `slug` | string | No | URL-friendly identifier |
| `languages` | string[] | No | Languages the voice supports (e.g. `["en", "fr"]`) |
| `gender` | string | No | Gender label (e.g. `"female"`, `"male"`) |
| `age` | integer | No | Approximate age of the speaker |
| `tags` | string[] | No | Arbitrary tags for filtering |
  </ExplorerTab>
  <ExplorerTab value="list" label="List">
    List all available voices with offset-based pagination.

<Tabs groupId="code">
  <TabItem value="python" label="python">
    <Tabs groupId="sdk-version">
      <TabItem value="v1" label="V1" default>

```python
from mistralai import Mistral

client = Mistral(api_key="your-api-key")

result = client.audio.voices.list(limit=10, offset=0)

print(f"Total voices: {result.total}")
for voice in result.items:
    print(f"  - {voice.name} ({voice.id})  languages={voice.languages}")

# Paginate through all voices
offset = 0
all_voices = []
while True:
    page = client.audio.voices.list(limit=10, offset=offset)
    all_voices.extend(page.items)
    if offset + len(page.items) >= page.total:
        break
    offset += len(page.items)
```

      </TabItem>
      <TabItem value="v2" label="V2">

```python
from mistralai.client import Mistral

client = Mistral(api_key="your-api-key")

result = client.audio.voices.list(limit=10, offset=0)

print(f"Total voices: {result.total}")
for voice in result.items:
    print(f"  - {voice.name} ({voice.id})  languages={voice.languages}")

# Paginate through all voices
offset = 0
all_voices = []
while True:
    page = client.audio.voices.list(limit=10, offset=offset)
    all_voices.extend(page.items)
    if offset + len(page.items) >= page.total:
        break
    offset += len(page.items)
```

      </TabItem>
    </Tabs>
  </TabItem>
  <TabItem value="typescript" label="typescript">

```typescript

const client = new Mistral({ apiKey: "your-api-key" });

const result = await client.audio.voices.list({ limit: 10, offset: 0 });

console.log(`Total voices: ${result.total}`);
for (const voice of result.items ?? []) {
  console.log(`  - ${voice.name} (${voice.id})  languages=${voice.languages}`);
}

// Paginate through all voices
let offset = 0;
const allVoices = [];
while (true) {
  const page = await client.audio.voices.list({ limit: 10, offset });
  allVoices.push(...(page.items ?? []));
  if (offset + (page.items?.length ?? 0) >= page.total) break;
  offset += page.items?.length ?? 0;
}
```

  </TabItem>
  <TabItem value="curl" label="curl">

```bash
curl "https://api.mistral.ai/v1/audio/voices?limit=10&offset=0" \
  -H "Authorization: Bearer $MISTRAL_API_KEY"
```

  </TabItem>
  <TabItem value="output" label="output">

```json
{
  "items": [
    {
      "id": "a3e8f2b1-4c9d-4a6b-8e2f-1c3d5e7a9b0c",
      "name": "my-voice",
      "slug": null,
      "languages": ["en", "fr"],
      "gender": "male",
      "age": null,
      "tags": null,
      "created_at": "2026-03-20T18:34:32.118943Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

  </TabItem>
</Tabs>
  </ExplorerTab>
  <ExplorerTab value="get" label="Get">
    Retrieve metadata for a specific voice by its ID.

<Tabs groupId="code">
  <TabItem value="python" label="python">
    <Tabs groupId="sdk-version">
      <TabItem value="v1" label="V1" default>

```python
from mistralai import Mistral

client = Mistral(api_key="your-api-key")

voice = client.audio.voices.get(voice_id="your-voice-id")

print(f"Name:      {voice.name}")
print(f"Languages: {voice.languages}")
print(f"Gender:    {voice.gender}")
print(f"Created:   {voice.created_at}")
```

      </TabItem>
      <TabItem value="v2" label="V2">

```python
from mistralai.client import Mistral

client = Mistral(api_key="your-api-key")

voice = client.audio.voices.get(voice_id="your-voice-id")

print(f"Name:      {voice.name}")
print(f"Languages: {voice.languages}")
print(f"Gender:    {voice.gender}")
print(f"Created:   {voice.created_at}")
```

      </TabItem>
    </Tabs>
  </TabItem>
  <TabItem value="typescript" label="typescript">

```typescript

const client = new Mistral({ apiKey: "your-api-key" });

const voice = await client.audio.voices.get({ voiceId: "your-voice-id" });

console.log(`Name:      ${voice.name}`);
console.log(`Languages: ${voice.languages}`);
console.log(`Gender:    ${voice.gender}`);
console.log(`Created:   ${voice.createdAt}`);
```

  </TabItem>
  <TabItem value="curl" label="curl">

```bash
curl "https://api.mistral.ai/v1/audio/voices/$VOICE_ID" \
  -H "Authorization: Bearer $MISTRAL_API_KEY"
```

  </TabItem>
  <TabItem value="output" label="output">

```json
{
  "id": "a3e8f2b1-4c9d-4a6b-8e2f-1c3d5e7a9b0c",
  "name": "my-voice",
  "slug": null,
  "languages": ["en", "fr"],
  "gender": "male",
  "age": null,
  "tags": null,
  "created_at": "2026-03-20T18:34:32.118943Z"
}
```

  </TabItem>
</Tabs>
  </ExplorerTab>
  <ExplorerTab value="update" label="Update">
    Partially update a voice's metadata. Only the fields you provide will be changed.

<Tabs groupId="code">
  <TabItem value="python" label="python">
    <Tabs groupId="sdk-version">
      <TabItem value="v1" label="V1" default>

```python
from mistralai import Mistral

client = Mistral(api_key="your-api-key")

updated = client.audio.voices.update(
    voice_id="your-voice-id",
    name="my-updated-voice",
    languages=["en", "fr", "es"],
    tags=["narrator", "calm"],
)

print(f"Updated name: {updated.name}")
print(f"Updated languages: {updated.languages}")
```

      </TabItem>
      <TabItem value="v2" label="V2">

```python
from mistralai.client import Mistral

client = Mistral(api_key="your-api-key")

updated = client.audio.voices.update(
    voice_id="your-voice-id",
    name="my-updated-voice",
    languages=["en", "fr", "es"],
    tags=["narrator", "calm"],
)

print(f"Updated name: {updated.name}")
print(f"Updated languages: {updated.languages}")
```

      </TabItem>
    </Tabs>
  </TabItem>
  <TabItem value="typescript" label="typescript">

```typescript

const client = new Mistral({ apiKey: "your-api-key" });

const updated = await client.audio.voices.update({
  voiceId: "your-voice-id",
  voiceUpdateRequest: {
    name: "my-updated-voice",
    languages: ["en", "fr", "es"],
    tags: ["narrator", "calm"],
  },
});

console.log(`Updated name: ${updated.name}`);
console.log(`Updated languages: ${updated.languages}`);
```

  </TabItem>
  <TabItem value="curl" label="curl">

```bash
curl -X PATCH "https://api.mistral.ai/v1/audio/voices/$VOICE_ID" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-updated-voice",
    "languages": ["en", "fr", "es"],
    "tags": ["narrator", "calm"]
  }'
```

  </TabItem>
  <TabItem value="output" label="output">

```json
{
  "id": "a3e8f2b1-4c9d-4a6b-8e2f-1c3d5e7a9b0c",
  "name": "my-updated-voice",
  "slug": null,
  "languages": ["en", "fr", "es"],
  "gender": "male",
  "age": null,
  "tags": ["narrator", "calm"],
  "created_at": "2026-03-20T18:34:32.118943Z"
}
```

  </TabItem>
</Tabs>
  </ExplorerTab>
  <ExplorerTab value="delete" label="Delete">
    Permanently delete a voice. Any speech requests using its `voice_id` will fail after deletion.

<Tabs groupId="code">
  <TabItem value="python" label="python">
    <Tabs groupId="sdk-version">
      <TabItem value="v1" label="V1" default>

```python
from mistralai import Mistral

client = Mistral(api_key="your-api-key")

result = client.audio.voices.delete(voice_id="your-voice-id")
print(f"Deleted: {result.id}")
```

      </TabItem>
      <TabItem value="v2" label="V2">

```python
from mistralai.client import Mistral

client = Mistral(api_key="your-api-key")

result = client.audio.voices.delete(voice_id="your-voice-id")
print(f"Deleted: {result.id}")
```

      </TabItem>
    </Tabs>
  </TabItem>
  <TabItem value="typescript" label="typescript">

```typescript

const client = new Mistral({ apiKey: "your-api-key" });

const result = await client.audio.voices.delete({ voiceId: "your-voice-id" });
console.log(`Deleted: ${result.id}`);
```

  </TabItem>
  <TabItem value="curl" label="curl">

```bash
curl -X DELETE "https://api.mistral.ai/v1/audio/voices/$VOICE_ID" \
  -H "Authorization: Bearer $MISTRAL_API_KEY"
```

  </TabItem>
  <TabItem value="output" label="output">

```json
{
  "id": "a3e8f2b1-4c9d-4a6b-8e2f-1c3d5e7a9b0c",
  "name": "my-updated-voice",
  "slug": null,
  "languages": ["en", "fr", "es"],
  "gender": "male",
  "age": null,
  "tags": ["narrator", "calm"],
  "created_at": "2026-03-20T18:34:32.118943Z"
}
```

  </TabItem>
</Tabs>
  </ExplorerTab>
  <ExplorerTab value="sample" label="Sample">
    Retrieve the original audio sample that was used to create the voice, returned as raw audio bytes.

<Tabs groupId="code">
  <TabItem value="python" label="python">
    <Tabs groupId="sdk-version">
      <TabItem value="v1" label="V1" default>

```python
from pathlib import Path
from mistralai import Mistral

client = Mistral(api_key="your-api-key")

audio_bytes = client.audio.voices.get_sample_audio(voice_id="your-voice-id")
Path("voice_sample.wav").write_bytes(audio_bytes)
print("Saved sample to voice_sample.wav")
```

      </TabItem>
      <TabItem value="v2" label="V2">

```python
from pathlib import Path
from mistralai.client import Mistral

client = Mistral(api_key="your-api-key")

audio_bytes = client.audio.voices.get_sample_audio(voice_id="your-voice-id")
Path("voice_sample.wav").write_bytes(audio_bytes)
print("Saved sample to voice_sample.wav")
```

      </TabItem>
    </Tabs>
  </TabItem>
  <TabItem value="typescript" label="typescript">

```typescript

const client = new Mistral({ apiKey: "your-api-key" });

const audioBytes = await client.audio.voices.getSampleAudio({
  voiceId: "your-voice-id",
});
writeFileSync("voice_sample.wav", Buffer.from(audioBytes));
console.log("Saved sample to voice_sample.wav");
```

  </TabItem>
  <TabItem value="curl" label="curl">

```bash
curl "https://api.mistral.ai/v1/audio/voices/$VOICE_ID/sample" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  > voice_sample.wav
```

  </TabItem>
</Tabs>
  </ExplorerTab>
</ExplorerTabs>

---
id: tts_speech
title: Speech Generation
sidebar_position: 2
---

# Speech Generation

Generate speech from text using a [saved voice](voices) (`voice_id`) or a one-off reference audio clip (`ref_audio`).

<SectionTab as="h1" sectionId="generate">Generate</SectionTab>

<ExplorerTabs id="tts-voice-options">
  <ExplorerTab value="saved-voice" label="Saved Voice">
    Generate speech using a previously [saved voice](voices) (`voice_id`) identifier.

<ExplorerTabs id="tts-generate">
  <ExplorerTab value="basic" label="Basic">
    <Tabs groupId="code">
  <TabItem value="python" label="python">
    <Tabs groupId="sdk-version">
      <TabItem value="v1" label="V1" default>

```python
import base64
from pathlib import Path
from mistralai import Mistral

client = Mistral(api_key="your-api-key")

response = client.audio.speech.complete(
    model="voxtral-mini-tts-2603",
    input="Hello! This is Voxtral, Mistral's text-to-speech model.",
    voice_id="your-voice-id",
    response_format="mp3",
)

Path("output.mp3").write_bytes(base64.b64decode(response.audio_data))
print("Saved to output.mp3")
```

      </TabItem>
      <TabItem value="v2" label="V2">

```python
import base64
from pathlib import Path
from mistralai.client import Mistral

client = Mistral(api_key="your-api-key")

response = client.audio.speech.complete(
    model="voxtral-mini-tts-2603",
    input="Hello! This is Voxtral, Mistral's text-to-speech model.",
    voice_id="your-voice-id",
    response_format="mp3",
)

Path("output.mp3").write_bytes(base64.b64decode(response.audio_data))
print("Saved to output.mp3")
```

      </TabItem>
    </Tabs>
  </TabItem>
  <TabItem value="typescript" label="typescript">

```typescript

const client = new Mistral({ apiKey: "your-api-key" });

const response = await client.audio.speech.complete({
  model: "voxtral-mini-tts-2603",
  input: "Hello! This is Voxtral, Mistral's text-to-speech model.",
  voiceId: "your-voice-id",
  responseFormat: "mp3",
});

writeFileSync("output.mp3", response.audioData);
console.log("Saved to output.mp3");
```

  </TabItem>
  <TabItem value="curl" label="curl">

```bash
curl -X POST "https://api.mistral.ai/v1/audio/speech" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "voxtral-mini-tts-2603",
    "input": "Hello! This is Voxtral, Mistral'\''s text-to-speech model.",
    "voice_id": "your-voice-id",
    "response_format": "mp3"
  }' | jq -r '.audio_data' | base64 -d > output.mp3
```

  </TabItem>
  <TabItem value="output" label="output">

```json
{
  "audio_data": "SUQzBAAAAAAAIlRTU0UAAAAOAAADTGF2ZjYxLjcu...<base64_encoded_audio>"
}
```

  </TabItem>
</Tabs>
  </ExplorerTab>
  <ExplorerTab value="streaming" label="Streaming">
    Each chunk is a `speech.audio.delta` event with a base64-encoded audio fragment. The stream ends with a `speech.audio.done` event containing usage info.

:::tip
Use `response_format="pcm"` for the lowest streaming latency (~0.7s time-to-first-audio vs ~2s for `mp3`).
:::

<Tabs groupId="code">
  <TabItem value="python" label="python">
    <Tabs groupId="sdk-version">
      <TabItem value="v1" label="V1" default>

```python
import base64
from mistralai import Mistral

client = Mistral(api_key="your-api-key")

audio_chunks = []

with client.audio.speech.complete(
    model="voxtral-mini-tts-2603",
    input="Streaming makes voice agents feel more responsive and natural.",
    voice_id="your-voice-id",
    response_format="opus",
    stream=True,
) as stream:
    for event in stream:
        if event.event == "speech.audio.delta":
            audio_chunks.append(base64.b64decode(event.data.audio_data))
        elif event.event == "speech.audio.done":
            print(f"Done. Tokens used: {event.data.usage}")

audio_bytes = b"".join(audio_chunks)
with open("output_streamed.opus", "wb") as f:
    f.write(audio_bytes)
```

      </TabItem>
      <TabItem value="v2" label="V2">

```python
import base64
from mistralai.client import Mistral

client = Mistral(api_key="your-api-key")

audio_chunks = []

with client.audio.speech.complete(
    model="voxtral-mini-tts-2603",
    input="Streaming makes voice agents feel more responsive and natural.",
    voice_id="your-voice-id",
    response_format="opus",
    stream=True,
) as stream:
    for event in stream:
        if event.event == "speech.audio.delta":
            audio_chunks.append(base64.b64decode(event.data.audio_data))
        elif event.event == "speech.audio.done":
            print(f"Done. Tokens used: {event.data.usage}")

audio_bytes = b"".join(audio_chunks)
with open("output_streamed.opus", "wb") as f:
    f.write(audio_bytes)
```

      </TabItem>
    </Tabs>
  </TabItem>
  <TabItem value="typescript" label="typescript">

```typescript

const client = new Mistral({ apiKey: "your-api-key" });

const stream = await client.audio.speech.complete({
  model: "voxtral-mini-tts-2603",
  input: "Streaming makes voice agents feel more responsive and natural.",
  voiceId: "your-voice-id",
  responseFormat: "opus",
  stream: true,
});

const audioChunks: Uint8Array[] = [];

for await (const event of stream) {
  if (event.event === "speech.audio.delta") {
    audioChunks.push(Buffer.from(event.data.audioData, "base64"));
  } else if (event.event === "speech.audio.done") {
    console.log("Done. Tokens used:", event.data.usage);
  }
}

const audioBytes = Buffer.concat(audioChunks);
writeFileSync("output_streamed.opus", audioBytes);
```

  </TabItem>
  <TabItem value="output" label="output">

```json
[
  {
    "event": "speech.audio.delta",
    "data": {
      "audio_data": "<base64_audio_chunk>"
    }
  },
  {
    "event": "speech.audio.delta",
    "data": {
      "audio_data": "<base64_audio_chunk>"
    }
  },
  {
    "event": "speech.audio.done",
    "data": {
      "usage": {
        "prompt_tokens": 56,
        "completion_tokens": 94080,
        "total_tokens": 94136
      }
    }
  }
]
```

  </TabItem>
</Tabs>
  </ExplorerTab>
</ExplorerTabs>
  </ExplorerTab>
  <ExplorerTab value="ref-audio" label="Ref Audio">
    Pass a base64-encoded audio clip directly via `ref_audio` to clone a voice on the fly, without creating a saved voice.

<ExplorerTabs id="tts-ref-audio">
  <ExplorerTab value="basic" label="Basic">
    <Tabs groupId="code">
  <TabItem value="python" label="python">
    <Tabs groupId="sdk-version">
      <TabItem value="v1" label="V1" default>

```python
import base64
from pathlib import Path
from mistralai import Mistral

client = Mistral(api_key="your-api-key")

ref_audio_b64 = base64.b64encode(Path("sample.mp3").read_bytes()).decode()

response = client.audio.speech.complete(
    model="voxtral-mini-tts-2603",
    input="This speech will sound like the voice in the reference audio.",
    ref_audio=ref_audio_b64,
    response_format="wav",
)

Path("output.wav").write_bytes(base64.b64decode(response.audio_data))
```

      </TabItem>
      <TabItem value="v2" label="V2">

```python
import base64
from pathlib import Path
from mistralai.client import Mistral

client = Mistral(api_key="your-api-key")

ref_audio_b64 = base64.b64encode(Path("sample.mp3").read_bytes()).decode()

response = client.audio.speech.complete(
    model="voxtral-mini-tts-2603",
    input="This speech will sound like the voice in the reference audio.",
    ref_audio=ref_audio_b64,
    response_format="wav",
)

Path("output.wav").write_bytes(base64.b64decode(response.audio_data))
```

      </TabItem>
    </Tabs>
  </TabItem>
  <TabItem value="typescript" label="typescript">

```typescript

const client = new Mistral({ apiKey: "your-api-key" });

const refAudio = readFileSync("sample.mp3").toString("base64");

const response = await client.audio.speech.complete({
  model: "voxtral-mini-tts-2603",
  input: "This speech will sound like the voice in the reference audio.",
  refAudio: refAudio,
  responseFormat: "wav",
});

writeFileSync("output.wav", response.audioData);
```

  </TabItem>
  <TabItem value="curl" label="curl">

```bash
REF_AUDIO=$(base64 -i sample.mp3)

curl -X POST "https://api.mistral.ai/v1/audio/speech" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"voxtral-mini-tts-2603\",
    \"input\": \"This speech will sound like the voice in the reference audio.\",
    \"ref_audio\": \"$REF_AUDIO\",
    \"response_format\": \"wav\"
  }" | jq -r '.audio_data' | base64 -d > output.wav
```

  </TabItem>
  <TabItem value="output" label="output">

```json
{
  "audio_data": "UklGRv////9XQVZFZm10IBAAAAABAAEAwF0AAIC7...<base64_encoded_audio>"
}
```

  </TabItem>
</Tabs>
  </ExplorerTab>
  <ExplorerTab value="streaming" label="Streaming">
    Each chunk is a `speech.audio.delta` event with a base64-encoded audio fragment. The stream ends with a `speech.audio.done` event containing usage info.

:::tip
Use `response_format="pcm"` for the lowest streaming latency (~0.7s time-to-first-audio vs ~2s for `mp3`).
:::

<Tabs groupId="code">
  <TabItem value="python" label="python">
    <Tabs groupId="sdk-version">
      <TabItem value="v1" label="V1" default>

```python
import base64
from pathlib import Path
from mistralai import Mistral

client = Mistral(api_key="your-api-key")

ref_audio_b64 = base64.b64encode(Path("sample.mp3").read_bytes()).decode()
audio_chunks = []

with client.audio.speech.complete(
    model="voxtral-mini-tts-2603",
    input="Streaming makes voice agents feel more responsive and natural.",
    ref_audio=ref_audio_b64,
    response_format="opus",
    stream=True,
) as stream:
    for event in stream:
        if event.event == "speech.audio.delta":
            audio_chunks.append(base64.b64decode(event.data.audio_data))
        elif event.event == "speech.audio.done":
            print(f"Done. Tokens used: {event.data.usage}")

audio_bytes = b"".join(audio_chunks)
with open("output_streamed.opus", "wb") as f:
    f.write(audio_bytes)
```

      </TabItem>
      <TabItem value="v2" label="V2">

```python
import base64
from pathlib import Path
from mistralai.client import Mistral

client = Mistral(api_key="your-api-key")

ref_audio_b64 = base64.b64encode(Path("sample.mp3").read_bytes()).decode()
audio_chunks = []

with client.audio.speech.complete(
    model="voxtral-mini-tts-2603",
    input="Streaming makes voice agents feel more responsive and natural.",
    ref_audio=ref_audio_b64,
    response_format="opus",
    stream=True,
) as stream:
    for event in stream:
        if event.event == "speech.audio.delta":
            audio_chunks.append(base64.b64decode(event.data.audio_data))
        elif event.event == "speech.audio.done":
            print(f"Done. Tokens used: {event.data.usage}")

audio_bytes = b"".join(audio_chunks)
with open("output_streamed.opus", "wb") as f:
    f.write(audio_bytes)
```

      </TabItem>
    </Tabs>
  </TabItem>
  <TabItem value="typescript" label="typescript">

```typescript

const client = new Mistral({ apiKey: "your-api-key" });

const refAudio = readFileSync("sample.mp3").toString("base64");
const stream = await client.audio.speech.complete({
  model: "voxtral-mini-tts-2603",
  input: "Streaming makes voice agents feel more responsive and natural.",
  refAudio: refAudio,
  responseFormat: "opus",
  stream: true,
});

const audioChunks: Uint8Array[] = [];

for await (const event of stream) {
  if (event.event === "speech.audio.delta") {
    audioChunks.push(Buffer.from(event.data.audioData, "base64"));
  } else if (event.event === "speech.audio.done") {
    console.log("Done. Tokens used:", event.data.usage);
  }
}

const audioBytes = Buffer.concat(audioChunks);
writeFileSync("output_streamed.opus", audioBytes);
```

  </TabItem>
  <TabItem value="output" label="output">

```json
[
  {
    "event": "speech.audio.delta",
    "data": {
      "audio_data": "<base64_audio_chunk>"
    }
  },
  {
    "event": "speech.audio.delta",
    "data": {
      "audio_data": "<base64_audio_chunk>"
    }
  },
  {
    "event": "speech.audio.done",
    "data": {
      "usage": {
        "prompt_tokens": 56,
        "completion_tokens": 94080,
        "total_tokens": 94136
      }
    }
  }
]
```

  </TabItem>
</Tabs>
  </ExplorerTab>
</ExplorerTabs>

<SectionTab as="h2" sectionId="ref-audio-guidelines">`ref_audio` Guidelines</SectionTab>

When using `ref_audio` for zero-shot cloning:

- **Duration**: 3–25 seconds
- **Single speaker only**
- **Clean recording** with no background noise
- **Neutral prosody** — avoid excessive pausing or disfluencies
- **Expressive pitch** (flat voices produce flat output)
  </ExplorerTab>
</ExplorerTabs>

<SectionTab as="h2" sectionId="response-formats">Response Audio Formats</SectionTab>

| Format | Description |
|--------|-------------|
| `mp3` | Compressed, suitable for most use cases |
| `wav` | Uncompressed PCM, highest quality |
| `pcm` | Raw float32 LE samples — recommended for streaming (lowest latency) |
| `flac` | Lossless compression |
| `opus` | Low bitrate, good for streaming |
