Databases handler
=================

``gcpds.utils.loaddb`` contains a handler to load databases.

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

There is some common information for the database.

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

Is possible to select the runs by ``channel`` and/or ``class``

.. code:: ipython3

    # This will return the first two classes (left hand, right hand) for the channels C3 and C4
    run, class_ = db.get_run(1, classes=['left hand', 'right hand'], channels=['C3', 'C4'])
    run.shape, class_.shape




.. parsed-literal::

    ((24, 2, 1750), (24,))



The classes and the channels can be indexes instead of labels:

.. code:: ipython3

    run, class_ = db.get_data(classes=[1, 3], channels=[1, 5, 10])
    run.shape, class_.shape




.. parsed-literal::

    ((144, 3, 1750), (144,))



The channels indexes, by convention, are 1-based array.
