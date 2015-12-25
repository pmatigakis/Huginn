var Avionics = Avionics || {};

Avionics.PrimaryFlightDisplay = function(canvas){
	this.canvas = canvas;
	this.context = canvas.getContext("2d");
	
	this.skyColor = "#0028C9";
	this.groundColor = "#C96800";
	this.pitchAngleTextColor = "#ffffff";
	this.flightDataTextColor = "#ffffff";
	
	this.roll = 0.0;
	this.pitch = 0.0;
	
	this.altitude = 0.0;
	this.altitudeUnits = "meters";
	
	this.airspeed = 0.0;
	this.airspeedUnits = "m/s";
	
	this.heading = 0.0;
	this.headingUnits = "degrees";
	
	this.displayWidth = canvas.width;
	this.displayHeight = canvas.height;
	
	this.textSize = Math.floor(canvas.width / 20.0);
	this.pitchLineSpan = Math.floor(canvas.width / 10.0)
	this.pitchLineWidth = Math.floor(canvas.height / 150.0)

	this.pitchSpacing = Math.floor(canvas.height / 10.0)
	
	this.aircraftLineWidth = canvas.height / 50.0;
};

Avionics.PrimaryFlightDisplay.prototype.drawFlightData = function(){
	var context = this.context;
	
	context.font = this.textSize + "px Sans-Serif";

	var headingText = Math.round(this.heading).toString();
	
	var textWidth = context.measureText(headingText).width;
	var unitTextWidth = context.measureText(this.headingUnits).width; 
	if(unitTextWidth > textWidth){
		textWidth = unitTextWidth; 
	}

	context.fillStyle = "#000000";
	context.fillRect((this.displayWidth/2.0) - (textWidth/2.0)*1.2 , 0, textWidth*1.2, this.textSize*2.2);
	
	context.fillStyle = this.flightDataTextColor;
	context.textBaseline = "top";
	context.textAlign = "center";
	context.fillText(headingText, this.displayWidth/2.0, 0);
	context.fillText(this.headingUnits, this.displayWidth/2.0, this.textSize);
	
	var altitudeText = Math.round(this.altitude).toString(); 
	
	var textWidth = context.measureText(altitudeText).width;
	var unitTextWidth = context.measureText(this.altitudeUnits).width; 
	if(unitTextWidth > textWidth){
		textWidth = unitTextWidth; 
	}

	context.fillStyle = "#000000";
	context.fillRect(this.displayWidth - (textWidth*1.2), (this.displayHeight/2.0) - this.textSize, textWidth*1.2, (this.textSize*2.0)*1.4);
	
	context.fillStyle = this.flightDataTextColor;
	context.textBaseline = "middle";
	context.textAlign = "right";
	context.fillText(altitudeText, this.displayWidth, this.displayHeight/2.0);
	context.fillText(this.altitudeUnits, this.displayWidth, (this.displayHeight/2.0) + this.textSize);
	
	var airspeedText = Math.round(this.airspeed).toString();
	
	var textWidth = context.measureText(airspeedText).width;
	var unitTextWidth = context.measureText(this.airspeedUnits).width; 
	if(unitTextWidth > textWidth){
		textWidth = unitTextWidth; 
	}

	context.fillStyle = "#000000";
	context.fillRect(0.0, (this.displayHeight/2.0) - this.textSize, textWidth*1.2, (this.textSize*2.0)*1.4);
	
	context.fillStyle = this.flightDataTextColor;
	
	context.textAlign = "left";
	context.fillText(airspeedText, 0, this.displayHeight/2.0);
	context.fillText(this.airspeedUnits, 0, (this.displayHeight/2.0) + this.textSize);
}

