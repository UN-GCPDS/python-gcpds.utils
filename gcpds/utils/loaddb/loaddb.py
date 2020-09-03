
from .base import Database, BCIilliteracy, ALL
from typing import Optional, Tuple
import numpy as np
from . import databases
import warnings
import logging


########################################################################
class GIGA(Database):
    """"""
    metadata = databases.giga

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int, mode: str = 'training') -> None:
        """"""
        data = super().load_subject(subject, mode)
        self.data = data['eeg'][0][0]

    # ----------------------------------------------------------------------
    def get_run(self, run: int, classes: Optional[list] = ALL, channels: Optional[list] = ALL, reject_bad_trials: Optional[bool] = True) -> Tuple[np.ndarray, np.ndarray]:
        """"""
        classes = self.format_class_selector(classes)
        channels = self.format_channels_selectors(channels)
        super().get_run(run, classes, channels, reject_bad_trials)

        # Index of starts of all cues
        all_cues = np.where(self.data[11][0] == 1)[0]

        # Split in runs and select the specified run
        trials_count = self.data[9][0][0]
        cues = np.array([all_cues[i:i + 20]
                         for i in range(0, trials_count, 20)][run])

        start = (self.metadata['sampling_rate'] * 2) - 1
        end = int(self.metadata['sampling_rate']
                  * self.metadata['duration']) + 1

        # reject bad trial
        if reject_bad_trials:
            bad_trials = []
            for cls in classes:
                trials_runs = np.ones((trials_count,), dtype=bool)
                # 14 bad trials--bad trials MI
                tmp = self.data[14][0][0][1][0][cls]
                if len(tmp) != 0:
                    trials_runs[tmp - 1] = 0
                bad_trials.extend([trials_runs[i:i + 20]
                                   for i in range(0, trials_count, 20)])
        #
        trials = []
        classes_out = []
        for cls in classes:
            data = self.data[7 + cls]  # classes starts in index 7
            if reject_bad_trials:
                # cls*max_runs -- run-1
                x = bad_trials[(cls * self.runs) + run]
                cues_r = cues[x]
                if len(cues_r):
                    trials.extend([data[:, cue - start:cue + end]
                                   for cue in cues_r])
                    classes_out.extend([cls] * len(cues_r))
            else:
                trials.extend([data[:, cue - start:cue + end] for cue in cues])
                classes_out.extend([cls] * len(cues))

        if not len(trials):
            logging.warning(
                f'The subject {self.subject} in the run {run} has no data.')
            return None, None

        # Select only EEG channels
        run = np.array(trials)[:, :len(self.metadata['channel_names']), :]

        # Select channels
        run = run[:, channels, :]

        return run, np.array(classes_out)

    # # ----------------------------------------------------------------------
    # def resting(self, channels: Optional[list] = ALL) -> np.ndarray:
        # """"""
        # channels = self.format_channels_selectors(channels)
        # resting = self.data[1]
        # resting = resting[channels]
        # return resting


########################################################################
class BCI2a(Database):
    """"""
    metadata = databases.bci2a

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int, mode: str = 'training') -> None:
        """"""
        data = super().load_subject(subject, mode)
        self.data = data['data'][0]

    # ----------------------------------------------------------------------
    def get_run(self, run: int, classes: Optional[list] = ALL, channels: Optional[list] = ALL, reject_bad_trials: Optional[bool] = True) -> Tuple[np.ndarray, np.ndarray]:
        """"""
        classes = self.format_class_selector(classes)
        channels = self.format_channels_selectors(channels)
        super().get_run(run, classes, channels, reject_bad_trials)
        artifacts = self.data[3 + run][0][0][5].T[0] == 1

        # A04T contains only the eye movement condition
        if self.subject == 4 and self.mode == 'training':
            run = run - 2

        classes_list = np.array([i[0] for i in self.data[3 + run][0][0][2]])
        starts = [s[0] for s in self.data[3 + run][0][0][1]]
        end = int(self.metadata['sampling_rate'] * self.metadata['duration'])

        run = np.array([self.data[3 + run][0][0][0][start:start + end]
                        for start in starts])

        # Remove EOG
        run = run[:, :, :22]

        # Select channels
        run = run[:, :, channels]

        # trial x channel x time
        run = np.moveaxis(run, 2, 1)

        # reject bad trials
        if reject_bad_trials:
            run = run[~artifacts]
            classes_list = classes_list[~artifacts]

        idx = []
        c = []
        for cls in classes:
            idx.append(np.where(np.array(classes_list) == cls + 1)[0])
            c.append([cls] * len(idx[-1]))

        return run[np.concatenate(idx), :, :], np.concatenate(c)


########################################################################
class HighGamma(Database):
    """"""
    metadata = databases.highgamma

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int, mode: str = 'training') -> None:
        """"""
        data = super().load_subject(subject, mode)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.data = data.root
            # DataTypeWarning: Unsupported type for attribute 'MATLAB_fields' in node 'mrk'
            self.data_mrk = data.root.mrk

    # ----------------------------------------------------------------------
    def get_run(self, run: int, classes: Optional[list] = ALL, channels: Optional[list] = ALL, reject_bad_trials: Optional[bool] = True) -> Tuple[np.ndarray, np.ndarray]:
        """"""
        classes = self.format_class_selector(classes)
        channels = self.format_channels_selectors(channels)
        super().get_run(run, classes, channels, reject_bad_trials)

        classes_list = self.data_mrk.event.desc.read()[0]
        starts = ((self.data_mrk.time.read() / 1000) * 500).T[0].astype(int)
        end = int(self.metadata['sampling_rate'] * self.metadata['duration'])

        data = np.concatenate(
            [getattr(self.data, f"ch{ch+1}") for ch in channels])

        run = np.array([data[:, start:start + end] for start in starts])

        idx = []
        c = []
        for cls in classes:
            idx.append(np.where(np.array(classes_list) == cls + 1)[0])
            c.append([cls] * len(idx[-1]))

        return run[np.concatenate(idx), :, :], np.concatenate(c)


########################################################################
class BCIilliteracy_MI(BCIilliteracy):
    """"""
    metadata = databases.bciilliteracy_mi

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int, mode: str = 'training') -> None:
        """"""
        data_ = super().load_subject(subject, mode)

        if mode == 'training':
            self.data_ = [d['EEG_MI_train'][0][0] for d in data_]
        elif mode == 'evaluation':
            self.data_ = [d['EEG_MI_test'][0][0] for d in data_]


########################################################################
class BCIilliteracy_ERP(BCIilliteracy):
    """"""
    metadata = databases.bciilliteracy_erp

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int, mode: str = 'training') -> None:
        """"""
        data_ = super().load_subject(subject, mode)

        if mode == 'training':
            self.data_ = [d['EEG_ERP_train'][0][0] for d in data_]
        elif mode == 'evaluation':
            self.data_ = [d['EEG_ERP_test'][0][0] for d in data_]


########################################################################
class BCIilliteracy_SSVEP(BCIilliteracy):
    """"""
    metadata = databases.bciilliteracy_ssvep

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int, mode: str = 'training') -> None:
        """"""
        data_ = super().load_subject(subject, mode)

        if mode == 'training':
            self.data_ = [d['EEG_SSVEP_train'][0][0] for d in data_]
        elif mode == 'evaluation':
            self.data_ = [d['EEG_SSVEP_test'][0][0] for d in data_]
