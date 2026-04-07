port = 2015 
ip ="192.168.10.111" 
init_tcp_server(port)        
sleep(5)
elite_print("init over")

-- 创建位姿队列和预计算队列
local raw_pose_queue = {}  -- 存储原始位姿数据
local calculated_pose_queue = {}  -- 存储已计算好逆解的位姿数据
local processing = false
local pose_counter = 0

-- 设置D000的默认值为0
set_global_variable("D000", 0)

-- 处理关节角度，确保不超过360度
function normalize_joint_angles(joints)
    if not joints then return nil end
    
    local normalized = {}
    for i = 1, #joints do
        normalized[i] = joints[i]
        if normalized[i] > 360 then
            normalized[i] = normalized[i] - 360
            elite_print("关节 " .. i .. " 角度超过360度，已修正为: " .. string.format("%.2f", normalized[i]))
        end
        if normalized[i] < -360 then
            normalized[i] = normalized[i] + 360
            elite_print("关节 " .. i .. " 角度超过360度，已修正为: " .. string.format("%.2f", normalized[i]))

        end
    end
    return normalized
end

-- 检查机器人是否到达目标位置
function check_robot_arrived(current_joint, target_joint)
    if not current_joint or not target_joint then return false end
    for i = 1, 6 do
        if math.abs(current_joint[i] - target_joint[i]) > 0.5 then
            return false
        end
    end
    return true
end

-- 计算位姿逆解
function calculate_inverse_kinematics()
    if #raw_pose_queue > 0 and #calculated_pose_queue < 3 then  -- 保持最多3组预计算的数据
        local pose = raw_pose_queue[1]
        -- 创建Z轴上升5cm的预备位姿
        local elevated_pose = {pose[1], pose[2], pose[3] + 25, pose[4], pose[5], pose[6]}
        
        -- 对预备位姿进行逆解
        local elevated_ret = get_inv_kinematics(elevated_pose)
        local target_ret = get_inv_kinematics(pose)
        
        -- 对关节角度进行处理，确保不超过360度
        elevated_ret = normalize_joint_angles(elevated_ret)
        target_ret = normalize_joint_angles(target_ret)
        
        if elevated_ret and target_ret then
            table.insert(calculated_pose_queue, {
                prep_pose = elevated_ret,
                target_pose = target_ret
            })
            table.remove(raw_pose_queue, 1)
            return true
        else
            elite_print("位姿逆解计算失败")
            table.remove(raw_pose_queue, 1)
            return false
        end
    end
    return false
end

-- 执行机器人运动
function execute_robot_motion()
    if #calculated_pose_queue > 0 and not processing then
        processing = true
        local current_poses = calculated_pose_queue[1]

        server_send_data(ip, "fall")
        
        set_global_variable("P001", table.unpack(current_poses.prep_pose))

        local arrived = false
        while not arrived do
            local current_joint = get_robot_joint()
            arrived = check_robot_arrived(current_joint, current_poses.prep_pose)
            calculate_inverse_kinematics()
            if not arrived then
                sleep(0.1)  -- 添加100ms的延时，避免过度占用CPU
            end
        end

        -- 移动到目标位置
        set_global_variable("P001", table.unpack(current_poses.target_pose))
        
        local target_arrived = false
        while not target_arrived do
            local current_joint = get_robot_joint()
            target_arrived = check_robot_arrived(current_joint, current_poses.target_pose)
            calculate_inverse_kinematics()
            if not target_arrived then
                sleep(0.1)  -- 添加100ms的延时，避免过度占用CPU
            end
        end

        
        pose_counter = pose_counter + 1
        if pose_counter % 2 == 0 then
            server_send_data(ip, "down")
            sleep(0.2)
        end

        set_global_variable("P001", table.unpack(current_poses.prep_pose))
        elite_print("返回预备位姿位置...")
        
        -- 移除已完成的位姿数据
        table.remove(calculated_pose_queue, 1)
        processing = false
        return true
    end
    return false
end

while(1)do 
    ret=is_client_connected(ip)     
    elite_print("client is connected")
    if(ret==1)then
        server_send_data(ip,"1")        
        recv="1"  
        while(recv ~= "2") do         
            sleep(0.1)                 
            Ret,recv=server_recv_data(ip,0,2015,0.5)
            ret=get_robot_joint()
            elite_print(recv ,Ret)
            
            if(Ret>=27.0)then
                local header, j1, j2, j3, j4, j5, j6 = string.match(recv, "([%a]+),([%-%d%.]+),([%-%d%.]+),([%-%d%.]+),([%-%d%.]+),([%-%d%.]+),([%-%d%.]+)")
                if(header == 'S')then
                    if j1 and j2 and j3 and j4 and j5 and j6 then
                        -- 将接收到的数据解析为位姿数据
                        local pose = {
                            tonumber(j1), tonumber(j2), tonumber(j3),
                            tonumber(j4), tonumber(j5), tonumber(j6)
                        }
                        
                        -- 添加到原始位姿队列
                        table.insert(raw_pose_queue, pose)
                        
                        -- 发送确认信号给PC，请求下一组数据
                        server_send_data(ip,"2")
                        
                        -- 尝试计算逆解
                        calculate_inverse_kinematics()
                    else
                        elite_print("Invalid position data format")
                    end
                end
            end
            
            -- 执行机器人运动（如果有已计算好的位姿）
            execute_robot_motion()
        end 
    end 
end
elite_print("over")
 