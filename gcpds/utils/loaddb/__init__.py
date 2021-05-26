# BCI2a, GIGA_Laplacian, databases
from .loaddb import GIGA, BCI2a, HighGamma, PhysionetMMI
from .loaddb import GIGA_MI_ME, BCI_CIV_2a, HighGamma_ME, PhysioNet_MI_ME, GIGA_BCI_ERP, GIGA_BCI_MI, GIGA_BCI_SSVEP
from .loaddb import AuditoryProcessing

available_databases = 'GIGA_MI_ME BCI_CIV_2a HighGamma_ME PhysioNet_MI_ME GIGA_BCI_ERP GIGA_BCI_MI GIGA_BCI_SSVEP AuditoryProcessing'.split()
