Databases handler
=================

``gcpds.utils.loaddb`` contains a handler to load databases.

.. code:: ipython3

    from gcpds.utils import loaddb

To list the databases available

.. code:: ipython3

    loaddb.databases




.. parsed-literal::

    ['GIGA', 'BCI2a', 'GIGA_Laplacian']



For example if we want to use ``BCI2a``, we must instatiate
``loaddb.BCI2a`` with the folder path that contains the database as
argumment:

.. code:: ipython3

    db = loaddb.BCI2a('BCI2a_database')

There is some common information for the database.

.. code:: ipython3

    print(db.subjects_files)  # Filenames
    print(db.channels)        # Channels names
    print(db.fs)              # Sampling frequency
    print(db.classes)         # Classes labels


.. parsed-literal::

    ['A01T.mat', 'A01E.mat', 'A09E.mat', 'A02T.mat', 'A04T.mat', 'A03E.mat', 'A02E.mat', 'A04E.mat', 'A03T.mat', 'A05T.mat', 'A05E.mat', 'A07T.mat', 'A07E.mat', 'A06E.mat', 'A08T.mat', 'A06T.mat', 'A09T.mat', 'A08E.mat']
    ['Fz', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'P1', 'Pz', 'P2', 'POz']
    250
    ['left hand', 'right hand', 'feet', 'tongue']


The data by subject can be accessed with:

.. code:: ipython3

    db.load_subject(1)
    print(f'The subject 1 has {db.runs} runs')


.. parsed-literal::

    The subject 1 has 6 runs


If the database does not exist or is corrupted, it will be downloaded.

After load a subject and when available, the trials can be read by runs.

.. code:: ipython3

    # This will return all trials and all channels for run 0
    run, class_ = db.get_run(0)
    run.shape, class_.shape




.. parsed-literal::

    ((48, 22, 1750), (48,))



The run are sorted in ``trials x channels x time``

Is possible to filter the runs by ``channel`` and/or ``class``

.. code:: ipython3

    # This will return the first two classes (left hand, right hand) for the channels C3 and C4
    run, class_ = db.get_run(1, class_=[0, 1], channels=['C3', 'C4'])
    run.shape, class_.shape




.. parsed-literal::

    ((24, 2, 1750), (24,))



.. code:: ipython3

    run, class_ = db.get_all_runs(class_=[0, 1], channels=['C3', 'Cz', 'C4'])
    run.shape, class_.shape




.. parsed-literal::

    ((144, 3, 1750), (144,))



--------------

References
~~~~~~~~~~

-  Cho, H., Ahn, M., Ahn, S., Kwon, M., & Jun, S. C. (2017). EEG
   datasets for motor imagery brain–computer interface. GigaScience,
   6(7), gix034.
-  Brunner, C., Leeb, R., Müller-Putz, G., Schlögl, A., & Pfurtscheller,
   G. (2008). BCI Competition 2008–Graz data set A. Institute for
   Knowledge Discovery (Laboratory of Brain-Computer Interfaces), Graz
   University of Technology, 16.
