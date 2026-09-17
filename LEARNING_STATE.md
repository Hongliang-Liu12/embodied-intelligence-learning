# 学习进度与下一次接续卡

> 本文件是当前进度的唯一权威记录。总计划见 MASTER_PLAN.md。自 v1.2 起，**只用 A01–H04 作为正式课程编号**；旧对话中的 M01–M08 只作为历史实操记录，不再决定下一课。

更新日期：2026-09-17。
课程基线：v1.0，72 单元 / 95 题；仓库执行修订：v1.2。
当前阶段：**B——UR5 系列、规划与控制**。
当前项目：P1——传统视觉抓取闭环（先完成机械臂与规划基础）。
当前课程：**B05——Dijkstra / A* 路径规划**。

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
- 已区分 `wrist_3_link`、`tool0`、`gripper_base`、TCP。
- 已理解夹爪内部可用 revolute/prismatic joint；机械耦合时可用 mimic joint。
- 已完成最小 URDF 实操思维验收：`wrist_3_link → tool0 → gripper_base → tcp_link`。

**B02 已完成首轮。**

## 4. B03 完成情况：ROS 2 与 TF

- 已建立整体层次：URDF 是模型描述层，ROS 2 是系统通信/组织层，MoveIt 是规划层，MuJoCo 是物理仿真层，真实 UR5 是硬件执行层。
- 已掌握 Node、Topic、Publisher、Subscriber、Service、Action 的基本职责与使用场景。
- 已完成 Publisher/Subscriber 最小 Python 实操：`robot_status_publisher` 在 `/robot_status` 上持续发布 String；`robot_status_subscriber` 持续收到消息。
- 已实际使用 `ros2 node list`、`ros2 topic list`、`ros2 topic echo` 检查 ROS graph 和消息流。
- 已总结 pub/sub 固定模板：Publisher = 定义 node → create_publisher → 构造 msg → publish；Subscriber = 定义 node → create_subscription → callback(msg)。
- 已理解 TF 是运行时坐标变换系统；fixed joint 对应静态关系，运动关节对应随状态变化的动态关系。
- 已明确 `tf2_echo target source` 的含义：把 source frame 的位姿表达在 target frame 下；target/source 与 parent/child 不是一套概念。
- 已完成静态 TF 实操：发布 `base_link → tool0` 与 `tool0 → tcp_link` 两段静态变换，并通过 `tf2_echo base_link tcp_link` 查询得到 Translation `[0.400, 0.200, 0.600]`，验证 TF 自动沿 tree 组合变换。

**B03 已完成首轮，并完成必要实操。**

## 5. B04 完成情况：UR5 逆解与奇异处理

- 已把二连杆多解迁移到 6 轴机械臂，理解同一 TCP 位姿可能对应多组关节角。
- 已理解 UR5 多解可从 shoulder / elbow / wrist 等不同几何分支直观理解。
- 已区分数学 IK 解与工程可用解：先做关节限位、碰撞等硬约束筛选，再做距离、连续性、奇异性等软代价排序。
- 已理解“离当前状态最近”是常用软代价，但不是绝对规则；连续轨迹中更应参考上一时刻关节状态，避免 IK 跳解。
- 已把 A07 的奇异性迁移到 UR5，理解肩部、肘部、腕部奇异的几何直觉与 Jacobian 降秩本质。
- 已明确近奇异时是 Jacobian 的小奇异值导致伪逆放大，不应仅表述为“某些元素小”。
- 已理解数值 IK：`e ≈ J Δq`、伪逆更新与 damped least squares；阻尼以部分末端精度换更有限、更稳定的关节更新。
- 已完成最小 Python 多解筛选实验：候选解先做 `[-π, π]` 限位过滤，再按与 `q_current` 的欧氏距离排序；实际选择 candidate 0，distance 约 0.33。
- 已形成面试回答框架：候选 IK → 限位/碰撞 → 连续性/距离 → 奇异风险/安全裕度 → 最终解；近奇异时结合阻尼、步长/速度限幅、换 branch 或重规划。

**B04 已完成首轮，并完成最小代码实操。**

## 6. 当前唯一任务：B05 Dijkstra / A*

知识目标：
1. 从零建立图搜索直觉：节点、边、边代价、路径代价。
2. 理解 Open Set / Closed Set 的作用，以及为什么需要维护“待扩展”和“已确认”的节点集合。
3. 理解 Dijkstra：按累计代价 `g(n)` 扩展，非负边权下可得到最短路。
4. 理解 A*：`f(n)=g(n)+h(n)`，其中 `h(n)` 是从当前节点到目标的启发式估计。
5. 理解 admissible / consistent heuristic 的直觉，不要求形式证明，但要知道为什么启发式不能随便高估。
6. 比较 Dijkstra 与 A*：A* 通过启发式减少无效扩展；当 `h=0` 时退化为 Dijkstra。
7. 做一个最小二维网格 Python 实操：障碍、起点、终点、Open/Closed、回溯路径。
8. 面试验收：能回答 A* / Dijkstra 区别、Open/Closed、heuristic 作用与常见距离选择。

教学顺序：图与网格 → Dijkstra → Open/Closed → A* → heuristic → 最小代码实验 → 面试整合。

## 7. B 阶段路线

| 正式课号 | 内容 | 状态 |
|---|---|---|
| B01 | URDF：link/joint、fixed origin、visual/collision/inertial | **已完成首轮** |
| B02 | 三维资产与夹爪：STL、mesh、材质、安装变换、工具坐标 | **已完成首轮** |
| B03 | ROS 2 与坐标传递：节点、话题、动作接口、TF | **已完成首轮 + 实操** |
| B04 | UR5 逆解与奇异处理：多解、限位、碰撞、连续性、代价 | **已完成首轮 + 实操** |
| **B05** | **Dijkstra / A*** | **当前课程** |
| B06 | RRT 与配置空间 | B05 后 |
| B07 | MoveIt 规划到执行 | B06 后 |
| B08 | PD/PID 深化：超调、稳态误差、噪声、积分饱和 | B07 后 |
| B09 | MPC | B08 后 |
| B10 | 延迟诊断 | B09 后 |

## 8. 实操与接续规则

继续保持“面经优先 + 必要实操”原则。B05 必须安排最小二维网格搜索代码实验，不把算法课变成只背定义。

每次开始先读本文件和 TEACHING_RULES.md。只按正式 A/B/C... 课号报进度。课后更新：实际完成、仍不理解、证据等级、下一正式单元。路线变化写 CHANGELOG.md。
