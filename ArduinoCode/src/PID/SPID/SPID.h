#pragma once
#include <NewPing.h>

class SPID {
public:
    double prop_num = 10;
    double integ_num = 1.5;
    double diff_num = 0.5;

    double integ_max = 0.2;
    double integ_min = -0.2;
    double integ_sum = 0;
    double prev_val = -1;

    double req_dist = 0.5; // m

    NewPing *sonar;

    SPID();
    SPID(NewPing *sonar);
    double calculate(double new_val);
    double calculate();
};