# LiveKit voice agent with AssemblyAI speech-to-text and text-to-speech

A complete LiveKit Agents voice agent where AssemblyAI handles both speech ends:

- **Speech-to-text:** [AssemblyAI STT 3.7 Realtime Agent](https://www.assemblyai.com/products/streaming-speech-to-text) (`assemblyai-stt-3-7-realtime-agent`) through `assemblyai.STT`, with AssemblyAI's own end-of-turn signal (`turn_detection="stt"`, `mode="balanced"`).
- **LLM:** OpenAI GPT-4o through the LiveKit OpenAI plugin.
- **Text-to-speech:** [AssemblyAI text-to-speech](https://www.assemblyai.com/products/text-to-speech) (`assemblyai-tts-1`) through `assemblyai.TTS`, with the voice Kyla (`aai-kyla`) and word-aligned transcripts.

This is the companion repo for the tutorial: [Build a voice agent with LiveKit: AssemblyAI speech-to-text and text-to-speech](https://www.assemblyai.com/blog/build-voice-agent-livekit).

## What's in the repo

| File | What it does |
|------|--------------|
| `agent.py` | The voice agent: STT, LLM, TTS, Silero VAD and turn handling wired into one `AgentSession` |
| `requirements.txt` | `livekit-agents` with the AssemblyAI, OpenAI, Silero and codecs plugins, plus `python-dotenv` |
| `.env.example` | The environment variables `agent.py` reads |

## Quick start

Requires Python 3.11 or later and `livekit-agents` 1.8.12 or later. 1.8.12 is the first release whose AssemblyAI plugin accepts `assemblyai-stt-3-7-realtime-agent` (1.8.9 added `assemblyai.TTS`).

```bash
git clone https://github.com/kelsey-aai/voice-agent-livekit-assemblyai
cd voice-agent-livekit-assemblyai

python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env and set ASSEMBLYAI_API_KEY and OPENAI_API_KEY
# (and the LIVEKIT_* values for dev mode)
```

### Console mode

Talk to the agent from your terminal with your microphone and speakers. No LiveKit Cloud connection needed. Use headphones, so the agent doesn't hear its own voice.

```bash
python agent.py console
```

Recent `livekit-agents` releases print a deprecation notice for `console` and point at `lk agent console`, which runs the same mode through the LiveKit CLI.

### Dev mode

Connect the agent to LiveKit Cloud, then talk to it in the [Agents Playground](https://agents-playground.livekit.io/):

```bash
python agent.py dev
```

## Configuration notes

- **One key for speech:** `assemblyai.STT` and `assemblyai.TTS` both read `ASSEMBLYAI_API_KEY`.
- **Voice:** set `voice` explicitly. The plugin's own default voice differs from the API default, `aai-kyla`. `voice` takes a library slug, a voice ID (UUID) or a cloned voice's slug. See [Voices](https://www.assemblyai.com/docs/tts/voices).
- **Turn detection:** with `turn_detection="stt"`, `mode="balanced"` applies `min_turn_silence=128` and `max_turn_silence=1280`, and entity-aware endpointing holds a turn open while a caller reads out a number. With `mode` unset, the plugin defaults both silences to 100 ms, which is too aggressive for STT-based turn detection.
- **Previous model:** Universal-3.6 Pro Realtime (`universal-3-6-pro`) is still fully supported. Swap the `model` string if you need to pin it.
- **VAD:** Silero's `activation_threshold` and the STT's `vad_threshold` are both 0.2, AssemblyAI's default, so the two agree on what counts as speech.

## Learn more

- [Tutorial: Build a voice agent with LiveKit](https://www.assemblyai.com/blog/build-voice-agent-livekit)
- [AssemblyAI on LiveKit (docs)](https://www.assemblyai.com/docs/voice-agents/livekit-universal-3-6-pro)
- [Model selection](https://www.assemblyai.com/docs/streaming/select-the-speech-model)
- [Streaming TTS on LiveKit](https://www.assemblyai.com/docs/tts/livekit)
