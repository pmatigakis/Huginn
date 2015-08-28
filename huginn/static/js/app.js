var map;
var follow_aircraft;
var aircraft_marker;

function init_map(){
	map = L.map('map').setView([51.0, 0.0], 13);
	
	L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
		attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);
	
	aircraft_marker = L.marker([51.0, 0.0]).addTo(map);
} 

function start_map_update(){
	setInterval(function(){
		$.getJSON("fdmdata", function(data){
			$("#location .longitude").text(data.fdm_data["longitude"]);
			$("#location .latitude").text(data.fdm_data["latitude"]);
			$("#location .altitude").text(data.fdm_data["altitude"]);
			$("#location .airspeed").text(data.fdm_data["airspeed"]);
			$("#location .heading").text(data.fdm_data["heading"]);
	      
			var latitude = data.fdm_data["latitude"];
			var longitude = data.fdm_data["longitude"];
			
			if(follow_aircraft){
	    		map.setView([latitude, longitude], 13);
			}
			
			aircraft_marker.setLatLng([latitude, longitude]);
		});
	}, 1000);
}

$(document).ready(function(){
	init_map();
	start_map_update();
	
	follow_aircraft = $("#follow_aircraft").is(":checked");
	
	$("#follow_aircraft").click(function(){
		follow_aircraft = this.checked;
	});
})