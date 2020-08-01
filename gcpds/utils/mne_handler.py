import numpy as np


# ----------------------------------------------------------------------
def apply_along_axis(func1d, axis, epochs):
    """"""

    data = np.apply_along_axis(func1d, axis, epochs)

    new_fs = data.shape[2] / \
        (epochs.get_data().shape[2] / epochs.info['sfreq'])
    epochs.resample(new_fs, npad='auto')
    epochs._data = data.astype(epochs._data.dtype)
    return epochs
