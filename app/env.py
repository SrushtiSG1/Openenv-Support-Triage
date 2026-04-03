from app.models import Observation, Action, Reward
from app.tasks import TASKS
from app.grader import grade_step
import random

class CustomerSupportEnv:

    def __init__(self):
        self.current_task = None
        self.state_data = {}
        self.steps = 0
        self.max_steps = 6

    def reset(self, task_id=None):
        self.steps = 0
        if task_id is None:
            task_id = random.randint(0, 2)

        self.current_task = TASKS[task_id]

        self.state_data = {
            "classified": False,
            "responded": False,
            "routed": False,
            "closed": False
        }

        return Observation(**self.current_task["observation"])

    def step(self, action: Action):
        self.steps += 1

        reward, info = grade_step(
            self.current_task,
            self.state_data,
            action
        )

        done = reward >= 0.95 or self.steps >= self.max_steps

        return (
            Observation(**self.current_task["observation"]),
            Reward(score=reward, breakdown=info, done=done),
            done,
            info
        )

    def state(self):
        return {
            "task": self.current_task,
            "state": self.state_data,
            "steps": self.steps
        }