Avionics.PrimaryFlightDisplay.prototype.drawHorizon = function(){
	var context = this.context;
	
	context.fillStyle = this.skyColor;
	context.fillRect(0, 0, this.displayWidth, this.displayHeight);

	var draw_pitch = this.pitch;
	if (draw_pitch > 90.0){
		draw_pitch = 90.0;
	}else if(draw_pitch < -90.0){
		draw_pitch = -90.0;
	}
	
	var p = (draw_pitch * (9 * this.pitchSpacing))/ 90.0;
	
	context.save();
	context.translate(this.displayWidth/2.0, this.displayHeight/2.0);
	
	var draw_roll = this.roll % 360.0;

	context.rotate(-draw_roll * (Math.PI / 180));
	context.translate(0, p);
	
	context.fillStyle = this.groundColor;
	context.fillRect(-this.displayWidth, 0, this.displayWidth*2.0, this.displayHeight*2.0);
	
	context.restore();
}

Avionics.PrimaryFlightDisplay.prototype.drawPitchAngles = function(){
	var context = this.context;
	
	context.font = this.textSize + "px Sans-Serif";
	context.textBaseline = "middle";
	context.fillStyle = this.pitchAngleTextColor;
	
	var draw_pitch = this.pitch;
	if (draw_pitch > 90.0){
		draw_pitch = 90.0;
	}else if(draw_pitch < -90.0){
		draw_pitch = -90.0;
	}
	
	var p = (draw_pitch * (9 * this.pitchSpacing))/ 90.0;
	
	context.save();
	context.translate(this.displayWidth/2.0, this.displayHeight/2.0);
	
	var draw_roll = this.roll % 360.0;

	context.rotate(-draw_roll * (Math.PI / 180));
	context.translate(0, p);
	
	context.strokeStyle = "white";
	context.lineWidth = this.pitchLineWidth;
	context.lineCap = 'square';
	
	
	for (var i = 1; i <= 9; i++){
		context.textAlign = "right";
		context.fillText(-i * 10, -this.pitchLineSpan * 1.3, i * this.pitchSpacing);
		context.textAlign = "left";
		context.fillText(-i * 10, this.pitchLineSpan * 1.3, i * this.pitchSpacing);
		context.beginPath();
		context.moveTo(-this.pitchLineSpan, i * this.pitchSpacing);
		context.lineTo(this.pitchLineSpan, i * this.pitchSpacing);
		context.stroke();
		context.closePath();
	}
	
	for (var i = 1; i <= 9; i++){
		context.textAlign = "right";
		context.fillText(i * 10, -this.pitchLineSpan * 1.3, -i * this.pitchSpacing);
		context.textAlign = "left";
		context.fillText(i * 10, this.pitchLineSpan * 1.3, -i * this.pitchSpacing);
		context.beginPath();
		context.moveTo(-this.pitchLineSpan, -i * this.pitchSpacing);
		context.lineTo(this.pitchLineSpan, -i * this.pitchSpacing);
		context.stroke();
		context.closePath();
	}
	
	context.restore();
}

Avionics.PrimaryFlightDisplay.prototype.drawAircraft = function() {
	var context = this.context;
	
	context.strokeStyle = "yellow";
	context.lineWidth = this.aircraftLineWidth;
	context.lineCap = 'square';
	
	var p1x = 0.3 * this.displayWidth;
	var p2x = 0.4 * this.displayWidth;
	var p3y = (this.displayHeight/2.0) + this.displayHeight * 0.05;
	
	context.beginPath();
	context.moveTo(p1x, this.displayHeight/2.0);
	context.lineTo(p2x, this.displayHeight/2.0);
	context.lineTo(p2x, p3y);
	context.stroke();
	context.closePath();
	
	var p1x = 0.7 * this.displayWidth;
	var p2x = 0.6 * this.displayWidth;
	var p3y = (this.displayHeight/2.0) + this.displayHeight * 0.05;
	
	context.beginPath();
	context.moveTo(p1x, this.displayHeight/2.0);
	context.lineTo(p2x, this.displayHeight/2.0);
	context.lineTo(p2x, p3y);
	context.stroke();
	context.closePath();
}

Avionics.PrimaryFlightDisplay.prototype.draw = function(){
	var context = this.context;
			
    this.drawHorizon();
	this.drawPitchAngles();
	this.drawAircraft();
	this.drawFlightData();
}