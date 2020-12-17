# -*- coding: utf8 -*-
# Copyright (c) 2020 Nicholas de Jong

__title__ = "arpwitch"
__author__ = "Nicholas de Jong <contact@nicholasdejong.com>"
__version__ = '0.3.6'
__license__ = "BSD2"

__logger_default_level__ = 'info'

__sniff_batch_size__ = 16
__sniff_batch_timeout__ = 2
__save_data_interval__default__ = 30
__nmap__exec__ = 'nmap -n -T4 -Pn -oX ' + __title__ + '-nmap-{IP}-{ts}.xml {IP}'
__exec_max_runtime__ = 30
