# 🚀 AEVA快速参考手册

## 📁 项目概览

**当前规模**:
- Python代码: ~13,000行
- 模块数量: 11个
- 示例代码: 5个
- 文档: 20+份

---

## 🗂️ 目录结构速查

```
AVEA-P/
├── aeva/                       # 主代码包
│   ├── core/                   # 核心框架
│   ├── guard/                  # 质量门禁
│   ├── bench/                  # 标准基准
│   ├── auto/                   # 自动化流水线
│   ├── brain/                  # 智能诊断
│   ├── report/                 # 报告生成 ⭐
│   └── comparison/             # 模型对比 ⭐
│
├── demo/                       # 离线演示
│   ├── index.html              # Demo页面
│   └── README.md               # 使用指南
│
├── examples/                   # 示例代码
│   ├── basic_usage.py
│   ├── advanced_brain_analysis.py
│   └── report_generation_example.py  ⭐
│
└── docs/                       # 技术文档
    ├── ENHANCEMENT_PLAN.md
    ├── ENHANCEMENTS_IMPLEMENTED.md
    └── ARCHITECTURE.md
```

---

## ⚡ 快速启动

### 1. 离线Demo演示 (最快)

```bash
cd demo
open index.html
```

### 2. 运行示例代码

```bash
# 基础使用
python examples/basic_usage.py

# Brain智能分析
python examples/advanced_brain_analysis.py

# 报告生成
python examples/report_generation_example.py
```

### 3. 交互式使用

```python
from aeva import AEVA

# 初始化平台
aeva = AEVA(config_path="config/aeva.yaml")

# 运行评测
result = aeva.run(pipeline, algorithm)
```

---

## 📊 核心模块API速查

### AEVA核心

```python
from aeva import AEVA

aeva = AEVA()
result = aeva.run(pipeline, algorithm)
status = aeva.get_status()
aeva.shutdown()
```

### Guard质量门禁

```python
from aeva.guard import QualityGate, ThresholdGate

gate = ThresholdGate(
    name="accuracy_gate",
    threshold=0.90,
    metric_name="accuracy",
    blocking=True
)
```

### Bench基准测试

```python
from aeva.bench import BenchmarkSuite

suite = BenchmarkSuite.load("standard_ml_bench")
results = suite.run(model)
```

### Brain智能分析

```python
from aeva.brain import BrainManager

brain = BrainManager(config)
analysis = brain.analyze(result)
# analysis包含: summary, root_causes, recommendations
```

### Report报告生成 ⭐

```python
from aeva.report import ReportGenerator, HTMLTemplate

generator = ReportGenerator(
    template=HTMLTemplate(),
    language='zh'
)

# 单模型报告
html = generator.generate(result, output_path='report.html')

# 对比报告
comparison = generator.generate_comparison_report(
    results=[r1, r2, r3],
    output_path='comparison.html'
)
```

### Comparison模型对比 ⭐

```python
from aeva.comparison import ModelComparator

comparator = ModelComparator()
comparison = comparator.compare([r1, r2, r3])

print(comparison.rankings)     # {model: rank}
print(comparison.best_model)   # {metric: model}
print(comparison.summary)      # 文本摘要
```

### Champion/Challenger

```python
from aeva.comparison import ChampionChallengerManager

manager = ChampionChallengerManager(promotion_threshold=0.02)
manager.set_champion(production_result)
manager.set_challenger(candidate_result)

decision = manager.should_promote()
if decision['should_promote']:
    manager.promote_challenger()
```

---

## 🎯 面试关键数据

### 项目数据

- 代码行数: **~13,000行**
- Python文件: **52个**
- 模块数量: **11个**
- 示例数量: **5个**

### 关键数字

- OpenShift测试: **100-1000节点**
- OVN优化提升: **85%**
- Brain效率提升: **96%**
- AEVA代码量: **13,000+行**
- 开源贡献: **kube-burner PR#299**

### 核心模块

**4大核心**:
1. Guard - 质量门禁
2. Bench - 标准基准
3. Auto - 自动化流水线
4. Brain - 智能诊断

**2大增强**:
5. Report - 报告生成
6. Comparison - 模型对比

---

## 📖 文档速查

### 面试准备文档

| 文档 | 用途 | 优先级 |
|-----|------|--------|
| 00_文档总览 | 资料包导航 | ⭐⭐⭐⭐ |
| 01_核心问题回答 | 技术问题 | ⭐⭐⭐⭐⭐ |
| 02_工程能力展示 | 工程案例 | ⭐⭐⭐⭐⭐ |
| 04_项目演示方案 | 演示脚本 | ⭐⭐⭐⭐⭐ |
| 08_面试清单 | 准备清单 | ⭐⭐⭐⭐⭐ |
| 09_自我介绍脚本 | 自我介绍 | ⭐⭐⭐⭐⭐ |
| 10_离线演示方案 | Demo使用 | ⭐⭐⭐⭐⭐ |

