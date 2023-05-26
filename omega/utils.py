import logging

import glm

from raid_helper import utils as raid_utils
from raid_helper.utils.typing import *
from raid_helper.data import special_actions

omega = raid_utils.MapTrigger(1122)

center = glm.vec3(100, 0, 100)

logger = logging.getLogger('raid_helper/omega')

_is_enable = omega.add_value(raid_utils.BoolCheckBox('enable', False))


def if_enable(func):
    def wrapper(*args, **kwargs):
        if _is_enable.value:
            return func(*args, **kwargs)
        else:
            logger.debug(f'{func.__name__} disabled')

    return wrapper
