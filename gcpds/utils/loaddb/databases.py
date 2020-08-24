import json
import os

fids = json.load(
    open(os.path.join(os.path.dirname(__file__), 'fids.json'), 'rb'))


giga = {
    'channel_names': ['Fp1', 'AF7', 'AF3', 'F1', 'F3', 'F5', 'F7', 'FT7', 'FC5', 'FC3', 'FC1', 'C1', 'C3', 'C5', 'T7', 'TP7', 'CP5', 'CP3', 'CP1', 'P1', 'P3', 'P5', 'P7', 'P9', 'PO7', 'PO3', 'O1', 'Iz', 'Oz', 'POz', 'Pz', 'CPz', 'Fpz', 'Fp2', 'AF8', 'AF4', 'AFz', 'Fz', 'F2', 'F4', 'F6', 'F8', 'FT8', 'FC6', 'FC4', 'FC2', 'FCz', 'Cz', 'C2', 'C4', 'C6', 'T8', 'TP8', 'CP6', 'CP4', 'CP2', 'P2', 'P4', 'P6', 'P8', 'P10', 'PO8', 'PO4', 'O2'],
    'classes': ['left hand', 'right hand'],
    'sampling_rate': 512,
    'montage': 'standard_1005',
    'tmin': -2,
    'reference': '',
    'runs_training': [5, 5, 5, 5, 5, 5, 6, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5],
    'runs_evaluation': [],
    'artifacts': [],

    'subject_training_files': fids['GIGA training'],
    'subject_training_pattern': lambda subject: f's{str(subject).rjust(2, "0")}.mat',

    'subject_evaluation_files': {},
    'subject_evaluation_pattern': lambda subject: f'{subject}.mat',
}


bci2a = {
    'channel_names': ['Fz', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'P1', 'Pz', 'P2', 'POz'],
    'classes': ['left hand', 'right hand', 'feet', 'tongue'],
    'sampling_rate': 250,
    'montage': 'standard_1020',
    'tmin': -2,
    'reference': '',
    'runs_training': [6, 6, 6, 6, 6, 6, 6, 6, 6],
    'runs_evaluation': [6, 6, 6, 6, 6, 6, 6, 6, 6],
    'artifacts': [],

    'subject_training_files': fids['BCI2a training'],
    'subject_training_pattern': lambda subject: f'A{str(subject).rjust(2, "0")}T.mat',

    'subject_evaluation_files': fids['BCI2a evaluation'],
    'subject_evaluation_pattern': lambda subject: f'A{str(subject).rjust(2, "0")}E.mat',

}


highgamma = {
    'channel_names': ['Fp1', 'Fp2', 'Fpz', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6', 'M1', 'T7', 'C3', 'Cz', 'C4', 'T8', 'M2', 'CP5', 'CP1', 'CP2', 'CP6', 'P7', 'P3', 'Pz', 'P4', 'P8', 'POz', 'O1', 'Oz', 'O2', 'EOGh', 'EOGv', 'EMG_RH', 'EMG_LH', 'EMG_RF', 'AF7', 'AF3', 'AF4', 'AF8', 'F5', 'F1', 'F2', 'F6', 'FC3', 'FCz', 'FC4', 'C5', 'C1', 'C2', 'C6', 'CP3', 'CPz', 'CP4', 'P5', 'P1', 'P2', 'P6', 'PO5', 'PO3', 'PO4', 'PO6', 'FT7', 'FT8', 'TP7', 'TP8', 'PO7', 'PO8', 'FT9', 'FT10', 'TPP9h', 'TPP10h', 'PO9', 'PO10', 'P9', 'P10', 'AFF1', 'AFz', 'AFF2', 'FFC5h', 'FFC3h', 'FFC4h', 'FFC6h', 'FCC5h', 'FCC3h', 'FCC4h', 'FCC6h', 'CCP5h', 'CCP3h', 'CCP4h', 'CCP6h', 'CPP5h', 'CPP3h', 'CPP4h', 'CPP6h', 'PPO1', 'PPO2', 'I1', 'Iz', 'I2', 'AFp3h', 'AFp4h', 'AFF5h', 'AFF6h', 'FFT7h', 'FFC1h', 'FFC2h', 'FFT8h', 'FTT9h', 'FTT7h', 'FCC1h', 'FCC2h', 'FTT8h', 'FTT10h', 'TTP7h', 'CCP1h', 'CCP2h', 'TTP8h', 'TPP7h', 'CPP1h', 'CPP2h', 'TPP8h', 'PPO9h', 'PPO5h', 'PPO6h', 'PPO10h', 'POO9h', 'POO3h', 'POO4h', 'POO10h', 'OI1h', 'OI2h'],
    'classes': ['right hand', 'left hand', 'rest', 'feet'],
    'sampling_rate': 500,
    'montage': 'standard_1005',
    'tmin': 0,
    'reference': '',
    'runs_training': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'runs_evaluation': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'artifacts': [],

    'subject_training_files': fids['HighGamma training'],
    'subject_training_pattern': lambda subject: os.path.join('train', f'{subject}.mat'),

    'subject_evaluation_files': fids['HighGamma evaluation'],
    'subject_evaluation_pattern': lambda subject: os.path.join('test', f'{subject}.mat'),

}






