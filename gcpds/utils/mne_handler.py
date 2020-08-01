import numpy as np


# ----------------------------------------------------------------------
def apply_along_epochs(func1d, epochs):
    """"""
    epochs_ = epochs.copy()

    data = np.apply_along_axis(func1d, 2, epochs_)

    new_fs = data.shape[2] / \
        (epochs_.get_data().shape[2] / epochs_.info['sfreq'])
    epochs_.resample(new_fs, npad='auto')
    epochs_._data = data.astype(epochs_._data.dtype)
    return epochs_
