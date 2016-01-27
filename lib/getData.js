var exports = module.exports = {};
'use strict';
var _us = require("underscore");
var fs = require('fs');
var parse = require('csv-parse');
var MdArray = require('../../MdArray/lib/MdArray');
var linReg = require('linRegression');

var parsedIntoColumns = function(rs, cb)
{
    var newTable;
    var output = [];
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

var main = function() {
    var dFile = "Galton.csv";
    rs = fs.createReadStream(dFile);
    parsedIntoColumns(rs, runRegression);
};

function enumerateTable(tbl) {
    _us.each(_us.keys(tbl), function(k) {
	console.log("Key = " + k);
	console.log("Length of tbl[" + k + "] = " + tbl[k].length);
    });
}

function runRegression(tbl) {
    var requiredData  = {};
    var maleData = { Father: [], Mother: [], Height: []};
    var femaleData = { Father: [], Mother: [], Height: []};
    _us.each(tbl.Gender, function(el, idx) {
	var currentData = maleData;
	if (el == 'F') {
	    currentData = femaleData;
	}
	currentData.Father.push(Number(tbl.Father[idx]));
	currentData.Mother.push(Number(tbl.Mother[idx]));
	currentData.Height.push(Number(tbl.Height[idx]));
    });

    _us.each(_us.keys(maleData), function(k) {
	console.log("Male Data has key == " + k);
	console.log("Male Data length is: " + maleData[k].length);
    });
    var xData = _us.zip(maleData.Father, maleData.Mother,
			    maleData.Height);
    //xData = _us.shuffle(xData);
    //var divided = divideData(xData, [60,20,20]);
    //var trainData = divided[0];
    var trainData = xData;
    var x = [];
    var y = [];
    _us.each(trainData, function(val) {
	x.push([val[0], val[1]]);
	y.push(val[2]);
    });

    var X = MdArray.createFromRows(x);
    var Y = new MdArray({data : y, shape: [y.length, 1]});

    var linreg = new linReg(X, Y, 'MINMAX');
}

/**
 * Shuffle the data d into a new copy of d randomly shuffled.
 *
 * @param d      An arra or other type of collection to be shuffled.
 *
 * @returns A version of d that has been shuffled using underscore's
 *          implementation.
 */
function shuffleData(d) {
    return _us.shuffle(d);
};

/**
 * Return an array containing the data d divided up according to the
 * proporations in the array proportions.
 *
 * @param d       An array containing an entry for each element in the
 *                dataset
 * @param proportions
 *                An array containing the proportions into which the data
 *                is to be divided.
 * @returns An array containing arrays for each division of data found.
 */
function divideData(d, proportions) {
    var divided = [];
    var numPortions = _us.reduce(proportions, function(memo, val) {
	return memo + Number(val);
    }, 0);
    var currentStart = 0;
    for (var i = 0; i < proportions.length; i++) {
	var portionSize = Math.ceil(d.length * proportions[i]/ numPortions);	    
	var nextPortion = d.slice(currentStart, currentStart + portionSize);
	divided.push(nextPortion);
	currentStart += portionSize;
    }
    return divided;
};


if (require.main === module) {
    main();
}















