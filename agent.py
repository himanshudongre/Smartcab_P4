import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from Qagent import QLearningAgent

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.next_waypoint=None
        self.net_reward=0


    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.next_waypoint=None
        self.state=None

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        #self.state=self.next_waypoint
        # TODO: Select action according to your policy

    def get_policy(self,state):
        return random.choice(Environment.valid_actions)

        action=self.get_policy(state)

        take_action = True
        if self.next_waypoint == 'right':
            if inputs['light'] == 'red':
                take_action = False
        elif self.next_waypoint == 'straight':
            if inputs['light'] == 'red':
                take_action = False
        elif self.next_waypoint == 'left':
            if inputs['light'] == 'red' or (inputs['oncoming'] == 'forward' or inputs['oncoming'] == 'right'):
                take_action = False

        if not take_action:
         action = None

        # Execute action and get reward
        reward = self.env.act(self, action)
        self.net_reward += reward

        # TODO: Learn policy based on state, action, reward

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(QLearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=0.0001)  # reduce update_delay to speed up simulation
    sim.run(n_trials=200)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
