from abc import ABC, abstractmethod


class BeliefModel(ABC):
    @abstractmethod
    def sample(self, *args) -> float:
        return NotImplemented


class StaticExactBelief(BeliefModel):
    def __init__(self, val):
        self.value = val

    def sample(self, *args):
        return self.value


class TimeVaryingExactBelief(BeliefModel):
    def __init__(self, val_func):
        self.val_func = val_func

    def sample(self, t):
        return self.val_func(t)
