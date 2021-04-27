
from .base import Database, GIGA_BCI, PhysioNet, ALL
from typing import Optional, Tuple
import numpy as np
from . import databases
import warnings
import logging


# ----------------------------------------------------------------------
def deprecated(replace):
    def wrap(fn):
        def wrap2(cls, *args, **kwargs):
            logging.warning(
                f"The '{fn}' have been deprecated, please use '{replace}'")
            return fn(cls, *args, **kwargs)
        return wrap2
    return wrap


########################################################################
class GIGA_MI_ME(Database):
    """"""
    metadata = databases.giga

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int, mode: str = 'training') -> None:
        """"""
        data = super().load_subject(subject, mode)
        self.data = data['eeg'][0][0]

    # ----------------------------------------------------------------------
    def get_run(self, run: int, classes: list = ALL, channels: Optional[list] = ALL, reject_bad_trials: Optional[bool] = True) -> Tuple[np.ndarray, np.ndarray]:
        """"""
        classes = self.format_class_selector(classes)
        channels = self.format_channels_selectors(channels)
        # super().get_run(run, classes, channels, reject_bad_trials)

        if (0 in classes or 1 in classes) and (2 in classes or 3 in classes):
            raise Exception(
                '`get_run()` not support merged classes, use only `mm` or `mi`')

        if classes[0] in [2, 3]:  # mm
            if run > 0:
                raise Exception('There is only 1 run for motor movement.')
            reject_bad_trials = False
            COUNT = 6
            CUE = 5
            TRIAL = 3

        elif classes[0] in [0, 1]:  # mi
            super().get_run(run, classes, channels, reject_bad_trials)
            COUNT = 9
            CUE = 11
            TRIAL = 7

        BAD = 14
        # Index of starts of all cues
        all_cues = np.where(self.data[CUE][0] == 1)[0]

        # Split in runs and select the specified run
        trials_count = self.data[COUNT][0][0]
        cues = np.array([all_cues[i:i + 20]
                         for i in range(0, trials_count, 20)][run])

        start = (self.metadata['sampling_rate'] * 2) - 1
        end = int(self.metadata['sampling_rate']
                  * (self.metadata['duration']+self.metadata['tmin'])) + 1

        # reject bad trial
        if reject_bad_trials:
            bad_trials = {}
            for cls in classes:
                trials_runs = np.ones((trials_count,), dtype=bool)
                # 14 bad trials--bad trials MI
                tmp = self.data[BAD][0][0][1][0][cls]
                if len(tmp) != 0:
                    trials_runs[tmp - 1] = 0
                bad_trials[cls] = [trials_runs[i:i + 20]
                                   for i in range(0, trials_count, 20)]
        #
        trials = []
        classes_out = []
        for cls in classes:

            if cls > 1:
                # classes starts in index 7 for mm
                data = self.data[TRIAL + cls - 2]
            else:
                # classes starts in index 3 for mi
                data = self.data[TRIAL + cls]

            if reject_bad_trials:
                # cls*max_runs -- run-1
                # x = bad_trials[(cls * self.runs) + run]
                x = bad_trials[cls][run]
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
        run = run[:, channels - 1, :]

        return run, np.array(classes_out)

    # ----------------------------------------------------------------------
    def get_data(self, classes: Optional[list] = ALL, channels: Optional[list] = ALL, reject_bad_trials: Optional[bool] = True, keep_runs_separated: bool = False) -> list:
        """Return all runs."""
        classes = self.format_class_selector(classes)

        runs_copy = self.runs
        runs = []
        classes_out = []

        for cls in classes:
            if cls in [2, 3]:  # mm
                self.runs = 1
                r, c = super().get_data([cls], channels, reject_bad_trials)
            elif cls in [0, 1]:  # mi
                self.runs = runs_copy
                r, c = super().get_data([cls], channels, reject_bad_trials)

            runs.append(r)
            classes_out.append(c)

        self.runs = runs_copy

        if keep_runs_separated:
            return list(zip(runs, classes_out))

        else:
            return np.concatenate(runs), np.concatenate(classes_out)

    # ----------------------------------------------------------------------
    @deprecated('non_task')
    def resting(self, channels: Optional[list] = ALL) -> np.ndarray:
        """"""
        channels = self.format_channels_selectors(channels)
        resting = self.data[1]
        resting = np.array([resting[channels - 1]])
        return resting

    # ----------------------------------------------------------------------
    def non_task(self, non_task_classes: Optional[list] = ALL, runs: Optional = None, channels: Optional[list] = ALL) -> np.ndarray:
        """"""
        channels = self.format_channels_selectors(channels)
        non_task_classes = self.format_non_class_selector(non_task_classes)
        all_non_task = (self.data[1], *[_[0] for _ in self.data[0]])
        non_task = []
        for index in non_task_classes:
            non_task.append(all_non_task[index][channels - 1])
        return [non_task]


########################################################################
class BCI_CIV_2a(Database):
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

        # # A04T contains only the eye movement condition
        if self.subject == 4 and self.mode == 'training':
            run = run - 2

        artifacts = self.data[3 + run][0][0][5].T[0] == 1
        classes_list = np.array([i[0] for i in self.data[3 + run][0][0][2]])
        starts = [s[0] for s in self.data[3 + run][0][0][1]]
        end = int(self.metadata['sampling_rate'] * self.metadata['duration'])

        run = np.array([self.data[3 + run][0][0][0][start:start + end]
                        for start in starts])

        # Remove EOG
        run = run[:, :, : 22]

        # Select channels
        run = run[:, :, channels - 1]

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
class HighGamma_ME(Database):
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
            [getattr(self.data, f"ch{ch}") for ch in channels])

        run = np.array([data[:, start:start + end] for start in starts])

        idx = []
        c = []
        for cls in classes:
            idx.append(np.where(np.array(classes_list) == cls + 1)[0])
            c.append([cls] * len(idx[-1]))

        return run[np.concatenate(idx), :, :], np.concatenate(c)


