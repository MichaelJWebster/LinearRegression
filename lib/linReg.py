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

    def __init__(self, tSet, normalisation = MINMAX, alpha = 1.0, lbda=0.0):
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
        ones = np.ones(len(tSet)).reshape(len(tSet),1)
        self.X = np.append(ones, self.X, axis=1)
        print("X with 0nes is:\n%s" % self.X)
        self.m, self.nFeatures = self.X.shape
        self.theta = np.ones((self.nFeatures, 1), dtype=np.float)

    def normaliseFeatures(self):
        """
        Normalise each feature column according to the normalisation type
        requested. Back up self.X first.
        """
        if (self.normalisationType != linReg.NONE):
            if (self.normalisationType == linReg.MINMAX):
                self.X = self.normaliseMinMax(self.X)
            else:
                self.X = self.normaliseStdDev(self.X)

    def normaliseMinMax(self, X):
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
        minX = X.min(0)
        mu = X.mean(0)
        denom = maxX - minX
        XSubMu = X - mu
        rval = XSubMu/denom
        self.normalise = normaliseMinMax(maxX, minX, mu)
        return rval

    def normaliseStdDev(self, X):
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
        rval = (X - mu)/sigma
        self.normalise = normaliseSTD(mu, sigma)
        return rval

    @staticmethod
    def costFn(theta, X, Y):
        """
        Return the value of J(Theta) at X, Y.
        
        Args:
            theta:  The theta vector to run through the cost function.
            X:      An array or matrix of features.
            Y:      The actual observed values for Y.

        Returns:
            The cost for the particular theta.
        """
        lenX, _ = Y.shape
        yh = X.dot(theta).reshape(X.shape[0], 1)
        diff_vector = yh - Y
        cost_val = (np.square(diff_vector)).sum() / float(2 * lenX)
        return cost_val
    
    @staticmethod
    def regLinRegGrad(X, Y, theta, alpha, lbda):
        # grad is the same shape as theta.
        m = X.shape[0]
        theta = theta.reshape(max(theta.shape), 1)
        grad = np.zeros((theta.shape), dtype=np.float)
        #print("theta.shape is %s" % str(theta.shape))
        h_theta = X.dot(theta)
        grad[0] = (alpha/m) * ((h_theta - Y) * X[:, 0].reshape(X.shape[0],1)).sum()
        print("grad[0] is: %f\n" % grad[0])
        mainSum = ((h_theta - Y) * X[:, 1:]).sum(axis=0)
        print("mainSum is: %s\n" % mainSum)
        mainSum = mainSum.reshape(mainSum.shape[0], 1)
        print("mainSum2 is: %s\n" % mainSum)
        grad[1:] = ((alpha/m) * (mainSum + lbda * theta[1:]))
        print("grad is: %s\n" % grad);
        return grad
    
    def updateHyp(self):
        """
        Update the hypothesis by calculating new theta values.
        """
        grad = linReg.regLinRegGrad(self.X, self.Y, self.theta, self.alpha, self.lbda)
        self.theta = self.theta - grad
    
    def runRegression(self, numIters, costs=False):
        """
        Run the regression, and return costs if requested.
        
        Args:
            numIters:  The number of times to iterate.
            costs:     Record costs, and return them.
        Returns:
        An array containing costs if costs is True, otherwise None;
        """
        i = 0
        costVals = None
        if costs:
            costVals = np.zeros(numIters)
        while i < numIters:
            self.updateHyp()
            if costs:
                costVals[i] = linReg.costFn(self.theta, self.X, self.Y)
            i += 1
        return costVals

    def predict(self, X):
        normalisedX = self.normalise(X)
        normalisedX = np.append(np.ones((1,1)), normalisedX, axis=1)
        return normalisedX.dot(self.theta).reshape(normalisedX.shape[0], 1)

def normaliseMinMax(maxX, minX, mu):
    denom = float(maxX) - float(minX)
    def nminMax(X):
        return (X - mu)/denom
    return nminMax

def normaliseSTD(mu, sigma):
    def nstd(X):
        return (X - mu) / sigma
    return nstd


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
    rgMale = linReg(np.asarray(dfMale), normalisation=linReg.STD, alpha=0.5)

    costs = rgMale.runRegression(20, costs=True)
    for i in range(0, len(costs)):
        print("cost[%d] is: %f" % (i, costs[i]))
    print("theta = %s" % str(rgMale.theta))
    XEg = np.array([70, 63]).reshape(1, 2)
    x = rgMale.predict(XEg)
    print("x predicted is:\n%s" % x)
    #dfMale = dfMale.drop(["Mother"], axis=1)
    #rgMale = linReg(np.asarray(dfMale))
    #rgMale.plotRegression(2000)
    #print("theta = %s" % str(rgMale.theta))
    #rgMale.plotBestFit()    
    sys.exit(0)
        
