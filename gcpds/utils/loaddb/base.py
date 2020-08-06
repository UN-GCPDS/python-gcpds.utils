""""""

from .google_drive_downloader import GoogleDriveDownloader as gdd
from scipy.io import loadmat
import os
from abc import ABCMeta, abstractmethod
from typing import Union, Optional
import numpy as np
import json
import mne
import sys
import tables
import logging

ALL = 'all'


# ----------------------------------------------------------------------
def load_mat(path: str, mat: str, fid: str, overwrite: Optional[bool] = False) -> np.ndarray:
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
            return load_mat(path, mat, fid, overwrite=True)

    else:
        logging.warning('Database not found!')
        logging.warning('downloading...')

        os.makedirs(path, exist_ok=True)
        gdd.download_file_from_google_drive(file_id=fid,
                                            dest_path=filepath,
                                            unzip=False,
                                            overwrite=overwrite)
        return load_mat(path, mat, fid)


########################################################################
class Database(metaclass=ABCMeta):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, path: Optional[str] = '.') -> None:
        """Constructor"""
        self.path = path

    # ----------------------------------------------------------------------
    @abstractmethod
    def load_subject(self, subject: int) -> None:
        """"""
        filename_subject = self.metadata['subject_pattern'](subject)

        if filename_subject not in self.metadata['subject_files'].keys():
            logging.warning(f"Subject {subject} not in list of subjects.")
            sys.exit()

        fid = self.metadata['subject_files'][filename_subject]

        self.runs = self.metadata['runs'][subject]
        # self.data = load_mat(self.path, filename_subject, fid)['eeg'][0][0]
        return load_mat(self.path, filename_subject, fid)

    # ----------------------------------------------------------------------
    @abstractmethod
    def get_run(self, run: int, classes: Union[int, str], channels=Union[int, str]) -> np.ndarray:
        """"""
        if run > self.runs:
            logging.error(f'The current user only have {self.runs} runs.')
            sys.exit()

        if isinstance(channels, (list, tuple)) and -1 in channels:
            logging.warning('The channels are 1-based arrays')
            sys.exit()

        if isinstance(classes, (list, tuple)) and np.max(classes) >= len(self.metadata['classes']):
            logging.warning(
                f"The class index {np.max(classes)} is out of range.")
            sys.exit()

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
    def mne_epochs(self, run=ALL, **kwargs):
        """"""
        info = mne.create_info(
            self.metadata['channel_names'], sfreq=self.metadata['sampling_rate'], ch_types="eeg")
        info.set_montage(self.metadata['montage'])

        if run != ALL:
            data, classes = self.get_run(run)
        else:
            data, classes = self.get_data(run)

        events = [[i, 1, cls] for i, cls in enumerate(classes)]
        event_id = {e: i for i, e in enumerate(self.metadata['classes'])}

        return mne.EpochsArray(data, info, events=events, tmin=self.metadata['tmin'], event_id=event_id, **kwargs)
