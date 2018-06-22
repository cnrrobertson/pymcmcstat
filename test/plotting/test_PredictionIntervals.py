# -*- coding: utf-8 -*-

"""
Created on Mon Jan. 15, 2018

Description: This file contains a series of utilities designed to test the
features in the 'PredictionIntervals.py" package of the pymcmcstat module.  The
functions tested include:
    - empirical_quantiles(x, p = np.array([0.25, 0.5, 0.75])):

@author: prmiles
"""
from pymcmcstat.plotting.PredictionIntervals import PredictionIntervals
from pymcmcstat.settings.DataStructure import DataStructure
import unittest
import numpy as np

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

# define test model function
def predmodelfun(data, theta):
    m = theta[0]
    b = theta[1]
    nrow = data.xdata[0].shape[0]
    y = np.zeros([nrow,1])
    y[:,0] = m*data.xdata[0].reshape(nrow,) + b
    return y

def basic_data_structure():
    DS = DataStructure()
    x = np.random.random_sample(size = (100, 1))
    y = np.random.random_sample(size = (100, 1))
    DS.add_data_set(x = x, y = y)
    return DS

def non_basic_data_structure():
    DS = DataStructure()
    x = np.random.random_sample(size = (100, 1))
    y = np.random.random_sample(size = (100, 1))
    DS.add_data_set(x = x, y = y)
    x = np.random.random_sample(size = (100, 1))
    y = np.random.random_sample(size = (100, 2))
    DS.add_data_set(x = x, y = y)    
    return DS

def setup_pseudo_results():
    results = {
            'chain': np.random.random_sample(size = (100,5)),
            's2chain': np.random.random_sample(size = (100,1)),
            'sschain': np.random.random_sample(size = (100,1)),
            'parind': np.random.random_sample(size = (100,1)),
            'local': np.random.random_sample(size = (100,1)),
            'model_settings': {'nbatch': np.random.random_sample(size = (100,1))},
            'theta': np.random.random_sample(size = (1,5)),
            'sstype': np.random.random_sample(size = (100,1)),
            }
    return results

# --------------------------------------------
class Empirical_Quantiles_Test(unittest.TestCase):

    def test_does_default_empirical_quantiles_return_3_element_array(self):
        PI = PredictionIntervals()
        test_out = PI._empirical_quantiles(np.random.rand(10,1))
        self.assertEqual(test_out.shape, (3,1), msg = 'Default output shape is (3,1)')
        
    def test_does_non_default_empirical_quantiles_return_2_element_array(self):
        PI = PredictionIntervals()
        test_out = PI._empirical_quantiles(np.random.rand(10,1), p = np.array([0.2, 0.5]))
        self.assertEqual(test_out.shape, (2,1), msg = 'Non-default output shape should be (2,1)')
        
    def test_empirical_quantiles_should_not_support_list_input(self):
        PI = PredictionIntervals()
#        test_out = empirical_quantiles(np.random.rand(10,1))
        with self.assertRaises(AttributeError):
#            empirical_quantiles(test_out)
            PI._empirical_quantiles([-1,0,1])
            
    def test_empirical_quantiles_vector(self):
        PI = PredictionIntervals()
        out = PI._empirical_quantiles(np.linspace(10,20, num = 10).reshape(10,1), p = np.array([0.22, 0.57345]))
        exact = np.array([[12.2], [15.7345]])
        comp = np.linalg.norm(out - exact)
        self.assertAlmostEqual(comp, 0)
        
