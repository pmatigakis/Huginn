#include <JSBSim/FGFDMExec.h>
#include <JSBSim/initialization/FGInitialCondition.h>
#include <JSBSim/initialization/FGTrim.h>
#include "FGFDMExec.h"

FGFDMExec::FGFDMExec(){
	exec = new JSBSim::FGFDMExec();
}

FGFDMExec::~FGFDMExec(){
	delete exec;
}

void FGFDMExec::set_root_dir(const char *path){
	exec->SetRootDir(path);
}

bool FGFDMExec::set_aircraft_path(const char *path){
	return exec->SetAircraftPath(path);
}

bool FGFDMExec::set_engine_path(const char *path){
	return exec->SetEnginePath(path);
}

bool FGFDMExec::set_systems_path(const char *path){
	return exec->SetSystemsPath(path);
}

void FGFDMExec::set_dt(double dt){
	exec->Setdt(dt);
}

double FGFDMExec::get_dt(){
	return exec->GetDeltaT();
}

double FGFDMExec::get_sim_time(){
	return exec->GetSimTime();
}

void FGFDMExec::print_property_catalog(){
	exec->PrintPropertyCatalog();
}

void FGFDMExec::print_simulation_configuration(){
	exec->PrintSimulationConfiguration();
}

bool FGFDMExec::run_ic(){
	return exec->RunIC();
}

bool FGFDMExec::run(){
	return exec->Run();
}

void FGFDMExec::process_message(){
	exec->ProcessMessage();
}

void FGFDMExec::enable_increment_then_hold(int timesteps){
	exec->EnableIncrementThenHold(timesteps);
}

void FGFDMExec::check_incremental_hold(){
	exec->CheckIncrementalHold();
}

void FGFDMExec::hold(){
	exec->Hold();
}

void FGFDMExec::resume(){
	exec->Resume();
}

bool FGFDMExec::holding(){
	return exec->Holding();
}

double FGFDMExec::get_property_value(const char *property){
	return exec->GetPropertyValue(property);
}

void FGFDMExec::set_property_value(const char *property, double value){
	exec->SetPropertyValue(property, value);
}

bool FGFDMExec::load_model(const char *model, bool add_model_to_path){
	return exec->LoadModel(model, add_model_to_path);
}

bool FGFDMExec::load_ic(const char*reset_name){
	JSBSim::FGInitialCondition *ic = exec->GetIC();

	return ic->Load(reset_name);
}

bool FGFDMExec::trim(){
	JSBSim::FGTrim *trimmer = new JSBSim::FGTrim(exec, JSBSim::tFull);

	bool result = trimmer->DoTrim();

	delete trimmer;

	return result;
}
