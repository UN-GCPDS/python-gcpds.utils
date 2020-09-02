""""""

from .google_drive_downloader import GoogleDriveDownloader as gdd
from scipy.io import loadmat
import os
from abc import ABCMeta, abstractmethod
from typing import Union, Optional, Tuple
import numpy as np
import json
import mne
import tables
import logging
import warnings

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
            try:
                return tables.open_file(filepath, driver="H5FD_CORE")
            except tables.exceptions.HDF5ExtError:
                logging.warning('Corrupt database!!\n, overwriting...')
                return load_mat(path, mat, fid, size, overwrite=True)

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


# ----------------------------------------------------------------------
def download_metadata(path, metadata):
    """"""
    os.makedirs(path, exist_ok=True)
    for file in metadata:
        fid, size = metadata[file]
        gdd.download_file_from_google_drive(file_id=fid,
                                            dest_path=os.path.join(path, file),
                                            unzip=False,
                                            overwrite=True,
                                            size=size)


# # ----------------------------------------------------------------------
# def get_menmap_filename():
    # """"""
    # filename = ''.join([random.choice(string.ascii_lowercase)
                        # for i in range(16)])
    # return f'{filename}.menmap'


########################################################################
class Database(metaclass=ABCMeta):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, path: Optional[str] = '.') -> None:
        """Constructor"""
        self.path = path
        # self.usemenmap = usemenmap

    # ----------------------------------------------------------------------
    @abstractmethod
    def load_subject(self, subject: int, mode: str) -> None:
        """"""
        if not mode in ['training', 'evaluation']:
            raise Exception(
                f"No mode {mode} available, only 'training', 'evaluation'")

        filename_subject = self.metadata[f'subject_{mode}_pattern'](subject)

        if os.path.split(filename_subject)[-1] not in self.metadata[f'subject_{mode}_files'].keys():
            raise Exception(f"Subject {subject} not in list of subjects.")

        fid, size = self.metadata[f'subject_{mode}_files'][os.path.split(
            filename_subject)[-1]]

        self.subject = subject
        self.mode = mode

        self.runs = self.metadata[f'runs_{mode}'][subject - 1]
        # self.data = load_mat(self.path, filename_subject, fid)['eeg'][0][0]
        return load_mat(self.path, filename_subject, fid, size)

    # # ----------------------------------------------------------------------
    # def to_menmap(self, array):
        # """"""
        # array = np.array(array.tolist())

        # filename = os.path.join(self.path, get_menmap_filename())
        # fp = np.memmap(filename, dtype=array.dtype,
                       # mode='w+', shape=array.shape)
        # fp[:] = array[:]
        # del array, fp
        # mmap = np.memmap(filename, mode='r')
        # return mmap

    # ----------------------------------------------------------------------
    @abstractmethod
    def get_run(self, run: int, classes: Union[int, str], channels=Union[int, str], reject_bad_trials: Optional[bool] = True) -> np.ndarray:
        """"""
        if run > self.runs:
            raise Exception(f'The current user only have {self.runs} runs.')

        if isinstance(channels, (list, tuple)) and -1 in channels:
            raise Exception('The channels are 1-based arrays')

        if isinstance(classes, (list, tuple)) and np.max(classes) >= len(self.metadata['classes']):
            raise Exception(
                f"The class index {np.max(classes)} is out of range.")

    # ----------------------------------------------------------------------
    def get_data(self, classes: Optional[list] = ALL, channels: Optional[list] = ALL, reject_bad_trials: Optional[bool] = True):
        """Return all runs."""

        start = 0
        for _ in range(self.runs):
            r, c = self.get_run(start, classes=classes, channels=channels,
                                reject_bad_trials=reject_bad_trials)
            if not r is None:
                break
            else:
                start += 1

        for run in range(start + 1, self.runs):
            r_, c_ = self.get_run(
                run, classes=classes, channels=channels, reject_bad_trials=reject_bad_trials)
            if not r_ is None:
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
    def get_epochs(self, run=ALL, **kwargs):
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

    # ----------------------------------------------------------------------
    def get_metadata(self):
        """"""
        download_metadata(os.path.join(self.path, 'metadata'),
                          self.metadata['metadata'])


########################################################################
class BCIilliteracy(Database):
    """"""

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int, mode: str) -> None:
        """"""
        if not mode in ['training', 'evaluation']:
            raise Exception(
                f"No mode {mode} available, only 'training', 'evaluation'")

        self.runs = self.metadata[f'runs'][subject - 1]

        sessions = []
        for run in range(self.runs):
            filename_subject = self.metadata[f'subject_pattern'](
                subject, run + 1)

            if os.path.split(filename_subject)[-1] not in self.metadata[f'subject_files'].keys():
                raise Exception(f"Subject {subject} not in list of subjects.")

            fid, size = self.metadata[f'subject_files'][os.path.split(
                filename_subject)[-1]]

            self.subject = subject
            self.mode = mode

            sessions.append(load_mat(self.path, filename_subject, fid, size))

        return sessions

    # ----------------------------------------------------------------------
    def get_run(self, run: int, classes: Optional[list] = ALL, channels: Optional[list] = ALL, reject_bad_trials: Optional[bool] = True) -> Tuple[np.ndarray, np.ndarray]:
        """"""
        classes = self.format_class_selector(classes)
        channels = self.format_channels_selectors(channels)
        super().get_run(run, classes, channels, reject_bad_trials)

        data = self.data_[run]

        classes_list = data[4][0]
        starts = data[2][0]
        end = int(self.metadata['sampling_rate'] * self.metadata['duration'])

        run = np.array([data[1][start:start + end] for start in starts])

        # trial x channel x time
        run = np.moveaxis(run, 2, 1)

        # Select channels
        run = run[:, channels, :]

        idx = []
        c = []
        for cls in classes:
            idx.append(np.where(np.array(classes_list) == cls + 1)[0])
            c.append([cls] * len(idx[-1]))

        return run[np.concatenate(idx), :, :], np.concatenate(c)

