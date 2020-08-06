import numpy as np
import mne
import pandas as pd


# ----------------------------------------------------------------------
def apply_along_epochs(func1d, epochs):
    """"""
    epochs_ = epochs.copy()

    data = np.apply_along_axis(func1d, 2, epochs_)

    new_fs = data.shape[2] / \
        (epochs_.get_data().shape[2] / epochs_.info['sfreq'])
    epochs_.resample(new_fs, npad='auto')
    epochs_._data = data
    # epochs_._data = data - data.mean(axis=2)[..., np.newaxis]

    return epochs_


# ----------------------------------------------------------------------
def get_best_montage(channels):
    """"""
    data = {}
    target = set(channels)

    for montage_name in mne.channels.get_builtin_montages():
        montage = mne.channels.make_standard_montage(montage_name)
        count = len(target.intersection(set(montage.ch_names)))
        missings = target.difference(set(montage.ch_names))
    #     counts.append([count, missings, montage_name])

        data.setdefault('count', []).append(count)
        data.setdefault('missings', []).append(len(missings))
        data.setdefault('missings channels', []).append(missings)
        data.setdefault('montage', []).append(montage_name)

    df = pd.DataFrame.from_dict(data)
    return df.sort_values('count', ascending=False, ignore_index=True)

