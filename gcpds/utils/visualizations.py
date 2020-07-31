import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import matplotlib
import mne


# ----------------------------------------------------------------------
def plot_eeg(data, channels, fs, sca=1, cmap='viridis'):
    """"""
    plt.gcf()
    time = np.linspace(0, data.shape[1] / fs, data.shape[1])
    # sumf = sca * \
        # np.max(
            # data - np.matlib.repmat(data.mean(axis=1).reshape(-1, 1), 1, data.shape[1]))

    sumf = sca * np.max(data - data.mean(axis=1)[..., np.newaxis])

    cmap = cm.get_cmap(cmap, len(channels))
    [plt.plot(time, (ch - ch.mean()) + sumf * i, color=cmap(i), zorder=10)
     for i, ch in enumerate(data)]

    plt.yticks(np.arange(0, sumf * len(channels), sumf), channels)
    plt.grid(True, zorder=-1, alpha=0.2)
    plt.ylabel('Channels')
    plt.xlabel('Time [$s$]')


# ----------------------------------------------------------------------
def plot_topoplot(data, channels, fs, sca=1, cmap='plasma', montage='standard_1020', **kwargs):

    info = mne.create_info(channels, sfreq=fs, ch_types="eeg")
    info.set_montage(montage)

    fig = plt.gcf()
    ax = plt.gca()

#     Colorbar
    cax = fig.add_axes([0.95, 0.15, 0.05, 0.75])
    norm = matplotlib.colors.Normalize(vmin=kwargs.get(
        'vmin', data.min()), vmax=kwargs.get('vmax', data.max()))
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, cax=cax)

    mne.viz.plot_topomap(data, info, names=channels,
                         cmap=cmap, axes=ax, **kwargs)

