#ifndef FDM_H
#define FDM_H

#include <JSBSim/FGFDMExec.h>

class FDM{
public:
	FDM();
	~FDM();
	void set_data_path(char *path);
    void set_dt(double dt);
    void load_model(char *model);
    void start_engines();
    void load_ic(char *ic);
    bool run_ic();
    bool run();
    void print_simulation_configuration();
    void dump_state();

    double get_latitude();
    double get_longitude();
    double get_airspeed();
    double get_altitude();
    double get_heading();

    double get_x_acceleration();
    double get_y_acceleration();
    double get_z_acceleration();

    double get_roll_rate();
    double get_pitch_rate();
    double get_yaw_rate();

    double get_temperature();

    double get_pressure();
    double get_total_pressure();

    double get_roll();
    double get_pitch();

    double get_aileron();
    double get_elevator();
    double get_rudder();
    double get_throttle();

    void set_aileron(double aileron);
    void set_elevator(double elevator);
    void set_rudder(double rudder);
    void set_throttle(double throttle);

    double get_thrust();

    double get_dt();
    double get_sim_time();

    bool reset(bool do_trim=false);
    bool trim();

    void set_initial_condition(double latitude, double longitude, double altitude, double airspeed, double heading);

private:
	JSBSim::FGFDMExec *fdmexec;
};

#endif
