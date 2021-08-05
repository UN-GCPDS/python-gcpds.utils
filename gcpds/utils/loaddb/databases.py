import json
import os

fids = json.load(
    open(os.path.join(os.path.dirname(__file__), 'fids.json'), 'rb'))


giga_mi_me = {
    'channels': ['Fp1', 'AF7', 'AF3', 'F1', 'F3', 'F5', 'F7', 'FT7', 'FC5', 'FC3', 'FC1', 'C1', 'C3', 'C5', 'T7', 'TP7', 'CP5', 'CP3', 'CP1', 'P1', 'P3', 'P5', 'P7', 'P9', 'PO7', 'PO3', 'O1', 'Iz', 'Oz', 'POz', 'Pz', 'CPz', 'Fpz', 'Fp2', 'AF8', 'AF4', 'AFz', 'Fz', 'F2', 'F4', 'F6', 'F8', 'FT8', 'FC6', 'FC4', 'FC2', 'FCz', 'Cz', 'C2', 'C4', 'C6', 'T8', 'TP8', 'CP6', 'CP4', 'CP2', 'P2', 'P4', 'P6', 'P8', 'P10', 'PO8', 'PO4', 'O2'],
    'classes': ['left hand mi', 'right hand mi', 'left hand mm', 'right hand mm'],
    'non_task_classes': ['resting', 'eye_blinking', 'eye_up_down', 'eye_left_right', 'jaw_clenching', 'head_left_right'],
    'sampling_rate': 512,
    'montage': 'standard_1005',
    'tmin': -2,
    'duration': 7,
    'reference': '',
    'subjects': 52,
    'runs_training': [5, 5, 5, 5, 5, 5, 6, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5],

    'subject_training_files': fids['GIGA training'],
    'subject_training_pattern': lambda subject: f's{str(subject).rjust(2, "0")}.mat',

    'subject_evaluation_files': {},
    'subject_evaluation_pattern': lambda subject: f's{str(subject).rjust(2, "0")}.mat',

    'metadata': fids['GIGA metadata'],
    'directory': 'databases/GIGA-MI_ME',
}


bci_civ_2a = {
    'channels': ['Fz', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'P1', 'Pz', 'P2', 'POz', 'EOG1', 'EOG2', 'EOG3'],
    'classes': ['left hand', 'right hand', 'feet', 'tongue'],
    'sampling_rate': 250,
    'montage': 'standard_1020',
    'tmin': -2,
    'duration': 7,
    'reference': '',
    'subjects': 9,
    'runs_training': [6, 6, 6, 6, 6, 6, 6, 6, 6],
    'runs_evaluation': [6, 6, 6, 6, 6, 6, 6, 6, 6],

    'subject_training_files': fids['BCI2a training'],
    'subject_training_pattern': lambda subject: f'A{str(subject).rjust(2, "0")}T.mat',

    'subject_evaluation_files': fids['BCI2a evaluation'],
    'subject_evaluation_pattern': lambda subject: f'A{str(subject).rjust(2, "0")}E.mat',

    'metadata': fids['BCI2a metadata'],
    'directory': 'databases/BCI_Competition_IV/dataset_2a',
}


