import os
import pandas as pd

from unittest import TestCase, main
from metapool.metapool import parse_sample_sheet
from metapool.prep import (preparations_for_run, remove_qiita_id,
                           get_run_prefix, is_nonempty_gz_file,
                           get_machine_code, get_model_and_center,
                           sample_sheet_to_dataframe, parse_illumina_run_id)


class Tests(TestCase):
    def setUp(self):
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.good_run = os.path.join(data_dir, 'runs',
                                     '191103_D32611_0365_G00DHB5YXX')

        self.ss = os.path.join(self.good_run, 'sample-sheet.csv')

    def test_preparations_for_run(self):
        ss = sample_sheet_to_dataframe(parse_sample_sheet(self.ss))
        obs = preparations_for_run(self.good_run, ss)

        exp = {'191103_D32611_0365_G00DHB5YXX.Baz.1',
               '191103_D32611_0365_G00DHB5YXX.Baz.3',
               '191103_D32611_0365_G00DHB5YXX.FooBar_666.3'}
        self.assertEqual(set(obs.keys()), exp)

        data = [['important-sample44', 'EXPERIMENT_DESC',
                 'LIBRARY_PROTOCOL', 'Illumina', 'UCSDMI', '2019-11-03',
                 'sample44_S14_L003', 'sequencing by synthesis', 'CENTER_NAME',
                 'Baz', 'Illumina HiSeq 2500',
                 '191103_D32611_0365_G00DHB5YXX', 'Baz_p3', 'B99',
                 'iTru7_107_14', 'GTCCTAAG', 'iTru5_01_A', 'CATCTGCT', '3',
                 'Baz', 'Baz.Baz_p3.B99']]
        columns = ['sample_name', 'experiment_design_description',
                   'library_construction_protocol', 'platform', 'run_center',
                   'run_date', 'run_prefix', 'sequencing_meth', 'center_name',
                   'center_project_name', 'instrument_model', 'runid',
                   'sample_plate', 'sample_well', 'i7_index_id', 'index',
                   'i5_index_id', 'index2', 'lane', 'sample_project',
                   'well_description']

        data = [['important-sample1', 'EXPERIMENT_DESC',
                 'LIBRARY_PROTOCOL', 'Illumina', 'UCSDMI', '2019-11-03',
                 'sample1_S11_L003', 'sequencing by synthesis', 'CENTER_NAME',
                 'Baz', 'Illumina HiSeq 2500',
                 '191103_D32611_0365_G00DHB5YXX', 'FooBar_666_p1', 'A3',
                 'iTru7_107_09', 'GCCTTGTT', 'iTru5_01_A', 'AACACCAC', '3',
                 'Baz', 'FooBar_666_p1.sample1.A3'],
                ['important-sample44', 'EXPERIMENT_DESC',
                 'LIBRARY_PROTOCOL', 'Illumina', 'UCSDMI', '2019-11-03',
                 'sample44_S14_L003', 'sequencing by synthesis', 'CENTER_NAME',
                 'Baz', 'Illumina HiSeq 2500',
                 '191103_D32611_0365_G00DHB5YXX', 'Baz_p3', 'B99',
                 'iTru7_107_14', 'GTCCTAAG', 'iTru5_01_A', 'CATCTGCT', '3',
                 'Baz', 'Baz_p3.sample44.B99']]
        exp = pd.DataFrame(data=data, columns=columns)
        obs_df = obs['191103_D32611_0365_G00DHB5YXX.Baz.3']
        pd.testing.assert_frame_equal(obs_df, exp)

        data = [['important-sample1', 'EXPERIMENT_DESC',
                 'LIBRARY_PROTOCOL', 'Illumina', 'UCSDMI', '2019-11-03',
                 'sample1_S11_L001', 'sequencing by synthesis', 'CENTER_NAME',
                 'Baz', 'Illumina HiSeq 2500',
                 '191103_D32611_0365_G00DHB5YXX', 'FooBar_666_p1', 'A3',
                 'iTru7_107_09', 'GCCTTGTT', 'iTru5_01_A', 'AACACCAC', '3',
                 'Baz', 'Baz.FooBar_666_p1.A3'],
                ['important-sample44', 'EXPERIMENT_DESC',
                 'LIBRARY_PROTOCOL', 'Illumina', 'UCSDMI', '2019-11-03',
                 'sample44_S14_L001', 'sequencing by synthesis', 'CENTER_NAME',
                 'Baz', 'Illumina HiSeq 2500',
                 '191103_D32611_0365_G00DHB5YXX', 'Baz_p3', 'B99',
                 'iTru7_107_14', 'GTCCTAAG', 'iTru5_01_A', 'CATCTGCT', '3',
                 'Baz', 'Baz.Baz_p3.B99']]
        data = [['important-sample1', 'EXPERIMENT_DESC',
                 'LIBRARY_PROTOCOL', 'Illumina', 'UCSDMI', '2019-11-03',
                 'sample1_S11_L001', 'sequencing by synthesis', 'CENTER_NAME',
                 'Baz', 'Illumina HiSeq 2500',
                 '191103_D32611_0365_G00DHB5YXX', 'FooBar_666_p1', 'A1',
                 'iTru7_107_07', 'CCGACTAT', 'iTru5_01_A', 'ACCGACAA', '1',
                 'Baz', 'FooBar_666_p1.sample1.A1'],
                ['important-sample2', 'EXPERIMENT_DESC',
                 'LIBRARY_PROTOCOL', 'Illumina', 'UCSDMI', '2019-11-03',
                 'sample2_S10_L001', 'sequencing by synthesis', 'CENTER_NAME',
                 'Baz', 'Illumina HiSeq 2500',
                 '191103_D32611_0365_G00DHB5YXX', 'FooBar_666_p1', 'A2',
                 'iTru7_107_08', 'CCGACTAT', 'iTru5_01_A', 'CTTCGCAA', '1',
                 'Baz', 'FooBar_666_p1.sample2.A2']]
        exp = pd.DataFrame(columns=columns, data=data)
        obs_df = obs['191103_D32611_0365_G00DHB5YXX.Baz.1']
        pd.testing.assert_frame_equal(obs_df, exp)

        data = [['important-sample31', 'EXPERIMENT_DESC',
                 'LIBRARY_PROTOCOL', 'Illumina', 'UCSDMI', '2019-11-03',
                 'sample31_S13_L003', 'sequencing by synthesis',
                 'CENTER_NAME', 'FooBar', 'Illumina HiSeq 2500',
                 '191103_D32611_0365_G00DHB5YXX', 'FooBar_666_p1', 'A5',
                 'iTru7_107_11', 'CAATGTGG', 'iTru5_01_A', 'GGTACGAA', '3',
                 'FooBar_666', 'FooBar_666_p1.sample31.A5'],
                ['important-sample32', 'EXPERIMENT_DESC',
                 'LIBRARY_PROTOCOL', 'Illumina', 'UCSDMI', '2019-11-03',
                 'sample32_S19_L003', 'sequencing by synthesis', 'CENTER_NAME',
                 'FooBar', 'Illumina HiSeq 2500',
                 '191103_D32611_0365_G00DHB5YXX', 'FooBar_666_p1', 'B6',
                 'iTru7_107_12', 'AAGGCTGA', 'iTru5_01_A', 'CGATCGAT', '3',
                 'FooBar_666', 'FooBar_666_p1.sample32.B6'],
                ['important-sample34', 'EXPERIMENT_DESC',
                 'LIBRARY_PROTOCOL', 'Illumina', 'UCSDMI', '2019-11-03',
                 'sample34_S33_L003', 'sequencing by synthesis', 'CENTER_NAME',
                 'FooBar', 'Illumina HiSeq 2500',
                 '191103_D32611_0365_G00DHB5YXX', 'FooBar_666_p1', 'B8',
                 'iTru7_107_13', 'TTACCGAG', 'iTru5_01_A', 'AAGACACC', '3',
                 'FooBar_666', 'FooBar_666_p1.sample34.B8']]
        exp = pd.DataFrame(columns=columns, data=data)
        obs_df = obs['191103_D32611_0365_G00DHB5YXX.FooBar_666.3']
        pd.testing.assert_frame_equal(obs_df, exp)

    def test_remove_qiita_id(self):
        obs = remove_qiita_id('project_1')
        self.assertEqual(obs, 'project')

        obs = remove_qiita_id('project_00333333')
        self.assertEqual(obs, 'project')

        obs = remove_qiita_id('project')
        self.assertEqual(obs, 'project')

        obs = remove_qiita_id('project_')
        self.assertEqual(obs, 'project_')

    def test_get_run_prefix(self):
        # project 1
        obs = get_run_prefix(self.good_run, 'Baz', 'sample1', '1')
        self.assertEqual('sample1_S11_L001', obs)

        obs = get_run_prefix(self.good_run, 'Baz', 'sample1', '3')
        self.assertEqual('sample1_S11_L003', obs)

        obs = get_run_prefix(self.good_run, 'Baz', 'sample2', '1')
        self.assertEqual('sample2_S10_L001', obs)

        obs = get_run_prefix(self.good_run, 'Baz', 'sample2', '3')
        self.assertIsNone(obs)

        # project 2
        obs = get_run_prefix(self.good_run, 'FooBar_666', 'sample31', '3')
        self.assertEqual('sample31_S13_L003', obs)

        obs = get_run_prefix(self.good_run, 'FooBar_666', 'sample32', '3')
        self.assertEqual('sample32_S19_L003', obs)

        obs = get_run_prefix(self.good_run, 'FooBar_666', 'sample34', '3')
        self.assertEqual('sample34_S33_L003', obs)

    def test_is_non_empty_gz_file(self):
        non_empty = os.path.join(self.good_run, 'Baz', 'sample2_S10_L001_R1_00'
                                 '1.fastq.gz')
        self.assertTrue(is_nonempty_gz_file(non_empty))
        non_empty = os.path.join(self.good_run, 'Baz', 'sample2_S10_L001_R2_00'
                                 '1.fastq.gz')
        self.assertTrue(is_nonempty_gz_file(non_empty))

        empty = os.path.join(self.good_run, 'Baz/atropos_qc/sample2_S10_L003_R'
                             '1_001.fastq.gz')
        self.assertFalse(is_nonempty_gz_file(empty))
        empty = os.path.join(self.good_run, 'Baz/atropos_qc/sample2_S10_L003_R'
                             '2_001.fastq.gz')
        self.assertFalse(is_nonempty_gz_file(empty))

    def test_sample_sheet_to_dataframe(self):
        ss = parse_sample_sheet(self.ss)
        obs = sample_sheet_to_dataframe(ss)

        columns = ['lane', 'sample_name', 'sample_plate', 'sample_well',
                   'i7_index_id', 'index', 'i5_index_id', 'index2',
                   'sample_project', 'well_description']
        index = ['sample1', 'sample2', 'sample1', 'sample2', 'sample31',
                 'sample32', 'sample34', 'sample44']

        exp = pd.DataFrame(index=index, data=DF_DATA, columns=columns)
        exp.index.name = 'sample_id'
        pd.testing.assert_frame_equal(obs, exp)

    def test_parse_illumina_run_id(self):
        date, rid = parse_illumina_run_id('161004_D00611_0365_AH2HJ5BCXY')
        self.assertEqual(date, '2016-10-04')
        self.assertEqual(rid, 'D00611_0365_AH2HJ5BCXY')

        date, rid = parse_illumina_run_id('160909_K00180_0244_BH7VNKBBXX')
        self.assertEqual(date, '2016-09-09')
        self.assertEqual(rid, 'K00180_0244_BH7VNKBBXX')

    def test_machine_code(self):
        obs = get_machine_code('K00180')
        self.assertEqual(obs, 'K')

        obs = get_machine_code('D00611')
        self.assertEqual(obs, 'D')

        obs = get_machine_code('MN01225')
        self.assertEqual(obs, 'MN')

        with self.assertRaisesRegex(ValueError,
                                    'Cannot find a machine code. This '
                                    'instrument model is malformed 8675309. '
                                    'The machine code is a one or two '
                                    'character prefix.'):
            get_machine_code('8675309')

    def test_get_model_and_center(self):
        obs = get_model_and_center('D32611_0365_G00DHB5YXX')
        self.assertEqual(obs, ('Illumina HiSeq 2500', 'UCSDMI'))

        obs = get_model_and_center('A86753_0365_G00DHB5YXX')
        self.assertEqual(obs, ('Illumina NovaSeq', 'UCSDMI'))

        obs = get_model_and_center('A00953_0032_AHWMGJDDXX')
        self.assertEqual(obs, ('Illumina NovaSeq', 'IGM'))

        obs = get_model_and_center('A00169_8131_AHKXYNDHXX')
        self.assertEqual(obs, ('Illumina NovaSeq', 'LJI'))

        obs = get_model_and_center('M05314_0255_000000000-J46T9')
        self.assertEqual(obs, ('Illumina MiSeq', 'KLM'))

        obs = get_model_and_center('K00180_0957_AHCYKKBBXY')
        self.assertEqual(obs, ('Illumina HiSeq 4000', 'IGM'))

        obs = get_model_and_center('D00611_0712_BH37W2BCX3_RKL0040')
        self.assertEqual(obs, ('Illumina HiSeq 2500', 'IGM'))

        obs = get_model_and_center('MN01225_0002_A000H2W3FY')
        self.assertEqual(obs, ('Illumina MiniSeq', 'CMI'))


