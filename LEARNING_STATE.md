# 学习进度与下一次接续卡

> 本文件是当前进度的唯一权威记录。总计划见 MASTER_PLAN.md。自 v1.2 起，**只用 A01–H04 作为正式课程编号**；旧对话中的 M01–M08 只作为历史实操记录，不再决定下一课。

更新日期：2026-09-16。
课程基线：v1.0，72 单元 / 95 题；仓库执行修订：v1.2。
当前阶段：**B——UR5 系列、规划与控制**。
当前项目：P1——传统视觉抓取闭环（先完成机械臂与规划基础）。
当前课程：**B03——ROS 2 与坐标传递：节点、话题、动作接口、TF**。

## 1. A 阶段完成情况

### A01–A08
- A01–A08 已完成首轮学习与核心验收。
- 已覆盖 MuJoCo 基础、body/geom/frame、joint、qpos/qvel、FK/IK、Jacobian/奇异性、actuator/ctrl、PD 控制、控制周期、限位/饱和、扰动恢复。
- 已完成单关节 PD 与扰动恢复实验；P0 仍有少量代码统一提交和二连杆 MuJoCo 数值证据可在后续项目整理时补齐，但不阻塞主线。
- A08 详见 `learning_logs/2026-09-16_A08_control.md`。

## 2. B01 完成情况：URDF

- 已理解 URDF 的 `link` / `joint` 树结构，parent/child 由 joint 显式建立。
- 已掌握 joint 的 `origin xyz/rpy`、`axis`、`limit`，并区分固定安装变换与运行时关节角。
- 已理解 `visual` / `collision` / `inertial` 各自职责及其 origin 的参考系。
- 已理解 geometry origin 不等于端点；box 默认以几何中心为 origin。
- 已把 URDF 运动链与前面 FK / Transformation Matrix 联系起来。
- 已完成最小二连杆 URDF 面试级阅读。

**B01 已完成首轮。**

## 3. B02 完成情况：三维资产与夹爪

- 已从零理解 mesh / STL：STL 主要描述三角网格几何，不等于完整材质/纹理模型。
- 已区分颜色、材质、纹理；纯色可在 URDF `material/color` 指定，真正纹理贴图通常需要 UV，并更适合 OBJ/DAE 等格式和相应工具链。
- 已理解 mesh `scale`、单位与坐标轴问题；常见 `0.001` 是 mm→m。
- 已形成调试口诀：位置错看 `xyz`，方向错看 `rpy`，尺寸错看 `scale`。
- 已理解夹爪通过 fixed joint 挂到 UR5 末端；模型自由度应与真实机构一致。
- 已区分 `wrist_3_link`、`tool0`、`gripper_base`、TCP：tool0 是标准工具接口参考 frame，TCP 是真正任务执行参考 frame。
- 已理解夹爪内部可用 revolute/prismatic joint；机械耦合时可用 mimic joint，是否 mimic 取决于真实机构。
- 已完成最小 URDF 实操思维验收：`wrist_3_link → tool0 → gripper_base → tcp_link`，能修改 fixed joint 的 `xyz/rpy` 并处理 cm→m、deg→rad。
- 用户明确提出：后续继续以面经进度为主，但在必要节点必须增加代码/工程实操；不要求每个概念都打断主线做实验。

**B02 已完成首轮。**

## 4. 当前唯一任务：B03 ROS 2 与 TF

知识目标：
1. 先定义 ROS 2 是什么，它在机器人系统里解决什么问题；不要默认知道 ROS/节点/中间件。
2. 理解 node、topic、publisher、subscriber：谁产生数据、谁消费数据、消息如何流动。
3. 理解 service 与 action，尤其为什么 MoveIt / 机械臂执行常更适合 action 而不是普通 topic。
4. 理解 message / interface 的最小概念：消息不是“随便一个 Python 变量”，而是有结构的通信类型。
5. 理解 TF / TF2 是运行时坐标变换系统，和 URDF 中的静态/运动学结构如何衔接。
6. 区分 static transform 与 dynamic transform；理解 robot_state_publisher / joint_states 在整条链中的作用。
7. 能从 `base_link → ... → tool0 → tcp_link` 理解 TF tree，并回答一个点从 camera frame 转到 base frame 的基本思路。
8. 做一个最小 ROS 2 / TF 实操或代码级演示；如果本机环境不便，则至少做可运行的最小节点/消息代码阅读，不把 B03 变成纯名词课。

教学顺序：ROS 2 为什么存在 → node/topic → service/action → message → TF tree → URDF 与 TF → 最小代码/实操 → 面试验收。

## 5. B 阶段路线

| 正式课号 | 内容 | 状态 |
|---|---|---|
| B01 | URDF：link/joint、fixed origin、visual/collision/inertial | **已完成首轮** |
| B02 | 三维资产与夹爪：STL、mesh、材质、安装变换、工具坐标 | **已完成首轮** |
| **B03** | **ROS 2 与坐标传递：节点、话题、动作接口、TF** | **当前课程** |
| B04 | UR5 逆解与奇异处理：多解、限位、碰撞、连续性、代价 | B03 后 |
| B05 | Dijkstra / A* | B04 后 |
| B06 | RRT 与配置空间 | B05 后 |
| B07 | MoveIt 规划到执行 | B06 后 |
| B08 | PD/PID 深化：超调、稳态误差、噪声、积分饱和 | B07 后 |
| B09 | MPC | B08 后 |
| B10 | 延迟诊断 | B09 后 |

## 6. 实操与证据边界

用户已报告本地存在 MuJoCo 单杆、重力、Actuator、PD、IK/FK 数学验证等实验文件，但尚未完整统一提交到仓库。不伪造源码。

B03 开始保持“面经优先 + 必要实操”原则：概念若不影响后续理解可快速通过；遇到 TF、MoveIt、GraspNet、SAC 等仅靠口头难以掌握的节点，必须安排最小代码/工程验证。

## 7. 接续规则

每次开始先读本文件和 TEACHING_RULES.md。只按正式 A/B/C... 课号报进度。课后更新：实际完成、仍不理解、证据等级、下一正式单元。路线变化写 CHANGELOG.md。
