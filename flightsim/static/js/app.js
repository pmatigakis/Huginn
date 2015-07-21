var view = new ol.View({
	center: ol.proj.transform([37.41, 8.82], 'EPSG:4326', 'EPSG:3857'),
	zoom: 4
});
  
var map = new ol.Map({
	target: 'map',
	layers: [
	         new ol.layer.Tile({
	        	 source: new ol.source.MapQuest({layer: 'osm'})
	         })
	         ],
	view: view
});
      
setInterval(function(){
	$.getJSON("fdmdata", function(data){
	$("#location .longitude").text(data.fdm_data["position/long-gc-deg"]);
	$("#location .latitude").text(data.fdm_data["position/lat-gc-deg"]);
	$("#location .altitude").text(data.fdm_data["position/h-sl-ft"]);
    $("#location .airspeed").text(data.fdm_data["velocities/vtrue-kts"]);
    $("#location .heading").text(data.fdm_data["attitude/heading-true-rad"] / 0.0174532925);
      
    view.setCenter(ol.proj.transform([data.fdm_data["position/long-gc-deg"], data.fdm_data["position/lat-gc-deg"]], 'EPSG:4326', 'EPSG:3857'));});
}, 1000);