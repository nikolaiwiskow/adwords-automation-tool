// set link for charts button
$(document).ready(function() {
	var url = window.location.href;
	url = url.replace("/results", "/charts");
	$("#charts-button").attr("href", url);
});

// DataTable
$(document).ready( function () {
	var height = parseInt($("#data-wrapper").css("height")) - 100;
	//initialize data table
    $('#sorter').DataTable(	{	fixedHeader: true, 
    							responsive: true, 
    							select: true,
    							searching: false,
    							scrollY: height,
    							paging: false,
    							lengthChange: false	});
});

// Navigational Tag Link
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
	var url = window.location.href;
    var device = url.match("device=([^&]*)") ? url.match("device=([^&]*)")[1] : null;
    var matchtype = url.match("matchtype=([^&]*)") ? url.match("matchtype=([^&]*)")[1] : null;

    if(device) {
    	$("#"+ device.toLowerCase()).css("color", "black");
    	$("#"+ device.toLowerCase()).css("font-weight", "bold");
    } else if (matchtype) {
	    $("#"+ matchtype.toLowerCase()).css("color", "black");
	    $("#"+ matchtype.toLowerCase()).css("font-weight", "bold");
    }
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
	} else {
		url = url + "&ags=true";
	}

	//check if question mark still in url
	url = url.search(/\?/) > -1 ? url : url.replace(/\&/, "?");
	console.log(url);
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


//
$(".filter").click(function() {
	var id = $(this).attr("id");
	var parent = $(this).parent().attr("id");

	// get url and check which seperator to use for new token
	var url = window.location.href;
	var sep = url.search(/\?/) > -1 ? "&" : "?";

	//match regex
	var regex = new RegExp("[\?\&]"+parent+"=([^0-9&]*)");
	var reg = url.match(regex);

	//build new url
	if (reg && id=="all") {
		url = url.replace(reg[0], "");
		//check if url still has question mark
		url = url.search(/\?/) > -1 ? url : url.replace(/\&/, "?");
	} else if (reg) {
		url = url.replace(reg[0], reg[0][0] + parent + "=" + id.toUpperCase());
	} else if (id != "all") {
		url = url + sep + parent + "=" + id.toUpperCase();
	}

	window.location = url;
});