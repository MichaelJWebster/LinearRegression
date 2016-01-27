/*
 * linRegression
 * https://github.com/michaelw/LinearRegression
 *
 * Copyright (c) 2016 Michael Webster
 * Licensed under the MIT license.
 */
//define(function(require, exports, module) {
    var MdArray = require('../../MdArray/lib/MdArray');
    var _ = require("underscore");

    'use strict';

    /**
     * @classdesc Perform Linear regression on a data set. 
     *
     * Construct an initialized linReg object from X and Y. X is an n column
     * MdArray with m rows - where m is the number of examples in the dataset,
     * and n is the number of features. Y is an m X 1 MdArray the value of the
     * dependent variable corresponding to each of the m rows of X.
     *
     * Normalise X according to the normalisation method requested, and then
     * prepend a column of 1's to it.
     *
     * Initialise theta to be an MdArray of n rows by 1 column all set to 0.
     *
     * @param X       An MdArray of independent feature values, with 1 row for
     *                each example in the traning set.
     * @param Y       An MdArray of values of the dependent variable, with 1
     *                value for each example in the training set.
     * @param normalisation
     *                The type of normalisation to use on the features.
     * @param alpha   The learning rate.
     * @param lambda  The regularisation parameter.
     *
     * @returns An initialise linReg object ready to perform linear regression.
     * @constructor
     */
    var linReg = function(X, Y, normalisation, alpha, lambda) {
	'use strict';
	assert(X instanceof MdArray,
	       "linReg: X must be an instance of MdArray.");
	assert(Y instanceof MdArray,
	       "linReg: Y must be an instance of MdArray.");

	this.norm = normalisation || "NONE";
	this.alpha = alpha || 1.0;
	this.lambda = lambda || 0.0;

	this.XOrg = X.copy();
	this.Y = Y;

	this.X = (this.norm == "NONE") ? X : normalise(X, this.norm);
	//console.log("this.X is: " + this.X);
	// Return this for chaining?
	return this;
    };
    
    linReg.prototype = {
	constructor: linReg
    };

    function normalise(X, normType) {
	if (normType === 'MINMAX') {
	    return normaliseMinMax(X);
	}
	else {
	    return normaliseStd(X);
	}
    }

    /**
     * Return a new Md array containing:
     *
     * (xi - mu(col)) / (max(col) - min(col))
     *
     * for each Xi in each column.
     * 
     * @param X    An MdArray containing some columns of data to be normalised.
     *
     * @returns A new MdArray with normalised values from X.
     */
    function normaliseMinMax(X) {
	var maxX = X.max(1);
	console.log("maxX is: " + maxX);
	var minX = X.min(1);
	console.log("minX is: " + minX);
	mu = X.mean(1);
	console.log("mu is: " + mu);
	var denom = maxX.sub(minX);
	console.log("denom == " + denom);
	console.log("X == " + X);
	var XSubMu = X.sub(mu);
	console.log("XSubMu == " + XSubMu);
	var rval = XSubMu.div(denom);
	console.log("rval is:\n" + rval);
	return rval;
    }

    function normaliseStd(X) {
	assert(false, "normaliseStd unimplemented.");
	return X;
    }
    
    /**
     * Raise an error if possible, when there is a violation of the expectations
     * of the ml-ndarray module.
     */
    function assert(condition, message) {
	'use strict';
	if (!condition) {
            message = message || "Assertion failed";
            if (typeof Error !== "undefined") {
		throw new Error(message);
            }
            throw message;
	}
    }

    module.exports = linReg;

//}();

