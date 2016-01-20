#include <stdio.h>
#include <string>
#include <JSBSim/FGFDMExec.h>
#include <JSBSim/models/FGPropulsion.h>
#include <JSBSim/models/FGFCS.h>
#include <JSBSim/models/FGPropagate.h>
#include <JSBSim/models/FGAuxiliary.h>
#include <JSBSim/models/FGAtmosphere.h>
#include <JSBSim/models/propulsion/FGEngine.h>
#include <JSBSim/models/propulsion/FGThruster.h>
#include <JSBSim/initialization/FGInitialCondition.h>
#include "fdm.h"

FDM::FDM(){
	fdmexec = new JSBSim::FGFDMExec();
}

FDM::~FDM(){
	delete fdmexec;
}

void FDM::set_data_path(char *path){
	fdmexec->SetRootDir(path);

	fdmexec->SetAircraftPath("");

	std::string engine_path = std::string(path) + "/Engines";
	fdmexec->SetEnginePath(engine_path.c_str());

	std::string systems_path = std::string(path) + "/Systems";
	fdmexec->SetSystemsPath(systems_path.c_str());
}

void FDM::set_dt(double dt){
    fdmexec->Setdt(dt);
}

void FDM::load_model(char *model){
	fdmexec->LoadModel(model);
}

void FDM::start_engines(){
	fdmexec->GetPropulsion()->GetEngine(0)->SetRunning(1);
}

void FDM::load_ic(char *ic){
    fdmexec->GetIC()->Load(ic);
}

bool FDM::run_ic(){
	return fdmexec->RunIC();
}

bool FDM::run(){
	fdmexec->ProcessMessage();
	fdmexec->CheckIncrementalHold();

    return fdmexec->Run();
}

void FDM::print_simulation_configuration(){
	fdmexec->PrintSimulationConfiguration();
}

void FDM::dump_state(){
	fdmexec->GetPropagate()->DumpState();
}

double FDM::get_latitude(){
    JSBSim::FGPropagate *propagate = fdmexec->GetPropagate();

	return propagate->GetLatitudeDeg();
}

double FDM::get_longitude(){
    JSBSim::FGPropagate *propagate = fdmexec->GetPropagate();

    return propagate->GetLongitudeDeg();
}

double FDM::get_airspeed(){
    JSBSim::FGAuxiliary *auxiliary = fdmexec->GetAuxiliary();

    return auxiliary->GetVtrueFPS();
}

double FDM::get_altitude(){
    JSBSim::FGPropagate *propagate = fdmexec->GetPropagate();

    return propagate->GetAltitudeASLmeters();
}

double FDM::get_heading(){
    JSBSim::FGPropagate *propagate = fdmexec->GetPropagate();

    return propagate->GetEuler(3);
}

double FDM::get_x_acceleration(){
    JSBSim::FGAuxiliary *auxiliary = fdmexec->GetAuxiliary();

    return auxiliary->GetPilotAccel(1);
}

double FDM::get_y_acceleration(){
    JSBSim::FGAuxiliary *auxiliary = fdmexec->GetAuxiliary();

    return auxiliary->GetPilotAccel(2);
}

double FDM::get_z_acceleration(){
    JSBSim::FGAuxiliary *auxiliary = fdmexec->GetAuxiliary();

    return auxiliary->GetPilotAccel(3);
}

double FDM::get_roll_rate(){
    JSBSim::FGAuxiliary *auxiliary = fdmexec->GetAuxiliary();

    return auxiliary->GetEulerRates(1);
}

double FDM::get_pitch_rate(){
    JSBSim::FGAuxiliary *auxiliary = fdmexec->GetAuxiliary();

    return auxiliary->GetEulerRates(2);
}

double FDM::get_yaw_rate(){
    JSBSim::FGAuxiliary *auxiliary = fdmexec->GetAuxiliary();

    return auxiliary->GetEulerRates(3);
}

double FDM::get_temperature(){
    JSBSim::FGAtmosphere *atmosphere = fdmexec->GetAtmosphere();

    return atmosphere->GetTemperature();
}

double FDM::get_pressure(){
    JSBSim::FGAtmosphere *atmosphere = fdmexec->GetAtmosphere();

    return atmosphere->GetPressure();
}

double FDM::get_total_pressure(){
    JSBSim::FGAuxiliary *auxiliary = fdmexec->GetAuxiliary();

    return auxiliary->GetTotalPressure();
}

double FDM::get_roll(){
    JSBSim::FGPropagate *propagate = fdmexec->GetPropagate();

    return propagate->GetEulerDeg(1);
}

double FDM::get_pitch(){
    JSBSim::FGPropagate *propagate = fdmexec->GetPropagate();

    return propagate->GetEulerDeg(2);
}

double FDM::get_aileron(){
    JSBSim::FGFCS *fcs = fdmexec->GetFCS();

    return fcs->GetDaCmd();
}

double FDM::get_elevator(){
    JSBSim::FGFCS *fcs = fdmexec->GetFCS();

    return fcs->GetDeCmd();
}

double FDM::get_rudder(){
    JSBSim::FGFCS *fcs = fdmexec->GetFCS();

    return fcs->GetDrCmd();
}

double FDM::get_throttle(){
    JSBSim::FGFCS *fcs = fdmexec->GetFCS();

    return fcs->GetThrottleCmd(0);
}

void FDM::set_aileron(double aileron){
    JSBSim::FGFCS *fcs = fdmexec->GetFCS();

    fcs->SetDaCmd(aileron);
}

void FDM::set_elevator(double elevator){
    JSBSim::FGFCS *fcs = fdmexec->GetFCS();

    fcs->SetDeCmd(elevator);
}

void FDM::set_rudder(double rudder){
    JSBSim::FGFCS *fcs = fdmexec->GetFCS();

    fcs->SetDrCmd(rudder);
}

void FDM::set_throttle(double throttle){
    JSBSim::FGFCS *fcs = fdmexec->GetFCS();

    for(unsigned int i = 0; i < fdmexec->GetPropulsion()->GetNumEngines(); i++){
        fcs->SetThrottleCmd(i, throttle);
    }
}

double FDM::get_thrust(){
    return fdmexec->GetPropulsion()->GetEngine(0)->GetThruster()->GetThrust();
}

double FDM::get_dt(){
    return fdmexec->GetDeltaT();
}

double FDM::get_sim_time(){
    return fdmexec->GetSimTime();
}

bool FDM::reset(){
    fdmexec->Resume();

    fdmexec->ResetToInitialConditions(0);

    set_aileron(0.0);
    set_elevator(0.0);
    set_rudder(0.0);
    set_throttle(0.2);

    fdmexec->PrintSimulationConfiguration();

    fdmexec->GetPropagate()->DumpState();

    return fdmexec->Run();
}
