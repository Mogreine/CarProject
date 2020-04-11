import vrep
import sys
import math
import time
import numpy as np
import matplotlib.pyplot as plt

class Robot:
    # точки графика изменения расстояния до стены во времени
    timeLine = list()
    dists = list()
    
    # идентификатор подключения
    clientID = -1

    # коэффициенты для состовляющих ПИД-регулятора
    propConst = 12
    integralConst = 0.05
    diffConst = 5

    # максмальное и минимальное значение интеграла
    integralMaxVal = 0.2
    integralMinVal = -0.2
    # текущее значение интеграла
    integralSum = 0.0
    # предыдущее расстояние до стены
    prevDist = -1

    # стандартная скорость колес
    leftWeelSpeed = 1
    rightWeelSpeed = 1
    # максимальная скорость колес
    maxSpeed = 2

    # требуемое расстояние в метрах
    reqDist = 1

    # вывод сообщения об ошибке в консоль
    def erCheck(self, e, str):
        if e == -1:
            print('Somthing wrong with {0}'.format(str))
            sys.exit()

    # изменение скорости левых колес
    def addLeftSpeed(self, newSpeed):
        newSpeed += self.leftWeelSpeed
        newSpeed = min(self.maxSpeed, newSpeed)
        e = vrep.simxSetJointTargetVelocity(self.clientID, self.back_left, newSpeed, vrep.simx_opmode_oneshot_wait)
        e = vrep.simxSetJointTargetVelocity(self.clientID, self.front_left, newSpeed, vrep.simx_opmode_oneshot_wait)

    # изменение скорости правых колес
    def addRightSpeed(self, newSpeed):
        newSpeed += self.rightWeelSpeed
        newSpeed = min(self.maxSpeed, newSpeed)
        e = vrep.simxSetJointTargetVelocity(self.clientID, self.back_right, -newSpeed, vrep.simx_opmode_oneshot_wait)
        e = vrep.simxSetJointTargetVelocity(self.clientID, self.front_right, -newSpeed, vrep.simx_opmode_oneshot_wait)

    def __init__(self):
        vrep.simxFinish(-1)
        self.clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
        if self.clientID == -1:
            print('Connection not successful')
            sys.exit('Could not connect')
        else:
            print("Connected to remote server")
        
        # начинаем симуляцию, функция доступна только, если клиент стартовал на 19997 порте
        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_streaming)
        
        # получаем обработчики для колес
        errorCode, self.back_left = vrep.simxGetObjectHandle(self.clientID, 'joint_back_left_wheel', vrep.simx_opmode_oneshot_wait)
        self.erCheck(errorCode, 'back left motor')
        errorCode, self.back_right = vrep.simxGetObjectHandle(self.clientID, 'joint_back_right_wheel', vrep.simx_opmode_oneshot_wait)
        self.erCheck(errorCode, 'back right motor')
        errorCode, self.front_left = vrep.simxGetObjectHandle(self.clientID, 'joint_front_left_wheel', vrep.simx_opmode_oneshot_wait)
        self.erCheck(errorCode, 'front left motor')
        errorCode, self.front_right = vrep.simxGetObjectHandle(self.clientID, 'joint_front_right_wheel', vrep.simx_opmode_oneshot_wait)
        self.erCheck(errorCode, 'front right motor')

        # получаем обработчики для сенсоров
        errorCode, self.sonic_sensor = vrep.simxGetObjectHandle(self.clientID, 'disk_sensor', vrep.simx_opmode_oneshot_wait)
        self.erCheck(errorCode, 'sonic sensor')
        errorCode, self.front_sonic_sensor = vrep.simxGetObjectHandle(self.clientID, 'front_disk_sensor', vrep.simx_opmode_oneshot_wait)
        self.erCheck(errorCode, 'sonic sensor')

        # начинаем движение со стандартной скоростью
        self.addLeftSpeed(0)
        self.addRightSpeed(0)
    
    # нахождение высоты с боковыми сторонами a и b
    def getH(self, a, b):
        c = math.sqrt(a ** 2 + b ** 2)
        if abs(c - 0) < 0.000001:
            c = 1.0
        h = a * b / c
        return h

    # функция подсчета и передачи упрвляющего воздействия
    def calulate(self, state, dist):
        deltaDist = self.reqDist - dist

        # расчет пропорциональной компоненты
        propComponent = self.propConst * deltaDist

        # расчет интегральной компоненты
        self.integralSum = self.integralSum + deltaDist
        self.integralSum = min(self.integralSum, self.integralMaxVal)
        self.integralSum = max(self.integralSum, self.integralMinVal)
        integralComponent = self.integralConst * self.integralSum

        if self.prevDist == -1:
            self.prevDist = dist

        # подсчет дифференциальной компоненты 
        diffComponent = self.diffConst * (dist - self.prevDist)

        self.prevDist = dist
        # управляющее воздействие
        result = propComponent - diffComponent + integralComponent

        # регуляция движения робота 
        self.addLeftSpeed(-result)
        self.addRightSpeed(result)

        print('dist = {0} speedLeft = {1} speedRight = {2} res = {3}'.format(dist, self.leftWeelSpeed - result, self.rightWeelSpeed + result, result))

    def rotL(self):
        self.addLeftSpeed(-2.0 * self.leftWeelSpeed)

    def simulate(self):
        plt.xlabel('time')
        plt.ylabel('ditance, meters')
        while vrep.simxGetConnectionId(self.clientID) != -1:
            # получаем данные с сенсоров
            (errorCode, sensorState, sensorDetection, detectedObjectHandle,
                detectedSurfaceNormalVectorUp) = vrep.simxReadProximitySensor(self.clientID, self.sonic_sensor, vrep.simx_opmode_streaming)
            (errorCode, frontState, frontDetection, detectedObjectHandle,
                detectedSurfaceNormalVectorFr) = vrep.simxReadProximitySensor(self.clientID, self.front_sonic_sensor, vrep.simx_opmode_streaming)
            if (frontState and sensorState):
                # есть данные с двух сенсоров
                self.calulate(sensorState, min(sensorDetection[2], frontDetection[2]))
                self.dists.append(min(sensorDetection[2], frontDetection[2]))
            elif (frontState):
                # данные только с переднего сенсора
                self.calulate(frontState, frontDetection[2])
                self.dists.append(frontDetection[2])
            elif (sensorState):
                # данные только с бокового сенсора
                self.calulate(sensorState, sensorDetection[2])
                self.dists.append(sensorDetection[2])
            else:
                # нет данных
                self.calulate(sensorState, self.reqDist + 0.1)
                self.dists.append(self.reqDist + 0.1)
            self.timeLine.append(time.clock())
            # добавляем точку на график в реальном времени
            plt.scatter(self.timeLine[-1], self.dists[-1])
            plt.pause(0.05)
            time.sleep(0.12)
        plt.show()


if __name__ == "__main__":
    pio = Robot()
    pio.simulate()