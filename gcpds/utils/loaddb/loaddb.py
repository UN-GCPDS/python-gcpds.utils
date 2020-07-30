from scipy.io import loadmat
import os
import numpy as np


########################################################################
class GIGA:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, path='.'):
        """"""

        self.path = path
        self.channels = ['FP1', 'AF7', 'AF3', 'F1', 'F3', 'F5', 'F7', 'FT7', 'FC5', 'FC3', 'FC1', 'C1', 'C3', 'C5', 'T7', 'TP7', 'CP5', 'CP3', 'CP1', 'P1', 'P3', 'P5', 'P7', 'P9', 'PO7', 'PO3', 'O1', 'Iz', 'Oz', 'POz', 'Pz',
                         'CPz', 'FPz', 'FP2', 'AF8', 'AF4', 'AFz', 'Fz', 'F2', 'F4', 'F6', 'F8', 'FT8', 'FC6', 'FC4', 'FC2', 'FCz', 'Cz', 'C2', 'C4', 'C6', 'T8', 'TP8', 'CP6', 'CP4', 'CP2', 'P2', 'P4', 'P6', 'P8', 'P10', 'PO8', 'PO4', 'O2']
        self.classes = ['left hand', 'right hand']
        self.subjects = 52

    # ----------------------------------------------------------------------
    def load_subject(self, subject):
        """"""
        self.data = loadmat(os.path.join(
            self.path, f's{str(subject).rjust(2, "0")}.mat'))['eeg'][0][0]

        self.fs = self.data[2][0][0]
        self.runs = self.data[9][0][0] // 20

    # ----------------------------------------------------------------------
    # def get_run(self, run, /, class_=None, channels='All'):
    def get_run(self, run, class_=None, channels='All'):
        """"""
        starts = np.where(self.data[11][0] == 1)[0]

        if class_ is None:
            data = np.concatenate([self.data[7], self.data[8]])
            classes = [0] * 20 + [1] * 20
        else:
            data = self.data[7 + class_]
            classes = [class_] * 20

        trials = self.data[9][0][0]
        s = [starts[i:i + 20] for i in range(0, trials, 20)][run]

        run = np.array(
            [data[:, s_ - (self.fs * 2) + 1:s_ + (self.fs * 5) - 3] for s_ in s])

        if channels != 'All':
            run = run[:, [self.channels.index(ch) for ch in channels], :]

        run = np.moveaxis(run, 1, 0)
        run = run - run.mean(axis=2)[..., np.newaxis]

        if class_ is None:
            return run, classes
        else:
            return run

    # ----------------------------------------------------------------------
    def get_all_runs(self, class_=None, channels='All'):
        """"""
        if class_ is None:
            r, c = self.get_run(0, class_=class_, channels=channels)
            for run in range(1, self.runs):
                r_, c_ = self.get_run(run, class_=class_, channels=channels)
                r = np.concatenate([r, r_], axis=1)
                c = np.concatenate([c, c_])

            return r, c

        else:
            r = self.get_run(0, class_=class_, channels=channels)
            for run in range(1, self.runs):
                r_ = self.get_run(run, class_=class_, channels=channels)
                r = np.concatenate([r, r_], axis=1)
            return r

    # ----------------------------------------------------------------------
    def resting(self, channels='All'):
        """"""
        rst = self.data[1]

        if channels != 'All':
            rst = rst[[self.channels.index(ch) for ch in channels]]

        return rst