# --------------------------------------------
class Observation_Sample_Test(unittest.TestCase):
    
    def test_does_observation_sample_unknown_sstype_cause_system_exit(self):
        PI = PredictionIntervals()
        s2elem = np.array([[2.0]])
        ypred = np.linspace(2.0, 3.0, num = 5)
        ypred = ypred.reshape(5,1)
        sstype = 4
        with self.assertRaises(SystemExit):
            PI._observation_sample(s2elem, ypred, sstype)
            
    def test_does_observation_sample_return_right_size_array(self):
        PI = PredictionIntervals()
        s2elem = np.array([[2.0]])
        ypred = np.linspace(2.0, 3.0, num = 5)
        ypred = ypred.reshape(5,1)
        sstype = 0
        opred = PI._observation_sample(s2elem, ypred, sstype)
        self.assertEqual(opred.shape, ypred.shape)
        
    def test_does_observation_sample_wrong_size_s2elem_break_right_size_array(self):
        PI = PredictionIntervals()
        s2elem = np.array([[2.0, 1.0]])
        ypred = np.linspace(2.0, 3.0, num = 5)
        ypred = ypred.reshape(5,1)
        sstype = 0
        with self.assertRaises(SystemExit):
            PI._observation_sample(s2elem, ypred, sstype)
            
    def test_does_observation_sample_2_column_ypred_right_size_array(self):
        PI = PredictionIntervals()
        s2elem = np.array([[2.0, 1.0]])
        ypred = np.linspace(2.0, 3.0, num = 10)
        ypred = ypred.reshape(5,2)
        sstype = 0
        opred = PI._observation_sample(s2elem, ypred, sstype)
        self.assertEqual(opred.shape, ypred.shape)
        
    def test_does_observation_sample_2_column_ypred_with_1_s2elem_right_size_array(self):
        PI = PredictionIntervals()
        s2elem = np.array([[2.0]])
        ypred = np.linspace(2.0, 3.0, num = 10)
        ypred = ypred.reshape(5,2)
        sstype = 0
        opred = PI._observation_sample(s2elem, ypred, sstype)
        self.assertEqual(opred.shape, ypred.shape)
        
    def test_does_observation_sample_off_s2elem_greater_than_1_cause_system_exit(self):
        PI = PredictionIntervals()
        s2elem = np.array([[2.0, 1.0]])
        ypred = np.linspace(2.0, 3.0, num = 15)
        ypred = ypred.reshape(5,3)
        sstype = 0
        with self.assertRaises(SystemExit):
            PI._observation_sample(s2elem, ypred, sstype)
   
# --------------------------------------------
class AnalyzeDataStructure(unittest.TestCase):
    def test_basic_ds(self):
        PI = PredictionIntervals()
        DS = basic_data_structure()
        ndatabatches, nrows, ncols = PI._analyze_data_structure(data = DS)
        self.assertEqual(ndatabatches, 1, msg = 'Expect 1 batch')
        self.assertEqual(nrows, [100], msg = 'Expect [100]')
        self.assertEqual(ncols, [1], msg = 'Expect [1]')
        
    def test_ds_2_nbatch(self):
        PI = PredictionIntervals()
        DS = non_basic_data_structure()
        ndatabatches, nrows, ncols = PI._analyze_data_structure(data = DS)
        self.assertEqual(ndatabatches, 2, msg = 'Expect 2 batches')
        self.assertEqual(nrows, [100, 100], msg = 'Expect [100, 100]')
        self.assertEqual(ncols, [1, 2], msg = 'Expect [1, 1]')
# --------------------------------------------
class SetupDataStructureForPrediction(unittest.TestCase):
    def test_basic_datapred(self):
        PI = PredictionIntervals()
        DS = basic_data_structure()
        datapred = PI._setup_data_structure_for_prediction(data = DS, ndatabatches = 1)
        self.assertTrue(np.array_equal(datapred[0].xdata[0], DS.xdata[0]), msg = 'Arrays should match')
        self.assertTrue(np.array_equal(datapred[0].ydata[0], DS.ydata[0]), msg = 'Arrays should match')
        
    def test_non_basic_datapred(self):
        PI = PredictionIntervals()
        DS = non_basic_data_structure()
        datapred = PI._setup_data_structure_for_prediction(data = DS, ndatabatches = 2)
        self.assertTrue(np.array_equal(datapred[0].xdata[0], DS.xdata[0]), msg = 'Arrays should match')
        self.assertTrue(np.array_equal(datapred[0].ydata[0], DS.ydata[0]), msg = 'Arrays should match')
        self.assertTrue(np.array_equal(datapred[1].xdata[0], DS.xdata[1]), msg = 'Arrays should match')
        self.assertTrue(np.array_equal(datapred[1].ydata[0], DS.ydata[1]), msg = 'Arrays should match')
