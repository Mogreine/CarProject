#include "SPID.h"

SPID::SPID() {
    count_sensors = 0;
}

SPID::SPID(NewPing *sonar) {
    this->sonar = sonar;
    count_sensors = 1;
}

SPID::SPID(NewPing *sonar, NewPing *sonar_front) {
    this->sonar = sonar;
    this->sonar_front = sonar_front;
    count_sensors = 2;
}

double SPID::calculate(double new_val) {
    // new_val = (double)kf.updateEstimate(new_val);
	  Serial.printf("dist: %f\n", new_val);
    double delta = req_dist - new_val;

    double prop_comp = prop_num * delta;

    integ_sum += delta;
    integ_sum = std::max(integ_sum, integ_min);
    integ_sum = std::min(integ_sum, integ_max);
    double integ_comp = integ_num * integ_sum;

    if (prev_val == -1)
        prev_val = new_val;
    
    double diff_comp = diff_num * (new_val - prev_val);
    prev_val = new_val;
    
    return prop_comp + integ_comp - diff_comp;
}

double SPID::calculate() {
    if (count_sensors == 0) {
        return 0;
    }
    else if (count_sensors == 1) {
        double new_val = (double)sonar->ping_cm() / 100; // in m
        if (new_val < 1e-3) {
            new_val = 3;
            return calculate(prev_pid_val == -1 ? req_dist : prev_pid_val);
        }
        return prev_pid_val = SPID::calculate(new_val);
    }
    else {
        double front_val = (double)sonar_front->ping_cm() / 100; // in m
        double right_val = (double)sonar->ping_cm() / 100; // in m
        if (front_val < 1e-3 && right_val < 1e-3) {
            return calculate(prev_pid_val == -1 ? req_dist : prev_pid_val);
        }
        else if (front_val < 1e-3) {
          prev_pid_val = right_val;
            return calculate(right_val);
        }
        else if (right_val < 1e-3) {
          prev_pid_val = front_val / 2;
            return calculate(front_val / 2);
        }
        else {
          prev_pid_val = min(front_val / 2, right_val);
            return calculate(min(front_val / 2, right_val));
        }
    }
}
