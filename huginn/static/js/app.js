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

function update_hud(altitude, airspeed, heading, roll, pitch){
	myhud.roll = roll;
	myhud.pitch = pitch;
	myhud.airspeed = airspeed;
	myhud.altitude = altitude;
	myhud.heading = heading;
	
	myhud.draw();
}

function update_map(latitude, longitude, altitude, airspeed, heading){	
	$("#location .longitude").text(longitude);
	$("#location .latitude").text(latitude);
	$("#location .altitude").text(altitude);
	$("#location .airspeed").text(airspeed);
	$("#location .heading").text(heading);
  
	if(follow_aircraft){
		map.setView([latitude, longitude], 13);
	}
	
	aircraft_marker.setLatLng([latitude, longitude]);
}

function start_data_update(){
	setInterval(function(){
		$.getJSON("ins", function(data){
			var roll = data.fdm_data["roll"];
			var pitch = data.fdm_data["pitch"];
			var airspeed = data.fdm_data["airspeed"];
			var altitude = data.fdm_data["altitude"];
			var heading = data.fdm_data["heading"];
			var latitude = data.fdm_data["latitude"];
			var longitude = data.fdm_data["longitude"];
			
			update_hud(altitude, airspeed, heading, roll, pitch);
			update_map(latitude, longitude, altitude, airspeed, heading);
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
	
	start_data_update();
	
	follow_aircraft = $("#follow_aircraft").is(":checked");
	
	$("#follow_aircraft").click(function(){
		follow_aircraft = this.checked;
	});
})