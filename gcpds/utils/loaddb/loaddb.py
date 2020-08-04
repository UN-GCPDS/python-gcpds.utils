
from .base import Database, ALL
from typing import Optional, Tuple
import numpy as np
from . import databases


########################################################################
class GIGA(Database):
    """"""
    metadata = databases.giga

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int) -> None:
        """"""
        data = super().load_subject(subject)
        self.data = data['eeg'][0][0]

    # ----------------------------------------------------------------------
    def get_run(self, run: int, classes: Optional[list] = ALL, channels: Optional[list] = ALL) -> Tuple[np.ndarray, np.ndarray]:
        """"""
        super().get_run(run, classes, channels)
        classes, channels = self.format_selectors(classes, channels)

        # Index of starts of all cues
        all_cues = np.where(self.data[11][0] == 1)[0]

        # Split in runs and select the specified run
        trials_count = self.data[9][0][0]
        cues = [all_cues[i:i + 20] for i in range(0, trials_count, 20)][run]

        start = (self.metadata['sampling_rate'] * 2) - 1
        end = (self.metadata['sampling_rate'] * 5) + 1

        trials = []
        classes_out = []
        for cls in classes:
            data = self.data[7 + cls]  # classes starts in index 7
            trials.extend([data[:, cue - start:cue + end] for cue in cues])
            classes_out.extend([cls] * len(cues))

        # Select only EEG channels
        run = np.array(trials)[:, :len(self.metadata['channel_names']), :]

        # Select channels
        run = run[:, channels, :]

        return run, np.array(classes_out)


########################################################################
class BCI2a(Database):
    """"""
    metadata = databases.bci2a

    # ----------------------------------------------------------------------
    def load_subject(self, subject: int) -> None:
        """"""
        data = super().load_subject(subject)
        self.data = data['data'][0]

    # ----------------------------------------------------------------------
    def get_run(self, run: int, classes: Optional[list] = ALL, channels: Optional[list] = ALL) -> Tuple[np.ndarray, np.ndarray]:
        """"""
        super().get_run(run, classes, channels)
        classes, channels = self.format_selectors(classes, channels)

        classes_list = [i[0] for i in self.data[3 + run][0][0][2]]
        starts = [s[0] for s in self.data[3 + run][0][0][1]]
        run = np.array([self.data[3 + run][0][0][0][start:start +
                                                    (self.metadata['sampling_rate'] * 7)] for start in starts])

        # Remove EOG
        run = run[:, :, :22]

        # Select channels
        run = run[:, :, channels]

        run = np.moveaxis(run, 2, 1)

        idx = []
        c = []
        for cls in classes:
            idx.append(np.where(np.array(classes_list) == cls + 1)[0])
            c.append([cls] * len(idx[-1]))

        return run[np.concatenate(idx), :, :], np.concatenate(c)
