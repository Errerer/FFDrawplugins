import time

from .utils import *
from raid_helper import utils as raid_utils
from raid_helper.utils.typing import *
from raid_helper.data import special_actions, delay_until




@omega.on_set_channel(84)
@if_enable
def on_bladedance_tether(msg: ActorControlMessage[actor_control.SetChanneling]):
    # 执行技能 32629 Optimized Bladedance
    # 扇形，范围 100，deg 90
    # 接线死刑
    omjid = raid_utils.NActor.by_id(msg.source_id)
    target_actor = raid_utils.NActor.by_id(msg.param.target_id)
    raid_utils.timeout_when_channeling_change(
        raid_utils.draw_fan(degree=85, radius=50, pos=omjid,
                            facing=lambda _: glm.polar(target_actor.update().pos - omjid.update().pos).y,
                            duration=16),
        msg.source_id, msg.param.target_id, msg.param.idx  # 传监控参

    )

@omega.on_cast(31539)
def on_cast_p2sheshoutianjian(msg: NetworkMessage[zone_server.ActorCast]):
    #执行技能 31539 射手天剑
    # 直线读条技能 ，宽度5  长度 50
    # 随机点一人引导射手天剑，引导判定后固定位置

    raid_utils.draw_rect(width=5, length=45, pos=center, facing=lambda _: glm.polar(msg.source_id.update().pos).y,
                         duration=end_after ,color=glm.vec4(0, .7, 1, .2))