DF_DATA = [
    ['1', 'sample1', 'FooBar_666_p1', 'A1', 'iTru7_107_07', 'CCGACTAT',
     'iTru5_01_A', 'ACCGACAA', 'Baz', 'important-sample1'],
    ['1', 'sample2', 'FooBar_666_p1', 'A2', 'iTru7_107_08', 'CCGACTAT',
     'iTru5_01_A', 'CTTCGCAA', 'Baz', 'important-sample2'],
    ['3', 'sample1', 'FooBar_666_p1', 'A3', 'iTru7_107_09', 'GCCTTGTT',
     'iTru5_01_A', 'AACACCAC', 'Baz', 'important-sample1'],
    ['3', 'sample2', 'FooBar_666_p1', 'A4', 'iTru7_107_10', 'AACTTGCC',
     'iTru5_01_A', 'CGTATCTC', 'Baz', 'important-sample2'],
    ['3', 'sample31', 'FooBar_666_p1', 'A5', 'iTru7_107_11', 'CAATGTGG',
     'iTru5_01_A', 'GGTACGAA', 'FooBar_666', 'important-sample31'],
    ['3', 'sample32', 'FooBar_666_p1', 'B6', 'iTru7_107_12', 'AAGGCTGA',
     'iTru5_01_A', 'CGATCGAT', 'FooBar_666', 'important-sample32'],
    ['3', 'sample34', 'FooBar_666_p1', 'B8', 'iTru7_107_13', 'TTACCGAG',
     'iTru5_01_A', 'AAGACACC', 'FooBar_666', 'important-sample34'],
    ['3', 'sample44', 'Baz_p3', 'B99', 'iTru7_107_14', 'GTCCTAAG',
     'iTru5_01_A', 'CATCTGCT', 'Baz', 'important-sample44']]


if __name__ == "__main__":
    main()
