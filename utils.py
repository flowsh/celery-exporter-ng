# from https://stackoverflow.com/questions/2437617/how-to-limit-the-size-of-a-dictionary
# adapted to prevent adding more if dictionary is at limit
from collections import OrderedDict
from logger import log


class LimitedSizeDict(OrderedDict):
    def __init__(self, *args, **kwds):
        self.size_limit = kwds.pop("size_limit", None)
        OrderedDict.__init__(self, *args, **kwds)

    def __setitem__(self, key, value):
        if self._check_size_limit():
            OrderedDict.__setitem__(self, key, value)
        else:
            log.warning(f"MAX_TASKS_CAPTURED reached, could not add task to memory!")

    def _check_size_limit(self):
        if self.size_limit is not None:
            free_space = False if len(self) > self.size_limit else True
            return free_space
        else:
            return True
