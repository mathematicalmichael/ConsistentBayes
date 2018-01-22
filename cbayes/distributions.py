#!/home/mpilosov/anaconda3/envs/py3/bin/python
## Copyright (C) 2018 Michael Pilosov
import scipy.stats as sstats
from scipy.stats import gaussian_kde
"""
This module defines supported distributions and associated utility functions.
They are as follows:
    :class:`cbayes.distributions.gkde` (needs test)
    :class:`cbayes.distributions.parametric_dist` (needs development) 
    :method:`cbayes.distributions.supported_distributions` (tested)
    :method:`cbayes.distributions.assign_dist` (tested)
"""

def supported_distributions(d=None):
    """
    TODO flesh out description.
    currently supports 'normal' and 'uniform'
    
    rtype: :class:`scipy.stats._distn_infrastructure`
    :returns: scipy distribution object 
    
    rtype: :dict:
    :returns: dictionary with supported types.
    """
    # 
    # both take kwags `loc` and `scale` of type `numpy.ndarray` or `list`
    # method `sample_set.set_dist` just creates a handle for the chosen distribution. The longer of 
    # `loc` and `scale` is then inferred to be the dimension, which is written to sample_set.dim

    #: DICTIONARY OF SUPPORTED DISTRIBUTIONS:
    D = {
        'normal': sstats.norm, 
        'uniform': sstats.uniform,
        }

    if d is not None: 
        if d.lower() in ['gaussian', 'gauss', 'normal', 'norm', 'n']:
            d = 'normal'
        elif d.lower() in  ['uniform', 'uni', 'u']:
            d = 'uniform'

        try:
            return D.get(d)
        except KeyError:
            print('Please specify a supported distribution. Type `?supported_distributions`')
    else: # if d is unspecified, simply return the dictionary.
        return D

def assign_dist(distribution, *kwags):
    """
    TODO clean up description of how this is overloaded.
    If a string is passed, it will be matched against the options for `supported_distributions`
    attach the scipy.stats._continuous_distns class to our sample set object
    
    rtype: :class:`scipy.stats._distn_infrastructure`
    :returns: scipy distribution object 
    """
    if type(distribution) is str:
        distribution = supported_distributions(distribution)
    return distribution(*kwags)

class gkde(object):
    """
    
    Custom wrapper around `scipy.stats.gaussian_kde` to conform
    to our prefered size indexing of (num, dim). 

    """

    def __init__(self, data):
        self.kde_object = gaussian_kde( data.transpose() )
        #: This is the primary difference
        self.d = self.kde_object.d
        self.n = self.kde_object.n

    def rvs(self, size=1):
        """
        Generates random variables from a kde object. Wrapper function for 
        `scipy.stats.gaussian_kde.resample`.
        
        :param int size: number of random samples to generate
        :param tuple size: number of samples is taken to be the first argument
        """
        if type(size) is tuple: 
            size=size[0]
        return self.kde_object.resample(size).transpose()
        #TODO write a test that makes sure this returns the correct shape
    
    def pdf(self, eval_points):
        """
        Generates random variables from a kde object. Wrapper function for 
        `scipy.stats.gaussian_kde.pdf`.
        
        :param eval_points: points on which to evaluate the density.
        :type eval_points: :class:`numpy.ndarray` of shape (num, dim)
        """
        
        p = self.kde_object.pdf( eval_points.transpose() ).reshape(eval_points.shape)
        #: TODO write a test that makes sure this returns the correct shape
        # alternative syntax:
        # p = self.kde_object.pdf( eval_points.transpose() ) 
        # p = p[:,np.newaxis]
        return p
    
class parametric_dist(object): 
    """
    TODO: add description. 
    TODO: add actual math. this is supposed to mimick scipy.stats, 
        except generalized to arbitrary mixtures, using familiar syntax 
        that hides the complexity
    """
    def __init__(self, dim):
        self.dim = dim
        self.distributions = {str(d): None for d in range(dim)}
        
    def rvs(self, size = None):
        if size is None: # if nothing specified, just generate one draw from the distribution of the RV
            size = (self.dim, 1)
        #TODO parse dict, hcat results.
        pass 

    def args(self): 
        pass

