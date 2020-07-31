from google.colab import drive
import os
import sys
import logging

SHARED_DRIVE = 'GCPDS'


# ----------------------------------------------------------------------
def mount():
    """"""
    mount_dst = os.path.join('/', 'content', 'drive')
    drive.mount(mount_dst, force_remount=False)

    gcpds_drive = os.path.join(mount_dst, 'Shared drives', SHARED_DRIVE)
    if not os.path.exists(gcpds_drive):
        logging.warning(
            f"You haven't access to {SHARED_DRIVE} shared drive, ask for one.")
        return

    os.chdir(gcpds_drive)
    logging.warning(
        f"Your working directory is now the root of the shared drive '{SHARED_DRIVE}'.")
