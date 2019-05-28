// DataTable & Navigational Tag Link
$(document).ready( function () {
    //build going back link
    var url = window.location.href;
	var reg = url.match("[\&\?]tag=([^&]*)");
	var tags = reg ? reg[1].split(".") : [];
	var parts = tags.length

	if (reg && parts > 2) {
		tag = "";
		for (i=1; i<parts-1; i++) {
			tag += "." + tags[i];
		}
		url = url.replace(reg[0], reg[0][0]+"tag="+tag); 

	} else if (reg) { 	
		url = url.replace(reg[0], "");
		tag = "/";	

	} else {
		tag = "";
	}

	url = url.search(/\?/) > -1 ? url : url.replace(/\&/, "?");
	$("#path > a").text(tag);
    $("#path > a").attr("href", url);
} );

//color selected selectors black
$(document).ready(function () {
	$("#Cost").css("color", "black");
	$("#Cost").css("font-weight", "bold");
})

// download buttons
$("#dl-button").click(function () {
	$("#charts-dl-buttons").hide();
	$("#dl-button-wrapper").fadeIn(400);

	$("#dl-view").click(function() {
		$("#dl-view").attr("href", "download?mode=filtered_result")
	});
	$("#dl-full").click(function() {
		$("#dl-full").attr("href", "download?mode=all_data")
	});
	$("#dl-view-data").click(function() {
		$("#dl-view-data").attr("href", "download?mode=filtered_raw_data")
	});

	setTimeout(function() {
		$("#dl-button-wrapper").fadeOut(200);
		$("#charts-dl-buttons").fadeIn(400);
	}, 5000);
});


$("#ag-button").click(function() {
	var url = window.location.href;
	var reg = url.match("([\?\&])ags=true");

	if(reg) {
		url = url.replace(reg[0], "");
		//check if question mark still in url
		url = url.search(/\?/) > -1 ? url : url.replace(/\&/, "?");
	} else {
		url = url + "&ags=true";
		url = url.search(/\?/) > -1 ? url : url.replace(/\&/, "?");
	}
	window.location = url;
});

// provide filtering via url tokens
$(".tagselect").click(function() {
	var url = window.location.href;
	var tag = $(this).text();
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
});

// adding and removing datasets to chart
$("#kpis > .filter").click(function() {
	var id = $(this).attr("id");
	var parent = $(this).parent().attr("id");

	if(order_array.indexOf(id) > -1) {
		removeDataset(id);
		$("#"+ id).css("color", "");
    	$("#"+ id).css("font-weight", "");
	} else {
		addDataset(id);
		$("#"+ id).css("color", "black");
    	$("#"+ id).css("font-weight", "bold");
	}
});

// set charttypes buttons
$("#charttypes > .filter").click(function() {
	var id = $(this).attr("id");
	setCharttype(id);
});

// link for table/chart button
$(document).ready(function() {
	var url = window.location.href;
	url = url.replace("/charts", "/results");
	$("#charts-button").attr("href", url);
})