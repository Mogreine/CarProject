#include "SPID.h"

SPID::SPID(NewPing *sonar) {
    this->sonar = sonar;
}

double SPID::calculate(double new_val) {
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
    
    return prop_comp + integ_comp + diff_comp;
}

double SPID::calculate() {
    double new_val = (double)sonar->ping_cm() / 100; // in m
    return calculate(new_val);
}