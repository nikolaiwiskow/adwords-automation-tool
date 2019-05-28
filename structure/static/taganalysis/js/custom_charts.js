var labels = [];
var colors = [];

var charttype = "doughnut";
var datasets = [];
var order_array = [];

var ctx = document.getElementById('myChart').getContext('2d');
var chart = renderChart(ctx);

// renders the chart
function renderChart(ctx) {
	var chart =  new Chart(ctx, {
	// The type of chart we want to create
	type: charttype,

	// The data for our dataset
	data: {
	    datasets: datasets.length === 0 ? [{
	        label: "Cost",
	        data: getDataSet("Cost"),
	        backgroundColor: colors,
	    }] : datasets,
	    labels: labels,
	},

	// Configuration options go here
	options: {
		legend: {display: false},
		title: {display: true},
		plugins: { datalabels: {color: "#000000"}},
		onClick: click,
	}
	});

	if(charttype == "bar") {chart.options.legend["display"] = false;}
	datasets = chart.data.datasets;
	trackKpiOrder();
	return chart;
}


// keeps track of dataset orders, for adding / removal of proper dataset
function trackKpiOrder() {
	order_array = [];
	for(var i in datasets) {
		order_array.push(datasets[i].label);
	}
}


// adds dataset to chart
function addDataset(str_metric) {
	datasets.push({	label: str_metric,
					data: getDataSet(str_metric),
					backgroundColor: colors});

	chart.data.datasets = datasets;
	trackKpiOrder();
	chart.update();
}

// removes dataset from chart
function removeDataset(str_metric) {
	var index = order_array.indexOf(str_metric);
	datasets.splice(index, 1);
	chart.data.datasets = datasets;
	trackKpiOrder();
	chart.update();
}

// switch Charttypes
function setCharttype(str_charttype) {
	chart.destroy();
	charttype = str_charttype;
	chart = renderChart(ctx);
}


//generate dataset
function getDataSet(str_metric) {
	// initial run ops:
	if (datasets.length === 0 && colors.length === 0) {
		getColors();
		labels = [];

		var data = [];
		var sort_helper = {};

		// get data from filtered_data and populate sort_helper for sorting
		for(var i in filtered_data) {
			var data_point = filtered_data[i][str_metric];
			data.push(data_point);
			sort_helper[data_point.toString()] = i;
		}

		//sort data in descending order
		var sorted_data = data.sort(function(a, b) {return b-a});

		// push labels into array in order of data
		for(var j in sorted_data) {
			var label = sort_helper[sorted_data[j].toString()];
			labels.push(label);
		}

		return sorted_data;
	// if there's already a dataset
	} else {
		var data = [];

		for(var i in labels) {
			data.push(filtered_data[labels[i]][str_metric])
		}

		return data;
	}
}


function click(e, array) {
	var url = window.location.href;
	var tag = labels[array[0]._index];
	var sep = url.search(/\?/) > -1 ? "&" : "?";

	var regex = new RegExp("tag=([^&]*)");
	var reg = url.match(regex);

	//build new url
	if (reg && reg[1] == tag) {
		url = url + "&ags=true";
	} else if (reg) {
		url = url.replace(reg[0], "tag="+tag);
	} else {
		url = url + sep + "tag=" + tag;
	}

	window.location = url;
}




//on first run, get colors and labels
function getColors() {
	var basse_colors = ["#66C5CC","#F6CF71","#F89C74","#DCB0F2","#87C55F","#9EB9F3","#FE88B1","#C9DB74","#8BE0A4","#B497E7","#D3B484","#B3B3B3"];
	var base_colors = ["#EF5350", "#EC407A", "#AB47BC", "#7E57C2", "#42A5F5", "#29B6F6", "#26C6DA", "#26A69A", "#9CCC65", "#D4E157", "#FFEE58", "#FFCA28", "#FF7043", "#8D6E63", "#BDBDBD", "#78909C"];
	var index = 0;
	var color_count = base_colors.length;

	for(var i in filtered_data) {
		//colors
		colors.push(base_colors[index]);
		if(index < color_count) {
			index++;
		} else {
			index = 0;
		}
	}
}