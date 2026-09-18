# P1-A 项目课表：UR5e + Robotiq 2F-85 + MoveIt + MuJoCo

> 项目定位：B10 完成后、C01 前的必做工程关卡。
> 目标：把 B 阶段知识串成第一个完整机械臂工程：**已知目标位姿 → MoveIt 规划 → RobotTrajectory → MuJoCo 执行 → 夹爪闭合 → 抬起**。
> 机器人固定为 **UR5e**，夹爪固定为 **Robotiq 2F-85**。
> 首版不加入相机、GraspNet；视觉抓取在 P1-B 再加入。

## 课程结构

P1-A 固定为 **6 讲，共 24 小节**。每讲 4 小节。

每一小节都按以下顺序教学：

**新概念解释 → 和已有知识建立关系 → 预测/小题 → 实际命令或代码 → 读取真实结果 → 考察 → 通过后进入下一节。**

任何第一次出现的 ROS 2 topic/service/action、controller、message 字段、MoveIt API、MuJoCo 接口、文件格式都必须先解释，不能先让学生执行再补概念。

## 第 1 讲｜把 UR5e 真正“跑起来”：模型、状态、TF、控制器

目标：理解 RViz 里为什么能出现一台会更新状态的 UR5e，并验证 ROS 2 控制链，而不是只看一张机器人模型。

### 1.1 启动层次：UR 模型、fake hardware、MoveIt、RViz
必须理解：
- URDF/Xacro 与 robot_description 是什么。
- fake hardware 是什么，为什么它不等于 MuJoCo 物理仿真。
- RViz 是可视化器，不是仿真器、规划器或控制器。
- UR driver / ros2_control / MoveIt / RViz 各在什么层。

验收：两个固定 zsh 终端可以启动，RViz 正常显示 UR5e。

### 1.2 TF：base、tool0 与机器人坐标树
必须理解：
- frame、TF、parent/child。
- tf2_echo target source 的含义。
- base → tool0 是当前工具坐标系相对基座的位姿。
- TF 与 FK 的关系。

实验：tf2_echo base tool0。

### 1.3 controller_manager 与两个核心 controller
必须理解：
- controller_manager 管理什么。
- joint_state_broadcaster：状态反馈出口。
- joint_trajectory_controller：关节轨迹执行入口。
- active 的意义。
- command interface 与 state interface 的基本区别。

实验：当前 Humble 环境不用不存在的 ros2 control CLI，改用：
~~~zsh
ros2 service call \
  /controller_manager/list_controllers \
  controller_manager_msgs/srv/ListControllers \
  "{}"
~~~

### 1.4 /joint_states 与 robot_state_publisher
必须理解：
- /joint_states 是 Topic。
- sensor_msgs/msg/JointState 中 name / position / velocity / effort 的含义。
- revolute joint 的 position 单位是 rad，velocity 是 rad/s，effort 通常按 N·m 理解；fake hardware 下 effort 不等于真实测得扭矩。
- name[i] 与 position[i] 等数组按索引对应；工程代码应按名字建立映射，不能假设固定顺序。
- robot_state_publisher 根据 **URDF + 当前 joint states** 发布 TF，本质上承担机器人状态对应的 FK/TF 发布工作。

实验：
~~~zsh
ros2 topic echo /joint_states --once
~~~

验收：能独立解释“状态从硬件如何到 /joint_states，再如何变成 TF”。

## 第 2 讲｜把夹爪装上去：URDF/Xacro、tool0、TCP、Robotiq

目标：把此前 B01/B02 的 URDF 知识真正用于 UR5e + Robotiq 2F-85 工程。

### 2.1 找到实际机器人描述文件
必须理解：
- ROS package 安装位置和工作空间 overlay。
- ur_description、ur_moveit_config 分工。
- Xacro 为什么用于生成 URDF。

实验：定位本机包路径和 UR5e 描述入口。

### 2.2 tool0、flange、gripper_base、tcp_link
必须理解：
- tool0 是工具接口 frame，不等于夹爪 TCP。
- fixed joint 安装变换。
- TCP 是任务使用的工具点。
- frame 命名与真实几何安装的关系。

实验：画出并核对：
wrist_3_link → tool0 → gripper_base → tcp_link。

### 2.3 Robotiq 2F-85 模型与关节
必须理解：
- 夹爪哪些 link/joint 真正运动。
- mimic/耦合关系为什么可能出现。
- visual、collision、inertial 都要关注。
- mesh 尺度和单位。

实验：加载/补齐 2F-85 描述，确认开合方向和尺度。

### 2.4 安装后的 TF 与 collision 验证
必须理解：
- “看起来装上了”不等于 TF/collision 正确。
- fixed transform、collision geometry、TCP 必须一致。

验收：RViz 中模型正确，TF 可查询，MoveIt 能识别正确末端工具链。

## 第 3 讲｜第一次真正 MoveIt 规划：从目标 Pose 到路径

目标：不用相机，手工指定一个安全目标位姿，让 MoveIt 生成机械臂运动计划。

