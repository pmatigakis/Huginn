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
			$("#location .longitude").text(data.fdm_data["position/long-gc-deg"]);
			$("#location .latitude").text(data.fdm_data["position/lat-gc-deg"]);
			$("#location .altitude").text(data.fdm_data["position/h-sl-ft"]);
			$("#location .airspeed").text(data.fdm_data["velocities/vtrue-kts"]);
			$("#location .heading").text(data.fdm_data["attitude/heading-true-rad"] / 0.0174532925);
	      
			var latitude = data.fdm_data["position/lat-gc-deg"];
			var longitude = data.fdm_data["position/long-gc-deg"];
			
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