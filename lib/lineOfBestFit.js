var exports = module.exports = {};
'use strict';
var _us = require("underscore");
var fs = require('fs');
var parse = require('csv-parse');
// Maybe try fast-csv - looks like easier.
//var rs = fs.createReadStream("./MergedOECDData.csv");
var dFile = "MergedOECDData.csv";
rs = fs.createReadStream(dFile);

var parsedIntoColumns = function(rs, cb)
{
    var newTable;
    var output = [];
    /*var parser = parse(null, function(err, data) {
	var header = data[0];
	var columns = _us.unzip(_us.rest(data, 1));
	newTable = _us.object(header, columns);
     });*/
    var parser = parse();
    parser.on('readable', function() {
	var record;
	while (record = parser.read()) {
	    output.push(record);
	}
    });

    parser.on('error', function() {
	console.log(err.message);
    });
	      
    parser.on('finish', function() {
	var header = output[0];
	var columns = _us.unzip(_us.rest(output, 1));
	var newTable = _us.object(header, columns);
	cb(newTable);
    });
    
    parser.on('error', function(err) {
	console.log(err.message);
    });

    rs.pipe(parser);
};

var cBestFit = function(XName, YName) {
    return function(data) {
	var X = {};
	X[XName] = data[XName];
	var Y = {};
	Y[YName] = data[YName];
	calcBestFit(X, Y);
    };
};
    
parsedIntoColumns(rs, cBestFit('Gini Coefficient', 'Deaths per 1000 Births'));
parsedIntoColumns(rs, cBestFit('Gini Coefficient', 'Suicides per 100000'));

bestFitLines = {};

function calcBestFit(X, Y) {
    var xKey = _us.keys(X)[0];
    var xVals = _us.map(X[xKey], function(d) {
	return isNaN(d) ? d : Number(d);
    });
    var yKey = _us.keys(Y)[0];
    var yVals = _us.map(Y[yKey], function(d) {
	return isNaN(d) ? d : Number(d);
    });

    console.log("Calculating Best Fit for: " + xKey + " against " + yKey);

    var xSum = _us.reduce(xVals, function(memo, num) {
	return memo + num;
    }, 0);
    var xBar = xSum/xVals.length;
    console.log("xSum is: " + xSum + " xBar is: " + xBar);
    var ySum = _us.reduce(yVals, function(memo, num) {
	return memo + num;
    }, 0);
    var yBar = ySum/yVals.length;
    console.log("ySum is: " + ySum + " yBar is: " + yBar);

    var xy = _us.zip(xVals, yVals);
    var topSum = _us.reduce(xy, function(memo, vals) {
	return memo + (vals[0] - xBar) * (vals[1] - yBar);
    }, 0);
    console.log("topSum is: " + topSum);

    var sumX2 = _us.reduce(xVals, function(memo, x) {
	return memo + Math.pow((x - xBar), 2);
    }, 0);

    var slope = topSum/sumX2;
    console.log("slope is: " + slope);

    var b = yBar - slope * xBar;
    var result = { "m" : slope, "b" : b };
    return result;
}













