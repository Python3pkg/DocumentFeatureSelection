#! -*- coding: utf-8 -*-




import sys
python_version = sys.version_info

if python_version > (3, 0, 0):
    from DocumentFeatureSelection.pmi.PMI_python3 import PMI
else:
    raise SystemError('Not Implemented yet')