#ifndef _FGFDMEXEC_H
#define _FGFDMEXEC_H

#include <JSBSim/FGFDMExec.h>

class FGFDMExec{
public:
	FGFDMExec();
	~FGFDMExec();
	void set_root_dir(const char *path);
	bool set_aircraft_path(const char *path);
	bool set_engine_path(const char *path);
	bool set_systems_path(const char *path);
	void set_dt(double dt);
	double get_dt();
	double get_sim_time();
	void print_property_catalog();
	void print_simulation_configuration();
	bool run_ic();
	bool run();
	void process_message();
	void enable_increment_then_hold(int timesteps);
	void check_incremental_hold();
	void hold();
	void resume();
	bool holding();
	double get_property_value(const char *property);
	void set_property_value(const char *property, double value);
	bool load_model(const char *model, bool add_model_to_path = true);
	bool load_ic(const char*reset_name);
	bool trim();

private:
	JSBSim::FGFDMExec *exec;
};

#endif
