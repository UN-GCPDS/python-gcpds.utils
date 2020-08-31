from google.colab import drive
import os
import sys
import logging

SHARED_DRIVE = 'GCPDS'


# ----------------------------------------------------------------------
def mount(shared_drive=SHARED_DRIVE, mount='drive', force_remount=False):
    """"""
    mount_dst = os.path.join('/', 'content', mount)
    drive.mount(mount_dst, force_remount=force_remount)

    gcpds_drive = os.path.join(mount_dst, 'Shared drives', shared_drive)
    if not os.path.exists(gcpds_drive):
        logging.warning(
            f"You haven't access to {shared_drive} shared drive, ask for one.")
        return

    os.chdir(gcpds_drive)
    logging.warning(
        f"Your working directory is now the root of the shared drive '{shared_drive}'.")
