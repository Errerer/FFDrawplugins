import time

from .utils import *
from raid_helper import utils as raid_utils
from raid_helper.utils.typing import *
from raid_helper.data import special_actions, delay_until

special_actions[32368] = raid_utils.fan_shape(60)

delay_until[32368] = 5


@omega.on_set_channel(89)
@if_enable
def on_blaster_tether(evt: 'ActorControlMessage[actor_control.SetChanneling]'):
    # 执行技能 31498 Blaster
    # 圆形，范围 15
    # 带体力衰减（新时代易伤）
    # 带一层死刻
    actor = raid_utils.NActor.by_id(evt.param.target_id)
    logger.debug(f'Blaster tether {actor=} {actor.base_id=:x}')
    if actor.base_id == 0x3d5c:
        raid_utils.timeout_when_channeling_change(raid_utils.draw_circle(
            radius=15,
            pos=raid_utils.NActor.by_id(evt.source_id),
            duration=30
        ), evt.source_id, evt.param.target_id, evt.param.idx)


@omega.on_lockon(23)
@if_enable
def on_lockon_wave_cannon_kyrios(msg: ActorControlMessage[actor_control.SetLockOn]):
    # 一次点仨
    # 点名后 5.1s 触发
    # 执行技能 31505 Wave Cannon Kyrios
    # 矩形， 范围 50， 宽6
    # 首次触发作为5*2大扇形的触发
    omega = next(raid_utils.find_actor_by_base_id(0x3d5c))
    t_actor = raid_utils.NActor.by_id(msg.source_id)
    raid_utils.draw_rect( 
        pos=omega, facing=lambda _: glm.polar(t_actor.update().pos - omega.update().pos).y,
        width=6, length=50, duration=5.1

    )


@omega.on_lockon(23)
@if_enable
def on_lockon_wave_cannon_kyrios_far(msg: ActorControlMessage[actor_control.SetLockOn]):
    # 5*2大扇形
    # 执行技能 31504 Diffuse Wave Cannon Kyrios
    # 扇形， 范围 60， deg120
    # 目标为最远两人
    # 持续时间简单6.1够了
    omega = next(raid_utils.find_actor_by_base_id(0x3d5c))

    raid_utils.draw_fan(
        pos=omega, facing=lambda _: glm.polar(raid_utils.get_actor_by_dis(omega, -1).pos - omega.update().pos).y, 
        degree=120, radius=60, duration=6.1

    )
    raid_utils.draw_fan(
        pos=omega,  
        facing=lambda _: glm.polar(raid_utils.get_actor_by_dis(omega, -2).pos - omega.update().pos).y, 
        degree=120, radius=60, duration=6.1

    )


@omega.on_object_spawn(0x1EB83C)
def print_object_spawn(evt: 'NetworkMessage[zone_server.ObjectSpawn]'):
    # 塔生成的时候给它画个圈
    # p1的时候没有双人单人塔
    # 所以两个塔全画
    # 塔两个base id 0x1EB83D,0x1EB83C

    # logger.debug(f'spawn obj S{evt.message.base_id=:x}')
    time.sleep(.1)  # FIX: on spawn 的等待内存里面生成对象
    tower = raid_utils.NActor.by_id(evt.header.source_id)
    raid_utils.draw_circle(
        radius=3, pos=tower, duration=10, color=glm.vec4(0.9, 1, 0, 0.6)
    )


@omega.on_add_status(3507, 3508, 3509, 3510)
def on_add_staus_wave_cannon_p1threeplayer(evt: 'ActorControlMessage[actor_control.AddStatus]'):
    if raid_utils.assert_status(raid_utils.NActor.by_id(evt.source_id), evt.param.status_id, 5):
        omega = next(raid_utils.find_actor_by_base_id(0x3d5c))
        t_actor = raid_utils.NActor.by_id(evt.source_id)
        raid_utils.draw_rect(
            pos=omega, facing=lambda _: glm.polar(t_actor.update().pos - omega.update().pos).y,
            width=6, length=60, duration=5.1

        )


@omega.on_add_status(3424, 3495, 3496, 3497)
def on_add_status_aoeone(evt: 'ActorControlMessage[actor_control.AddStatus]'):
    # 10s/16s/22s/28s 大约有个0.1s延迟，和上面同时判定
    # 执行技能 31502 Guided Missile Kyrios
    # 圆形，范围 5
    # 明显的3311分散
    actor = raid_utils.NActor.by_id(evt.source_id)
    if raid_utils.assert_status(actor, evt.param.status_id, 5):
        raid_utils.draw_circle(radius=3, pos=actor, duration=5)
