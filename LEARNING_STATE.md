# 学习进度与下一次接续卡

> 本文件是当前进度的唯一权威记录。总计划见 MASTER_PLAN.md。自 v1.2 起，**只用 A01–H04 作为正式课程编号**；旧对话中的 M01–M08 只作为历史实操记录，不再决定下一课。

更新日期：2026-09-16。
课程基线：v1.0，72 单元 / 95 题；仓库执行修订：v1.2。
当前阶段：**B——UR5 系列、规划与控制**。
当前项目：P1——传统视觉抓取闭环（先完成机械臂与规划基础）。
当前课程：**B02——三维资产与夹爪：STL、mesh、材质、安装变换、工具坐标**。

## 1. A 阶段完成情况

### A01 环境与已有进度核验
- MuJoCo 3.13.0 已安装并可用；Viewer 已运行。
- 最小 MJCF 已建立。
- 证据：用户报告完成。

### A02 刚体、形状与坐标系
- 已学习 body / geom、body frame、局部坐标、父子关系。
- 已理解 geom 的几何长度不会自动决定下一个 body/joint 的连接位置。
- 已讨论 body 原点由建模者定义，而不是由杆本身自动决定。

### A03 关节位置、方向与默认值
- 已学习 hinge、joint pos、axis、局部轴和 world/body frame。
- 已实际尝试 axis=`0 1 0`、`1 0 0`、`1 1 0`。
- 已明确 joint pos 是关节轴经过的点，axis 是方向向量。
- 已明确不能省略影响理解的默认值、单位、参考系和继承前提。

### A04 仿真状态与 FK
- 已学习 qpos/qvel、mj_forward/mj_step、直接改状态与推进动力学的区别。
- 已做 45° 初始角度的重力摆动实验。
- 已完成二连杆 FK 公式、坐标变换、Transformation Matrix 的推导与纸笔计算。
- 二连杆 FK 与 MuJoCo 末端坐标的统一代码证据尚可在后续项目整理时补齐，但不阻塞 B 阶段。

### A05 驱动命令与直接改状态
- 已学习 joint / actuator / qpos / qvel / ctrl 的区别。
- 已完成 motor actuator 实验：正负 ctrl 改变驱动方向。
- 已完成 position actuator 实验：ctrl 作为目标关节位置；已说明 position 默认不能未经参数检查直接称完整 PD。
- 已理解 motor 的 ctrl 不是目标角度；gear / transmission 会影响最终广义力/力矩。

### A06 二连杆 IK
- 已区分位置 IK 与完整位姿 IK。
- 已理解解析 IK 的两分支、0/1/2 个几何解、可达范围和边界解。
- 已学习数值 IK：初值、任务空间误差、局部 Jacobian、步长/阻尼与收敛。
- 已运行独立 Python 数学验证：`(1,1)` 两解、`(2,0)` 两分支合并为一个几何解、`(3,0)` 无解。
- MuJoCo 联动后置到控制/轨迹执行需要时，不为形式强行增加实验。

### A07 Jacobian、奇异性与阻尼
- 已理解 Jacobian 是关节小变化/速度到末端小变化/速度的局部线性映射。
- 已理解行 = 任务空间运动量，列 = 关节变量；二维二连杆位置任务为 2×2。
- 已从 FK 偏导得到二连杆位置 Jacobian，并用小角度变化理解 `Δx ≈ JΔq`。
- 已理解 rank/线性相关、正常/近奇异/完全奇异构型差别。
- 已理解伪逆在近奇异处放大关节速度，以及阻尼最小二乘用任务误差换稳定性的核心直觉。

### A08 最小控制与验收
- 已区分开环/闭环。
- 已理解 P/D/I：P 看位置误差，D 提供阻尼，I 处理长期稳态误差但有 windup 风险。
- 已理解典型关节 PD：`tau = Kp(q_des-q) - Kd*qvel`，目标是位置，输出通常是力矩。
- 已理解 control period 与 simulation timestep 可以不同。
- 已理解 joint limit 与 actuator saturation 的区别。
- 已完成 MuJoCo 单关节 PD 实验：目标 45°，无明显超调/振荡，未长期触发 ±10 力矩饱和；稳态 torque 约 1.5，与重力负载下 PD 的稳态误差直觉一致。
- 已完成扰动恢复实验：关节被拨离稳定位置后能回到原稳定位置附近，无明显超调，也未触发力矩饱和。
- 详见 `learning_logs/2026-09-16_A08_control.md`。

### A 阶段结论