### 3.1 planning group 与 current state
必须理解：
- planning group 是哪几个 joint/link 的规划集合。
- ur_manipulator 与末端执行器的关系。
- current state 从哪里来：/joint_states。

### 3.2 Pose 目标与参考系
必须理解：
- position + orientation。
- Pose 属于哪个参考 frame。
- quaternion 与 rpy 的关系。
- 已知目标 Pose 和后续视觉估计 Pose 的区别。

### 3.3 Pose → IK → q_goal
必须理解：
- MoveIt 接到 Pose 后为什么需要 IK。
- 多解、限位、碰撞、连续性。
- IK 成功不等于路径一定可行。

### 3.4 Plan 与 Execute 分开
必须理解：
- Plan：产生路径/轨迹。
- Execute：把轨迹交给控制器。
- RViz 中看到规划轨迹不等于真实执行。

实验：先只 Plan 一个安全目标，再执行一次 fake hardware。

验收：能解释从目标 Pose 到 joint_trajectory_controller 的完整链。

## 第 4 讲｜读懂 RobotTrajectory：MoveIt 到底输出了什么

目标：不再只看 RViz 动画，真正读取 MoveIt 的轨迹数据。

### 4.1 RobotTrajectory 的层次
必须理解：
- RobotTrajectory。
- JointTrajectory。
- joint_names。
- points。

### 4.2 每个 trajectory point 有什么
必须理解：
- positions：rad。
- velocities：rad/s。
- accelerations：rad/s²。
- time_from_start：该点相对轨迹起点的时间。
- 为什么路径加入时间后才是轨迹。

### 4.3 关节名与顺序映射
必须理解：
- MoveIt 数组顺序不能直接假设等于 MuJoCo actuator/qpos 顺序。
- 必须建立 joint_name → index 映射。
- 缺失/多余 joint 怎么检查。

### 4.4 导出轨迹
实验：把一次真实规划导出为可检查的 JSON/CSV/NumPy 数据。

验收：学生可以自己读出“第几个时间点，每个 UR5e 关节应该到多少 rad”。

## 第 5 讲｜MoveIt → MuJoCo：把规划变成物理执行

目标：显式连接两个系统，不把“两个软件都装好了”误认为自动互通。

### 5.1 两边机器人模型的一致性
必须理解：
- UR5e 型号必须一致。
- joint name、零位、方向、限位、单位必须一致。
- tool/TCP 定义必须一致。

### 5.2 时间与插值
必须理解：
- MoveIt time_from_start 与 MuJoCo timestep 的关系。
- 为什么控制周期通常比 trajectory point 更密。
- 最小插值思想。

### 5.3 控制执行，不直接改 qpos
必须理解：
- 直接写 qpos 是改状态，不是机械执行。
- 首版用 position/PD actuator 跟踪目标关节轨迹。
- desired q 与 actual q 的区别。

### 5.4 回放与误差验证
实验：MuJoCo 按 MoveIt 轨迹运动，记录 desired/actual joint positions。

验收：至少一条 UR5e 轨迹可以按时间执行，且关节映射、方向、单位正确。

## 第 6 讲｜完成最小抓取：接近、闭合、抬起与项目答辩

目标：完成第一个端到端机械臂项目，而不是只让机械臂空跑。

### 6.1 场景与已知抓取 Pose
必须理解：
- grasp pose、pre-grasp/approach pose。
- 为什么通常先接近再闭合。
- 目标物体 pose 首版直接已知。

### 6.2 Robotiq 闭合
必须理解：
- 夹爪 command 与 finger joint 状态。
- 接触、摩擦、夹持宽度。
- “闭合命令发出”不等于抓取成功。

### 6.3 抬起与成功判据
必须理解：
- lift trajectory。
- 物体是否随夹爪移动。
- 成功判据不能只是视觉上“好像抓住”。

### 6.4 失败分类与项目材料
失败分为：
- 模型/TF；
- IK；
- collision/path；
- trajectory mapping；
- controller；
- contact/friction/slip。

交付：
- 冻结启动命令；
- 版本/模型；
- 轨迹文件；
- MoveIt → MuJoCo 映射代码；
- 抓取录像/截图；
- README；
- 可回答面试追问。

## 当前进度

总进度：**P1-A 共 6 讲 / 24 小节**。

- 第 1 讲：进行中
  - 1.1 ✅ 完成：UR5e fake hardware + MoveIt + RViz 启动链。
  - 1.2 ✅ 完成：TF，已实测 base → tool0。
  - 1.3 ✅ 完成：controller_manager 与两个核心 controller，已实测均 active。
  - 1.4 ⏳ 当前：/joint_states 与 robot_state_publisher；概念已讲，等待读取一次真实 /joint_states 完成验收。
- 第 2–6 讲：未开始。

当前工程小节进度：**3 / 24 完成，当前第 4 小节**。

> 注意：这里的 3/24 是 P1-A 工程课表进度，不替代总课程 72 单元进度。A01–B10 已完成首轮，P1-A 是 B10 后插入的必做工程关卡。
