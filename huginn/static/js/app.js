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
	    iconUrl: 'images/32px-Airplane_silhouette.png',

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

function update_map(latitude, longitude){	  
	if(follow_aircraft){
		map.setView([latitude, longitude], 13);
	}
	
	aircraft_marker.setLatLng([latitude, longitude]);
}

function update_fdm_data_table(data){
	$("#fdm-data .longitude").text(data["longitude"]);
	$("#fdm-data .latitude").text(data["latitude"]);
	$("#fdm-data .altitude").text(data["altitude"]);
	$("#fdm-data .airspeed").text(data["airspeed"]);
	$("#fdm-data .heading").text(data["heading"]);
	$("#fdm-data .x-acceleration").text(data["x_acceleration"]);
	$("#fdm-data .y-acceleration").text(data["y_acceleration"]);
	$("#fdm-data .z-acceleration").text(data["z_acceleration"]);
	$("#fdm-data .roll-rate").text(data["roll_rate"]);
	$("#fdm-data .pitch-rate").text(data["pitch_rate"]);
	$("#fdm-data .yaw-rate").text(data["yaw_rate"]);
	$("#fdm-data .temperature").text(data["temperature"]);
	$("#fdm-data .static-pressure").text(data["static_pressure"]);
	$("#fdm-data .total-pressure").text(data["total_pressure"]);
	$("#fdm-data .roll").text(data["roll"]);
	$("#fdm-data .pitch").text(data["pitch"]);
	$("#fdm-data .thrust").text(data["thrust"]);
	$("#fdm-data .aileron").text(data["aileron"]);
	$("#fdm-data .elevator").text(data["elevator"]);
	$("#fdm-data .rudder").text(data["rudder"]);
	$("#fdm-data .throttle").text(data["throttle"]);
}

function start_data_update(){
	setInterval(function(){
		$.getJSON("fdm", function(data){
			var roll = data["roll"];
			var pitch = data["pitch"];
			var airspeed = data["airspeed"];
			var altitude = data["altitude"];
			var heading = data["heading"];
			var latitude = data["latitude"];
			var longitude = data["longitude"];
			
			update_hud(altitude, airspeed, heading, roll, pitch);
			update_map(latitude, longitude);
			update_fdm_data_table(data);
		});
	}, 250);
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