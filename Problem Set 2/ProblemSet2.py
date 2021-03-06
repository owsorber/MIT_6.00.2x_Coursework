"""
6.00.2x Problem Set 2: Simulating Robots 
Problem 1: 10/10 points
Problem 2: 10/10 points
Problem 3: 10/10 points
Problem 4: 10/10 points
Problem 5: 10/10 points
Problem 6: 6/6 points

@author: owsorber
"""

import math
import random

import ps2_visualize
import pylab

# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        
        # Store width and height as instance data for later use
        self.width = width
        self.height = height
        
        # Dictionary maps a tile (represented by an ordered pair) to a boolean (true if clean)
        self.tiles = {}
        
        for i in range(0, width):
            for j in range(0, height):
                self.tiles[(i, j)] = False # by default, all are dirty
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        
        tile = (int(pos.x), int(pos.y)) # Floor the position to get the tile ordered pair
        
        self.tiles[tile] = True # Cleaned

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        
        return self.tiles[(m, n)]
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        
        count = 0
        for tile in self.tiles: 
            if self.tiles[tile]:
                count += 1 # tile is cleaned so add to count
        
        return count

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        
        # Calculate x and y based on random() and width/height
        x = random.random() * self.width
        y = random.random() * self.height
        
        
        return Position(x, y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        
        withinWidth = pos.x < self.width and pos.x >= 0
        withinHeight = pos.y < self.height and pos.y >= 0
        
        return withinWidth and withinHeight


# === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        
        # Initialize room and robot speed
        self.room = room
        self.speed = speed
        
        # Initilaize positional components
        self.pos = self.room.getRandomPosition()
        self.angle = random.random() * 360
        
        # Clean tile robot is currently on
        self.room.cleanTileAtPosition(self.pos)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        
        return int(self.angle)

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        
        self.angle = direction

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        
        self.setRobotPosition(self.pos.getNewPosition(self.angle, self.speed))
        self.room.cleanTileAtPosition(self.pos)
        
        raise NotImplementedError # don't change this!


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        
        newPos = self.pos.getNewPosition(self.angle, self.speed)
        
        # if new position is achievable, go to it; else, change direction
        if self.room.isPositionInRoom(newPos):
            self.setRobotPosition(newPos)
            self.room.cleanTileAtPosition(self.pos)
        else:
            self.setRobotDirection(random.random() * 360)


#standardbot = StandardRobot(RectangularRoom(20, 20), 0.5)
#standardbot.testRobotMovement()


# === Problem 4
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    
    
    sumSteps = 0
    for trial in range(0, num_trials):
        robots = []
        room = RectangularRoom(width, height)
        for i in range(0, num_robots):
            robots.append(robot_type(room, speed))
        steps = 0
        
        while room.getNumCleanedTiles() / room.getNumTiles() < min_coverage:
            for i in range(0, len(robots)):
                robots[i].updatePositionAndClean()
            steps += 1
        sumSteps += steps
        
    return sumSteps / num_trials


# Uncomment this line to see how much your simulation takes on average
#print(runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot))


# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        
        newPos = self.pos.getNewPosition(self.angle, self.speed)
        
        if self.room.isPositionInRoom(newPos):
            self.setRobotPosition(newPos)
            self.room.cleanTileAtPosition(self.pos)
        
        self.setRobotDirection(random.random() * 360)

#randombot = RandomWalkRobot(RectangularRoom(20, 20), 0.5)
#randombot.testRobotMovement()

def testRobotMovement(robot_types, room, speed, delay):
    """
    Runs a simulation of a single robot of type robot_type in a RectangularRoom.
    
    robot_types: a dict, mapping a robot class to the number of that kind of robot to be tested
    """
    
    robots = []
    for robot_type in robot_types:
        for i in range(0, robot_types[robot_type]):
            robots.append(robot_type(room, speed))
    
    anim = ps2_visualize.RobotVisualization(len(robots), room.width, room.height, delay)
    while room.getNumCleanedTiles() < room.getNumTiles():
        for robot in robots:
            robot.updatePositionAndClean()
        anim.update(room, robots)
    anim.done()


# === Problem 6
def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    
    The Time It Takes 1 - 10 Robots To Clean 80% Of A Room
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    
    The Time It Takes Two Robots To Clean 80% Of Variously Sized Rooms
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

def showPlot3(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    
    The Time It Takes Robots To Clean Different Percentages of a Room
    """
    percentages = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    times1 = []
    times5 = []
    times10 = []
    for percentage in percentages:
        print("Plotting for ", percentage * 100, "% of room")
        times1.append(runSimulation(1, 1.0, 20, 20, percentage, 20, StandardRobot))
        times5.append(runSimulation(5, 1.0, 20, 20, percentage, 20, StandardRobot))
        times10.append(runSimulation(10, 1.0, 20, 20, percentage, 20, StandardRobot))
    pylab.plot(percentages, times1)
    pylab.plot(percentages, times5)
    pylab.plot(percentages, times10)
    pylab.title(title)
    pylab.legend(('1 Robot', '5 Robots', '10 Robots'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


""" TESTING PLOTS """
#showPlot1("Time It Takes 1 - 10 Robots To Clean 80% Of A Room", "Num Robots", "Time")
#showPlot2("Time It Takes Two Robots To Clean 80% Of Variously Sized Rooms", "Ratio Between Width and Height", "Time")    
#showPlot3("Time It Takes Robots To Clean Different Percentages of a Room", "Percentage", "Time")

""" TESTING ROBOT MOVEMENT """
testRobotMovement({StandardRobot: 15, RandomWalkRobot: 5}, RectangularRoom(20, 20), 1, 0.1)




