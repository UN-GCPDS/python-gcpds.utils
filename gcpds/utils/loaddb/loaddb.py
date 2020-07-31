"""
LoadDB
======



"""

from .google_drive_downloader import GoogleDriveDownloader as gdd
from typing import Optional, Tuple
from scipy.io import loadmat
import os
import numpy as np
import logging
import pickle
import mne
# import shutil

import logging
logging.basicConfig(level=logging.INFO)


FIDS = os.path.join(os.path.dirname(__file__), 'fids.pickle')
databases = [
    'GIGA',
    'BCI2a',
    'GIGA_Laplacian'
]


# ----------------------------------------------------------------------
def load_mat(dbname: str, path: str, mat: str, overwrite: Optional[bool] = False) -> np.ndarray:
    """Get the raw data for one individual file.

    If the file does not exist in the specified path then tries to download it
    from Google Drive.
    """

    filepath = os.path.join(path, mat)

    if os.path.exists(filepath) and not overwrite:
        try:
            return loadmat(filepath)
        except:
            logging.warning('Corrupt database!!\n, overwriting...')
            return load_mat(dbname, path, mat, overwrite=True)

    else:
        logging.warning('Database not found!')
        logging.warning('downloading...')

        fid = pickle.load(open(FIDS, 'rb'))[dbname][mat]

        os.makedirs(path, exist_ok=True)
        gdd.download_file_from_google_drive(file_id=fid,
                                            dest_path=filepath,
                                            unzip=False,
                                            overwrite=overwrite)
        return load_mat(dbname, path, mat)


########################################################################
class GIGA:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, path: Optional[str] = '.') -> None:
        """"""
        self.path = path
        self.channels = ['FP1', 'AF7', 'AF3', 'F1', 'F3', 'F5', 'F7', 'FT7', 'FC5', 'FC3', 'FC1', 'C1', 'C3', 'C5', 'T7', 'TP7', 'CP5', 'CP3', 'CP1', 'P1', 'P3', 'P5', 'P7', 'P9', 'PO7', 'PO3', 'O1', 'Iz', 'Oz', 'POz', 'Pz',
                         'CPz', 'Fpz', 'Fp2', 'AF8', 'AF4', 'AFz', 'Fz', 'F2', 'F4', 'F6', 'F8', 'FT8', 'FC6', 'FC4', 'FC2', 'FCz', 'Cz', 'C2', 'C4', 'C6', 'T8', 'TP8', 'CP6', 'CP4', 'CP2', 'P2', 'P4', 'P6', 'P8', 'P10', 'PO8', 'PO4', 'O2']
        self.classes = ['left hand', 'right hand']

        self.subjects = list(pickle.load(open(FIDS, 'rb'))['GIGA'].keys())
        # self.subjects_count = len(self.subjects)
        self.fs = 512

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int) -> None:
        """"""
        self.data = load_mat('GIGA', self.path,
                             f's{str(subject).rjust(2, "0")}.mat')['eeg'][0][0]

        # self.fs = self.data[2][0][0]
        self.runs = self.data[9][0][0] // 20

    # ----------------------------------------------------------------------:
    def get_run(self, run: int, class_: Optional[list] = None, channels: Optional[list] = 'All') -> Tuple[np.ndarray, np.ndarray]:
        """"""

        starts = np.where(self.data[11][0] == 1)[0]

        # data = []
        classes = []

        if class_ is None:
            class_ = range(len(self.classes))

        # for cls in class_:
            # classes.append([cls] * len(self.data[7 + cls]))

        trials = self.data[9][0][0]
        s = [starts[i:i + 20] for i in range(0, trials, 20)][run]

        trials = []
        for cls in class_:
            data = self.data[7 + cls]
            trials.append(
                [data[:, s_ - (self.fs * 2) + 1:s_ + (self.fs * 5) - 3] for s_ in s])

            classes.append([cls] * len(trials[-1]))

        # remove eog
        run = np.concatenate(trials)[:, :len(self.channels), :]

        if channels != 'All':
            run = run[:, [self.channels.index(ch) for ch in channels], :]

        # run = np.moveaxis(run, 1, 0)
        # run = run - run.mean(axis=2)[..., np.newaxis]

        return run, np.concatenate(classes)

    # ----------------------------------------------------------------------
    def get_all_runs(self, class_: Optional[int] = None, channels: Optional[list] = 'All') -> Tuple[np.ndarray, np.ndarray]:
        """"""
        r, c = self.get_run(0, class_=class_, channels=channels)
        for run in range(1, self.runs):
            r_, c_ = self.get_run(run, class_=class_, channels=channels)
            r = np.concatenate([r, r_], axis=0)
            c = np.concatenate([c, c_])

        return r, c

    # ----------------------------------------------------------------------
    def resting(self, channels: Optional[list] = 'All') -> np.ndarray:
        """"""
        rst = self.data[1]

        if channels != 'All':
            rst = rst[[self.channels.index(ch) for ch in channels]]

        return rst

    # ----------------------------------------------------------------------
    def mne_epochs(self, **kwargs):
        """"""
        info = mne.create_info(self.channels, sfreq=self.fs, ch_types="eeg")
        info.set_montage('standard_1020')

        data, classes = self.get_all_runs()

        events = [[i, 1, cls] for i, cls in enumerate(classes)]
        event_id = {e: i for i, e in enumerate(self.classes)}

        return mne.EpochsArray(data, info, events=events, tmin=-2,
                               event_id=event_id, **kwargs)


