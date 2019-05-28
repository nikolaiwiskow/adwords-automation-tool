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
	$("#Cost > a").css("color", "black");
	$("#Cost > a").css("font-weight", "bold");
})

// download buttons
$("#dl-button").click(function () {
	$(this).hide();
	$("#dl-button-wrapper").fadeIn(400);

	$("#dl-view").click(function() {
		$("#dl-view > a").attr("href", "download?mode=filtered_result")
	});
	$("#dl-full").click(function() {
		$("#dl-full > a").attr("href", "download?mode=all_data")
	});
	$("#dl-view-data").click(function() {
		$("#dl-view-data > a").attr("href", "download?mode=filtered_raw_data")
	});

	setTimeout(function() {
		$("#dl-button").fadeIn(400);
		$("#dl-button-wrapper").fadeOut(100);
	}, 5000);
});


// provide filtering via url tokens
$(".tagselect").click(function() {
	var url = window.location.href;
	var tag = $(this).text();
	var sep = url.search(/\?/) > -1 ? "&" : "?";

	var regex = new RegExp("tag=([^&]*)");
	var reg = url.match(regex);

	//build new url
	if (reg) {
		url = url.replace(reg[0], "tag="+tag);
	} else {
		url = url + sep + "tag=" + tag;
	}

	window.location = url;

});

// adding and removing datasets to chart
$(".filter").click(function() {
	var id = $(this).attr("id");
	var parent = $(this).parent().attr("id");

	if(id in added_dimensions) {
		removeDataset(id);
		$("#"+ id +" > a").css("color", "");
    	$("#"+ id +" > a").css("font-weight", "");
	} else {
		addDataset(id);
		$("#"+ id +" > a").css("color", "black");
    	$("#"+ id +" > a").css("font-weight", "bold");
	}
});