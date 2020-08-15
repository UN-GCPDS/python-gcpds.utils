""""""

from .google_drive_downloader import GoogleDriveDownloader as gdd
from scipy.io import loadmat
import os
from abc import ABCMeta, abstractmethod
from typing import Union, Optional
import numpy as np
import json
import mne
import tables
import logging

ALL = 'all'


# ----------------------------------------------------------------------
def load_mat(path: str, mat: str, fid: str, size: Optional[int] = None, overwrite: Optional[bool] = False) -> np.ndarray:
    """Get the raw data for one individual file.

    If the file does not exist in the specified path then tries to download it
    from Google Drive.
    """

    filepath = os.path.join(path, mat)

    if os.path.exists(filepath) and not overwrite:
        try:
            return loadmat(filepath)
        except ValueError:
            return tables.open_file(filepath, driver="H5FD_CORE")
        except:
            logging.warning('Corrupt database!!\n, overwriting...')
            return load_mat(path, mat, fid, size, overwrite=True)

    else:
        logging.warning('Database not found!')
        logging.warning('downloading...')

        os.makedirs(path, exist_ok=True)
        gdd.download_file_from_google_drive(file_id=fid,
                                            dest_path=filepath,
                                            unzip=False,
                                            overwrite=overwrite,
                                            size=size)
        return load_mat(path, mat, fid, size)


########################################################################
class Database(metaclass=ABCMeta):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, path: Optional[str] = '.') -> None:
        """Constructor"""
        self.path = path

    # ----------------------------------------------------------------------
    @abstractmethod
    def load_subject(self, subject: int, mode: str) -> None:
        """"""
        if not mode in ['training', 'evaluation']:
            raise Exception(
                f"No mode {mode} available, only 'training', 'evaluation'")

        filename_subject = self.metadata[f'subject_{mode}_pattern'](subject)

        if filename_subject not in self.metadata[f'subject_{mode}_files'].keys():
            raise Exception(f"Subject {subject} not in list of subjects.")

        fid, size = self.metadata[f'subject_{mode}_files'][filename_subject]

        self.subject = subject
        self.mode = mode

        self.runs = self.metadata[f'runs_{mode}'][subject - 1]
        # self.data = load_mat(self.path, filename_subject, fid)['eeg'][0][0]
        return load_mat(self.path, filename_subject, fid, size)

    # ----------------------------------------------------------------------
    @abstractmethod
    def get_run(self, run: int, classes: Union[int, str], channels=Union[int, str]) -> np.ndarray:
        """"""
        if run > self.runs:
            raise Exception(f'The current user only have {self.runs} runs.')

        if isinstance(channels, (list, tuple)) and -1 in channels:
            raise Exception('The channels are 1-based arrays')

        if isinstance(classes, (list, tuple)) and np.max(classes) >= len(self.metadata['classes']):
            raise Exception(
                f"The class index {np.max(classes)} is out of range.")

    # ----------------------------------------------------------------------
    def get_data(self, classes: Optional[list] = ALL, channels: Optional[list] = ALL):
        """Return all runs."""
        r, c = self.get_run(0, classes=classes, channels=channels)
        for run in range(1, self.runs):
            r_, c_ = self.get_run(run, classes=classes, channels=channels)
            r = np.concatenate([r, r_], axis=0)
            c = np.concatenate([c, c_])

        return r, c

    # ----------------------------------------------------------------------
    def format_channels_selectors(self, channels=None):
        """Generate the channels vector.

        If no selector then all channels will be used, the channels cant be
        indicated with the name or the index. If index is used this must be
        1-based array.
        """

        if channels != ALL:
            channels = [self.metadata['channel_names'].index(
                ch) if isinstance(ch, str) else (ch - 1) for ch in channels]
        else:
            channels = list(range(len(self.metadata['channel_names'])))

        return channels

    # ----------------------------------------------------------------------
    def format_class_selector(self, classes):
        """"""
        if classes != ALL:
            classes = [self.metadata['classes'].index(
                cls) if isinstance(cls, str) else cls for cls in classes]
        else:
            classes = range(len(self.metadata['classes']))

        return classes

    # ----------------------------------------------------------------------
    def remove_artifacts(self):
        """"""

    # ----------------------------------------------------------------------
    def get_epochs(self, run=ALL, ** kwargs):
        """"""
        # Remove channels that not correspond with the montage
        montage = mne.channels.make_standard_montage(self.metadata['montage'])
        channels_names = set(self.metadata['channel_names']).intersection(
            set(montage.ch_names))
        channels_missings = set(self.metadata['channel_names']).difference(
            set(montage.ch_names))

        logging.warning(
            f"Missing {channels_missings} channels in {self.metadata['montage']} montage.\n"
            f"Missing channels will be removed from MNE Epochs")

        info = mne.create_info(
            list(channels_names), sfreq=self.metadata['sampling_rate'], ch_types="eeg")
        info.set_montage(self.metadata['montage'])

        if run != ALL:
            data, classes = self.get_run(
                run, channels=list(channels_names))
        else:
            data, classes = self.get_data(
                run, channels=list(channels_names))

        events = [[i, 1, cls] for i, cls in enumerate(classes)]
        event_id = {e: i for i, e in enumerate(self.metadata['classes'])}

        return mne.EpochsArray(data, info, events=events, tmin=self.metadata['tmin'], event_id=event_id, **kwargs)

