# ----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd

import io
import unittest
from collections import OrderedDict

from skbio import TabularMSA, Protein, DNA, RNA
from skbio.io import StockholmFormatError
from skbio.io.format.stockholm import (_stockholm_to_tabular_msa,
                                       _tabular_msa_to_stockholm,
                                       _stockholm_sniffer)
from skbio.util import get_data_path


class TestStockholmSniffer(unittest.TestCase):
    def setUp(self):
        self.positives = [get_data_path(e) for e in [
            'stockholm_extensive',
            'stockholm_minimal',
            'stockholm_rna',
            'stockholm_runon_gf',
            'stockholm_duplicate_sequence_names',
            'stockholm_duplicate_gr',
            'stockholm_duplicate_gc',
            'stockholm_invalid_nonexistent_gr',
            'stockholm_invalid_nonexistent_gs',
            'stockholm_no_data',
            'stockholm_blank_lines',
            'stockholm_differing_gc_data_length',
            'stockholm_differing_gr_data_length',
            'stockholm_differing_seq_lengths',
            'stockholm_duplicate_sequence_names',
            'stockholm_duplicate_tree_ids',
            'stockholm_extensive_mixed',
            'stockholm_invalid_data_type',
            'stockholm_malformed_gf_line',
            'stockholm_malformed_gs_line',
            'stockholm_malformed_gr_line',
            'stockholm_malformed_gc_line',
            'stockholm_malformed_data_line',
            'stockholm_metadata_only',
            'stockholm_multiple_msa',
            'stockholm_multiple_trees',
            'stockholm_runon_gs',
            'stockholm_single_tree_with_id',
            'stockholm_single_tree_without_id',
            'stockholm_whitespace_only_lines',
            'stockholm_all_data_types',
            'stockholm_two_of_each_metadata',
            'stockholm_data_only',
            'stockholm_nonstring_labels'
            ]]

        self.negatives = [get_data_path(e) for e in [
            'stockholm_missing_header',
            'empty',
            'whitespace_only'
            ]]

    def test_positives(self):
        for fp in self.positives:
            self.assertEqual(_stockholm_sniffer(fp), (True, {}))

    def test_negatives(self):
        for fp in self.negatives:
            self.assertEqual(_stockholm_sniffer(fp), (False, {}))


