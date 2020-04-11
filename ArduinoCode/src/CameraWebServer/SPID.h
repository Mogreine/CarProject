#pragma once
#include <NewPing.h>
#include "SimpleKalmanFilter.h"
/**
 * @brief Класс ПИД-регулятора
 * 
 */
class SPID {
    // указатель на объект взаимодействия с боковым ультразвуковым датчиком
    NewPing *sonar;
    // указатель на объект взаимодействия с передним ультразвуковым датчиком
    NewPing *sonar_front;
public:
    // пропорциональный коэффициент
    double prop_num = 120;
    // интегральный коэффициент
    double integ_num = 0.5;
    // дифференциальный коэффициент
    double diff_num = 50;

    // максимальное значение интегрального компонента
    double integ_max = 10;
    // минимальное значение интегрального компонента
    double integ_min = -10;
    // значение интегрального компонента
    double integ_sum = 0;
    // предыдущее значение измеренной дистанции (-1, если измерение является первым)
    double prev_val = -1;

    // требуемое расстояние между роботом и стеной в метрах
    double req_dist = 0.3;
    // предыдущее значение пид-регулятора
    double prev_pid_val = -1;
    // количество используемых сенсоров (при 1 используются только данные с бокового сенсора, при 2 - используются данные с обоих сенсоров)
    int8_t count_sensors;

    // объект фильтра калмана 
    // 1 параметр - неопределенность измерения (насколько сильно будут варьироваться измерения)
    // 2 параметр - неопределенность оценки - можно задавать равным первому параметру, потому что фильтр сам будет его варьировать
    // 3 параметр - дисперсия процесса - скорость изменения измерения (обычно от 0.001 до 1)
    SimpleKalmanFilter kf = SimpleKalmanFilter(10, 10, 0.02);

    /**
     * @brief Конструктор по умолчанию
     */
    SPID();

    /**
     * @brief Конструктор для регулятора только с боковым сенсором
     * 
     * @param sonar указатель на объект сенсора
     */
    SPID(NewPing *sonar);

    /**
     * @brief Конструктор для регулятора с боковым и передним сенсором
     * 
     * @param sonar указатель на боковой датчик
     * @param sonar_front указатель на передний датчик
     */
    SPID(NewPing *sonar, NewPing *sonar_front);

    /**
     * @brief Функция расчета управляющего воздействия с явной передачей текущего значения
     * 
     * @param new_val текущее расстояние между роботом и стеной
     * @return double управляющее воздействие
     */
    double calculate(double new_val);

    /**
     * @brief Функция расчета управляющего воздействия с неявным использованием данных от датчиков
     * 
     * @return double управляющее воздействие
     */
    double calculate();
};