########################################################################
class BCI2a:

    # ----------------------------------------------------------------------
    def __init__(self, path='.'):
        """"""
        self.path = path

        self.channels = ['Fz', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'C5', 'C3', 'C1', 'Cz',
                         'C2', 'C4', 'C6', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'P1', 'Pz', 'P2', 'POz']
        self.classes = ['left hand', 'right hand', 'feet', 'tongue']
        self.subjects = 9

    # ----------------------------------------------------------------------
    def load_subject(self, subject):
        """"""
        self.data = loadmat(os.path.join(
            self.path, f'A{str(subject).rjust(2, "0")}T.mat'))['data'][0]

        self.runs = 6
        self.fs = self.data[3][0][0][3][0][0]

    # ----------------------------------------------------------------------
    # def get_run(self, run, /, eog=False, class_=None, channels='All'):
    def get_run(self, run, eog=False, class_=None, channels='All'):
        """"""
        # fs = self.data[3 + run][0][0][3][0][0]
        classes = [i[0] for i in self.data[3 + run][0][0][2]]
        starts = [s[0] for s in self.data[3 + run][0][0][1]]
        run = np.array([self.data[3 + run][0][0][0]
                        [start:start + (self.fs * 7)] for start in starts])

        if not eog:
            run = run[:, :, :22]

        if channels != 'All':
            run = run[:, :, [self.channels.index(ch) for ch in channels]]

        run = np.moveaxis(run, 2, 0)
        run = run - run.mean(axis=2)[..., np.newaxis]

        if class_ is None:
            return run, np.array(classes)
        else:
            idx = np.where(np.array(classes) == class_ + 1)[0]
            return run[:, idx, :]

    # ----------------------------------------------------------------------
    def get_all_runs(self, eog=False, class_=None, channels='All'):
        """"""
        if class_ is None:
            r, c = self.get_run(0, eog=eog, class_=class_, channels=channels)
            for run in range(1, self.runs):
                r_, c_ = self.get_run(
                    run, eog=eog, class_=class_, channels=channels)
                r = np.concatenate([r, r_], axis=1)
                c = np.concatenate([c, c_])

            return r, c

        else:
            r = self.get_run(0, eog=eog, class_=class_, channels=channels)
            for run in range(1, self.runs):
                r_ = self.get_run(
                    run, eog=eog, class_=class_, channels=channels)
                r = np.concatenate([r, r_], axis=1)
            return r


########################################################################
class LaplaceGIGA:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, path='.'):
        """"""

        self.path = path
        self.channels = ['FP1', 'AF7', 'AF3', 'F1', 'F3', 'F5', 'F7', 'FT7', 'FC5', 'FC3', 'FC1', 'C1', 'C3', 'C5', 'T7', 'TP7', 'CP5', 'CP3', 'CP1', 'P1', 'P3', 'P5', 'P7', 'P9', 'PO7', 'PO3', 'O1', 'Iz', 'Oz', 'POz', 'Pz',
                         'CPz', 'FPz', 'FP2', 'AF8', 'AF4', 'AFz', 'Fz', 'F2', 'F4', 'F6', 'F8', 'FT8', 'FC6', 'FC4', 'FC2', 'FCz', 'Cz', 'C2', 'C4', 'C6', 'T8', 'TP8', 'CP6', 'CP4', 'CP2', 'P2', 'P4', 'P6', 'P8', 'P10', 'PO8', 'PO4', 'O2']
        self.classes = ['left hand', 'right hand']
        self.subjects = 52

    # ----------------------------------------------------------------------
    def load_subject(self, subject):
        """"""
        self.data = loadmat(os.path.join(
            self.path, f'Lp_sub_{subject}clas.mat'))['Lap'][0]

        self.fs = 512

    # ----------------------------------------------------------------------
    def get_all_runs(self, class_=None, channels='All'):
        """"""
        if class_ is None:
            run = np.concatenate([self.data[0], self.data[1]])
        else:
            run = self.data[class_]


        if channels != 'All':
            run = run[:, [self.channels.index(ch) for ch in channels], :]
                  
        run = np.moveaxis(run, 1, 0)
        run = run - run.mean(axis=2)[..., np.newaxis]

        run = run[:,:,5:]

        if class_ is None:
           return run, [0]*len(self.data[0])+[1]*len(self.data[0])
        else:
            return run

    # ----------------------------------------------------------------------
    def resting(self, channels='All'):
        """"""
        rst = self.data[1]

        if channels != 'All':
            rst = rst[[self.channels.index(ch) for ch in channels]]

        return rst

# # db_bci2a = BCI2a()
# # db_bci2a.load_subject(1)


# # data = db_bci2a.get_run(0, class_=1, channels=['C3', 'C4'])
# # data.shape


# db_giga = GIGA()
# db_giga.load_subject(1)
# db_giga.runs

# data = db_giga.get_run(0, class_=0, channels=['C3', 'C4'])
# data.shape  # channels X trial X time
