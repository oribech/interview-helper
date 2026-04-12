"""Mic capture + RealtimeSTT transcription.

Continuously captures audio from microphone and outputs transcript chunks.
Uses RealtimeSTT with faster-whisper for local, low-latency transcription.
"""

import threading
import time
from typing import Callable, Optional


class AudioTranscriber:
    """Wraps RealtimeSTT to provide real-time mic → text transcription."""

    def __init__(
        self,
        on_text: Callable[[str], None],
        on_realtime_text: Optional[Callable[[str], None]] = None,
        model: str = "small",
        language: str = "en",
    ):
        """
        Args:
            on_text: called with final transcribed sentence
            on_realtime_text: called with partial/interim text (for live ticker)
            model: whisper model size (tiny/base/small/medium/large)
            language: language code
        """
        self.on_text = on_text
        self.on_realtime_text = on_realtime_text
        self.model = model
        self.language = language
        self.recorder = None
        self._running = False

    def start(self):
        """Start listening to microphone in background thread."""
        from RealtimeSTT import AudioToTextRecorder

        self.recorder = AudioToTextRecorder(
            model=self.model,
            language=self.language,
            spinner=False,
            # VAD settings for interview pace
            silero_sensitivity=0.4,
            post_speech_silence_duration=0.8,
            # Realtime display callback
            enable_realtime_transcription=self.on_realtime_text is not None,
            realtime_processing_pause=0.2,
            on_realtime_transcription_update=self._handle_realtime,
        )

        self._running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
        print("[Audio] Listening...")

    def _listen_loop(self):
        """Blocking loop that feeds transcriptions to callback."""
        while self._running:
            try:
                t0 = time.perf_counter()
                text = self.recorder.text()
                elapsed = (time.perf_counter() - t0) * 1000
                if text and text.strip():
                    print(f"[Timing] Audio STT: {elapsed:.0f}ms for '{text.strip()[:50]}'")
                    self.on_text(text.strip())
            except Exception as e:
                print(f"[Audio] Error: {e}")

    def _handle_realtime(self, text: str):
        """Forward realtime partial text."""
        if self.on_realtime_text and text and text.strip():
            self.on_realtime_text(text.strip())

    def change_model(self, new_model: str):
        """Change the whisper model at runtime by restarting the recorder."""
        if new_model == self.model:
            return
        print(f"[Audio] Switching model: {self.model} → {new_model}")
        self.model = new_model
        self.stop()
        import time
        time.sleep(0.5)
        self.start()

    def stop(self):
        """Stop listening."""
        self._running = False
        if self.recorder:
            try:
                self.recorder.stop()
            except Exception:
                pass
        print("[Audio] Stopped")
