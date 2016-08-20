import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import math
from collections import namedtuple


class QLearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(QLearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.qTable = dict() #Q table implemented as a dictionary
        self.learning_rate = 0.9
        self.epsilon  = 0.1
        self.discount = 0.35
        self.previous_state = None
        self.state = None
        self.previous_action = None
        self.previous_reward = None
        self.total_reward = 0
        valid_actions = ['forward', 'left', 'right', None]

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.planner.route_to(destination)
        self.previous_state = None
        self.state = None
        self.previous_action = None
        self.epsilon = 0.1
        self.total_reward = 0

    def flipCoin(self, p):   #random coin flip to be used in case of ties
        r = random.random()
        return r < p

    def get_Qvalue(self,state,action): #fetch q value for a state and action
        return self.qTable.get((state, action), 0.0)

    def get_maxQvalue(self,state):   #return max Q value
        maxQvalue = -999999999
        valid_actions = ['forward', 'left', 'right', None]
        for action in valid_actions:
            if(self.get_Qvalue(state, action) > maxQvalue):
                maxQvalue = self.get_Qvalue(state, action)
        return maxQvalue

    def get_policy(self,state): #get best possible action in a state
        bestAction = None
        maxQvalue = -999999999
        valid_actions = ['forward', 'left', 'right', None]
        for action in valid_actions:
            if(self.get_Qvalue(state, action) > maxQvalue):
                maxQvalue = self.get_Qvalue(state, action)
                bestAction = action
            if(self.get_Qvalue(state, action) == maxQvalue):
                if(self.flipCoin(.5)):
                    maxQvalue = self.get_Qvalue(state, action)
                    bestAction = action
        return bestAction

    def make_state(self,state): #create a namedtuple state
        State = namedtuple("State", ["light","next_waypoint"])
        return State(light = state['light'],next_waypoint = self.planner.next_waypoint())

    def get_action(self, state): #return an action based on state
        action = None
        valid_actions = ['forward', 'left', 'right', None]
        if (self.flipCoin(self.epsilon)):
            action = random.choice(valid_actions)
        else:
            action = self.get_policy(state)
        return action

    def update_Qtable(self, state, action, nextState, reward): #update Q table
        if((state, action) not in self.qTable):
            self.qTable[(state, action)] = 0.0
        else:
            self.qTable[(state, action)] = self.qTable[(state, action)] + self.learning_rate * (reward + self.discount * self.get_maxQvalue(nextState) - self.qTable[(state, action)])


    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        self.state = self.make_state(self.env.sense(self))

        # TODO: Select action according to your policy
        action = self.get_action(self.state)

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Update state
        ## in case of initial configuration don't update the q table, else update q table
        if self.previous_reward!= None:
            self.update_Qtable(self.previous_state,self.previous_action,self.state,self.previous_reward)

        # store the previous action and state so that we can update the q table on the next iteration
        self.previous_action = action
        self.previous_state = self.state
        self.previous_reward = reward
        self.total_reward += reward


        # TODO: Learn policy based on state, action, reward

        #print "QLearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(QLearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline = True )  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=0.0001)  # reduce update_delay to speed up simulation
    sim.run(n_trials=200)  # press Esc or close pygame window to quit



if __name__ == '__main__':
    run()
