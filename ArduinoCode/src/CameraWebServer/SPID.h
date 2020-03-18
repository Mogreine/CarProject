#pragma once
#include <NewPing.h>
#include "SimpleKalmanFilter.h"

class SPID {
public:
    double prop_num = 150;
    double integ_num = 1.5;
    double diff_num = 1;

    double integ_max = 10;
    double integ_min = -10;
    double integ_sum = 5;
    double prev_val = -5;

    double req_dist = 0.3; // m

    NewPing *sonar;
    SimpleKalmanFilter kf = SimpleKalmanFilter(10, 10, 0.02);

    SPID();
    SPID(NewPing *sonar);
    double calculate(double new_val);
    double calculate();
};