.. code:: ipython3

    %matplotlib inline

Plotting topographic maps of evoked data
========================================

Load evoked data and plot topomaps for selected time points using
multiple additional options.

.. code:: ipython3

    # Authors: Christian Brodbeck <christianbrodbeck@nyu.edu>
    #          Tal Linzen <linzen@nyu.edu>
    #          Denis A. Engeman <denis.engemann@gmail.com>
    #          Mikołaj Magnuski <mmagnuski@swps.edu.pl>
    #          Eric Larson <larson.eric.d@gmail.com>
    #
    # License: BSD (3-clause)
    
    import numpy as np
    import matplotlib.pyplot as plt
    
    from mne.datasets import sample
    from mne import read_evokeds
    
    print(__doc__)
    
    path = sample.data_path()
    fname = path + '/MEG/sample/sample_audvis-ave.fif'
    
    # load evoked corresponding to a specific condition
    # from the fif file and subtract baseline
    condition = 'Left Auditory'
    evoked = read_evokeds(fname, condition=condition, baseline=(None, 0))


.. parsed-literal::

    Automatically created module for IPython interactive environment
    Using default location ~/mne_data for sample...
    Creating ~/mne_data
    Downloading archive MNE-sample-data-processed.tar.gz to /home/yeison/mne_data
    Downloading https://files.osf.io/v1/resources/rxvq7/providers/osfstorage/59c0e26f9ad5a1025c4ab159?version=5&action=download&direct (1.54 GB)



