#! -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from collections import Iterable
from scipy.sparse.csr import csr_matrix
from numpy import ndarray
import logging
import collections

__author__ = 'kensuke-mi'

ROW_COL_VAL = collections.namedtuple('ROW_COL_VAL', 'row col val')


def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:
             yield item


def __conv_into_dict_format(pmi_word_score_items):
    out_format_structure = {}
    for item in pmi_word_score_items:
        if out_format_structure not in item['label']:
            out_format_structure[item['label']] = [{'word': item['word'], 'score': item['score']}]
        else:
            out_format_structure[item['label']].append({'word': item['word'], 'score': item['score']})
    return out_format_structure


def extract_from_csr_matrix(weight_csr_matrix, vocabulary, label_id, row_id, col_id):
    assert isinstance(weight_csr_matrix, csr_matrix)
    assert isinstance(vocabulary, dict)
    assert isinstance(label_id, dict)


def __get_value_index(row_col_tuple, value_list, col_index, row_pointer):
    assert isinstance(row_col_tuple, tuple)
    assert isinstance(value_list, ndarray)
    assert isinstance(col_index, ndarray)
    assert isinstance(row_pointer, ndarray)
    value = value_list[row_pointer[row_col_tuple[0]] + col_index[row_col_tuple[1]]]
    assert value != 0
    return value


def make_non_zero_information(weight_csr_matrix):
    assert isinstance(weight_csr_matrix, csr_matrix)
    values = weight_csr_matrix.data
    col_index = weight_csr_matrix.indices
    row_pointer = weight_csr_matrix.indptr

    indices = zip(*weight_csr_matrix.nonzero())

    value_index_items = [
        ROW_COL_VAL(
            row_index_tuple[0],
            row_index_tuple[1],
            __get_value_index(row_index_tuple, values, col_index, row_pointer)
        )
        for row_index_tuple
        in indices
    ]

    return value_index_items


def get_label(row_col_val_tuple, label_id):
    assert isinstance(row_col_val_tuple, ROW_COL_VAL)
    assert isinstance(label_id, dict)

    return label_id[row_col_val_tuple.row]


def get_word(row_col_val_tuple, vocabulary):
    assert isinstance(row_col_val_tuple, ROW_COL_VAL)
    assert isinstance(vocabulary, dict)

    return vocabulary[row_col_val_tuple.col]


def feature_extraction_single(weight_csr_matrix, vocabulary, label_id, logger, outformat='items'):
    """This function returns PMI score between label and words.

    Input csr matrix must be 'document-frequency' matrix, where records #document that word appears in document set.
    [NOTE] This is not FREQUENCY.

    Ex.
    If 'iPhone' appears in 5 documents of 'IT' category document set, value must be 5.

    Even if 'iPhone' appears 10 time in 'IT' category document set, it does not matter.


    :param scipy.csr_matrix:pmi_csr_matrix document-frequency of input data
    :param dict vocabulary: vocabulary set dict of input data
    :param dict label_id: document id dict of input data
    :param logging.Logger logger:
    :param str outformat: you can choose 'items' or 'dict':
    :return:
    """
    assert isinstance(weight_csr_matrix, csr_matrix)
    assert isinstance(logger, logging.Logger)
    assert isinstance(vocabulary, dict)
    assert isinstance(label_id, dict)

    logging.debug(msg='Start making score objects')

    value_index_items = make_non_zero_information(weight_csr_matrix)
    id2label = {id:label for label, id in label_id.items()}
    id2vocab = {id:voc for voc, id in vocabulary.viewitems()}

    word_score_items = [
        {
            'score': row_col_val_tuple.val,
            'label': get_label(row_col_val_tuple, id2label),
            'word': get_word(row_col_val_tuple, id2vocab)
        }
        for row_col_val_tuple
        in value_index_items
    ]

    logging.debug(msg='End making score objects')

    return word_score_items


def get_feature_dictionary(weighted_matrix, vocabulary, label_group_dict, logger, outformat='items', n_job=1):
    """Get dictionary structure of PMI featured scores.

    You can choose 'dict' or 'items' for ```outformat``` parameter.

    If outformat='dict', you get

    >>> {label_name:
            {
                feature: score
            }
        }

    Else if outformat='items', you get

    >>> [
        {
            feature: score
        }
        ]


    :param string outformat: format type of output dictionary. You can choose 'items' or 'dict'
    :param bool cut_zero: return all result or not. If cut_zero = True, the method cuts zero features.
    """
    assert isinstance(weighted_matrix, csr_matrix)
    assert isinstance(vocabulary, dict)
    assert isinstance(label_group_dict, dict)
    assert isinstance(n_job, int)

    if n_job==1:
        score_objects = feature_extraction_single(
            weight_csr_matrix=weighted_matrix,
            vocabulary=vocabulary,
            label_id=label_group_dict,
            logger=logger,
            outformat=outformat
        )
    else:
        raise Exception('not implemented yet')

    return score_objects