# --------------------------------------------
class AssignFeaturesFromResultsStructure(unittest.TestCase):
    def test_feature_assignment(self):
        PI = PredictionIntervals()
        results = setup_pseudo_results()
        PI._assign_features_from_results_structure(results = results)
        PID = PI.__dict__
        check_these = ['chain', 's2chain', 'parind', 'local', 'theta', 'sstype']
        for ct in check_these:
            self.assertTrue(np.array_equal(PID[str('_PredictionIntervals__{}'.format(ct))], results[ct]), msg = str('Arrays should match: {}'.format(ct)))
        
        self.assertTrue(np.array_equal(PID['_PredictionIntervals__nbatch'], results['model_settings']['nbatch']), msg = 'Arrays should match: nbatch')
        
    def test_second_feature_assignment(self):
        PI = PredictionIntervals()
        results = setup_pseudo_results()
        results = removekey(results, 'sstype')
        PI._assign_features_from_results_structure(results = results)
        PID = PI.__dict__
        check_these = ['chain', 's2chain', 'parind', 'local', 'theta']
        for ct in check_these:
            self.assertTrue(np.array_equal(PID[str('_PredictionIntervals__{}'.format(ct))], results[ct]), msg = str('Arrays should match: {}'.format(ct)))
        
        self.assertTrue(np.array_equal(PID['_PredictionIntervals__nbatch'], results['model_settings']['nbatch']), msg = 'Arrays should match: nbatch')
        self.assertEqual(PID['_PredictionIntervals__sstype'], 0, msg = 'Should default to 0')
        
# --------------------------------------------
class DetermineShapeOfReponse(unittest.TestCase):
    def test_basic_modelfunction(self):
        PI = PredictionIntervals()
        DS = basic_data_structure()
        datapred = PI._setup_data_structure_for_prediction(data = DS, ndatabatches = 1)
        nrow, ncol = PI._determine_shape_of_response(modelfunction = predmodelfun, ndatabatches = 1, datapred = datapred, theta = [3.0, 5.0])
        self.assertEqual(nrow, [100], msg = 'Expect [100]')
        self.assertEqual(ncol, [1], msg = 'Expect [1]')
        
    def test_non_basic_modelfunction(self):
        PI = PredictionIntervals()
        DS = non_basic_data_structure()
        datapred = PI._setup_data_structure_for_prediction(data = DS, ndatabatches = 2)
        nrow, ncol = PI._determine_shape_of_response(modelfunction = predmodelfun, ndatabatches = 2, datapred = datapred, theta = [3.0, 5.0])
        self.assertEqual(nrow, [100, 100], msg = 'Expect [100, 100]')
        self.assertEqual(ncol, [1, 1], msg = 'Expect [1, 1]')
 
# --------------------------------------------
class AnalyzeS2Chain(unittest.TestCase):
    def test_s2chain_index_n_eq_1(self):
        PI = PredictionIntervals()
        ndatabatches = 1
        s2chain = np.random.random_sample(size = (100,1))
        ncol = [1]
        s2chain_index = PI._analyze_s2chain(ndatabatches = ndatabatches, s2chain = s2chain, ncol = ncol)
        self.assertTrue(np.array_equal(s2chain_index, np.array([[0,1]])), msg = str('Arrays should match: {}'.format(s2chain_index)))
        
    def test_s2chain_index_n_neq_1_tc_eq_n(self):
        PI = PredictionIntervals()
        ndatabatches = 3
        s2chain = np.random.random_sample(size = (100,3))
        ncol = [1, 1, 1]
        s2chain_index = PI._analyze_s2chain(ndatabatches = ndatabatches, s2chain = s2chain, ncol = ncol)
        self.assertTrue(np.array_equal(s2chain_index, np.array([[0,1],[1,2],[2,3]])), msg = str('Arrays should match: {}'.format(s2chain_index)))
        
        ndatabatches = 3
        s2chain = np.random.random_sample(size = (100,4))
        ncol = [1, 2, 1]
        s2chain_index = PI._analyze_s2chain(ndatabatches = ndatabatches, s2chain = s2chain, ncol = ncol)
        self.assertTrue(np.array_equal(s2chain_index, np.array([[0,1],[1,3],[3,4]])), msg = str('Arrays should match: {}'.format(s2chain_index)))
        
    def test_s2chain_index_n_neq_1_tc_neq_n(self):
        PI = PredictionIntervals()
        ndatabatches = 3
        s2chain = np.random.random_sample(size = (100,3))
        ncol = [1, 2, 1]
        s2chain_index = PI._analyze_s2chain(ndatabatches = ndatabatches, s2chain = s2chain, ncol = ncol)
        self.assertTrue(np.array_equal(s2chain_index, np.array([[0,1],[1,2],[2,3]])), msg = str('Arrays should match: {}'.format(s2chain_index)))
        
    def test_s2chain_index_n_neq_1_tc_neq_n_neq_ndatabatches(self):
        PI = PredictionIntervals()
        ndatabatches = 5
        s2chain = np.random.random_sample(size = (100,3))
        ncol = [1, 2, 1]
        with self.assertRaises(SystemExit, msg = 'Unrecognized data structure'):
            PI._analyze_s2chain(ndatabatches = ndatabatches, s2chain = s2chain, ncol = ncol)