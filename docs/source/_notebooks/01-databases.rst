.. code:: ipython3

    import os

Databases handler
=================

With ``gcpds.utils.loaddb`` is possible load databases, select classes
and electrodes, remove artifacts and create epochs for MNE tools.

.. code:: ipython3

    from gcpds.utils import loaddb

To list the databases available

.. code:: ipython3

    loaddb.available_databases




.. parsed-literal::

    ['GIGA', 'BCI2a', 'HighGamma']



For example if we want to use ``BCI2a``, we must instatiate
``loaddb.BCI2a`` with the folder path that contains the database as
argumment:

.. code:: ipython3

    db = loaddb.BCI2a('BCI2a_database')

There is some base information for the database in the object
``metadata``

.. code:: ipython3

    print(db.metadata['channel_names'])
    print(db.metadata['classes'])
    print(db.metadata['montage'])
    print(db.metadata['sampling_rate'])


.. parsed-literal::

    ['Fz', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'P1', 'Pz', 'P2', 'POz']
    ['left hand', 'right hand', 'feet', 'tongue']
    standard_1020
    250


Load Subject
------------

The data by subject can be accessed with the method ``load_subject``,
the ``training`` (default) or ``evaluation`` dataset can be selected
with the argument ``mode``.

.. code:: ipython3

    db.load_subject(1, mode='training')  # training dataset
    db.load_subject(1, mode='evaluation')  # evaluation dataset
    
    print(f'The subject 1 has {db.runs} runs')


.. parsed-literal::

    The subject 1 has 6 runs


NOTE: If the database does not exist or is corrupted, it will be
downloaded; Not all databases have an ``evaluation`` dataset.

Load runs
---------

After load a subject and when available, the trials can be read by runs.

.. code:: ipython3

    # This will return all trials and all channels for run 0
    run, class_ = db.get_run(0)
    run.shape, class_.shape




.. parsed-literal::

    ((48, 22, 1750), (48,))



Is possible to get all data for all available runs with ``get_data``:

.. code:: ipython3

    data, _ = db.get_data()
    data.shape




.. parsed-literal::

    (288, 22, 1750)



The EEG data are sorted in ``trials x channels x time``.

Select classes and channels
---------------------------

Is possible to select the runs by ``channel`` and/or ``class``

.. code:: ipython3

    # This will return the first two classes (left hand, right hand) for the channels C3 and C4
    run, class_ = db.get_run(1, classes=['left hand', 'right hand'], channels=['C3', 'C4'])
    run.shape, class_.shape




.. parsed-literal::

    ((24, 2, 1750), (24,))



The classes and the channels can be indexes instead of labels:

The channels indexes, by convention, are 1-based array.

.. code:: ipython3

    run, class_ = db.get_data(classes=[1, 3], channels=[1, 5, 10])
    run.shape, class_.shape




.. parsed-literal::

    ((144, 3, 1750), (144,))



Reject bad trials
-----------------

The argument ``reject_bad_trials`` is ``True`` by default and remove all
**documented** bad trials, this means that no algorithms are implemented
here, only the database owners recommendations.

.. code:: ipython3

    db = loaddb.GIGA('GIGA')
    db.load_subject(6)
    
    trials_cln, _ = db.get_data(reject_bad_trials=True)
    trials_raw, _ = db.get_data(reject_bad_trials=False)
    
    print(f"Cleaned trials shape:\t{trials_cln.shape}")
    print(f"Raw trials shape:\t\t{trials_raw.shape}")


.. parsed-literal::

    Cleaned trials shape:	(178, 64, 3584)
    Raw trials shape:		(200, 64, 3584)


This argument is avalibale to for ``get_run`` methods:

.. code:: ipython3

    trials_cln, _ = db.get_run(0, reject_bad_trials=True)
    trials_raw, _ = db.get_run(0, reject_bad_trials=False)
    
    print(f"Cleaned trials shape:\t{trials_cln.shape}")
    print(f"Raw trials shape:\t\t{trials_raw.shape}")


.. parsed-literal::

    Cleaned trials shape:	(36, 64, 3584)
    Raw trials shape:		(40, 64, 3584)


Download metadata
-----------------

Some databases has associated information like: papers, readme,
contents; this metadata can be downloaded with the method
``get_metadata()``, this will create a new folder called metadata.

.. code:: ipython3

    db = loaddb.GIGA('GIGA')
    db.get_metadata()
    
    os.listdir(os.path.join('GIGA', 'metadata'))


.. parsed-literal::

    Downloading 1-59y5Q9Nt6L8dq_QMsYhlSfLV36_KLuN into GIGA/metadata/cho2017.pdf... 



.. parsed-literal::

    HBox(children=(FloatProgress(value=0.0, description='GIGA/metadata/cho2017.pdf', max=51.470489501953125, style…


.. parsed-literal::

    
    Done.
    Downloading 12qRbFvF21OOOJZ_vrhRGWa2ykli2vpIs into GIGA/metadata/Questionnaire_results_of_52_subjects.xlsx... 



.. parsed-literal::

    HBox(children=(FloatProgress(value=0.0, description='GIGA/metadata/Questionnaire_results_of_52_subjects.xlsx',…


.. parsed-literal::

    
    Done.
    Downloading 12tko40nhuE2kFgFvJjanv_qE3FmH4wtJ into GIGA/metadata/readme.txt... 



.. parsed-literal::

    HBox(children=(FloatProgress(value=0.0, description='GIGA/metadata/readme.txt', max=0.068267822265625, style=P…


.. parsed-literal::

    
    Done.
    Downloading 12ums2JR9Wr_PaI9t46sJrubMo82Uzigi into GIGA/metadata/trial_sequence.zip... 



.. parsed-literal::

    HBox(children=(FloatProgress(value=0.0, description='GIGA/metadata/trial_sequence.zip', max=1.278961181640625,…


.. parsed-literal::

    
    Done.




.. parsed-literal::

    ['Questionnaire_results_of_52_subjects.xlsx',
     'cho2017.pdf',
     'readme.txt',
     'trial_sequence.zip']



--------------

References
~~~~~~~~~~

-  Cho, H., Ahn, M., & Ahn, S. (2017). Supporting data for “EEG datasets
   for motor imagery brain computer interface.”. GigaScience Database.
-  Brunner, C., Leeb, R., Müller-Putz, G., Schlögl, A., & Pfurtscheller,
   G. (2008). BCI Competition 2008–Graz data set A. Institute for
   Knowledge Discovery (Laboratory of Brain-Computer Interfaces), Graz
   University of Technology, 16.
-  Schirrmeister, R. T., Springenberg, J. T., Fiederer, L. D. J.,
   Glasstetter, M., Eggensperger, K., Tangermann, M., … & Ball, T.
   (2017). Deep learning with convolutional neural networks for EEG
   decoding and visualization. Human brain mapping, 38(11), 5391-5420.
