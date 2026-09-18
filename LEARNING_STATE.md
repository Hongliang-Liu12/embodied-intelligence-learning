# 学习进度与下一次接续卡

> 本文件是当前进度的唯一权威记录。总计划见 MASTER_PLAN.md。自 v1.2 起，**只用 A01–H04 作为正式课程编号**；旧对话中的 M01–M08 只作为历史实操记录，不再决定下一课。

更新日期：2026-09-18。
课程基线：v1.0，72 单元 / 95 题；仓库执行修订：v1.2。
当前阶段：**B——UR5 系列、规划与控制**。
当前项目：P1——传统视觉抓取闭环（先完成机械臂与规划基础）。
当前课程：**B08——PD/PID 深化：超调、稳态误差、噪声、积分饱和**。

## 1. A 阶段完成情况

- **A01–A08 已完成首轮学习与核心验收。**
- 已覆盖 MuJoCo 基础、body/geom/frame、joint、qpos/qvel、FK/IK、Jacobian/奇异性、actuator/ctrl、PD 控制、控制周期、限位/饱和、扰动恢复。
- 已完成单关节 PD 与扰动恢复实验；P0 仍有少量代码统一提交和二连杆 MuJoCo 数值证据可在后续项目整理时补齐，但不阻塞主线。
- A08 详见 `learning_logs/2026-09-16_A08_control.md`。

## 2. B01–B06 完成情况

- **B01 URDF**：已掌握 link/joint、parent/child、origin xyz/rpy、axis、limit、visual/collision/inertial，并完成最小二连杆 URDF 阅读。
- **B02 三维资产与夹爪**：已理解 STL/mesh、颜色/材质/纹理、UV、OBJ/DAE、scale、fixed joint、tool0、gripper_base、TCP、mimic joint；完成最小夹爪挂载 URDF 思维实操。
- **B03 ROS 2 与 TF**：已掌握 Node、Topic、Publisher/Subscriber、Service、Action、TF；完成 pub/sub Python 实操和静态 TF 实操。
- **B04 UR5 IK 与奇异处理**：已理解多分支 IK、硬约束/软代价、连续性、跳解、肩/肘/腕奇异、阻尼数值 IK；完成最小 Python 多解筛选实验。
- **B05 Dijkstra / A\***：已理解 g/h/f、Open/Closed、启发函数、松弛与路径回溯；完成二维网格 A* 实操并进一步拆解代码实现。
- **B06 RRT 与配置空间**：已理解 C-space、C_free/C_obs、sample/nearest/steer、goal bias、step size、edge collision check；完成二维 RRT 代码与可视化，并通过可视化主动发现“node collision-free ≠ edge collision-free”。

## 3. B07 完成情况：MoveIt 规划到执行

- 已明确 MoveIt 是**运动规划与执行协调框架**，不是物理仿真器；MuJoCo 才是物理仿真层。
- 已理解 MoveIt 可接收两类常见目标：joint target 与末端 Pose target；Pose target 通常需先通过 IK 转成目标关节状态。
- 已回答面经核心：MoveIt 真正用于执行的输出不是单个末端点，而是**带时间信息的关节轨迹（joint trajectory / RobotTrajectory 语义）**。
- 已区分 path 与 trajectory：path 只描述经过哪些配置，trajectory 还带时间，常包含位置/速度/加速度等执行信息。
- 已理解 Planning Scene 是 MoveIt 做碰撞检查与规划时使用的“机器人 + 环境”世界模型，不是物理仿真器。
- 已区分 planning group / end effector / TCP：planning group 定义哪些关节参与规划，end effector 是末端工具结构，TCP 是真正任务参考坐标系。
- 已理解 MoveIt 与 OMPL / RRT 的层级：MoveIt 是总框架，OMPL 是常用规划库，RRT/RRTConnect 是其中的采样式规划算法。
- 已串通完整链路：Pose target → IK → q_goal → 规划 → 时间参数化 → joint trajectory → controller → MuJoCo / 真实 UR5。
- 已理解 `plan()` 与 `execute()` 分离：plan 只生成轨迹，execute 才下发给控制器执行。
- 面试回答已形成：MoveIt 接受 Pose 或 joint target；最终执行给控制器的是关节轨迹，而不是单独末端点。

**B07 已完成首轮。**

## 4. 当前唯一任务：B08 PD/PID 深化

知识目标：
1. 复习 A08 的基本关节 PD：`tau = Kp(q_des-q) - Kd*qvel`，明确 P 看位置误差、D 看速度/变化趋势。
2. 深入理解超调、振荡、上升时间、稳定时间与阻尼之间的关系。
3. 理解稳态误差为什么会出现，以及 I 项为什么能消除持续偏差。
4. 理解 integral windup：执行器饱和时误差仍持续积分，导致恢复后严重过冲；理解 anti-windup 的基本思路。
5. 理解 D 项为什么容易放大测量噪声，以及工程上为什么常做滤波或使用速度测量而不是直接差分位置。
6. 区分 joint limit、actuator saturation、controller output clipping 与安全边界。
7. 能回答“kp 太大/太小、kd 太大/太小、ki 太大”的典型现象与调参逻辑。
8. 做一个最小数值/仿真实验：比较不同 Kp/Kd/Ki 对响应曲线、超调、稳态误差和 windup 的影响。

## 5. B 阶段路线

| 正式课号 | 内容 | 状态 |
|---|---|---|
| B01 | URDF：link/joint、fixed origin、visual/collision/inertial | **已完成首轮** |
| B02 | 三维资产与夹爪 | **已完成首轮** |
| B03 | ROS 2 与坐标传递 | **已完成首轮 + 实操** |
| B04 | UR5 逆解与奇异处理 | **已完成首轮 + 实操** |
| B05 | Dijkstra / A* | **已完成首轮 + 实操** |
| B06 | RRT 与配置空间 | **已完成首轮 + 实操** |
| B07 | MoveIt 规划到执行 | **已完成首轮** |
| **B08** | **PD/PID 深化** | **当前课程** |
| B09 | MPC | B08 后 |
| B10 | 延迟诊断 | B09 后 |

## 6. 实操与接续规则

继续保持“面经优先 + 必要实操”原则。代码不用死背，但核心数据结构、控制链与执行逻辑必须真正理解。B08 安排最小响应曲线/参数对比实验，不只停留在概念题。

每次开始先读本文件和 TEACHING_RULES.md。只按正式 A/B/C... 课号报进度。课后更新：实际完成、仍不理解、证据等级、下一正式单元。路线变化写 CHANGELOG.md。