**A01–A08 已完成首轮学习与核心验收。** P0 仍有少量代码统一提交和二连杆 MuJoCo 数值证据可在后续项目整理时补齐；这些属于项目证据补强，不再作为额外课程阻塞主线。

## 2. B01 完成情况：URDF

- 已理解 URDF 是机器人模型描述格式，核心结构是 `link` + `joint`。
- 已明确 URDF 的 parent/child 关系由 joint 显式建立；没有 joint，两个 link 不构成运动链。
- 已理解 `link` 是刚体节点，`joint` 是两个刚体之间的运动/约束关系。
- 已掌握 joint 的 `parent`、`child`、`origin xyz/rpy`、`axis`、`limit`。
- 已区分 joint `origin`（joint frame 相对 parent link frame）与运行时关节角 `q`。
- 已明确 URDF 中角度通常按 rad 表示；长度通常按 m 表示。
- 已理解 `visual`、`collision`、`inertial` 的职责：外观、碰撞、质量/惯量。
- 已明确 `visual/collision/inertial` 里的 origin 都相对当前 link frame；joint 里的 origin 相对 parent link frame。
- 已理解 geometry origin 不等于“端点”；box 的 origin 默认在几何中心，`size="1 0.1 0.1"` 表示沿自身 x/y/z 三轴尺寸。
- 已理解 geometry 的“横着/竖着”由局部轴和 `rpy` 决定，而不是只看 size。
- 已完成最小二连杆 URDF 整体阅读，并将 URDF 链与前面 FK 联系起来。
- 面试级验收：能解释为什么不同轴的旋转不能简单把角度相加，例如 `Rz(30°)Ry(20°)` 不能写成 50°。

**B01 已完成首轮。**

## 3. 当前唯一任务：B02 三维资产与夹爪

知识目标：
1. 从零定义 mesh / STL：它是什么、里面通常存什么、不存什么。
2. 理解 URDF 如何通过 `<mesh filename="..."/>` 引入三维资产，以及 `scale`、单位、坐标轴为什么容易出错。
3. 区分“几何颜色”和“真正纹理贴图”：STL 本身通常不保存标准纹理 UV/贴图；材质/纹理能力取决于模型格式和显示/仿真工具链。
4. 理解 visual mesh 与 collision mesh 为什么常常不同，如何做简化碰撞模型。
5. 从 link/joint 角度理解“把夹爪挂到 UR5 末端”：新增 gripper base link，用 fixed joint 连接 UR5 的末端/tool link。
6. 理解 fixed joint 的 `origin xyz/rpy` 就是机械安装外参/安装变换；解释装歪、装反、偏移的本质。
7. 理解 tool frame / TCP（Tool Center Point）是什么，以及为什么规划、抓取姿态不应该只盯着腕部 link frame。
8. 用一个最小“机械臂末端 + 夹爪”URDF 片段完成面试级验收。

教学顺序：STL/mesh 基础 → 材质/纹理 → fixed joint 安装 → tool frame/TCP → 最小夹爪结构 → 面试回答。不要默认用户知道 STL、UV、texture、TCP。

## 4. B 阶段路线

| 正式课号 | 内容 | 状态 |
|---|---|---|
| B01 | URDF：link/joint、fixed origin、visual/collision/inertial | **已完成首轮** |
| **B02** | **三维资产与夹爪：STL、mesh、材质、安装变换、工具坐标** | **当前课程** |
| B03 | ROS 2 与坐标传递：节点、话题、动作接口、TF | B02 后 |
| B04 | UR5 逆解与奇异处理：多解、限位、碰撞、连续性、代价 | B03 后 |
| B05 | Dijkstra / A* | B04 后 |
| B06 | RRT 与配置空间 | B05 后 |
| B07 | MoveIt 规划到执行 | B06 后 |
| B08 | PD/PID 深化：超调、稳态误差、噪声、积分饱和 | B07 后 |
| B09 | MPC | B08 后 |
| B10 | 延迟诊断 | B09 后 |

## 5. 现有本地文件与证据边界

用户已报告本地存在 MuJoCo 单杆、重力、Actuator、PD、IK/FK 数学验证等实验文件，但尚未完整统一提交到仓库。不伪造源码。

B02 先用最小通用 URDF 片段建立资产和夹爪安装概念；真实 UR5/UR5e 到 B04 前再冻结具体型号和仓库版本，避免混用型号参数。

## 6. 接续规则

每次开始先读本文件和 TEACHING_RULES.md。只按正式 A/B/C... 课号报进度。课后更新：实际完成、仍不理解、证据等级、下一正式单元。路线变化写 CHANGELOG.md。
