# 学习进度与下一次接续卡

> 本文件是当前进度的唯一权威记录。总计划见 MASTER_PLAN.md。自 v1.2 起，**只用 A01–H04 作为正式课程编号**；旧对话中的 M01–M08 只作为历史实操记录，不再决定下一课。

更新日期：2026-09-17。
课程基线：v1.0，72 单元 / 95 题；仓库执行修订：v1.2。
当前阶段：**B——UR5 系列、规划与控制**。
当前项目：P1——传统视觉抓取闭环（先完成机械臂与规划基础）。
当前课程：**B07——MoveIt：从目标到规划结果再到执行**。

## 1. A 阶段完成情况

### A01–A08
- A01–A08 已完成首轮学习与核心验收。
- 已覆盖 MuJoCo 基础、body/geom/frame、joint、qpos/qvel、FK/IK、Jacobian/奇异性、actuator/ctrl、PD 控制、控制周期、限位/饱和、扰动恢复。
- 已完成单关节 PD 与扰动恢复实验；P0 仍有少量代码统一提交和二连杆 MuJoCo 数值证据可在后续项目整理时补齐，但不阻塞主线。
- A08 详见 `learning_logs/2026-09-16_A08_control.md`。

## 2. B01–B04 完成情况

- **B01 URDF**：已掌握 link/joint、parent/child、origin xyz/rpy、axis、limit、visual/collision/inertial，并完成最小二连杆 URDF 阅读。
- **B02 三维资产与夹爪**：已理解 STL/mesh、颜色/材质/纹理、UV、OBJ/DAE、scale、fixed joint、tool0、gripper_base、TCP、mimic joint；完成最小夹爪挂载 URDF 思维实操。
- **B03 ROS 2 与 TF**：已掌握 Node、Topic、Publisher/Subscriber、Service、Action、TF；完成 pub/sub Python 实操和静态 TF 实操，验证 `base_link -> tool0 -> tcp_link` 组合变换。
- **B04 UR5 IK 与奇异处理**：已理解多分支 IK、硬约束/软代价、连续性、跳解、肩/肘/腕奇异、阻尼数值 IK；完成最小 Python 多解筛选实验。

## 3. B05 完成情况：Dijkstra / A*

- 已从零理解 node / edge / path cost。
- 已理解 Dijkstra 按累计代价 `g(n)` 最小扩展。
- 已理解 Open Set = 已发现待扩展，Closed Set = 已处理节点。
- 已理解 A* 使用 `f(n)=g(n)+h(n)`；`h(n)` 提供目标方向感，`h=0` 时退化为 Dijkstra。
- 已理解曼哈顿距离、欧氏距离与 admissible heuristic 的直觉。
- 已完成二维网格 A* Python 实操，成功得到路径：`(0,0)->(0,1)->(0,2)->(1,2)->(2,2)->(2,3)->(2,4)->(3,4)`。
- 已进一步拆解代码：`heapq`=Open 优先队列，`g_score`=`g(n)`，`heuristic`=`h(n)`，`closed`=Closed Set，`came_from`=路径回溯。
- 已澄清“发现节点”和“正式扩展节点”的区别：节点可先进入 Open，之后通过其他邻居发现更小 `g` 时更新；搜索阶段不是机器人已经实际走到该节点。

**B05 已完成首轮 + 最小代码实操。**

## 4. B06 完成情况：RRT 与配置空间

- 已理解 configuration 是完整关节状态 `q=[q1,...,qn]`；UR5 的 C-space 为 6 维关节空间。
- 已理解机械臂规划不能只看 TCP；整条机械臂每个中间 configuration 都必须无碰撞。
- 已理解 `C_free` 与 `C_obs`：现实障碍映射为配置空间中的不可行区域。
- 已理解 RRT 核心：随机采样 `q_rand` → 找最近 `q_near` → steer 得到 `q_new` → 局部路径碰撞检查 → 安全则加入树。
- 已澄清随机采样的意义是给搜索树提供探索方向，不是为了单独建立碰撞地图；目标仍是连通 `q_start` 和 `q_goal`。
- 已理解 goal bias：随机探索与偶尔直接朝目标采样的折中；step size：大步长快但粗，小步长慢但细。
- 已理解 RRT 适合连续高维空间，但原始路径通常不最优、不平滑，后续常做 shortcut/smoothing/trajectory optimization。
- 已完成二维 RRT Python 实操并成功找到路径；随后完成可视化。
- 用户通过可视化主动发现“端点均不碰撞但连线穿过障碍”的漏洞；已修正认识：**node collision-free 不等于 edge/local-path collision-free**，真实规划必须检查 `q_near -> q_new` 整段局部路径，连接 goal 时也同样检查。

**B06 已完成首轮 + 最小代码与可视化实操。**

## 5. 当前唯一任务：B07 MoveIt 规划到执行

知识目标：
1. 建立 MoveIt 在整个系统中的位置：URDF/TF 提供机器人模型和坐标，MoveIt 负责运动规划与执行协调，ROS 2 提供通信，控制器/MuJoCo/真实 UR5 负责执行。
2. 明确 MoveIt 的输入可能是末端 Pose 目标或关节目标，但规划器最终通常在关节配置空间中生成可执行轨迹。
3. 回答面经核心：**MoveIt 最后输出的不是“只有一个末端点”，而是带时间信息的关节轨迹（如 JointTrajectory / RobotTrajectory 语义）**；末端 Pose 目标需先经 IK/规划转成关节空间路径。
4. 理解 planning scene：机器人状态、障碍物、碰撞模型和允许碰撞关系。
5. 理解 planning group / end effector / TCP 与前面 URDF、tool0、gripper 的关系。
6. 理解“规划”和“执行”是两步：plan 生成轨迹，execute 通过控制接口下发给控制器；执行过程中可由 Action 提供反馈。
7. 结合 B05/B06 理解 MoveIt 底层可调用 OMPL 等规划器，RRT 系列只是其中一种；不要把 MoveIt 等同于 RRT。
8. 安排必要实操：先做最小 MoveIt/UR5 可运行或代码级验证；若环境安装成本过高，至少先完成消息结构和 plan→trajectory→controller 链路，再择机跑完整 demo。

## 6. B 阶段路线

| 正式课号 | 内容 | 状态 |
|---|---|---|
| B01 | URDF：link/joint、fixed origin、visual/collision/inertial | **已完成首轮** |
| B02 | 三维资产与夹爪：STL、mesh、材质、安装变换、工具坐标 | **已完成首轮** |
| B03 | ROS 2 与坐标传递：节点、话题、动作接口、TF | **已完成首轮 + 实操** |
| B04 | UR5 逆解与奇异处理 | **已完成首轮 + 实操** |
| B05 | Dijkstra / A* | **已完成首轮 + 实操** |
| B06 | RRT 与配置空间 | **已完成首轮 + 实操** |
| **B07** | **MoveIt 规划到执行** | **当前课程** |
| B08 | PD/PID 深化 | B07 后 |
| B09 | MPC | B08 后 |
| B10 | 延迟诊断 | B09 后 |

## 7. 实操与接续规则

继续保持“面经优先 + 必要实操”原则。用户希望先打通面经主线，但对 MoveIt、GraspNet、SAC、VLA 等仅靠口头难以掌握的节点必须安排最小工程验证；代码不用死背，但核心数据结构和执行链必须真正理解。

每次开始先读本文件和 TEACHING_RULES.md。只按正式 A/B/C... 课号报进度。课后更新：实际完成、仍不理解、证据等级、下一正式单元。路线变化写 CHANGELOG.md。
