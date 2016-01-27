import argparse
import sys
import os, os.path
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rc, cm

class linReg(object):
    '''
    This class performs multi variable linear regression.
    '''
    #
    # Some constants
    #
    MINMAX = "min_max"
    STD    = "std"
    NONE   = "None"

    # theta0 is the first parameter of the best fit line function.
    theta = None

    # theta0 is the first parameter of the best fit line function.
    thetaNew = None

    # The learning rate parameter.
    alpha = None

    # The regularisation parameter.
    lbda = 0

    # The training set X values
    X = None

    # The type of normalisation being done, if any
    normalisationType = None
    
    # The training set Y values
    Y = None    

    # The size of the training set.
    m = None

    # The number of features in the data set
    nFeatures = None

    def __init__(self, tSet, normalisation = MINMAX, alpha = 0.01, lbda=0.0):
        """
        Construct the linear regression object by splitting tSet into nFeatures
        columns in X, and 1 column in Y. Normalise X according to the
        normalisation method requested, and then prepend a column of 1's to
        it. Initialise theta to be all 0s.

        Args:
            tSet:         A matrix containing m feature value columns, and a Y
                          column.
            normlisation: The normalisation method we'd like to use.
            alpha:        The learning rate for the linear regression algorithm.
        """
        # X is all columns but the last one.
        self.normalisationType = normalisation
        self.alpha = float(alpha)
        self.lbda = float(lbda)
        self.X = tSet[0:, :-1].astype(float)
        self.XOrg = np.copy(self.X)        
        self.Y = tSet[0:, -1:].astype(float)
        self.normaliseFeatures()
        #ones = np.ones(len(tSet)).reshape(len(tSet),1)
        #self.X = np.append(ones, self.X, axis=1)
        #self.m, self.nFeatures = self.X.shape
        #self.theta = np.ones((self.nFeatures, 1), dtype=np.float)

    def normaliseFeatures(self):
        """
        Normalise each feature column according to the normalisation type
        requested. Back up self.X first.
        """
        if (self.normalisationType != linReg.NONE):
            if (self.normalisationType == linReg.MINMAX):
                self.X = linReg.normaliseMinMax(self.X)
            else:
                self.X = linReg.normaliseStdDev(self.X)

    @staticmethod
    def normaliseMinMax(X):
        """
        Return a matrix containing (xi - mu(col))/(max(col) - min(col)) for each
        xi and each column.

        Args:
            X: A matrix containin m feature values for n training set examples.

        Returns:
            The matrix with normalised columns created by replacing each
            value xi from column j by (xi - mu(j))/(max(j) - min(j)).
        """
        maxX = X.max(0)
        print("maxX is: %s" % maxX)
        minX = X.min(0)
        print("minX is: %s" % minX)
        mu = X.mean(0)
        print("mu is: %s" % mu)
        denom = maxX - minX
        print("denom == %s" % denom)
        print("X is:\n%s" % X)
        XSubMu = X - mu
        print("XSubMu =\n %s" % XSubMu)
        rval = XSubMu/denom
        print("rval =\n %s" % rval)
        return rval

    @staticmethod
    def normaliseStdDev(X):
        """
        Return a matrix containing (xi - mu(col))/(sigma(col)) for each
        xi and each column.

        Args:
            X: A matrix containin m feature values for n training set examples.

        Returns:
            The matrix with normalised columns created by replacing each value
            xi from column j by (xi - mu(j))/(std deviation over col j).
        """
        mu = X.mean(0)
        sigma = X.std(0)
        return (X - mu)/sigma


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage = sys.argv[0] + \
       " Perform Linear Regression.")

    parser.add_argument                                                     \
    (                                                                       \
        '-d',                                                               \
        dest='data_file', action='store',                                \
        help='The File containing the genome sequence to be searched.'      \
    )

    args = parser.parse_args()
    aDfile = args.data_file
    if not os.path.exists(aDfile):
        print("Error: Cannot find the %s data file." % aDfile)
        sys.exit(-1)
    df = pd.read_csv(aDfile)
    df = df[["Father", "Mother", "Gender", "Height"]]
    dfMale = df[df["Gender"] == "M"].drop(["Gender"], axis=1)
    rgMale = linReg(np.asarray(dfMale), normalisation=linReg.MINMAX, alpha=1.0)
    #print("X is:\n %s" % rgMale.X)
    sys.exit(0)
        