class TestStockholmReader(unittest.TestCase):
    def test_stockholm_extensive(self):
        fp = get_data_path('stockholm_extensive')
        msa = _stockholm_to_tabular_msa(fp, constructor=Protein)
        exp = TabularMSA([Protein('MTCRAQLIAVPRASSLAE..AIACAQKM....'
                                  'RVSRVPVYERS',
                                  positional_metadata={'SA': list('9998877564'
                                                                  '53524252..'
                                                                  '55152525..'
                                                                  '..36463774'
                                                                  '777')}),
                          Protein('EVMLTDIPRLHINDPIMK..GFGMVINN....'
                                  '..GFVCVENDE',
                                  metadata={'OS': 'Bacillus subtilis'},
                                  positional_metadata={'SS': list('CCCCCCCHHHH'
                                                                  'HHHHHHH..HE'
                                                                  'EEEEEE....E'
                                                                  'EEEEEE'
                                                                  'EEEH')}),
                          Protein('EVMLTDIPRLHINDPIMK..GFGMVINN...'
                                  '...GFVCVENDE',
                                  positional_metadata={'AS': list('___________'
                                                                  '_____*_____'
                                                                  '___________'
                                                                  '________'
                                                                  '__'),
                                                       'IN': list('___________'
                                                                  '_1_________'
                                                                  '_____2_____'
                                                                  '_____0_'
                                                                  '___')})],
                         metadata={'ID': 'CBS', 'AC': 'PF00571',
                                   'AU': 'Bateman A', 'SQ': '67'},
                         positional_metadata={'SS_cons': list('CCCCCHHHHHHHH'
                                                              'HHHHH..EEEEEE'
                                                              'EE....EEEEEEE'
                                                              'EEEH')},
                         index=['O83071/192-246', 'O31698/88-139',
                                'O31699/88-139'])
        self.assertEqual(msa, exp)

    def test_stockholm_extensive_mixed(self):
        fp = get_data_path('stockholm_extensive_mixed')
        msa = _stockholm_to_tabular_msa(fp, constructor=Protein)
        exp = TabularMSA([Protein('MTCRAQLIAVPRASSLAE..AIACAQKM....'
                                  'RVSRVPVYERS',
                                  positional_metadata={'SA': list('9998877564'
                                                                  '53524252..'
                                                                  '55152525..'
                                                                  '..36463774'
                                                                  '777')}),
                          Protein('EVMLTDIPRLHINDPIMK..GFGMVINN....'
                                  '..GFVCVENDE',
                                  metadata={'OS': 'Bacillus subtilis'},
                                  positional_metadata={'SS': list('CCCCCCCHHHH'
                                                                  'HHHHHHH..HE'
                                                                  'EEEEEE....E'
                                                                  'EEEEEE'
                                                                  'EEEH')}),
                          Protein('EVMLTDIPRLHINDPIMK..GFGMVINN...'
                                  '...GFVCVENDE',
                                  positional_metadata={'AS': list('___________'
                                                                  '_____*_____'
                                                                  '___________'
                                                                  '________'
                                                                  '__'),
                                                       'IN': list('___________'
                                                                  '_1_________'
                                                                  '_____2_____'
                                                                  '_____0_'
                                                                  '___')})],
                         metadata={'ID': 'CBS', 'AC': 'PF00571',
                                   'AU': 'Bateman A', 'SQ': '67'},
                         positional_metadata={'SS_cons': list('CCCCCHHHHHHHH'
                                                              'HHHHH..EEEEEE'
                                                              'EE....EEEEEEE'
                                                              'EEEH')},
                         index=['O83071/192-246', 'O31698/88-139',
                                'O31699/88-139'])
        self.assertEqual(msa, exp)

    def test_stockholm_minimal(self):
        fp = get_data_path('stockholm_minimal')
        msa = _stockholm_to_tabular_msa(fp, constructor=DNA)
        exp = TabularMSA([DNA('TGTGTCGCAGTTGTCGTTTG')], index=['0235244'])
        self.assertEqual(msa, exp)

    def test_stockholm_rna(self):
        fp = get_data_path('stockholm_rna')
        msa = _stockholm_to_tabular_msa(fp, constructor=RNA)
        exp = TabularMSA([RNA('AAGGGUUAUUUAUAUACUUU'),
                          RNA('UGCUAAGAGUGGGGAUGAUU'),
                          RNA('GCCACAACCGAUUAGAUAGA'),
                          RNA('UUAGAAACCGAUGGACCGAA')],
                         metadata={'AC': 'G2134T23', 'ID': 'ARD'},
                         positional_metadata=(
                         {'AC_cons': list('GGGACUGGACAUCUAUUCAG')}),
                         index=['RTC2231', 'RTF2124', 'RTH3322', 'RTB1512'])
        self.assertEqual(msa, exp)

    def test_stockholm_runon_gf(self):
        fp = get_data_path('stockholm_runon_gf')
        msa = _stockholm_to_tabular_msa(fp, constructor=DNA)
        exp = TabularMSA([DNA('ACTGGTTCAATG')],
                         metadata={'CC': 'CBS domains are small intracellular'
                                         ' modules mostly found in 2 or four '
                                         'copies within a protein.'},
                         index=['GG1344'])
        self.assertEqual(msa, exp)

    def test_stockholm_runon_gs(self):
        fp = get_data_path('stockholm_runon_gs')
        msa = _stockholm_to_tabular_msa(fp, constructor=DNA)
        exp = TabularMSA([DNA('ATCGTTCAGTG',
                              metadata={'AL': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'})],
                         index=['seq1'])
        self.assertEqual(msa, exp)

    def test_stockholm_metadata_only(self):
        fp = get_data_path('stockholm_metadata_only')
        msa = _stockholm_to_tabular_msa(fp, constructor=DNA)
        exp = TabularMSA([], metadata={'NM': 'Kestrel Gorlick',
                                       'DT': 'February 5th, 2016'})
        self.assertEqual(msa, exp)

    def test_stockholm_no_data(self):
        fp = get_data_path('stockholm_no_data')
        msa = _stockholm_to_tabular_msa(fp, constructor=DNA)
        exp = TabularMSA([])
        self.assertEqual(msa, exp)

    def test_stockholm_with_blank_lines(self):
        fp = get_data_path('stockholm_blank_lines')
        msa = _stockholm_to_tabular_msa(fp, constructor=DNA)
        exp = TabularMSA([], metadata={'AL': 'ABCD', 'NM': '1234'})
        self.assertEqual(msa, exp)

    def test_stockholm_with_whitespace_only_lines(self):
        fp = get_data_path('stockholm_whitespace_only_lines')
        msa = _stockholm_to_tabular_msa(fp, constructor=DNA)
        exp = TabularMSA([], metadata={'AL': 'ABCD', 'NM': '1234'})
        self.assertEqual(msa, exp)

    def test_stockholm_single_tree_without_id(self):
        fp = get_data_path('stockholm_single_tree_without_id')
        msa = _stockholm_to_tabular_msa(fp, constructor=DNA)
        exp = TabularMSA([], metadata={'NH': 'ABCD'})
        self.assertEqual(msa, exp)

    def test_stockholm_single_tree_with_id(self):
        fp = get_data_path('stockholm_single_tree_with_id')
        msa = _stockholm_to_tabular_msa(fp, constructor=DNA)
        exp = TabularMSA([], metadata={'NH': {'tree1': 'ABCD'}})
        self.assertEqual(msa, exp)

    def test_stockholm_multiple_trees(self):
        fp = get_data_path('stockholm_multiple_trees')
        msa = _stockholm_to_tabular_msa(fp, constructor=DNA)
        exp = TabularMSA([], metadata={'NH': {'tree1': 'ABCD',
                                              'tree2': 'EFGH',
                                              'tree3': 'IJKL'}})
        self.assertEqual(msa, exp)

    def test_multiple_msa_file(self):
        fp = get_data_path('stockholm_multiple_msa')
        msa = _stockholm_to_tabular_msa(fp, constructor=RNA)
        exp = TabularMSA([RNA('AAGGGUUAUUUAUAUACUUU'),
                          RNA('UGCUAAGAGUGGGGAUGAUU'),
                          RNA('GCCACAACCGAUUAGAUAGA'),
                          RNA('UUAGAAACCGAUGGACCGAA')],
                         metadata={'AC': 'G2134T23', 'ID': 'ARD'},
                         positional_metadata=(
                         {'AC_cons': list('GGGACUGGACAUCUAUUCAG')}),
                         index=['RTC2231', 'RTF2124', 'RTH3322', 'RTB1512'])
        self.assertEqual(msa, exp)

    def test_stockholm_maintains_order(self):
        fp = get_data_path('stockholm_two_of_each_metadata')
        msa = _stockholm_to_tabular_msa(fp, constructor=DNA)
        msa_order = list(msa.metadata.items())
        exp_order = [('NM', 'Kestrel Gorlick'), ('DT', 'February 5th, 2016')]
        self.assertEqual(msa_order, exp_order)
        msa_order = list(msa[0].metadata.items())
        exp_order = [('AL', 'ABCD'), ('NS', '1234')]
        self.assertEqual(msa_order, exp_order)
        msa_order = list(msa.positional_metadata.columns)
        exp_order = ['SS_cons', 'AS_cons']
        self.assertEqual(msa_order, exp_order)
        msa_order = list(msa[0].positional_metadata.columns)
        exp_order = ['SS', 'AS']
        self.assertEqual(msa_order, exp_order)

    def test_stockholm_duplicate_tree_id_error(self):
        fp = get_data_path('stockholm_duplicate_tree_ids')
        with self.assertRaisesRegex(StockholmFormatError,
                                    'Tree.*tree1.*in file.'):
            _stockholm_to_tabular_msa(fp, constructor=DNA)

    def test_nonexistent_gr_error(self):
        fp = get_data_path('stockholm_invalid_nonexistent_gr')
        with self.assertRaisesRegex(StockholmFormatError,
                                    'GS or GR.*nonexistent sequence.*RL1355.'):
            _stockholm_to_tabular_msa(fp, constructor=RNA)

    def test_nonexistent_gs_error(self):
        fp = get_data_path('stockholm_invalid_nonexistent_gs')
        with self.assertRaisesRegex(StockholmFormatError,
                                    'GS or GR.*nonexistent sequence.*AC14.'):
            _stockholm_to_tabular_msa(fp, constructor=RNA)

    def test_duplicate_sequence_names_error(self):
        fp = get_data_path('stockholm_duplicate_sequence_names')
        with self.assertRaisesRegex(
                StockholmFormatError,
                'duplicate sequence name.*ASR132.*supported by the reader.'):
            _stockholm_to_tabular_msa(fp, constructor=RNA)

    def test_duplicate_gr_error(self):
        fp = get_data_path('stockholm_duplicate_gr')
        with self.assertRaisesRegex(StockholmFormatError,
                                    'Found duplicate GR.*OS.*LFDR3.*supported '
                                    'by the reader.'):
            _stockholm_to_tabular_msa(fp, constructor=DNA)

    def test_duplicate_gc_error(self):
        fp = get_data_path('stockholm_duplicate_gc')
        with self.assertRaisesRegex(StockholmFormatError,
                                    'Found duplicate GC.*SS_cons.*supported '
                                    'by the reader.'):
            _stockholm_to_tabular_msa(fp, constructor=DNA)

    def test_empty_file_error(self):
        fp = get_data_path('empty')
        with self.assertRaisesRegex(StockholmFormatError, 'File is empty.'):
            _stockholm_to_tabular_msa(fp, constructor=RNA)

    def test_missing_header_error(self):
        fp = get_data_path('stockholm_missing_header')
        with self.assertRaisesRegex(StockholmFormatError,
                                    'File missing.*header'):
            _stockholm_to_tabular_msa(fp, constructor=DNA)

    def test_missing_footer_error(self):
        fp = get_data_path('stockholm_missing_footer')
        with self.assertRaisesRegex(StockholmFormatError,
                                    'Final line.*only "//".'):
            _stockholm_to_tabular_msa(fp, constructor=DNA)

    def test_data_type_error(self):
        fp = get_data_path('stockholm_invalid_data_type')
        with self.assertRaisesRegex(StockholmFormatError,
                                    "Unrecognized.*'#=GZ"):
            _stockholm_to_tabular_msa(fp, constructor=DNA)

    def test_malformed_gf_line_error(self):
        fp = get_data_path('stockholm_malformed_gf_line')
        with self.assertRaisesRegex(StockholmFormatError,
                                    'Line contains 2.*must contain.*3.'):
            _stockholm_to_tabular_msa(fp, constructor=DNA)

    def test_malformed_gs_line_error(self):
        fp = get_data_path('stockholm_malformed_gs_line')
        with self.assertRaisesRegex(StockholmFormatError,
                                    'Line contains 3.*must contain.*4.'):
            _stockholm_to_tabular_msa(fp, constructor=DNA)

    def test_malformed_gr_line_error(self):
        fp = get_data_path('stockholm_malformed_gr_line')
        with self.assertRaisesRegex(StockholmFormatError,
                                    'Line contains 2.*must contain.*4.'):
            _stockholm_to_tabular_msa(fp, constructor=DNA)

    def test_malformed_gc_line_error(self):
        fp = get_data_path('stockholm_malformed_gc_line')
        with self.assertRaisesRegex(StockholmFormatError,
                                    'Line contains 2.*must contain.*3.'):
            _stockholm_to_tabular_msa(fp, constructor=DNA)

    def test_malformed_data_line_error(self):
        fp = get_data_path('stockholm_malformed_data_line')
        with self.assertRaisesRegex(StockholmFormatError,
                                    'Line contains 1.*must contain.*2.'):
            _stockholm_to_tabular_msa(fp, constructor=DNA)

    def test_differing_sequence_lengths_error(self):
        fp = get_data_path('stockholm_differing_seq_lengths')
        with self.assertRaisesRegex(ValueError, 'Each sequence.*11 != 10'):
            _stockholm_to_tabular_msa(fp, constructor=RNA)

    def test_differing_data_lengths_gr_error(self):
        fp = get_data_path('stockholm_differing_gr_data_length')
        with self.assertRaisesRegex(ValueError, 'Number.*7.*(8).'):
            _stockholm_to_tabular_msa(fp, constructor=RNA)

    def test_differing_data_lengths_gc_error(self):
        fp = get_data_path('stockholm_differing_gc_data_length')
        with self.assertRaisesRegex(ValueError, 'Number.*12.*(10).'):
            _stockholm_to_tabular_msa(fp, constructor=RNA)

    def test_no_constructor_error(self):
        fp = get_data_path('empty')
        with self.assertRaisesRegex(ValueError, 'Must.*parameter.'):
            _stockholm_to_tabular_msa(fp)

    def test_unsupported_constructor_error(self):
        fp = get_data_path('empty')
        with self.assertRaisesRegex(TypeError,
                                    '`constructor`.*`GrammaredSequence`'):
            _stockholm_to_tabular_msa(fp, constructor=TabularMSA)


class TestStockholmWriter(unittest.TestCase):
    def test_msa_to_stockholm_extensive(self):
        fp = get_data_path('stockholm_all_data_types')
        msa = TabularMSA([DNA('GAGGCCATGCCCAGGTGAAG',
                              metadata=OrderedDict([('DT', 'February 1, 2016'),
                                                    ('NM', 'Unknown')])),
                          DNA('ACCTGAGCCACAGTAGAAGT'),
                          DNA('CCCTTCGCTGGAAATGTATG',
                              metadata={'DT': 'Unknown'},
                              positional_metadata=OrderedDict([('AS',
                                                                list('CCGAAAGT'
                                                                     'CGTTCGA'
                                                                     'AAATG')),
                                                               ('SS',
                                                                list('GGCGAGTC'
                                                                     'GTTCGAGC'
                                                                     'TGG'
                                                                     'C'))]))],
                         metadata=OrderedDict([('NM', 'Kestrel Gorlick'),
                                              ('DT', 'February 11, 2016'),
                                              ('FN', 'Writer test file')]),
                         positional_metadata=OrderedDict([('AS_cons',
                                                           list('CGTTCGTTCTAAC'
                                                                'AATTCCA')),
                                                          ('SS_cons',
                                                           list('GGCGCTACGACCT'
                                                                'ACGACCG'))]),
                         index=['seq1', 'seq2', 'seq3'])
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_msa_to_stockholm_minimal(self):
        fp = get_data_path('stockholm_minimal')
        msa = TabularMSA([DNA('TGTGTCGCAGTTGTCGTTTG')], index=['0235244'])
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_msa_to_stockholm_single_tree(self):
        fp = get_data_path('stockholm_single_tree_without_id')
        msa = TabularMSA([], metadata=OrderedDict([('NH', 'ABCD')]))
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_msa_to_stockholm_single_tree_as_dict(self):
        fp = get_data_path('stockholm_single_tree_with_id')
        msa = TabularMSA([], metadata={'NH': {'tree1': 'ABCD'}})
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_msa_to_stockholm_multiple_trees(self):
        fp = get_data_path('stockholm_multiple_trees')
        msa = TabularMSA([], metadata=OrderedDict([('NH',
                                                    OrderedDict([('tree1',
                                                                  'ABCD'),
                                                                 ('tree2',
                                                                  'EFGH'),
                                                                 ('tree3',
                                                                  'IJKL')]))]))
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_msa_to_stockholm_data_only(self):
        fp = get_data_path('stockholm_data_only')
        msa = TabularMSA([RNA('ACUCCGACAUGCUCC'),
                          RNA('UAGUGCCGAACGCUG'),
                          RNA('GUGUGGGCGUGAUUC')],
                         index=['seq1', 'seq2', 'seq3'])
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_msa_to_stockholm_nonstring_values(self):
        fp = get_data_path('stockholm_nonstring_labels')
        msa = TabularMSA([DNA('ACTG', metadata=OrderedDict([(8, 123)]),
                              positional_metadata=OrderedDict([(1.0,
                                                                [1, 2, 3, 4])])
                              )],
                         metadata=OrderedDict([(1.3, 2857)]),
                         positional_metadata=OrderedDict([(25, [4, 3, 2, 1])]),
                         index=[11214])
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_msa_to_stockholm_empty(self):
        fp = get_data_path('stockholm_no_data')
        msa = TabularMSA([])
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_round_trip_extensive(self):
        fp = get_data_path('stockholm_extensive')
        msa = _stockholm_to_tabular_msa(fp, constructor=Protein)
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_round_trip_minimal(self):
        fp = get_data_path('stockholm_minimal')
        msa = _stockholm_to_tabular_msa(fp, constructor=DNA)
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_round_trip_single_tree(self):
        fp = get_data_path('stockholm_single_tree_without_id')
        msa = _stockholm_to_tabular_msa(fp, constructor=Protein)
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_round_trip_multiple_trees(self):
        fp = get_data_path('stockholm_multiple_trees')
        msa = _stockholm_to_tabular_msa(fp, constructor=Protein)
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_round_trip_data_only(self):
        fp = get_data_path('stockholm_data_only')
        msa = _stockholm_to_tabular_msa(fp, constructor=RNA)
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_round_trip_nonstring_index_values(self):
        fp = get_data_path('stockholm_nonstring_labels')
        msa = _stockholm_to_tabular_msa(fp, constructor=DNA)
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_round_trip_empty(self):
        fp = get_data_path('stockholm_no_data')
        msa = _stockholm_to_tabular_msa(fp, constructor=Protein)
        fh = io.StringIO()
        _tabular_msa_to_stockholm(msa, fh)
        obs = fh.getvalue()
        fh.close()
        with io.open(fp) as fh:
            exp = fh.read()
        self.assertEqual(obs, exp)

    def test_unoriginal_index_error(self):
        msa = TabularMSA([DNA('ATCGCCAGCT'), DNA('TTGTGCTGGC')],
                         index=['seq1', 'seq1'])
        with self.assertRaisesRegex(StockholmFormatError,
                                    'index labels must be unique.'):
            fh = io.StringIO()
            _tabular_msa_to_stockholm(msa, fh)

    def test_unoriginal_gr_feature_names_error(self):
        pos_metadata_dataframe = pd.DataFrame.from_items([('AC',
                                                           list('GAGCAAGCCACTA'
                                                                'GA')),
                                                          ('SS',
                                                           list('TCCTTGAACTACC'
                                                                'CG')),
                                                          ('AS',
                                                           list('TCAGCTCTGCAGC'
                                                                'GT')),
                                                          ('SS',
                                                           list('GTCAGGCGCTCGG'
                                                                'TG'))])
        msa = TabularMSA([DNA('CGTCAATCTCGAACT',
                          positional_metadata=pos_metadata_dataframe)],
                         index=['seq1'])
        with self.assertRaisesRegex(StockholmFormatError,
                                    'Sequence-specific positional metadata.*'
                                    'must be unique. Found 1 duplicate'):
            fh = io.StringIO()
            _tabular_msa_to_stockholm(msa, fh)

    def test_unoriginal_gc_feature_names_error(self):
        pos_metadata_dataframe = pd.DataFrame.from_items([('AC',
                                                           list('GAGCAAGCCACTA'
                                                                'GA')),
                                                          ('SS',
                                                           list('TCCTTGAACTACC'
                                                                'CG')),
                                                          ('SS',
                                                           list('TCAGCTCTGCAGC'
                                                                'GT')),
                                                          ('AC',
                                                           list('GTCAGGCGCTCGG'
                                                                'TG'))])
        msa = TabularMSA([DNA('CCCCTGCTTTCGTAG')],
                         positional_metadata=pos_metadata_dataframe)
        with self.assertRaisesRegex(StockholmFormatError,
                                    'Multiple sequence alignment positional '
                                    'metadata.*must be unique. Found 2 '
                                    'duplicate'):
            fh = io.StringIO()
            _tabular_msa_to_stockholm(msa, fh)

    def test_gr_wrong_dataframe_item_length_error(self):
        seq1 = list('GAGCAAGCCACTAGA')
        seq1.append('GG')
        pos_metadata_dataframe = pd.DataFrame({'AC': seq1,
                                               'SS': list('TCCTTGAACTACCCGA'),
                                               'AS': list('TCAGCTCTGCAGCGTT')})
        msa = TabularMSA([DNA('TCCTTGAACTACCCGA',
                              positional_metadata=pos_metadata_dataframe)])
        with self.assertRaisesRegex(StockholmFormatError,
                                    'Sequence-specific positional metadata.*'
                                    'must contain a single character.*Found '
                                    'value\(s\) in column AC'):
            fh = io.StringIO()
            _tabular_msa_to_stockholm(msa, fh)

    def test_gc_wrong_dataframe_item_length_error(self):
        seq1 = list('GAGCAAGCCACTAGA')
        seq1.append('GG')
        pos_metadata_dataframe = pd.DataFrame({'AC': seq1,
                                               'SS': list('TCCTTGAACTACCCGA'),
                                               'AS': list('TCAGCTCTGCAGCGTT')})
        msa = TabularMSA([DNA('TCCTTGAACTACCCGA')],
                         positional_metadata=pos_metadata_dataframe)
        with self.assertRaisesRegex(StockholmFormatError,
                                    'Multiple sequence alignment positional '
                                    'metadata.*must contain a single character'
                                    '.*Found value\(s\) in column AC'):
            fh = io.StringIO()
            _tabular_msa_to_stockholm(msa, fh)

if __name__ == '__main__':
    unittest.main()
