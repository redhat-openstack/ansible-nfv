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
# from elasticsearch import Elasticsearch
import elasticsearch
import json

logging.basicConfig(level=logging.INFO)

class es_report:
    def __init__(self, results_path, es_instance, index, mapping_path, args):
        self.es = elasticsearch.Elasticsearch(es_instance)
        self.index_name = index
        self.args = args
        with open(results_path, 'r') as res:
            self.results = json.loads(res.read())
        with open(mapping_path, 'r') as map:
            self.mapping = json.loads(map.read())

    def __call__(self):
        if self.args.delete_mapping:
            self.delete_mapping()
        if self.args.create_mapping:
            self.create_index_mapping()
        if self.args.upload:
            self.upload_results()

    def create_index_mapping(self):
        try:
            self.es.indices.create(index=self.index_name,
                                         body={'mappings': self.mapping})
        except elasticsearch.RequestError as err:
            print('index mapping creation failed due to:')
            raise err

    def upload_results(self):
        try:
            self.es.index(
                index=self.index_name, body=self.results, doc_type='_doc')
        except elasticsearch.RequestError as err:
            print('result upload faild due to:')
            raise err

    def delete_mapping(self):
        try:
            self.es.indices.delete(index=self.index_name)
        except elasticsearch.RequestError as err:
            print('mapping delete failed due to:')
            raise err


def arg_parser():
    parser = argparse.ArgumentParser(description='Upload results to ELK')
    parser.add_argument('-p', '--result-file',
                        help='Path to results json file', required=True)
    parser.add_argument('-m', '--mapping-file',
                        help='Path to mapping json file, required when using '
                        '--create-mapping')
    parser.add_argument('--es-url', help='ES URL for uploading results to',
                        default="http://seal52.lab.eng.tlv2.redhat.com:9200")
    parser.add_argument('-i', '--index-name', help='Index name in ES',
                        default='nfv-perf-report-elk')
    parser.add_argument('--upload', action='store_true', help='Upload results')
    parser.add_argument('--create-mapping', action='store_true',
                        help='Create mapping')
    parser.add_argument('--delete-mapping', action='store_true',
                        help='Create mapping')
    args = parser.parse_args()
    if args.create_mapping and args.mapping_file == None:
      parser.error("--create-mapping requires --mapping-file, please specify mapping path.")
    if args.upload and args.result_file == None:
      parser.error("--upload requires --result-file, please specify result path.")
    return args


def main():
    args = arg_parser()
    es = es_report(args.result_file, args.es_url,
                   args.index_name, args.mapping_file, args=args)
    es()


if __name__ == "__main__":
    main()
