"""Shared DSP helpers used across laboratory modules."""

import numpy as np


def parse_int_sequence(text):
    """Parse space-separated integers; raises ValueError if invalid."""
    parts = text.strip().split()
    if not parts:
        raise ValueError("Sequence cannot be empty.")

    values = []
    for part in parts:
        try:
            values.append(int(part))
        except ValueError as exc:
            raise ValueError(
                f"'{part}' is not a valid integer."
            ) from exc

    return values


def z_transform(values):
    """Build Z-transform expression string, e.g. 1 + 2z^-1 - 1z^-2 + 3z^-3."""
    signed = [(n, v) for n, v in enumerate(values) if v != 0]

    if not signed:
        return "0"

    expression = ""
    for i, (n, value) in enumerate(signed):
        if n == 0:
            term = str(value)
        elif value > 0:
            term = f"{value}z^-{n}"
        else:
            term = f"{abs(value)}z^-{n}"

        if expression == "":
            expression = term
        elif value > 0:
            expression += " + " + term
        else:
            expression += " - " + term

    return expression


def format_dft_value(val):
    """Format one complex DFT coefficient for display."""
    real = int(round(val.real))
    imag = int(round(val.imag))

    if imag == 0:
        return str(real)

    if abs(imag) == 1:
        j_part = "j"
    else:
        j_part = f"{abs(imag)}j"

    if imag > 0:
        return f"{real} + {j_part}"
    return f"{real} - {j_part}"


def format_dft_sequence(X):
    """Format full DFT output like: {2, 1 + j, 0, 1 - j}"""
    parts = [format_dft_value(v) for v in X]
    return "{" + ", ".join(parts) + "}"


def style_axes(ax, title="", xlabel="", ylabel=""):
    """Apply consistent dark-theme styling to a matplotlib axis."""
    from config import BG_CARD, BORDER, TEXT_MUTED, TEXT_WHITE

    ax.set_facecolor(BG_CARD)
    ax.set_title(title, color=TEXT_WHITE)
    ax.set_xlabel(xlabel, color=TEXT_MUTED)
    ax.set_ylabel(ylabel, color=TEXT_MUTED)
    ax.tick_params(colors=TEXT_MUTED)

    for spine in ax.spines.values():
        spine.set_color(BORDER)

    ax.grid(True, alpha=0.2)


def stem_with_line(ax, x, y, stem_color, line_color, label=None):
    """Draw stem plot with connecting line (Lab 7 style)."""
    markerline, stemlines, _baseline = ax.stem(
        x,
        y,
        linefmt=stem_color,
        markerfmt="o",
        basefmt=" "
    )
    markerline.set_markerfacecolor(stem_color)
    markerline.set_markeredgecolor(stem_color)

    try:
        stemlines.set_color(stem_color)
    except Exception:
        pass

    ax.plot(x, y, color=line_color, linewidth=1.5, label=label)


def load_audio_file(path):
    """Load .wav or .mp3 as mono float array and sample rate."""
    path_lower = path.lower()

    if path_lower.endswith(".wav"):
        # WAV: soundfile is reliable on all platforms
        import soundfile as sf
        audio, sample_rate = sf.read(path)

    elif path_lower.endswith(".mp3"):
        # MP3 strategy 1: pydub (works on Windows without ffmpeg DLL fuss)
        loaded = False
        try:
            from pydub import AudioSegment
            import numpy as np
            seg = AudioSegment.from_mp3(path)
            sample_rate = seg.frame_rate
            samples = np.array(seg.get_array_of_samples(), dtype=np.float32)
            # Normalise to [-1.0, 1.0]
            samples = samples / (2 ** (8 * seg.sample_width - 1))
            # Mix down to mono if stereo
            if seg.channels == 2:
                samples = samples.reshape(-1, 2).mean(axis=1)
            audio = samples
            loaded = True
        except Exception:
            pass

        # MP3 strategy 2: librosa (needs ffmpeg in PATH)
        if not loaded:
            try:
                import librosa
                audio, sample_rate = librosa.load(path, sr=None, mono=True)
                loaded = True
            except Exception:
                pass

        # MP3 strategy 3: soundfile with libsndfile MP3 support (rare but possible)
        if not loaded:
            try:
                import soundfile as sf
                audio, sample_rate = sf.read(path)
                loaded = True
            except Exception:
                pass

        if not loaded:
            raise RuntimeError(
                "Could not decode MP3 file.\n\n"
                "Please install pydub:  pip install pydub\n"
                "pydub uses the built-in Windows MP3 codec — no extra downloads needed.\n\n"
                "Alternatively, convert your file to .wav and try again."
            )
    else:
        raise ValueError("Supported formats: .wav and .mp3")

    # Ensure 1-D mono
    import numpy as np
    audio = np.array(audio)
    if audio.ndim > 1:
        audio = audio[:, 0]

    return audio.astype(float), int(sample_rate)