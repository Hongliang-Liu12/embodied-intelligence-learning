# 学习进度与下一次接续卡

> 本文件是当前进度的唯一权威记录。总计划见 MASTER_PLAN.md。自 v1.2 起，**只用 A01–H04 作为正式课程编号**；旧对话中的 M01–M08 只作为历史实操记录，不再决定下一课。

更新日期：2026-09-18。
课程基线：v1.0，72 单元 / 95 题；仓库执行修订：v1.2。
当前阶段：**B——UR5 系列、规划与控制**。
当前项目：P1——传统视觉抓取闭环（先完成机械臂与规划基础）。
当前课程：**B10——响应延迟诊断与优化**。

## 1. A 阶段完成情况

- **A01–A08 已完成首轮学习与核心验收。**
- 已覆盖 MuJoCo 基础、body/geom/frame、joint、qpos/qvel、FK/IK、Jacobian/奇异性、actuator/ctrl、PD 控制、控制周期、限位/饱和、扰动恢复。
- 已完成单关节 PD 与扰动恢复实验；P0 仍有少量代码统一提交和二连杆 MuJoCo 数值证据可在后续项目整理时补齐，但不阻塞主线。

## 2. B01–B08 完成情况

- **B01 URDF**：已掌握 link/joint、parent/child、origin xyz/rpy、axis、limit、visual/collision/inertial。
- **B02 三维资产与夹爪**：已理解 STL/mesh、材质/纹理、UV、scale、fixed joint、tool0、TCP、mimic joint。
- **B03 ROS 2 与 TF**：已掌握 Node、Topic、Publisher/Subscriber、Service、Action、TF；完成 pub/sub 与静态 TF 实操。
- **B04 UR5 IK 与奇异处理**：已理解多分支 IK、硬约束/软代价、连续性、奇异性、阻尼数值 IK；完成最小筛选实验。
- **B05 Dijkstra / A\***：已理解 g/h/f、Open/Closed、启发函数、松弛与路径回溯；完成二维网格 A* 实操。
- **B06 RRT 与配置空间**：已理解 C-space、采样/nearest/steer、goal bias、step size、edge collision check；完成二维 RRT 与可视化。
- **B07 MoveIt 规划到执行**：已理解 Pose/joint target、Planning Scene、planning group / end effector / TCP、OMPL/RRT 层级、path/trajectory、plan/execute；面试核心结论：真正用于执行的是带时间信息的关节轨迹。
- **B08 PD/PID 深化**：已理解超调、上升/稳定时间、Kp/Kd 调参、稳态误差、I 项、windup、D 项噪声、saturation/clipping/joint limit；完成参数对比实操。

## 3. B09 完成情况：MPC

- 已理解 MPC = Model Predictive Control，Model 指用于预测未来状态的动力学/状态模型。
- 已理解离散预测关系：当前状态 + 控制输入 → 下一状态，并可连续滚动预测未来多步。
- 已理解 prediction horizon / control horizon 的含义。
- 已理解 cost function：可同时惩罚跟踪误差、控制量大小和控制变化率；Q/R/S 权重决定控制偏好。
- 已理解 constraints 可显式加入优化：关节角、速度、力矩、安全边界等。
- 已理解 receding horizon：每周期预测未来多步，但只执行第一步，再重新测量和优化。
- 已比较 MPC 与 PID：PID 简单、实时、弱模型依赖；MPC 显式预测未来、处理多变量和约束更强，但计算更重且依赖模型。
- 已完成第一版教学 MPC：只比较整段恒定控制序列，系统停在约 4.7，暴露候选序列过粗的问题。
- 已完成升级版多步控制序列搜索：使用 `itertools.product` 枚举未来多步控制组合，仍只执行第一步并滚动重算；实际达到目标 `x=5`。
- 已逐块理解代码：`predict()`=模型预测，`cost_function()`=方案打分，`mpc_control()`=搜索最优控制序列，主循环=执行第一步 + 滚动重优化。

**B09 已完成首轮 + 两版数值实操。**

## 4. 当前唯一任务：B10 响应延迟诊断与优化

知识目标：
1. 区分感知延迟、通信延迟、规划延迟、控制周期延迟、执行器/机械响应延迟。
2. 理解端到端 latency 与各模块 latency 的关系：总延迟通常是多段串联造成的。
3. 理解控制系统中的 delay 为什么会降低相位裕度、导致“慢半拍”、超调、振荡甚至不稳定。
4. 学会用 timestamp / profiling 对相机→算法→规划→控制器→执行器进行分段测时。
5. 理解控制频率、仿真 timestep、ROS 2 callback/queue、网络传输、GPU 推理时间等如何影响延迟。
6. 学会典型优化手段：提高关键回路频率、减少阻塞、异步流水线、降低模型推理时延、缩短队列、预测补偿等。
7. 区分“平均延迟”和“抖动 jitter”；机器人控制中稳定的小延迟与不稳定的大抖动影响不同。
8. 做一个最小 delay 数值实验或代码级演示，观察增加延迟后闭环响应如何恶化，并形成面试回答。

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
| B09 | MPC | **已完成首轮 + 两版实操** |
| **B10** | **延迟诊断** | **当前课程** |

## 6. 实操与接续规则

继续保持“面经优先 + 必要实操”原则。代码不用死背，但核心数据结构、控制链与执行逻辑必须真正理解。B10 安排最小延迟响应实验。

每次开始先读本文件和 TEACHING_RULES.md。只按正式 A/B/C... 课号报进度。课后更新：实际完成、仍不理解、证据等级、下一正式单元。路线变化写 CHANGELOG.md。
