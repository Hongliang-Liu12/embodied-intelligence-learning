# 学习进度与下一次接续卡

> 本文件是当前进度的唯一权威记录。总计划见 MASTER_PLAN.md。自 v1.2 起，**只用 A01–H04 作为正式课程编号**；旧对话中的 M01–M08 只作为历史实操记录，不再决定下一课。

更新日期：2026-09-17。
课程基线：v1.0，72 单元 / 95 题；仓库执行修订：v1.2。
当前阶段：**B——UR5 系列、规划与控制**。
当前项目：P1——传统视觉抓取闭环（先完成机械臂与规划基础）。
当前课程：**B04——UR5 逆解与奇异处理：多解、限位、碰撞、连续性、代价**。

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

**B02 已完成首轮。**

## 4. B03 完成情况：ROS 2 与 TF

- 已建立整体层次：URDF 是模型描述层，ROS 2 是系统通信/组织层，MoveIt 是规划层，MuJoCo 是物理仿真层，真实 UR5 是硬件执行层。
- 已理解 Node 是软件功能模块，不是硬件本身。
- 已掌握 Topic / Publisher / Subscriber：Publisher 通过 Topic 持续发布消息，Subscriber 订阅 Topic 并在 callback 中处理消息。
- 已掌握 Service：短请求/响应；Action：长时间任务，支持 Goal / Feedback / Result，并可取消。
- 已完成 Publisher/Subscriber 最小 Python 实操：`robot_status_publisher` 在 `/robot_status` 上持续发布 String；`robot_status_subscriber` 持续收到消息。
- 已实际使用 `ros2 node list`、`ros2 topic list`、`ros2 topic echo` 检查 ROS graph 和消息流。
- 已总结 pub/sub 固定模板：Publisher = 定义 node → create_publisher → 构造 msg → publish；Subscriber = 定义 node → create_subscription → callback(msg)。
- 已理解 TF 是运行时坐标变换系统；fixed joint 对应静态关系，运动关节对应随状态变化的动态关系。
- 已明确 `tf2_echo target source` 的含义：把 source frame 的位姿表达在 target frame 下；target/source 与 parent/child 不是一套概念。
- 已完成静态 TF 实操：发布 `base_link → tool0` 与 `tool0 → tcp_link` 两段静态变换，并通过 `tf2_echo base_link tcp_link` 查询得到 Translation `[0.400, 0.200, 0.600]`，验证 TF 自动沿 tree 组合变换。
- 已理解 `static_transform_publisher` 是向 TF tree 写入关系，`tf2_echo` 是查询已存在的关系；只有 frame 名还不够，tree 中必须先存在连接路径。

**B03 已完成首轮，并完成必要实操。**

## 5. 当前唯一任务：B04 UR5 逆解与奇异处理

知识目标：
1. 把 A06 的“二连杆多解”扩展到 6 轴机械臂，理解同一个末端位姿为什么可能对应多组关节角。
2. 区分解析 IK 与数值 IK 在 UR5/UR 系列中的工程意义，不要求死背完整解析公式，但要理解解的分支来源。
3. 学会筛选 IK 解：关节限位、碰撞、离当前构型的距离、轨迹连续性、奇异性、安全裕度与任务约束。
4. 理解“最近解”不是永远最优；当前姿态、下一时刻目标和整条轨迹都影响解选择。
5. 把 A07 Jacobian 奇异性迁移到 UR5：识别常见腕部/肘部/肩部奇异的直觉，并理解接近奇异点时关节速度放大。
6. 理解数值 IK 在近奇异时为何需要阻尼/步长/初值与约束。
7. 做一个最小代码级 IK 多解筛选或数值实验；不强求一开始接真实 UR5 大工程，但必须有实际筛选逻辑。
8. 面试验收：能回答“UR5 IK 多解怎么选”“没有解析解怎么办”“奇异点怎么办”。

教学顺序：从二连杆多解复习 → 6 轴多解来源 → 工程筛选 → 奇异性 → 数值 IK → 最小实操 → 面试整合。

## 6. B 阶段路线

| 正式课号 | 内容 | 状态 |
|---|---|---|
| B01 | URDF：link/joint、fixed origin、visual/collision/inertial | **已完成首轮** |
| B02 | 三维资产与夹爪：STL、mesh、材质、安装变换、工具坐标 | **已完成首轮** |
| B03 | ROS 2 与坐标传递：节点、话题、动作接口、TF | **已完成首轮 + 实操** |
| **B04** | **UR5 逆解与奇异处理：多解、限位、碰撞、连续性、代价** | **当前课程** |
| B05 | Dijkstra / A* | B04 后 |
| B06 | RRT 与配置空间 | B05 后 |
| B07 | MoveIt 规划到执行 | B06 后 |
| B08 | PD/PID 深化：超调、稳态误差、噪声、积分饱和 | B07 后 |
| B09 | MPC | B08 后 |
| B10 | 延迟诊断 | B09 后 |

## 7. 实操与证据边界

继续保持“面经优先 + 必要实操”原则：不是每个概念都打断主线做实验，但 TF、MoveIt、GraspNet、SAC、VLA 等仅靠口头难以掌握的节点必须安排最小工程验证。

## 8. 接续规则

每次开始先读本文件和 TEACHING_RULES.md。只按正式 A/B/C... 课号报进度。课后更新：实际完成、仍不理解、证据等级、下一正式单元。路线变化写 CHANGELOG.md。
