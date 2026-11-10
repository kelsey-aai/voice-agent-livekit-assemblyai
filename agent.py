from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, TurnHandlingOptions
from livekit.plugins import assemblyai, openai, silero

load_dotenv()

KYLA = "aai-kyla"  # library slug of an AssemblyAI voice
VAD_THRESHOLD = 0.2  # AssemblyAI's default; Silero should match it


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are a helpful voice AI assistant. Reply in short, "
                "plain sentences with no markdown, lists or emoji."
            )
        )


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    tts = assemblyai.TTS(
        model="assemblyai-tts-1",
        voice=KYLA,
    )
    tts.prewarm()  # Open the TTS session now, not on the first reply

    session = AgentSession(
        stt=assemblyai.STT(
            model="universal-3-6-pro",
            mode="balanced",               # min_turn_silence=128, max_turn_silence=1280
            vad_threshold=VAD_THRESHOLD,   # Match Silero's activation_threshold below
        ),
        llm=openai.LLM(model="gpt-4o"),
        tts=tts,
        vad=silero.VAD.load(
            activation_threshold=VAD_THRESHOLD,
        ),
        turn_handling=TurnHandlingOptions(
            turn_detection="stt",          # Use AssemblyAI's end-of-turn signal directly
            endpointing={"min_delay": 0},  # Avoid additive delay in STT mode
        ),
        use_tts_aligned_transcript=True,   # Word-timed transcripts from the TTS
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
    )

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=entrypoint)
    )
