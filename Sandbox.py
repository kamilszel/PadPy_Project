import pandas as pd
import numpy as np
import io
import os
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from dateutil import parser

def str_to_data(s):
    try:
        val = int(s)
        return val
    except ValueError:
        pass
    try:
        val = float(s)
        return val
    except ValueError:
        pass
    try:
        bool(s)
        val = True if s == 'True' else s
        val = False if s == 'False' else val
        if val!=s:
            return val
    except ValueError:
        pass
    try:
        val = parser.parse(s)
        return val
    except ValueError:
        pass
    return s


def iter_docs(root_node):
    # Method taken from:
    # https://stackoverflow.com/questions/28259301/how-to-convert-an-xml-file-to-nice-pandas-dataframe
    # and modified
    root_attr = root_node.attrib
    it = 0
    size = len(root_node)
    for doc in root_node:
        doc_dict = root_attr.copy()
        attrib_dict = {}
        attrib_dict.update(doc.attrib)
        for key,val in attrib_dict.items():
            attrib_dict.update({key:str_to_data(val)})
        doc_dict.update(attrib_dict)

        string = '['
        for k in range(int(it / size * 100)):
            string += '#'
        for k in range(100 - int(it / size * 100)):
            string += '-'
        string += ']'
        string += '{0:.2f}'.format(it / size * 100) + "%"
        print('\r' + string, sep='', end=' ', flush=True)
        it += 1

        yield doc_dict



def main(config_file):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    xml_path = os.path.join(dir_path, "assets", "xml")
    file_paths = []
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('max_colwidth', -1)
    for file in os.listdir(xml_path):
        if file.endswith(".xml"):
            file_paths.append(os.path.join(xml_path, file))
    for l in file_paths:
        tree = ET.parse(l)
        root = tree.getroot()
        doc_list = list(iter_docs(root))
        doc_df = pd.DataFrame(doc_list)
        doc_df = doc_df.replace(r'\\n', ' ', regex=True)
        doc_df = doc_df.replace(r'\\r', ' ', regex=True)
        doc_df.to_csv(l + ".csv", sep=';', index=False)
        doc_df = pd.read_csv(l + ".csv", sep=';')
        print()

        print(doc_df.head(20))

if __name__ == '__main__':
    # with open(JSON_PATH) as f:
    #     config = json.load(f)
    main(None)