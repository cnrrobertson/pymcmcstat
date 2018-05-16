#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 10:30:29 2018

@author: prmiles
"""
# import required packages
import numpy as np
from scipy.special import expit
from ..structures.ParameterSet import ParameterSet

class Metropolis:
    # -------------------------------------------
    def run_metropolis_step(self, old_set, parameters, R, prior_object, sos_object):
        '''
        Run Metropolis step
        
        **Args:**
            * **old_set** (:class:`~.ParameterSet`): Features of :math:`q^{k-1}`
            * **parameters** (:class:`~.ModelParameters`): Model parameters
            * **R** (:class:`~numpy.ndarray`): Cholesky decomposition of parameter covariance matrix
            * **priorobj** (:class:`~.PriorFunction`): Prior function
            * **sosobj** (:class:`~.SumOfSquares`): Sum-of-Squares function

        **Returns:**
            * **accept** (:py:class:`int`): 0 - reject, 1 - accept
            * **newset** (:class:`~.ParameterSet`): Features of :math:`q^*`
            * **outbound** (:py:class:`int`): 1 - rejected due to sampling outside of parameter bounds
            * **npar_sample_from_normal** (:class:`~numpy.ndarray`): Latet random sample points
        '''
           
        # unpack oldset
        oldpar, ss, oldprior, sigma2 = self.unpack_set(old_set)
        
        # Sample new candidate from Gaussian proposal
        npar_sample_from_normal = np.random.randn(1, parameters.npar)
        newpar = oldpar + np.dot(npar_sample_from_normal,R)   
        newpar = newpar.reshape(parameters.npar)
           
        # Reject points outside boundaries
        outsidebounds = self.is_sample_outside_bounds(newpar, parameters._lower_limits[parameters._parind[:]], parameters._upper_limits[parameters._parind[:]])
        if outsidebounds is True:
            # proposed value outside parameter limits
            accept = 0
            newprior = 0
            alpha = 0
            ss1 = np.inf
            ss2 = ss
            outbound = 1
        else:
            outbound = 0
            # prior SS for the new theta
            newprior = prior_object.evaluate_prior(newpar) 
            # calculate sum-of-squares
            ss2 = ss # old ss
            ss1 = sos_object.evaluate_sos_function(newpar)
            # evaluate likelihood
            alpha = self.evaluate_likelihood_function(ss1, ss2, sigma2, newprior, oldprior)
            # make acceptance decision
            accept = self.acceptance_test(alpha)
                    
        # store parameter sets in objects    
        newset = ParameterSet(theta = newpar, ss = ss1, prior = newprior, sigma2 = sigma2, alpha = alpha)
        
        return accept, newset, outbound, npar_sample_from_normal
    
    def unpack_set(self, parset):
        '''
        Unpack parameter set
        
        **Args:**
            * **parset** (:class:`~.ParameterSet`): Parameter set to unpack
            
        **Returns:**
            * **theta** (:class:`~numpy.ndarray`): Value of sampled model parameters
            * **ss** (:class:`~numpy.ndarray`): Sum-of-squares error using sampled value
            * **prior** (:class:`~numpy.ndarray`): Value of prior
            * **sigma2** (:class:`~numpy.ndarray`): Error variance
        '''
        theta = parset.theta
        ss = parset.ss
        prior = parset.prior
        sigma2 = parset.sigma2
        return theta, ss, prior, sigma2
    
    def is_sample_outside_bounds(self, theta, lower_limits, upper_limits):
        '''
        Check whether proposal value is outside parameter limits
        
        **Args:**
            * **theta** (:class:`~numpy.ndarray`): Value of sampled model parameters
            * **lower_limits** (:class:`~numpy.ndarray`): Lower limits
            * **upper_limits** (:class:`~numpy.ndarray`): Upper limits
            
        **Returns:**
            * **outsidebounds** (:py:class:`bool`): True -> Outside of parameter limits
        '''
        if (theta < lower_limits).any() or (theta > upper_limits).any():
            outsidebounds = True
        else:
            outsidebounds = False
        return outsidebounds
    
    def evaluate_likelihood_function(self, ss1, ss2, sigma2, newprior, oldprior):
        '''
        Evaluate likelihood function:
            
        :math:`\alpha = \exp[-0.5\Big(\sum(\frac{ss_1 - ss_2}{\sigma^2}) + p_1 - p_2\Big)]`
            
        '''
        alpha = expit(-0.5*(sum((ss1 - ss2)*(sigma2**(-1))) + newprior - oldprior))
        return sum(alpha)
    
    def acceptance_test(self, alpha):
        '''
        Run standard acceptance test
        
        **Args:**
            * **alpha** (:py:class:`float`): Result of likelihood function            
        **Returns:**
            * **accept** (:py:class:`int`): 0 - reject, 1 - accept
        '''
        if alpha <= 0:
                accept = 0
        elif alpha >= 1 or alpha > np.random.rand(1,1):
            accept = 1
        else:
            accept = 0
            
        return accept
    
    