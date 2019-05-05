def judge_room(average):
    if abs(average) <= 1:
        suggestion = 1
    elif average > 1:
        # 房间制冷量不足
        suggestion = "设定值不一致、温控系统出现问题或者末端供冷量不足。" \
                     "先检查监测点的温度真实设定值是否与现场设定值一致，" \
                     "若果是一致的其次需要检查温控系统是否出现了问题，" \
                     "如果存在问题建议修复温控系统，" \
                     "如果上述问题均不存在可以判断该监测点的负荷过大，" \
                     "需要增大末端供冷量，建议开大末端水阀。"
    else:
        # "楼层制冷量过盈"
        suggestion = "设定值不一致、盘管堵塞或者温控系统出现问题。" \
                     "先检查监测点的温度真实设定值是否与现场设定值一致，" \
                     "若果是一致的其次需要检查末端盘管是否出现了堵塞，" \
                     "如果是建议进行清洗，" \
                     "如果上述问题均不存在可以判断温控系统出现了问题，" \
                     "建议修复末端温控系统。"
    return suggestion


def judge_floor(average, floor_list):
    if abs(average) <= 1:
        suggestion = 1
    elif average > 1:
        # "楼层制冷量不足"
        if len(floor_list) <= 1:
            # "只有一层楼"
            suggestion = "该楼层制冷量不足。" \
                         "建议开该楼层的楼层冷冻水水阀以增加该楼层的制冷量," \
                         "如果冷冻水阀已经开至最大，" \
                         "建议增加增开冷机。"
        else:
            print("不止一层楼")
            suggestion = "该楼层制冷量不足。" \
                         "建议开大该楼层的楼层冷冻水水阀以增加该楼层的制冷量," \
                         "如果冷冻水阀已经开至最大，" \
                         "建议关小温度较底楼层的冷冻水阀。"
    else:
        # 过盈
        suggestion = "楼层整体制冷量过盈。建议关小该楼层的总冷冻水水阀减小流量。"
    return suggestion


def judge_building(average, building_list):
    if abs(average) <= 1:
        suggestion = 1
    elif average > 1:
        # "楼层制冷量不足"
        if len(building_list) <= 1:
            # "只有一层楼"
            suggestion = "楼栋整体制冷量不足。" \
                         "建议开大楼栋的总冷冻水水阀以增加该楼栋的制冷量," \
                         "如果冷冻水阀已经开至最大，" \
                         "建议增加增开冷机。"
        else:
            print("不止一栋楼")
            suggestion = "楼栋整体制冷量不足。" \
                         "建议开大该楼的楼栋冷冻水水阀以增加该楼栋的制冷量," \
                         "如果冷冻水阀已经开至最大，" \
                         "建议关小温度较底楼冻的冷冻水阀。"
    else:
        # 过盈
        suggestion = "楼栋整体制冷量过盈。建议关小该楼栋的总冷冻水水阀减小流量。"
    return suggestion



