#!/usr/bin/env python
"""
Copyright 2023 Ella Shulman <eshulman@redhat.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import argparse
import logging
from elasticsearch import Elasticsearch
import re
from configparser import ConfigParser
from datetime import datetime

logging.basicConfig(level=logging.INFO)
es = Elasticsearch("http://seal52.lab.eng.tlv2.redhat.com:9200")
INDEX = 'nfv-perf-report-elk'

MAPPING = dict({
    'properties': dict({
        'perf_results': dict({'type': 'float'}),
        'compute_cmdline': dict({'type': 'text'}),
        'compute_kernel': dict({'type': 'version'}),
        'compute_architecture': dict({'type': 'keyword'}),
        'compute_distribution': dict({'type': 'text'}),
        'compute_os_version': dict({'type': 'version'}),
        'compute_cpu_model': dict({'type': 'text'}),
        'compute_nics': dict({'type': 'string'}),
        'compute_ovn_version': dict({'type': 'version'}),
        'trex_kernel': dict({'type': 'version'}),
        'trex_architecture': dict({'type': 'keyword'}),
        'trex_distribution': dict({'type': 'text'}),
        'trex_os_version': dict({'type': 'version'}),
        'dut_type': dict({'type': 'keyword'}),
        'RHOS_version': dict({'type': 'version'}),
        'core_puddle_version': dict({'type': 'version'}),
        'compute_ovs_versions': dict({'type': 'version'}),
        'compute_dpdk_versions': dict({'type': 'version'}),
        'date': dict({'type': 'date'})
    })
})

es.indices.create(index=INDEX, body={mappings: MAPPING})
