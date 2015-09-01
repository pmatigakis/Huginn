var map;
var follow_aircraft;
var aircraft_marker;
var myhud;

function init_map(){
	map = L.map('map').setView([51.0, 0.0], 13);
	
	L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
		attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);
	
	var aircraftIcon = L.icon({
	    iconUrl: 'static/images/32px-Airplane_silhouette.png',

	    iconSize:     [32, 32],
	    iconAnchor:   [16, 16]
	});
	
	aircraft_marker = L.marker([51.0, 0.0], {icon: aircraftIcon}).addTo(map);
} 

function start_update(){
	setInterval(function(){
		$.getJSON("fdmdata", function(data){
			myhud.roll = data.fdm_data["roll"];
			myhud.pitch = data.fdm_data["pitch"];
			myhud.airspeed = data.fdm_data["airspeed"];
			myhud.altitude = data.fdm_data["altitude"];
			myhud.heading = data.fdm_data["heading"];
			
			myhud.draw();
			
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
	
	var primaryFlightDisplayCanvas = document.getElementById("primary_flight_diplay");
    
	myhud = new Avionics.PrimaryFlightDisplay(primaryFlightDisplayCanvas);
	
	myhud.roll = 0.0;
	myhud.pitch = 0.0;
	myhud.airspeed = 0.0;
	myhud.altitude = 0.0;
	myhud.heading = 0.0;
	
	myhud.draw();
	
	start_update();
	
	follow_aircraft = $("#follow_aircraft").is(":checked");
	
	$("#follow_aircraft").click(function(){
		follow_aircraft = this.checked;
	});
})