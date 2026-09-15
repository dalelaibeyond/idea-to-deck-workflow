# Idea-to-Deck Workflow

一个从“杂乱想法/原始资料”到“高说服力 PPT / HTML 演示文稿”的 5 阶段模块化 AI 工作流框架。本框架面向 **OpenCode CLI**、**Antigravity CLI**、**Codex** 等具备代码编写与终端执行能力的 Coding Agent 工具，通过“人机协作 + 阶段性分步触发 + 闭环自愈”的模式，保障演示文稿的商业叙事逻辑、文案精炼度与原生渲染质量。

---

## 阶段契约与数据流向速查表

| 阶段 | 提示词文件 | 核心输入 | 核心交付物 | 人机交互节点 (HITL) / 核心控制 |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1: Idea** | `01-idea/PROMPTS.md` | `00-inputs/*` | `06-outputs/info.md` | **主动追问 (Grilling)：** 确认受众、场景、核心目标与事实核验 |
| **Phase 2: Outline** | `02-outline/PROMPTS.md` | `06-outputs/info.md` | `06-outputs/outline.md` | **结构对齐：** 确认 SCQA 叙事主线与总页数规划 |
| **Phase 3: Content** | `03-deck-content/PROMPTS.md` | `06-outputs/outline.md` | `06-outputs/deck-content.md` | 审阅屏上文案字数密度、演讲口播稿与演说心法 |
| **Phase 4: Design** | `04-visual-design/PROMPTS.md` | `06-outputs/deck-content.md` *(仅屏上内容)* + `info.md` *(风格参考)* | `06-outputs/design.md` | 审阅全局配色 Hex、字体层级与 Archetype 版式映射 |
| **Phase 5: Export** | `05-deck-export/PROMPTS.md` | `06-outputs/design.md` + `deck-content.md`（预检时交叉核对 `outline.md`） | `presentation.pptx` / `presentation.html` | **预检 + 终端自愈闭环：** 渲染前校验三源一致性，报错自动修复 |

---

## 目录架构说明

```text
.
├── _archive/                        # [排除目录] 冷存储：历史 session、旧文档（Agent 不读不写）
├── _samples/                        # [排除目录] 人工维护的参考样例（Agent 不读不写）
├── _review/                         # [排除目录] 人工维护的评估与评审报告（Agent 不读不写）
├── AGENTS.md                       # 全局 Agent 执行协议（拓扑主图、自愈规则、Delta 传播链）
├── 00-inputs/                      # 原始输入文件夹（放置客户聊天记录、邮件、会议转写、笔记等）
├── 01-idea/
│   └── PROMPTS.md                  # Phase 1: 原始信息提取、杂音清洗与商业约束锁定
├── 02-outline/
│   └── PROMPTS.md                  # Phase 2: 基于 SCQA 框架与金字塔原理生成 Action Title 大纲
├── 03-deck-content/
│   └── PROMPTS.md                  # Phase 3: 逐页文案精练、Layout Tag 定量版式约束与演讲心法
├── 04-visual-design/
│   └── PROMPTS.md                  # Phase 4: 全局视觉规范、Archetype 注册表与页面映射
├── 05-deck-export/
│   └── PROMPTS.md                  # Phase 5: 双路径代码生成（Python-pptx 原生 & Marp HTML）
└── 06-outputs/                     # 运行时输出目录（保存所有中间 Markdown 与终态渲染文件）
    ├── info.md                     # Phase 1 交付物：已核实事实、假设与受众/目标元数据
    ├── outline.md                  # Phase 2 交付物：SCQA 故事线与逐页 Action Title
    ├── deck-content.md             # Phase 3 交付物：版式标签、屏上文案与演讲口播稿
    ├── design.md                   # Phase 4 交付物：配色 Hex、字体与 Archetype 映射表
    ├── build_deck.py              # Phase 5A: Python-pptx 原生渲染脚本
    ├── marp_deck.md               # Phase 5B: Marp 幻灯片源码
    ├── presentation.pptx          # 最终交付物：Office 原生可编辑 PPTX（内含口播备注）
    └── presentation.html          # 最终交付物：现代化 Web 互动幻灯片
```

---

## 快速使用指南 (SOP)

### 前置准备

1. 将原始素材（文本、会议纪要、文档片段等）放入 `00-inputs/` 目录下。
2. 运行依赖准备（按需，Agent 自愈循环中亦支持自动安装）：
   * **Path A（原生 PPTX）：** `pip install python-pptx`
   * **Path B（HTML 演示）：** `npx @marp-team/marp-cli@latest --version`
3. **排除目录提示：** `_archive/`、`_samples/` 与 `_review/` 为排除目录（Pipeline-Blind），全程由人工维护，Agent 不会读取或写入其中的任何内容。

---

### 分步执行指令