########################################################################
class GIGA_BCI_MI(GIGA_BCI):
    """"""
    metadata = databases.bciilliteracy_mi

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int, mode: str = 'training') -> None:
        """"""
        data_, artifacts_ = super().load_subject(subject, mode)

        if mode == 'training':
            self.data_ = [d['EEG_MI_train'][0][0] for d in data_]
        elif mode == 'evaluation':
            self.data_ = [d['EEG_MI_test'][0][0] for d in data_]

        self.artifacts_ = [a['EEG_Artifact'][0][0][0] for a in artifacts_]


########################################################################
class GIGA_BCI_ERP(GIGA_BCI):
    """"""
    metadata = databases.bciilliteracy_erp

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int, mode: str = 'training') -> None:
        """"""
        data_, artifacts_ = super().load_subject(subject, mode)

        if mode == 'training':
            self.data_ = [d['EEG_ERP_train'][0][0] for d in data_]
        elif mode == 'evaluation':
            self.data_ = [d['EEG_ERP_test'][0][0] for d in data_]

        self.artifacts_ = [a['EEG_Artifact'][0][0][0] for a in artifacts_]


########################################################################
class GIGA_BCI_SSVEP(GIGA_BCI):
    """"""
    metadata = databases.bciilliteracy_ssvep

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int, mode: str = 'training') -> None:
        """"""
        data_, artifacts_ = super().load_subject(subject, mode)

        if mode == 'training':
            self.data_ = [d['EEG_SSVEP_train'][0][0] for d in data_]
        elif mode == 'evaluation':
            self.data_ = [d['EEG_SSVEP_test'][0][0] for d in data_]

        self.artifacts_ = [a['EEG_Artifact'][0][0][0] for a in artifacts_]


########################################################################
class PhysioNet_MI_ME(PhysioNet):
    """"""
    metadata = databases.physionet_mmi

    # ----------------------------------------------------------------------
    def __init__(self, path: Optional[str] = None) -> None:
        """Constructor"""
        self.path = path

        self.classes = {
            'right fist mi': ([4, 8, 12], 'T1'),
            'left fist mi': ([4, 8, 12], 'T2'),

            'both fist mi': ([6, 10, 14], 'T1'),
            'both feet mi': ([6, 10, 14], 'T2'),

            'right fist mm': ([3, 7, 11], 'T1'),
            'left fist mm': ([3, 7, 11], 'T2'),

            'both fist mm': ([5, 9, 13], 'T1'),
            'both feet mm': ([5, 9, 13], 'T2'),
        }

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int, mode: 'str' = 'training', classes: Optional[list] = ALL) -> None:
        """"""
        self.data_ = super().load_subject(subject, mode, classes)

    # ----------------------------------------------------------------------
    def get_run(self, run: int, classes: Optional[list] = ALL, channels: Optional[list] = ALL, reject_bad_trials: Optional[bool] = True) -> Tuple[np.ndarray, np.ndarray]:
        """"""
        classes = self.format_class_selector(classes)
        channels = self.format_channels_selectors(channels)
        super().get_run(run, classes, channels, reject_bad_trials)

        data = []
        classes_out = []

        for class_ in classes:
            # self.metadata['classes'][class_]
            runs, desc = self.classes[self.metadata['classes'][class_]]

            if self.data_[runs[run] - 1]:
                raw_data = self.data_[runs[run] - 1].get_data()
                eeg = np.array([raw_data[:, int((cl - 4) * 160):int((cl - 4) * 160) + (160 * 8)] for cl in self.data_[
                               runs[run] - 1].annotations.onset[self.data_[runs[run] - 1].annotations.description == desc]])
                data.append(eeg)
                classes_out.extend([class_] * eeg.shape[0])

        run = np.concatenate(data)

        return run[:, channels - 1, :], np.array(classes_out)


########################################################################
class GIGA(GIGA_MI_ME):
    def __init__(self, *args, **kwargs):
        logging.warning(
            "'GIGA()' class will be removed, use 'GIGA_BCI()' instead")
        super().__init__(*args, **kwargs)


########################################################################
class BCI2a(BCI_CIV_2a):
    def __init__(self, *args, **kwargs):
        logging.warning(
            "'BCI2a()' class will be removed, use 'BCI_CIV_2a()' instead")
        super().__init__(*args, **kwargs)


########################################################################
class PhysionetMMI(PhysioNet_MI_ME):
    def __init__(self, *args, **kwargs):
        logging.warning(
            "'PhysionetMMI()' class will be removed, use 'PhysioNet_MI_ME()' instead")
        super().__init__(*args, **kwargs)


########################################################################
class HighGamma(HighGamma_ME):
    def __init__(self, *args, **kwargs):
        logging.warning(
            "'HighGamma()' class will be removed, use 'HighGamma_MI()' instead")
        super().__init__(*args, **kwargs)


########################################################################
class HighGamma_MI(HighGamma_ME):
    def __init__(self, *args, **kwargs):
        logging.warning(
            "'HighGamma_MI()' class will be removed, use 'HighGamma_ME()' instead")
        super().__init__(*args, **kwargs)

