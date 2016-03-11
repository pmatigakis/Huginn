var map;
var follow_aircraft;
var aircraft_marker;
var myhud;
var entity;
var markers = [];

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
	
	var aircraftIcon = L.icon({
	    iconUrl: 'static/images/32px-Airplane_silhouette.png',

	    iconSize:     [32, 32],
	    iconAnchor:   [16, 16]
	});
	
	aircraft_marker = L.marker([51.0, 0.0], {icon: aircraftIcon}).addTo(map);
	
	//aircraft_marker = L.marker([51.0, 0.0]).addTo(map);
	
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
		//$.getJSON("fdm", function(data){
		$.getJSON("api/ins_data", function(data){
			var roll = data["roll"];
			var pitch = data["pitch"];
			var airspeed = data["airspeed"];
			var altitude = data["altitude"];
			var heading = data["heading"];
			var latitude = data["latitude"];
			var longitude = data["longitude"];
			
			update_hud(altitude, airspeed, heading, roll, pitch);
			update_map(latitude, longitude);
			aircraft_info.update(data);
			
			//the -90 is required because the model is facing east
			update_3dmap(latitude, longitude, altitude, airspeed, heading-90.0, roll, pitch);
		});
	}, 250);
	
	//TODO: Comment out this until I add better waypoint drawing functions
	/*
	setInterval(function(){
		$.getJSON("map", function(data){
			for(var i = 0; i < markers.length; i++){
				map.removeLayer(markers[i]);
			}
			
			markers = [];
			
			for(var i = 0; i < data.length; i++){
				var latitude = data[i].latitude;
				var longitude = data[i].longitude;
				var marker = L.marker([latitude, longitude]);
				marker.addTo(map);
				markers.push(marker);
			}
		});
	}, 2000);
	*/
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
	            uri : "static/models/Cesium_Air.glb",
	            minimumPixelSize : 128,
	            maximumScale : 20000
	        }
	});
	
	viewer.trackedEntity = entity;
	
	$("#resume_button").click(function(){
		$.getJSON("simulator/resume", function(data){
			if(data["result"] != "ok"){
				alert("Failed to resume simulation");
			}
		});
	})
	
	$("#pause_button").click(function(){
		$.getJSON("simulator/pause", function(data){
			if(data["result"] != "ok"){
				alert("Failed to pause the simulator");
			}
		});
	})
	
	$("#reset_button").click(function(){
		$.getJSON("simulator/reset", function(data){
			if(data["result"] != "ok"){
				alert("Failed to reset the simulator");
			}
		});
	})
})