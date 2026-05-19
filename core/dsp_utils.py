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
        import soundfile as sf

        audio, sample_rate = sf.read(path)
    elif path_lower.endswith(".mp3"):
        try:
            import soundfile as sf

            audio, sample_rate = sf.read(path)
        except Exception:
            import librosa

            audio, sample_rate = librosa.load(path, sr=None, mono=True)
    else:
        raise ValueError("Supported formats: .wav and .mp3")

    if len(audio.shape) > 1:
        audio = audio[:, 0]

    return audio.astype(float), int(sample_rate)
