# 俄罗斯方块机械臂项目 — Claude 协作指南

## 项目简介

俯拍摄像头识别35个俄罗斯方块的位姿，6轴机械臂+吸盘将其依次放入14×10棋盘。

**系统组件：**
- PC (Python, `src/`) ↔ 机械臂 via TCP `192.168.10.200:2017`
- PC ↔ STM32吸盘 via Serial `COM4, 9600 baud`
- 机械臂端：`lua_http_control.lua`（部署在机械臂上，含厂家私有函数）

**TCP 指令格式：** `S,x,y,z,rx,ry,rz`（后三轴单位：弧度）
**机械臂回传信号：** `fall`（到达抓取位）→ 吸盘ON；`down`（到达放置位）→ 吸盘OFF

---

## 开发规则（必须严格遵守）

1. **禁止修改原始代码** — `src/modules/` 和 `src/main.py` 只读，不可编辑
2. **新脚本统一用 `zhuxy_` 前缀** — 例：`zhuxy_test_arm.py`
3. **先做最小功能单元** — 不要一上来就写完整流程
4. **可调参数写入配置文件** — 新功能的参数放到 `src/zhuxy_config.py` 或独立 json
5. **注释和 print 用中文**

---

## 关键文件速查

| 文件 | 说明 | 可否修改 |
|------|------|---------|
| `src/main.py` | 主入口（含 TEST_DATA 测试数据集） | ❌ 只读 |
| `src/modules/config.py` | 原项目配置（IP、串口、视觉参数等） | ❌ 只读 |
| `src/modules/tcp_client.py` | TCP通讯 + 串口控制 | ❌ 只读 |
| `src/modules/vision_processor.py` | 图像识别（已完成可靠，勿动） | ❌ 只读 |
| `src/modules/join_queue.py` | 生成机械臂动作队列 | ❌ 只读 |
| `src/modules/board.py` | 棋盘逻辑 | ❌ 只读 |
| `src/zhuxy_config.py` | **新脚本专用配置文件** | ✅ 可改 |
| `src/zhuxy_arm_controller.py` | **自动抓放序列控制器** | ✅ 可改 |

---

## 解集变量（视觉识别输出）

```python
stats        # 字典，所有方块的类型、矫正角度、坐标
number_list  # 各类型方块数量 [I, L_left, L_right, O, T, Z_left, Z_right]
center_list  # 放置坐标列表
type_list    # 放置顺序（方块类型）
angle_list   # 放置旋转角度
```

动作队列由 `join_queue(stats, number_list, center_list, type_list, angle_list)` 生成，
格式：`[[x,y,z,Rx,Ry,Rz], ...]`，偶数索引=抓取位置(Z≈100)，奇数索引=放置位置(Z≈90)。

---

## 当前开发状态

- [x] 图像识别与位姿解算（完成，稳定）
- [x] 棋盘摆放逻辑计算
- [x] `zhuxy_arm_controller.py` — 自动抓放序列控制器（状态机驱动，待实机测试）
- [ ] 实机联调验证 fall/down 信号时序
- [ ] 与视觉模块打通（目前用 TEST_DATA 绕过视觉求解）
- [ ] 完整流程集成测试

---

## 运行方式

```bash
# 工作目录必须是 src/
cd D:/Project/hzpt_robot_arm/src

# 测试自动抓放序列（使用 TEST_DATA）
python zhuxy_arm_controller.py

# 原始主程序（视觉+规划+执行完整流程）
python main.py
```

---

## 常用 Claude 指令

### 继续上次开发
```
继续开发，上次做到了 [具体描述]，现在要 [下一步]
```

### 创建新的最小功能测试
```
创建一个最小测试脚本，测试 [具体功能]，参数放到 zhuxy_config.py
```

### 查看当前文件结构
```
列出 src/ 目录下所有 zhuxy_ 开头的文件
```

### 调试某个模块
```
读取 [文件名]，分析 [具体问题]，不要修改原文件
```

### 修改配置参数
```
把 zhuxy_config.py 中的 [参数名] 改为 [新值]
```

### 添加新功能
```
在不修改原文件的前提下，新建 zhuxy_xxx.py 实现 [功能描述]
```

---

## 注意事项

- Lua 脚本中存在机械臂厂商私有函数（如 `table.insert`、`set_global_variable`），无法查看源码
- `to_Rz` 在 `join_queue.py` 中是**累加**的，每块旋转角度叠加到上一块的末尾角度上
- L形块（L_left/L_right）需要额外的中心点偏移（`L_shape_offset`）
- 串口连接失败时，`zhuxy_arm_controller.py` 会以无吸盘模式继续运行（用于纯机械臂运动测试）
