#! -*- coding: utf-8 -*-




import sys
python_version = sys.version_info

if python_version > (3, 0, 0):
    from DocumentFeatureSelection.soa.soa_python3 import SOA
else:
    raise SystemError('Not Implemented yet')