### 技术文档

- `ENHANCEMENT_PLAN.md` - 功能增强计划
- `ENHANCEMENTS_IMPLEMENTED.md` - 实现总结
- `CODE_ENHANCEMENT_COMPLETE.md` - 完成报告
- `ARCHITECTURE.md` - 架构设计

### 快速开始

- `README.md` - 项目主文档
- `QUICK_START_DEMO.md` - Demo快速开始
- `QUICK_REFERENCE.md` - 本文档

---

## 🎬 演示脚本速查

### 30秒电梯演讲

```
"我是李奇崔,Red Hat OpenShift性能测试工程师。

我有两个独特优势:
1. 大规模测试工程化能力(1000节点集群)
2. AI驱动质量保障实践(MCP+AEVA)

为了这次面试,我设计了AEVA完整的算法评测平台,
包含质量门禁、标准基准、自动化流水线、智能诊断
四大模块,以及报告生成和模型对比两大增强功能。

我准备好将OpenShift经验与AI技术结合,
为团队的算法评测体系做出贡献。"
```

### 5分钟Demo演示

**时间分配**:
- Dashboard: 30秒
- Guard: 45秒
- Bench: 30秒
- Auto: 45秒
- **Brain: 1分30秒** ⭐ 重点
- 总结: 30秒

**详细演示脚本**: See `demo/README.md` for detailed presentation guide

---

## 💡 常见问题速查

### Q: 项目是真实的吗?

**回答**:
```
"是的,这是我为面试专门设计和实现的完整项目。
13,000行Python代码,11个功能模块,完整可运行。
虽然是POC级别,但展示了我对算法评测的系统化思考。"
```

### Q: Brain是真实的LLM输出吗?

**回答**:
```
"Demo中是模拟数据,但实际代码中Brain真实调用Claude API。
我在MCP项目中已验证过这个方案,并在生产环境使用。
如果需要,我可以现场运行Python代码,调用真实API。"
```

### Q: 为什么能胜任AI评测?

**回答**:
```
"核心能力是相通的:
1. 大规模测试的复杂度管理和自动化 - 直接适用
2. MCP和AEVA证明了AI应用能力 - 不是纸上谈兵
3. 快速学习能力 - 2周OVN,1月AEVA

我的工程化能力是长期积累的核心竞争力。"
```

---

## 🔗 快速链接

### 核心文件

- Demo页面: `/Users/liqcui/goproject/github.com/liqcui/AVEA-P/demo/index.html`
- 主文档: `/Users/liqcui/goproject/github.com/liqcui/AVEA-P/README.md`
- 配置: `/Users/liqcui/goproject/github.com/liqcui/AVEA-P/config/aeva.yaml`

### 示例代码

- 基础使用: `examples/basic_usage.py`
- Brain分析: `examples/advanced_brain_analysis.py`
- 报告生成: `examples/report_generation_example.py`

### 核心模块

- 平台: `aeva/core/platform.py`
- Guard: `aeva/guard/manager.py`
- Brain: `aeva/brain/analyzer.py`
- Report: `aeva/report/generator.py`
- Comparison: `aeva/comparison/comparator.py`

---

## ✅ 面试前检查清单

### 技术准备
- [ ] 熟悉11个模块功能
- [ ] 理解架构设计
- [ ] 记住关键数字
- [ ] 准备代码演示

### Demo准备
- [ ] 打开index.html测试
- [ ] 练习5分钟演示
- [ ] 准备备用方案
- [ ] 录制演示视频

### 心理准备
- [ ] 复习核心价值主张
- [ ] 准备常见问题回答
- [ ] 深呼吸放松
- [ ] 享受展示过程

---

## 🎯 成功标准

面试成功应该让面试官记住:

1. ✅ "完整的架构设计"
2. ✅ "Brain智能分析很创新"
3. ✅ "结合了大规模测试经验"
4. ✅ "工程化能力强"
5. ✅ "准备充分专业"

---

**您已经准备好了！**

**核心优势**:
- ✅ 13,000行完整代码
- ✅ 11个功能模块
- ✅ 离线Demo可用
- ✅ 系统化文档

**Go and shine! 🌟**

---

*快速参考 v1.0*
*最后更新: 2026年4月11日*
