# 学习进度与下一次接续卡

> 本文件是当前进度的唯一权威记录。总计划见 MASTER_PLAN.md。自 v1.2 起，**只用 A01–H04 作为正式课程编号**；旧对话中的 M01–M08 只作为历史实操记录，不再决定下一课。

更新日期：2026-09-18。
课程基线：v1.0，72 单元 / 95 题；仓库执行修订：v1.2。
当前阶段：**B——UR5 系列、规划与控制**。
当前项目：P1——传统视觉抓取闭环（先完成机械臂与规划基础）。
当前课程：**B09——MPC：预测、滚动优化与约束控制**。

## 1. A 阶段完成情况

- **A01–A08 已完成首轮学习与核心验收。**
- 已覆盖 MuJoCo 基础、body/geom/frame、joint、qpos/qvel、FK/IK、Jacobian/奇异性、actuator/ctrl、PD 控制、控制周期、限位/饱和、扰动恢复。
- 已完成单关节 PD 与扰动恢复实验；P0 仍有少量代码统一提交和二连杆 MuJoCo 数值证据可在后续项目整理时补齐，但不阻塞主线。
- A08 详见 `learning_logs/2026-09-16_A08_control.md`。

## 2. B01–B07 完成情况

- **B01 URDF**：已掌握 link/joint、parent/child、origin xyz/rpy、axis、limit、visual/collision/inertial，并完成最小二连杆 URDF 阅读。
- **B02 三维资产与夹爪**：已理解 STL/mesh、颜色/材质/纹理、UV、OBJ/DAE、scale、fixed joint、tool0、gripper_base、TCP、mimic joint；完成最小夹爪挂载 URDF 思维实操。
- **B03 ROS 2 与 TF**：已掌握 Node、Topic、Publisher/Subscriber、Service、Action、TF；完成 pub/sub Python 实操和静态 TF 实操。
- **B04 UR5 IK 与奇异处理**：已理解多分支 IK、硬约束/软代价、连续性、跳解、肩/肘/腕奇异、阻尼数值 IK；完成最小 Python 多解筛选实验。
- **B05 Dijkstra / A\***：已理解 g/h/f、Open/Closed、启发函数、松弛与路径回溯；完成二维网格 A* 实操并进一步拆解代码实现。
- **B06 RRT 与配置空间**：已理解 C-space、C_free/C_obs、sample/nearest/steer、goal bias、step size、edge collision check；完成二维 RRT 代码与可视化，并通过可视化主动发现“node collision-free ≠ edge collision-free”。
- **B07 MoveIt 规划到执行**：已理解 MoveIt 的系统定位、Pose/joint target、Planning Scene、planning group / end effector / TCP、OMPL/RRT 层级、path 与 trajectory、plan 与 execute；已形成面试回答：真正用于执行的是带时间信息的关节轨迹，而不是单独末端点。

## 3. B08 完成情况：PD/PID 深化

- 已理解上升时间、稳定时间、超调和振荡之间的区别。
- 已掌握 Kp 调参直觉：Kp 小 → 响应慢/系统软；Kp 大 → 响应快但更易超调/振荡/饱和。
- 已掌握 Kd 调参直觉：Kd 小 → 阻尼不足、易超调振荡；Kd 大 → 过度阻尼、响应发闷变慢。
- 已理解纯 P/PD 在持续重力/负载下为什么会保留稳态误差：P 项必须依赖非零误差持续提供补偿力矩。
- 已理解 I 项通过累计历史误差消除长期偏差；同时掌握 integral windup：执行器饱和时积分仍累积，解除饱和后可能严重超调。
- 已理解 anti-windup 基本思路：饱和时暂停/限制积分，或用 back-calculation。
- 已理解 D 项容易放大高频噪声，尤其位置差分除以小 dt 时；工程上常直接使用 qvel / 状态估计速度或对 D 项做低通滤波。
- 已区分 joint limit、actuator saturation 与 software clipping：分别约束状态范围、执行器能力、控制命令软件限幅。
- 已完成最小 Python PID 响应对比实验：`Kp large, Kd small` 超调最明显；除 PID 外的 P/PD 在持续负载下均保留稳态误差；PID 最终最接近目标值。

**B08 已完成首轮 + 参数对比实操。**

## 4. 当前唯一任务：B09 MPC

知识目标：
1. 从零理解 MPC = Model Predictive Control，为什么叫“模型预测控制”。
2. 理解预测模型：根据当前状态和候选控制输入，预测未来若干步状态。
3. 理解 prediction horizon / control horizon：一次往未来看多远。
4. 理解 cost function：跟踪误差、控制量大小、控制变化率等可以同时进入优化目标。
5. 理解 constraints：关节角、速度、力矩、碰撞/安全边界等约束如何进入优化。
6. 理解 receding horizon：每个控制周期只执行优化结果的第一步，然后重新测量、重新优化。
7. 比较 MPC 与 PID：PID 主要基于当前/历史误差，MPC 显式预测未来并能直接处理多变量与约束，但计算更重、依赖模型。
8. 做一个最小一维/二阶系统 MPC 数值实验或代码级演示，并形成面试回答框架。

## 5. B 阶段路线

| 正式课号 | 内容 | 状态 |
|---|---|---|
| B01 | URDF | **已完成首轮** |
| B02 | 三维资产与夹爪 | **已完成首轮** |
| B03 | ROS 2 与坐标传递 | **已完成首轮 + 实操** |
| B04 | UR5 逆解与奇异处理 | **已完成首轮 + 实操** |
| B05 | Dijkstra / A* | **已完成首轮 + 实操** |
| B06 | RRT 与配置空间 | **已完成首轮 + 实操** |
| B07 | MoveIt 规划到执行 | **已完成首轮** |
| B08 | PD/PID 深化 | **已完成首轮 + 实操** |
| **B09** | **MPC** | **当前课程** |
| B10 | 延迟诊断 | B09 后 |

## 6. 实操与接续规则

继续保持“面经优先 + 必要实操”原则。代码不用死背，但核心数据结构、控制链与执行逻辑必须真正理解。B09 安排最小预测控制数值实验，不只停留在概念题。

每次开始先读本文件和 TEACHING_RULES.md。只按正式 A/B/C... 课号报进度。课后更新：实际完成、仍不理解、证据等级、下一正式单元。路线变化写 CHANGELOG.md。
