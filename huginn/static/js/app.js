var map;
var follow_aircraft;
var aircraft_marker;
var myhud;
var entity;

var aircraft_info = L.control();

aircraft_info.onAdd = function(map){
	this._div = L.DomUtil.create("div", "aircraft-info");
	this.update();
	return this._div;
}

aircraft_info.update = function(data){
	var contents;
	
	if(data){
		var airspeed = data["airspeed"];
		var altitude = data["altitude"];
		var heading = data["heading"];
		var latitude = data["latitude"];
		var longitude = data["longitude"];
		
		contents = "<b>Latitude:</b> " + latitude.toFixed(5) + " degrees<br>" + 
		           "<b>Longitude:</b> " + longitude.toFixed(5) +" degrees<br>" +
		           "<b>Altitude:</b> " + altitude.toFixed(1) + " meters<br>" +
		           "<b>Heading:</b> " + heading.toFixed(1) + " degrees<br>" +
		           "<b>Airspeed:</b> " + airspeed.toFixed(1) + " meters/sec";
	}else{
		contents = "no data";
	}
	
	this._div.innerHTML = contents;
}

function init_map(){
	map = L.map('map').setView([51.0, 0.0], 13);
	
	L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
		attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);
	
	/*
	var aircraftIcon = L.icon({
	    iconUrl: 'images/32px-Airplane_silhouette.png',

	    iconSize:     [32, 32],
	    iconAnchor:   [16, 16]
	});
	
	aircraft_marker = L.marker([51.0, 0.0], {icon: aircraftIcon}).addTo(map);
	*/
	aircraft_marker = L.marker([51.0, 0.0]).addTo(map);
	
	aircraft_info.addTo(map);
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

function update_3dmap(latitude, longitude, altitude, airspeed, heading, roll, pitch){
	var position = Cesium.Cartesian3.fromDegrees(longitude, latitude, altitude);
	var heading_in_radians = Cesium.Math.toRadians(heading);
	var roll_in_radians = Cesium.Math.toRadians(roll);
	var pitch_in_radians = Cesium.Math.toRadians(pitch);
    var orientation = Cesium.Transforms.headingPitchRollQuaternion(position, heading_in_radians, pitch_in_radians, roll_in_radians);
    
    entity.position = position;
    entity.orientation = orientation;
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
			aircraft_info.update(data);
			
			//the -90 is required because the model is facing east
			update_3dmap(latitude, longitude, altitude, airspeed, heading-90.0, roll, pitch);
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
	
	var viewer = new Cesium.Viewer('cesiumContainer');
	
	var position = Cesium.Cartesian3.fromDegrees(-123.0744619, 44.0503706, 5000.0);
	var heading = Cesium.Math.toRadians(135);
	var pitch = 0;
	var roll = 0;
	var orientation = Cesium.Transforms.headingPitchRollQuaternion(position, heading, pitch, roll);

	entity = viewer.entities.add({
	        name : "aircraft",
	        position : position,
	        orientation : orientation,
	        model : {
	            uri : "models/Cesium_Air.glb",
	            minimumPixelSize : 128,
	            maximumScale : 20000
	        }
	});
	
	viewer.trackedEntity = entity;
})