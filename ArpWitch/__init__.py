
from .__name__ import NAME
from .__version__ import VERSION

LOGGER_LEVEL_DEFAULT = 'warning'
SNIFF_BATCH_SIZE = 16
SNIFF_BATCH_TIMEOUT = 2
SAVE_DATA_INTERVAL_DEFAULT = 30
NMAP_EXEC = 'nmap -n -T4 -Pn -oX ' + NAME + '-nmap-{IP}-{ts}.xml {IP}'
EXEC_MAX_RUNTIME = 30

from .utils import out
from .utils import timestamp

from .logger import Logger
from .witch import ArpWitchWitch
from .datafile import ArpWitchDataFile
from .sniffer import ArpWitchSniffer
from .exec import ArpWitchExec

from .main import ArpWitch
