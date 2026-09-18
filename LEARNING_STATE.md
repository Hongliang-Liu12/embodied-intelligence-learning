# 学习进度与下一次接续卡

> 本文件是当前进度的唯一权威记录。总计划见 MASTER_PLAN.md。自 v1.2 起，**只用 A01–H04 作为正式课程编号**。

更新日期：2026-09-18。
课程基线：v1.0，72 单元 / 95 题；仓库执行修订：v1.2。
当前阶段：**P1-A——第一个真正机械臂端到端工程（B 阶段完成后插入）**。
当前项目：P1——传统视觉抓取闭环。
当前课程：**P1-A——已知目标位姿的 UR5e + Robotiq 2F-85 + MoveIt + MuJoCo 执行闭环**。
P1-A 工程课表：**6 讲 / 24 小节**，详见 [P1_A_PROJECT_PLAN.md](P1_A_PROJECT_PLAN.md)。
当前工程小节：**第 2 讲第 2.2 节：tool0、flange、gripper_base、tcp_link 与 fixed joint 安装变换（5/24 已完成，2.2 进行中）**。

## 1. A 阶段
A01–A08 已完成首轮学习与核心验收。

## 2. B 阶段完成情况
- B01 URDF：已完成首轮。
- B02 三维资产与夹爪：已完成首轮。
- B03 ROS 2 与 TF：已完成首轮 + 实操。
- B04 UR5 逆解与奇异处理：已完成首轮 + 实操。
- B05 Dijkstra / A*：已完成首轮 + 实操。
- B06 RRT 与配置空间：已完成首轮 + 实操。
- B07 MoveIt 规划到执行：已完成首轮。
- B08 PD/PID 深化：已完成首轮 + 参数对比实操。
- B09 MPC：已完成首轮 + 两版数值实操。
- B10 延迟诊断：已完成首轮 + 延迟实验。

### B10 实验结果
- 已区分感知、计算、通信、控制周期、执行器/机械响应等多段延迟。
- 已理解端到端 latency 是 processing / communication / waiting / queueing / physical response 的累积。
- 已理解反馈延迟会让控制器使用过时状态，引入相位滞后，导致超调、振荡，严重时不稳定。
- 已区分 latency 与 jitter。
- 已掌握 timestamp / profiling 分段测时思路。
- 已理解 ROS 2 queue/callback、GPU 推理、CPU-GPU 拷贝、跨机网络、同步等待、控制频率等常见延迟来源。
- 已理解典型优化手段：降低推理时延、减少旧消息排队、异步流水线、缩短队列、提高关键回路频率、减少跨机通信、简化规划与模型、必要时做预测补偿。
- 已完成最小 PD 延迟注入实验：比较 0/20/50/100 ms 反馈延迟；用户实测 **100 ms 时出现明显振荡**。

**B01–B10 已完成首轮。**

## 3. 当前唯一任务：P1-A 第一个真正机械臂端到端工程

目的：在进入 C01 视觉/相机阶段前，把 B 阶段零散知识串成一个完整机械臂工程。首版不加相机与 GraspNet，目标是“已知目标抓取位姿 → MoveIt 规划 → RobotTrajectory → MuJoCo 执行 → 夹爪闭合 → 抬起”。

### 项目固定步骤
1. 已冻结具体型号：**UR5e**，后续 P1 不混用经典 UR5 参数。
2. 已冻结夹爪：**Robotiq 2F-85**；后续明确 tool0 → gripper_base → tcp_link 的安装变换。
3. 在 ROS 2 / MoveIt 中加载机器人模型与 planning group，确认 TF 和 TCP。
4. 设置一个已知目标抓取 Pose，不依赖相机。
5. MoveIt 完成 IK、碰撞检查和路径规划。
6. 读取并记录 RobotTrajectory：关节名、顺序、单位、time_from_start。
7. 显式完成 MoveIt → MuJoCo 集成：首版允许“导出轨迹后在 MuJoCo 回放”，不假装两个库自动互通。
8. 在 MuJoCo 中按轨迹执行机械臂，夹爪闭合并抬起目标物体。
9. 记录失败类型：模型/TF、IK、碰撞、轨迹映射、控制、接触/滑落。
10. 形成可复现证据：命令、版本、模型、轨迹文件、运行录像/截图、README。

### P1-A 验收
- 机器人型号、关节名/顺序、单位、TCP 定义一致。
- MoveIt 输出能明确读出 joint trajectory，不只看 RViz 动画。
- MuJoCo 执行的是轨迹，不用直接改 qpos 冒充控制执行。
- 至少完成一次“接近 → 闭合 → 抬起”流程；若因环境阻塞未完成，必须记录阻塞点，不伪造成功。
- 首版目标是工程链路打通，不追求视觉智能与高成功率。

完成 P1-A 后再进入 C01，相机/深度/点云/标定/GraspNet 会把它升级成 P1 完整视觉抓取闭环。

## 4. 接续规则
当前不直接进入 C01。先完成 P1-A 必要机械臂工程，再继续 C01–C08。

## P1-A 当前冻结启动配方（本机 WSL / ROS 2 Humble）

本机使用 **zsh**。仅启动 MoveIt/RViz 不足以提供完整 TF；需要同时启动 UR 假硬件控制层、ros2_control、robot_state_publisher 与 joint_state_broadcaster。后续 P1-A 固定沿用下面两个 zsh 终端配置，两个终端必须保持相同的 ROS_DOMAIN_ID 与 RMW_IMPLEMENTATION。

终端一：UR5e 假硬件 + 控制器 + TF
```bash
source /opt/ros/humble/setup.zsh
export ROS_DOMAIN_ID=42
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

ros2 launch ur_robot_driver ur_control.launch.py \
  ur_type:=ur5e \
  robot_ip:=0.0.0.0 \
  use_fake_hardware:=true \
  launch_rviz:=false \
  launch_dashboard_client:=false \
  initial_joint_controller:=joint_trajectory_controller
```

终端二：MoveIt + RViz
```bash
source /opt/ros/humble/setup.zsh
export ROS_DOMAIN_ID=42
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export QT_FONT_DPI=144

ros2 launch ur_moveit_config ur_moveit.launch.py \
  ur_type:=ur5e \
  launch_rviz:=true
```

验证命令：
```bash
ros2 run tf2_ros tf2_echo base tool0

ros2 service call \
  /controller_manager/list_controllers \
  controller_manager_msgs/srv/ListControllers \
  "{}"

ros2 topic echo /joint_states --once
```

当前本机 ROS 2 CLI 中没有 `ros2 control` 扩展，因此 **不再使用 `ros2 control list_controllers`**；控制器状态通过 `/controller_manager/list_controllers` service 查询。

已实测 `tf2_echo base tool0` 持续输出正常变换，例如 Translation 约为 `[-0.001, -0.233, 1.079]`。刚启动 TF 时短暂出现 frame does not exist 可等待约 1 秒后重试，属于初始化时序。

已通过 `/controller_manager/list_controllers` service 实测：`joint_state_broadcaster` 与 `joint_trajectory_controller` 均为 `active`。已读取 `/joint_states`，确认 6 个 UR5e 关节状态；已讲清 `name[i]` 与状态数组按索引对应、revolute joint position 使用 rad，以及 `robot_state_publisher` 根据 URDF + joint states 发布 TF。P1-A 第 1 讲验收完成。

注意：官方较新的 UR ROS 2 Driver 文档使用 `use_mock_hardware` 作为参数名，但当前本机 Humble 安装环境已经实测 `use_fake_hardware:=true` 可用；P1-A 以“本机已验证命令”为准，不在中途随意切换参数名。