每个 Phase 均可**独立启动**，无需从头逐条触发。Agent 会自动检查该阶段的上游依赖是否存在；若缺失，会返回标准提示，引导你先完成前置阶段。

> 各阶段的调用示例文本如下。你可以随时从任意一个 Phase 开始，只要其前置依赖已满足。

#### Phase 1: 提取与收敛 (Idea)
> **前置依赖：** `00-inputs/` 中存在原始素材
```text
请读取 00-inputs/ 目录下的所有资料，执行 01-idea/PROMPTS.md 中的完整规范。
```

#### Phase 2: 逻辑大纲设计 (Outline)
> **前置依赖：** `06-outputs/info.md` 已存在
```text
请读取 06-outputs/info.md，执行 02-outline/PROMPTS.md 中的完整规范。
```

#### Phase 3: 逐页内容与版式约束 (Deck-Content)
> **前置依赖：** `06-outputs/outline.md` 已存在（`06-outputs/info.md` 作背景参考）
```text
请读取 06-outputs/outline.md（参考 info.md），执行 03-deck-content/PROMPTS.md 中的完整规范。
```

#### Phase 4: 视觉设计规范化 (Visual-Design)
> **前置依赖：** `06-outputs/deck-content.md` 已存在（`06-outputs/info.md` 提供风格上下文）
```text
请读取 06-outputs/deck-content.md（仅提取屏上文案与版式标签，跳过演说口播稿），执行 04-visual-design/PROMPTS.md 中的完整规范。
```

#### Phase 5: 双路径渲染与代码自愈 (Deck-Export)
> **前置依赖：** `06-outputs/design.md` 与 `06-outputs/deck-content.md` 均已存在（`06-outputs/outline.md` 供预检交叉核对）

根据交付目标选择 Path A 或 Path B：

* **选项 A（导出 Office 原生可编辑 PPTX，含演讲备注）：**
  ```text
  请读取 06-outputs/design.md 与 06-outputs/deck-content.md，执行 05-deck-export/PROMPTS.md 中的 Path A 规范。
  ```

* **选项 B（导出 Web 幻灯片 HTML）：**
  ```text
  请读取 06-outputs/design.md 与 06-outputs/deck-content.md，执行 05-deck-export/PROMPTS.md 中的 Path B 规范。
  ```

---

## 进阶工程实践

### 1. 增量微调 (Delta Update) 传播链条 (P0)
演示文稿制作常需局部修改，**严禁跨步导致数据不一致**。
**权威源规则：** `deck-content.md` 的 Layout Tag 是页面版式的唯一权威源；`outline.md` 的 Layout Suggestion 仅为建议，`design.md` 的 Archetype 映射由 deck-content 派生。任何版式变更先改 `deck-content.md`，再向下游传播。
* **仅修改文案、指标或口播词（Case A）：**
  直接修改 `06-outputs/deck-content.md` 对应页 → **直接重跑 Phase 5** 重新渲染。
* **修改页面版式或结构（Case B）：**
  修改 `06-outputs/deck-content.md` 的 Layout Tag → **必须同步更新 `06-outputs/design.md` 对应页的 Archetype 映射**（建议同步 `outline.md` 的 Layout Suggestion 防漂移）→ **再重跑 Phase 5** 重新渲染。
* **增删页面或重构故事线（Case C）：**
  修改 `06-outputs/outline.md` → 按顺序重新执行 Phase 3 → Phase 4 → Phase 5。
* **修改受众、场景、核心目标或核实事实（Case D）：**
  修改 `06-outputs/info.md` → 按顺序重新执行 Phase 2 → Phase 3 → Phase 4 → Phase 5，**严禁基于过期 info.md 向下游打补丁**。

### 2. 单工作区与多 Deck 隔离原则
* 当前工作区 `06-outputs/` 专注于维护**一份活跃的演示文稿**。
* 如需制作新演示文稿，请先将 `06-outputs/` 备份归档或清空，避免新旧文稿中间产物冲突。

### 3. 自愈执行闭环 (Self-Healing Loop)
* Agent 在 Phase 5 中具备终端执行与自动修复权限。渲染前先执行**三源一致性预检**（`total_slides` / Layout Tag 词表 / Archetype 映射），发现上游漂移即停并报告，而非盲目重建。
* 如果本地缺少 `python-pptx` 等依赖，Agent 将自动执行安装命令并重新构建，确保交付确定性。

### 4. 版本控制纪律 (Git)
* 工作区为 git 仓库。Agent 在每个阶段成功完成后自动 commit 对应产物，增量修改与重跑全程可 diff、可回退。
* `.gitignore` 已排除 `.DS_Store`、Python 缓存及全部排除目录（`_archive/`、`_samples/`、`_review/`）。
* 排除目录由人工维护、不入版本库 —— 重要评审结论请自行备份留档。
