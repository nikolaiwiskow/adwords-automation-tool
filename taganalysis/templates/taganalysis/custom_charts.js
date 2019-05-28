console.log("loading");

var filtered_data = JSON.parse('{{ filtered_data|escapejs }}');

var labels = [];
var colors = [];
var datasets_count = 0;

function getColorsAndLabels() {
	var base_colors = ["#66C5CC","#F6CF71","#F89C74","#DCB0F2","#87C55F","#9EB9F3","#FE88B1","#C9DB74","#8BE0A4","#B497E7","#D3B484","#B3B3B3"];
	var index = 0;
	var color_count = base_colors.length();

	for(var i in filtered_data) {
		//colors
		colors.push(base_colors[index]);
		if(index < color_count) {
			index++;
		} else {
			index = 0;
		}

		//labels
		labels.push(i);
	}
}

//generate dataset
function getDataSet(str_metric) {
	if (datasets_count === 0) {
		getColorsAndLabels();
		datasets_count++;
	}

	var data = [];

	//push data-values into dataset
	for(var i in filtered_data) {
		var data_point = filtered_data[i][str_metric];
		data.push(data_point);
	}

	return data;
}



// Chart
var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'doughnut',

    // The data for our dataset
    data: {
        labels: labels,
        datasets: [{
            label: "My First dataset",
            data: getDataSet("Clicks"),
            backgroundColor: colors,
        }],
    },

    // Configuration options go here
    options: {}
});