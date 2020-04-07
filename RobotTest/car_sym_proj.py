import vrep
import sys
import math
import time
import numpy as np
import matplotlib.pyplot as plt

class Pioneer:
    timeLine = list()
    errorsPoints = list()
    dists = list()
    leftSpeedPoints = list()
    rightSpeedPoints = list()

    clientID = -1
    #10.1, 0.5, 1.5
    propConst = 12
    integralConst = 0.05
    diffConst = 5 # 6

    integralMaxVal = 0.2
    integralMinVal = -0.2
    integralSum = 0.0
    prevDist = -1

    leftWeelSpeed = 1
    rightWeelSpeed = 1
    maxSpeed = 2

    reqDist = 1

    def erCheck(self, e, str):
        if e == -1:
            print('Somthing wrong with {0}'.format(str))
            sys.exit()

    def addLeftSpeed(self, newSpeed):
        newSpeed += self.leftWeelSpeed
        newSpeed = min(self.maxSpeed, newSpeed)
        e = vrep.simxSetJointTargetVelocity(self.clientID, self.back_left, newSpeed, vrep.simx_opmode_oneshot_wait)
        e = vrep.simxSetJointTargetVelocity(self.clientID, self.front_left, newSpeed, vrep.simx_opmode_oneshot_wait)

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
        
        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_streaming)
        
        errorCode, self.back_left = vrep.simxGetObjectHandle(self.clientID, 'joint_back_left_wheel', vrep.simx_opmode_oneshot_wait)
        self.erCheck(errorCode, 'back left motor')
        errorCode, self.back_right = vrep.simxGetObjectHandle(self.clientID, 'joint_back_right_wheel', vrep.simx_opmode_oneshot_wait)
        self.erCheck(errorCode, 'back right motor')
        errorCode, self.front_left = vrep.simxGetObjectHandle(self.clientID, 'joint_front_left_wheel', vrep.simx_opmode_oneshot_wait)
        self.erCheck(errorCode, 'front left motor')
        errorCode, self.front_right = vrep.simxGetObjectHandle(self.clientID, 'joint_front_right_wheel', vrep.simx_opmode_oneshot_wait)
        self.erCheck(errorCode, 'front right motor')

        errorCode, self.sonic_sensor = vrep.simxGetObjectHandle(self.clientID, 'disk_sensor', vrep.simx_opmode_oneshot_wait)
        self.erCheck(errorCode, 'sonic sensor')
        errorCode, self.front_sonic_sensor = vrep.simxGetObjectHandle(self.clientID, 'front_disk_sensor', vrep.simx_opmode_oneshot_wait)
        self.erCheck(errorCode, 'sonic sensor')

        self.addLeftSpeed(0)
        self.addRightSpeed(0)
    
    def getH(self, a, b):
        c = math.sqrt(a ** 2 + b ** 2)
        if abs(c - 0) < 0.000001:
            c = 1.0
        h = a * b / c
        return h
    def getH2(self, a, b):
        return min(a, b)

    def calulate(self, state, dist):
        deltaDist = self.reqDist - dist

        propComponent = self.propConst * deltaDist

        self.integralSum = self.integralSum + deltaDist
        self.integralSum = min(self.integralSum, self.integralMaxVal)
        self.integralSum = max(self.integralSum, self.integralMinVal)
        integralComponent = self.integralConst * self.integralSum

        if self.prevDist == -1:
            self.prevDist = dist
        
        diffComponent = self.diffConst * (dist - self.prevDist)

        self.prevDist = dist
        result = propComponent - diffComponent + integralComponent
        
        self.addLeftSpeed(-result)
        self.addRightSpeed(result)

        self.timeLine.append(time.clock())
        self.errorsPoints.append(deltaDist)
        self.rightSpeedPoints.append(self.rightWeelSpeed + result)
        self.leftSpeedPoints.append(self.leftWeelSpeed - result)

        print('dist = {0} speedLeft = {1} speedRight = {2} res = {3}'.format(dist, self.leftWeelSpeed - result, self.rightWeelSpeed + result, result))

    def rotL(self):
        self.addLeftSpeed(-2.0 * self.leftWeelSpeed)
        #self.addRightSpeed()

    def simulate(self):
        plt.xlabel('time')
        plt.ylabel('ditance, meters')
        while vrep.simxGetConnectionId(self.clientID) != -1:
            (errorCode, sensorState, sensorDetection, detectedObjectHandle,
                detectedSurfaceNormalVectorUp) = vrep.simxReadProximitySensor(self.clientID, self.sonic_sensor, vrep.simx_opmode_streaming)
            (errorCode, frontState, frontDetection, detectedObjectHandle,
                detectedSurfaceNormalVectorFr) = vrep.simxReadProximitySensor(self.clientID, self.front_sonic_sensor, vrep.simx_opmode_streaming)
            if (frontState and sensorState):
                self.calulate(sensorState, min(sensorDetection[2], frontDetection[2]))
                self.dists.append(min(sensorDetection[2], frontDetection[2]))
            elif (frontState):
                self.calulate(frontState, frontDetection[2])
                self.dists.append(frontDetection[2])
            elif (sensorState):
                self.calulate(sensorState, sensorDetection[2])
                self.dists.append(sensorDetection[2])
            else:
                self.calulate(sensorState, self.reqDist + 0.1)
                self.dists.append(self.reqDist + 0.1)
            self.timeLine.append(time.clock())
            plt.scatter(self.timeLine[-1], self.dists[-1])
            plt.pause(0.05)
            time.sleep(0.12)
        plt.show()


if __name__ == "__main__":
    pio = Pioneer()
    pio.simulate()