########################################################################
class BCI2a:

    # ----------------------------------------------------------------------
    def __init__(self, path: Optional[str] = '.') -> None:
        """"""
        self.path = path

        self.channels = ['Fz', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'C5', 'C3', 'C1', 'Cz',
                         'C2', 'C4', 'C6', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'P1', 'Pz', 'P2', 'POz']
        self.classes = ['left hand', 'right hand', 'feet', 'tongue']

        self.subjects = list(pickle.load(open(FIDS, 'rb'))['BCI2a'].keys())
        # self.subjects_count = len(self.subjects)
        self.fs = 250
        # self.montage = 'standard_1020'

        # self.info = mne.create_info(self.channels, sfreq=self.fs, ch_types="eeg")
        # self.info.set_montage(self.m)

    # ----------------------------------------------------------------------

    def load_subject(self, subject: int) -> None:
        """"""
        self.data = load_mat('BCI2a', self.path,
                             f'A{str(subject).rjust(2, "0")}T.mat')['data'][0]

        # self.fs = self.data[3][0][0][3][0][0]
        self.runs = 6

    # ----------------------------------------------------------------------
    # def get_run(self, run, /, eog=False, class_=None, channels='All'):
    def get_run(self, run: int, class_: Optional[list] = None, channels: Optional[list] = 'All') -> Tuple[np.ndarray, np.ndarray]:
        """"""
        # fs = self.data[3 + run][0][0][3][0][0]
        classes = [i[0] for i in self.data[3 + run][0][0][2]]
        starts = [s[0] for s in self.data[3 + run][0][0][1]]
        run = np.array([self.data[3 + run][0][0][0]
                        [start:start + (self.fs * 7)] for start in starts])

        # Remove eog
        run = run[:, :, :22]

        if channels != 'All':
            run = run[:, :, [self.channels.index(ch) for ch in channels]]

        run = np.moveaxis(run, 2, 1)
        # run = run - run.mean(axis=2)[..., np.newaxis]

        if class_ is None:
            class_ = range(len(self.classes))

        idx = []
        c = []
        for cls in class_:
            idx.append(np.where(np.array(classes) == cls + 1)[0])
            c.append([cls] * len(idx[-1]))

        return run[np.concatenate(idx), :, :], np.concatenate(c)

    # ----------------------------------------------------------------------
    def get_all_runs(self, class_: Optional[list] = None, channels: Optional[list] = 'All') -> Tuple[np.ndarray, np.ndarray]:
        """"""

        r, c = self.get_run(0, class_=class_, channels=channels)
        for run in range(1, self.runs):
            r_, c_ = self.get_run(
                run, class_=class_, channels=channels)
            r = np.concatenate([r, r_], axis=0)
            c = np.concatenate([c, c_])

        return r, c

    # ----------------------------------------------------------------------
    def mne_epochs(self, **kwargs):
        """"""
        info = mne.create_info(self.channels, sfreq=self.fs, ch_types="eeg")
        info.set_montage('standard_1020')

        data, classes = self.get_all_runs()

        events = [[i, 1, cls] for i, cls in enumerate(classes)]
        event_id = {e: i for i, e in enumerate(self.classes)}

        return mne.EpochsArray(data, info, events=events, tmin=-2,
                               event_id=event_id, **kwargs)


########################################################################
class GIGA_Laplacian:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, path: Optional[str] = '.') -> None:
        """"""
        self.path = path
        self.channels = ['Fp1', 'AF7', 'AF3', 'F1', 'F3', 'F5', 'F7', 'FT7', 'FC5', 'FC3', 'FC1', 'C1', 'C3', 'C5', 'T7', 'TP7', 'CP5', 'CP3', 'CP1', 'P1', 'P3', 'P5', 'P7', 'P9', 'PO7', 'PO3', 'O1', 'Iz', 'Oz', 'POz', 'Pz',
                         'CPz', 'FPz', 'FP2', 'AF8', 'AF4', 'AFz', 'Fz', 'F2', 'F4', 'F6', 'F8', 'FT8', 'FC6', 'FC4', 'FC2', 'FCz', 'Cz', 'C2', 'C4', 'C6', 'T8', 'TP8', 'CP6', 'CP4', 'CP2', 'P2', 'P4', 'P6', 'P8', 'P10', 'PO8', 'PO4', 'O2']
        self.classes = ['left hand', 'right hand']

        self.subjects = list(pickle.load(open(FIDS, 'rb'))
                             ['GIGA(laplacian)'].keys())
        # self.subjects_count = len(self.subjects)
        self.fs = 512

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int) -> None:
        """"""
        self.data = load_mat('GIGA(laplacian)', self.path,
                             f'Lp_sub_{subject}clas.mat')['Lap'][0]
        self.runs = None

    # ----------------------------------------------------------------------
    def get_all_runs(self, class_: Optional[list] = None, channels: Optional[list] = 'All') -> Tuple[np.ndarray, np.ndarray]:
        """"""
        if class_ is None:
            class_ = range(len(self.classes))

        run = []
        classes = []
        for cls in class_:
            run.append(self.data[cls])
            classes.append([cls] * run[-1].shape[0])

        # else:
            # run = self.data[class_]

        run = np.concatenate(run)

        if channels != 'All':
            run = run[:, [self.channels.index(ch) for ch in channels], :]

        # run = np.moveaxis(run, 1, 0)
        # run = run - run.mean(axis=2)[..., np.newaxis]

        run = run[:, :, 5:]

        return run, np.concatenate(classes)

    # ----------------------------------------------------------------------
    def mne_epochs(self, **kwargs):
        """"""
        info = mne.create_info(self.channels, sfreq=self.fs, ch_types="eeg")
        info.set_montage('standard_1020')

        data, classes = self.get_all_runs()

        events = [[i, 1, cls] for i, cls in enumerate(classes)]
        event_id = {e: i for i, e in enumerate(self.classes)}

        return mne.EpochsArray(data, info, events=events, tmin=-2,
                               event_id=event_id, **kwargs)