highgamma_me = {
    'channels': ['Fp1', 'Fp2', 'Fpz', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6', 'M1', 'T7', 'C3', 'Cz', 'C4', 'T8', 'M2', 'CP5', 'CP1', 'CP2', 'CP6', 'P7', 'P3', 'Pz', 'P4', 'P8', 'POz', 'O1', 'Oz', 'O2', 'EOGh', 'EOGv', 'EMG_RH', 'EMG_LH', 'EMG_RF', 'AF7', 'AF3', 'AF4', 'AF8', 'F5', 'F1', 'F2', 'F6', 'FC3', 'FCz', 'FC4', 'C5', 'C1', 'C2', 'C6', 'CP3', 'CPz', 'CP4', 'P5', 'P1', 'P2', 'P6', 'PO5', 'PO3', 'PO4', 'PO6', 'FT7', 'FT8', 'TP7', 'TP8', 'PO7', 'PO8', 'FT9', 'FT10', 'TPP9h', 'TPP10h', 'PO9', 'PO10', 'P9', 'P10', 'AFF1', 'AFz', 'AFF2', 'FFC5h', 'FFC3h', 'FFC4h', 'FFC6h', 'FCC5h', 'FCC3h', 'FCC4h', 'FCC6h', 'CCP5h', 'CCP3h', 'CCP4h', 'CCP6h', 'CPP5h', 'CPP3h', 'CPP4h', 'CPP6h', 'PPO1', 'PPO2', 'I1', 'Iz', 'I2', 'AFp3h', 'AFp4h', 'AFF5h', 'AFF6h', 'FFT7h', 'FFC1h', 'FFC2h', 'FFT8h', 'FTT9h', 'FTT7h', 'FCC1h', 'FCC2h', 'FTT8h', 'FTT10h', 'TTP7h', 'CCP1h', 'CCP2h', 'TTP8h', 'TPP7h', 'CPP1h', 'CPP2h', 'TPP8h', 'PPO9h', 'PPO5h', 'PPO6h', 'PPO10h', 'POO9h', 'POO3h', 'POO4h', 'POO10h', 'OI1h', 'OI2h'],
    'classes': ['right hand', 'left hand', 'rest', 'feet'],
    'sampling_rate': 500,
    'montage': 'standard_1005',
    'tmin': 0,
    'duration': 4,
    'reference': '',
    'subjects': 14,
    'runs_training': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'runs_evaluation': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

    'subject_training_files': fids['HighGamma training'],
    'subject_training_pattern': lambda subject: os.path.join('train', f'{subject}.mat'),

    'subject_evaluation_files': fids['HighGamma evaluation'],
    'subject_evaluation_pattern': lambda subject: os.path.join('test', f'{subject}.mat'),

    'metadata': fids['HighGamma metadata'],
    'directory': 'databases/HighGamma-ME',
}


giga_bci_mi = {
    'channels': ['Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6', 'T7', 'C3', 'Cz', 'C4', 'T8', 'TP9', 'CP5', 'CP1', 'CP2', 'CP6', 'TP10', 'P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10', 'FC3', 'FC4', 'C5', 'C1', 'C2', 'C6', 'CP3', 'CPz', 'CP4', 'P1', 'P2', 'POz', 'FT9', 'FTT9h', 'TTP7h', 'TP7', 'TPP9h', 'FT10', 'FTT10h', 'TPP8h', 'TP8', 'TPP10h', 'F9', 'F10', 'AF7', 'AF3', 'AF4', 'AF8', 'PO3', 'PO4'],
    'classes': ['right', 'left'],
    'non_task_classes': ['pre task', 'post task', 'eyemovement_blinking', 'eyemovement_horizen', 'eyemovement_vertical', 'teeth', 'EMG_bothHandGrasping'],
    'sampling_rate': 1000,
    'montage': 'standard_1020',
    'tmin': -3,
    'duration': 7,
    'reference': '',
    'subjects': 54,
    'runs_training': [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    'runs': [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],

    # 'subject_files': list(filter(lambda f: 'MI' in f, fids['BCIilliteracy'])),
    'subject_files': {key: fids['BCIilliteracy'][key] for key in fids['BCIilliteracy'] if ('MI' in key or 'Artifact' in key)},
    'subject_pattern': lambda subject, run: os.path.join(f'session{run}', f'sess{str(run).rjust(2, "0")}_subj{str(subject).rjust(2, "0")}_EEG_MI.mat'),
    'artifact_pattern': lambda subject, run: os.path.join(f'session{run}', f'sess{str(run).rjust(2, "0")}_subj{str(subject).rjust(2, "0")}_EEG_Artifact.mat'),

    'metadata': fids['BCIilliteracy metadata'],
    'directory': 'databases/GIGA-BCI',

}


giga_bci_erp = giga_bci_mi.copy()
giga_bci_erp.update({
    'classes': ['target', 'nontarget'],
    'tmin': -4.5,
    'duration': 14.5,
    # 'subject_files': list(filter(lambda f: 'ERP' in f, fids['BCIilliteracy'])),
    'subject_files': {key: fids['BCIilliteracy'][key] for key in fids['BCIilliteracy'] if ('ERP' in key or 'Artifact' in key)},
    'subject_pattern': lambda subject, run: os.path.join(f'session{run}', f'sess{str(run).rjust(2, "0")}_subj{str(subject).rjust(2, "0")}_EEG_ERP.mat'),
})


giga_bci_ssvep = giga_bci_mi.copy()
giga_bci_ssvep.update({
    'classes': ['up', 'left', 'right', 'down'],
    'tmin': -4,
    'duration': 8,
    # 'subject_files': list(filter(lambda f: 'SSVEP' in f, fids['BCIilliteracy'])),
    'subject_files': {key: fids['BCIilliteracy'][key] for key in fids['BCIilliteracy'] if ('SSVEP' in key or 'Artifact' in key)},
    'subject_pattern': lambda subject, run: os.path.join(f'session{run}', f'sess{str(run).rjust(2, "0")}_subj{str(subject).rjust(2, "0")}_EEG_SSVEP.mat'),
})


physionet_mi_me = {
    'channels': ['Fc5', 'Fc3', 'Fc1', 'Fcz', 'Fc2', 'Fc4', 'Fc6', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6', 'Cp5', 'Cp3', 'Cp1', 'Cpz', 'Cp2', 'Cp4', 'Cp6', 'Fp1', 'Fpz', 'Fp2', 'Af7', 'Af3', 'Afz', 'Af4', 'Af8', 'F7', 'F5', 'F3', 'F1', 'Fz', 'F2', 'F4', 'F6', 'F8', 'Ft7', 'Ft8', 'T7', 'T8', 'T9', 'T10', 'Tp7', 'Tp8', 'P7', 'P5', 'P3', 'P1', 'Pz', 'P2', 'P4', 'P6', 'P8', 'Po7', 'Po3', 'Poz', 'Po4', 'Po8', 'O1', 'Oz', 'O2', 'Iz'],
    'classes': ['right fist mi', 'left fist mi', 'both fist mi', 'both feet mi', 'right fist mm', 'left fist mm', 'both fist mm', 'both feet mm'],
    'sampling_rate': 160,
    'montage': 'standard_1005',
    'tmin': -4,
    'duration': 8,
    'reference': '',
    'subjects': 109,
    'runs': [3] * 109,

    'subject_files': fids['PhysionetMMI training'],
    'subject_pattern': lambda subject, run: os.path.join(f'S{str(subject).rjust(3, "0")}', f'S{str(subject).rjust(3, "0")}R{str(run).rjust(2, "0")}.edf'),

    'metadata': fids['PhysionetMMI metadata'],
    'directory': 'databases/PhysioNet-MI_ME',

}

auditory_processing = {
    'channels': ['Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'T3', 'C3', 'Cz', 'C4', 'T4', 'T5', 'P3', 'Pz', 'P4', 'T6', 'O1', 'O2'],
    'classes': ['noise-50', 'noise-100', 'noise-150', 'noise-200', 'music-50', 'music-100', 'music-150', 'music-200'],
    'non_task_classes': ['resting'],
    'sampling_rate': 1000,
    'montage': 'standard_1020',
    'tmin': 0,
    'duration': 9.5,
    'reference': '',
    'subjects': 21,
    'runs_training': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

    'subject_training_files': fids['AuditoryProcessing training'],
    'subject_training_pattern': lambda subject: f'P{subject}_BCMI_frontHN_2017.mat',

    'metadata': fids['AuditoryProcessing metadata'],
    'directory': 'databases/Auditory_processing',
}
