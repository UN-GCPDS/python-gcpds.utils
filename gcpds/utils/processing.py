import numpy as np
from scipy.fftpack import fft, fftfreq, fftshift
from scipy.signal import welch as sci_welch
from datetime import datetime


# ----------------------------------------------------------------------
def fourier(eeg, d=None, fs=None, timestamp=None, axis=-1):
    """Spectral power density using Fourier."""

    timestamp = np.array(timestamp)

    if timestamp.any():
        if isinstance(timestamp[-1], (int, float)):
            delta = datetime.fromtimestamp(
                timestamp[-1]) - datetime.fromtimestamp(timestamp[0])
        else:
            delta = timestamp[-1] - timestamp[0]
        fs = max(eeg.shape) / delta.total_seconds()

    if fs:
        d = 1 / fs

    Yf = fftshift(np.abs(fft(eeg, axis=axis)))
    f = fftshift(fftfreq(Yf.shape[1], d))

    n = (Yf.shape[1] // 2)
    Yf = Yf[:, n:] * (2 / Yf.shape[1])
    f = f[n:]

    return f, Yf


# ----------------------------------------------------------------------
def welch(eeg, d=None, fs=None, timestamp=None, axis=-1):
    """Spectral power density using Welch's method."""

    timestamp = np.array(timestamp)

    if timestamp.any():
        if isinstance(timestamp[-1], (int, float)):
            delta = datetime.fromtimestamp(
                timestamp[-1]) - datetime.fromtimestamp(timestamp[0])
        else:
            delta = timestamp[-1] - timestamp[0]
        fs = max(eeg.shape) / delta.total_seconds()

    if fs:
        d = 1 / fs

    # if axis is None:
        # # if eeg.shape[0] > eeg.shape[1]:
            # # axis = 0
            # # m_ = eeg.shape[0]
        # # else:
            # # axis = 1
            # # m_ = eeg.shape[1]
    # # else:
        # # m_ = eeg.shape[0]

    m_ = max(eeg.shape)

    f, p = sci_welch(eeg, 1 / d, window='flattop',
                     nperseg=min(m_, 1024), scaling='spectrum', axis=axis)
    return f, p