.. parsed-literal::

    HBox(children=(FloatProgress(value=0.0, description='Downloading', max=1652769680.0, style=ProgressStyle(descr…


::


    ---------------------------------------------------------------------------

    KeyboardInterrupt                         Traceback (most recent call last)

    <ipython-input-1-fe6ea9120dc7> in <module>
         15 print(__doc__)
         16 
    ---> 17 path = sample.data_path()
         18 fname = path + '/MEG/sample/sample_audvis-ave.fif'
         19 


    <decorator-gen-407> in data_path(path, force_update, update_path, download, verbose)


    /usr/lib/python3.8/site-packages/mne/datasets/sample/sample.py in data_path(path, force_update, update_path, download, verbose)
         17 def data_path(path=None, force_update=False, update_path=True, download=True,
         18               verbose=None):  # noqa: D103
    ---> 19     return _data_path(path=path, force_update=force_update,
         20                       update_path=update_path, name='sample',
         21                       download=download)


    /usr/lib/python3.8/site-packages/mne/datasets/utils.py in _data_path(path, force_update, update_path, download, name, check_version, return_version, archive_name)
        393         full_name = list()
        394         for u, an, h, fo in zip(url, archive_name, hash_, folder_orig):
    --> 395             remove_archive, full = _download(path, u, an, h)
        396             full_name.append(full)
        397         del archive_name


    /usr/lib/python3.8/site-packages/mne/datasets/utils.py in _download(path, url, archive_name, hash_, hash_type)
        450         if fetch_archive:
        451             logger.info('Downloading archive %s to %s' % (archive_name, path))
    --> 452             _fetch_file(url, full_name, print_destination=False,
        453                         hash_=hash_, hash_type=hash_type)
        454     return remove_archive, full_name


    <decorator-gen-3> in _fetch_file(url, file_name, print_destination, resume, hash_, timeout, hash_type, verbose)


    /usr/lib/python3.8/site-packages/mne/utils/fetching.py in _fetch_file(url, file_name, print_destination, resume, hash_, timeout, hash_type, verbose)
        115         else:
        116             initial_size = 0
    --> 117         _get_http(url, temp_file_name, initial_size, timeout, verbose_bool)
        118 
        119         # check hash sum eg md5sum


    /usr/lib/python3.8/site-packages/mne/utils/fetching.py in _get_http(***failed resolving arguments***)
         56         while True:
         57             t0 = time.time()
    ---> 58             chunk = response.read(chunk_size)
         59             dt = time.time() - t0
         60             if dt < 0.01:


    /usr/lib/python3.8/http/client.py in read(self, amt)
        452             # Amount is given, implement using readinto
        453             b = bytearray(amt)
    --> 454             n = self.readinto(b)
        455             return memoryview(b)[:n].tobytes()
        456         else:


    /usr/lib/python3.8/http/client.py in readinto(self, b)
        496         # connection, and the user is reading more bytes than will be provided
        497         # (for example, reading in 1k chunks)
    --> 498         n = self.fp.readinto(b)
        499         if not n and b:
        500             # Ideally, we would raise IncompleteRead if the content-length


    /usr/lib/python3.8/socket.py in readinto(self, b)
        667         while True:
        668             try:
    --> 669                 return self._sock.recv_into(b)
        670             except timeout:
        671                 self._timeout_occurred = True


    /usr/lib/python3.8/ssl.py in recv_into(self, buffer, nbytes, flags)
       1239                   "non-zero flags not allowed in calls to recv_into() on %s" %
       1240                   self.__class__)
    -> 1241             return self.read(nbytes, buffer)
       1242         else:
       1243             return super().recv_into(buffer, nbytes, flags)


    /usr/lib/python3.8/ssl.py in read(self, len, buffer)
       1097         try:
       1098             if buffer is not None:
    -> 1099                 return self._sslobj.read(len, buffer)
       1100             else:
       1101                 return self._sslobj.read(len)


    KeyboardInterrupt: 


Basic :func:``~mne.viz.plot_topomap`` options
---------------------------------------------

We plot evoked topographies using :func:``mne.Evoked.plot_topomap``. The
first argument, ``times`` allows to specify time instants (in seconds!)
for which topographies will be shown. We select timepoints from 50 to
150 ms with a step of 20ms and plot magnetometer data:

.. code:: ipython3

    times = np.arange(0.05, 0.151, 0.02)
    evoked.plot_topomap(times, ch_type='mag', time_unit='s')

If times is set to None at most 10 regularly spaced topographies will be
shown:

.. code:: ipython3

    evoked.plot_topomap(ch_type='mag', time_unit='s')

We can use ``nrows`` and ``ncols`` parameter to create multiline plots
with more timepoints.

.. code:: ipython3

    all_times = np.arange(-0.2, 0.5, 0.03)
    evoked.plot_topomap(all_times, ch_type='mag', time_unit='s',
                        ncols=8, nrows='auto')

Instead of showing topographies at specific time points we can compute
averages of 50 ms bins centered on these time points to reduce the noise
in the topographies:

.. code:: ipython3

    evoked.plot_topomap(times, ch_type='mag', average=0.05, time_unit='s')

We can plot gradiometer data (plots the RMS for each pair of
gradiometers)

.. code:: ipython3

    evoked.plot_topomap(times, ch_type='grad', time_unit='s')

Additional :func:``~mne.viz.plot_topomap`` options
--------------------------------------------------

We can also use a range of various :func:``mne.viz.plot_topomap``
arguments that control how the topography is drawn. For example:

-  ``cmap`` - to specify the color map
-  ``res`` - to control the resolution of the topographies (lower
   resolution means faster plotting)
-  ``outlines='skirt'`` to see the topography stretched beyond the head
   circle
-  ``contours`` to define how many contour lines should be plotted

.. code:: ipython3

    evoked.plot_topomap(times, ch_type='mag', cmap='Spectral_r', res=32,
                        outlines='skirt', contours=4, time_unit='s')

If you look at the edges of the head circle of a single topomap you’ll
see the effect of extrapolation. There are three extrapolation modes:

-  ``extrapolate='local'`` extrapolates only to points close to the
   sensors.
-  ``extrapolate='head'`` extrapolates out to the head head circle.
-  ``extrapolate='box'`` extrapolates to a large box stretching beyond
   the head circle.

The default value ``extrapolate='auto'`` will use ``'local'`` for MEG
sensors and ``'head'`` otherwise. Here we show each option:

.. code:: ipython3

    extrapolations = ['local', 'head', 'box']
    fig, axes = plt.subplots(figsize=(7.5, 4.5), nrows=2, ncols=3)
    
    # Here we look at EEG channels, and use a custom head sphere to get all the
    # sensors to be well within the drawn head surface
    for axes_row, ch_type in zip(axes, ('mag', 'eeg')):
        for ax, extr in zip(axes_row, extrapolations):
            evoked.plot_topomap(0.1, ch_type=ch_type, size=2, extrapolate=extr,
                                axes=ax, show=False, colorbar=False,
                                sphere=(0., 0., 0., 0.09))
            ax.set_title('%s %s' % (ch_type.upper(), extr), fontsize=14)
    fig.tight_layout()

More advanced usage
-------------------

Now we plot magnetometer data as topomap at a single time point: 100 ms
post-stimulus, add channel labels, title and adjust plot margins:

.. code:: ipython3

    evoked.plot_topomap(0.1, ch_type='mag', show_names=True, colorbar=False,
                        size=6, res=128, title='Auditory response',
                        time_unit='s')
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.88)

Animating the topomap
---------------------

Instead of using a still image we can plot magnetometer data as an
animation (animates only in matplotlib interactive mode)

.. code:: ipython3

    times = np.arange(0.05, 0.151, 0.01)
    fig, anim = evoked.animate_topomap(
        times=times, ch_type='mag', frame_rate=2, time_unit='s', blit=False)
