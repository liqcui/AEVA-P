# AEVA Demo HTML - Translation Analysis Report

## Summary

The demo HTML file (`/Users/liqcui/goproject/github.com/liqcui/AVEA-P/demo/index.html`) currently has partial bilingual support. Out of approximately 5,047 lines of code, **1,091 lines contain Chinese text that lacks `data-lang` attributes** and therefore won't be translated when switching to English mode.

## Current Translation Status

### ✅ Already Translated (Existing)
- Navigation menu items
- Dashboard stat cards
- Main headings with `data-lang` attributes
- Table headers (model-name, version, accuracy, performance, status, time)
- Some status badges (passed, warning, failed)
- Architecture page core elements

### ❌ Missing Translations (1,091 lines)

#### 1. Time Expressions (Throughout the file)
- "2分钟前", "15分钟前", "1小时前", "2小时前", "3小时前"
- "1天前", "3天前", "1周前"
- "本月", "上周", "今日"
- Month names: "1月", "2月", "3月", "4月", "5月"

#### 2. Interface Section (Lines ~613-838)
- Detailed descriptions under CLI and Web headings
- Feature tags and descriptions
- Code comments ("# 模型评测", "# 数据验证", etc.)
- Feature comparison details

#### 3. CLI Commands Section (Lines ~847-1105)
- Command category headings
- Individual command names and descriptions
- CLI output examples with Chinese text
- Installation and quick start commands

#### 4. Web Dashboard Features (Lines ~1110-2064)
- Page descriptions
- Interactive dashboard UI demo content
- All tab content:
  - System overview (📊 系统概览)
  - Charts and KPI labels
  - Explainability tab (🔍 模型可解释性分析)
  - Robustness tab (🛡️ 对抗鲁棒性测试)
  - Data Quality tab (📊 数据质量分析)
  - A/B Testing tab (📈 A/B测试分析)
  - Model Cards tab (📝 模型卡片生成)
  - LLM Evaluation tab (🤖 LLM专项评测)
  - Production Integration tab (⚙️ 生产集成)
  - Report Generation tab (📄 报告生成中心)

#### 5. Feature Comparison Matrix (Lines ~2094-2203)
- Feature names and descriptions
- Comparison cell content
- Legend items

#### 6. Usage Recommendations (Lines ~2211-2292)
- "使用 CLI 当您需要" section
- "使用 Web 当您需要" section
- Best practices workflow steps

#### 7. Quick Start Section (Lines ~2295-2330)
- Installation commands
- Quick command examples

#### 8. Architecture Page (Lines ~2333+)
- Component descriptions
- Service descriptions (Guard, Bench, Auto, Brain, Report)
- Capability lists
- Use case descriptions

## Recommended Approach

Due to the large scope, I recommend a **phased approach**:

### Phase 1: Critical User-Facing Text (Priority: HIGH)
Focus on text that users see first:
1. Time expressions in tables
2. Main page descriptions
3. Feature tags and labels
4. Status messages

**Estimated lines: ~200**

### Phase 2: Dashboard Content (Priority: MEDIUM)
5. All dashboard tab content
6. Charts and visualizations
7. Table content

**Estimated lines: ~400**

### Phase 3: Documentation & Details (Priority: MEDIUM-LOW)
8. CLI output examples
9. Architecture descriptions
10. Feature comparison details

**Estimated lines: ~300**

### Phase 4: Instructional Content (Priority: LOW)
11. Installation instructions
12. Best practices
13. Usage recommendations

**Estimated lines: ~191**

## Translation Keys Structure

I recommend organizing translation keys by section:

```javascript
// Time expressions
'time-2min': '2分钟前' / '2 minutes ago'
'time-15min': '15分钟前' / '15 minutes ago'

// Interface
'cli-heading': '🖥️ CLI 命令行' / '🖥️ CLI Command Line'
'web-heading': '🌐 Web 仪表板' / '🌐 Web Dashboard'

// Commands
'cmd-model-eval': '模型评测' / 'Model Evaluation'
'cmd-explainability': '可解释性' / 'Explainability'

// Pages
'page-home': '主页' / 'Home'
'page-explainability': '可解释性分析' / 'Explainability Analysis'

// Features
'tag-fast': '⚡ 快速' / '⚡ Fast'
'tag-automation': '🔄 自动化' / '🔄 Automation'

// Status
'status-passed': '✓ 通过' / '✓ Passed'
'status-warning': '⚠ 警告' / '⚠ Warning'

// Architecture
'guard-capability-1': '多维度阈值检查...' / 'Multi-dimensional Threshold Checks...'
```

## Automation Strategy

Given the file size, I recommend:

1. **Semi-automated approach**: Use scripts to identify and suggest changes, but review manually
2. **Section-by-section updates**: Update one major section at a time to avoid errors
3. **Testing after each phase**: Verify language toggle works correctly after each update

## Next Steps

1. Choose which phase to start with (recommend Phase 1)
2. I can provide:
   - Specific line-by-line edits for that phase
   - Complete translation key/value pairs to add to the translations object
   - Testing checklist

3. Implement and test one phase before moving to the next

## Files Affected

- `/Users/liqcui/goproject/github.com/liqcui/AVEA-P/demo/index.html` - Add `data-lang` attributes
- JavaScript translations object (lines ~4804-5003) - Add English translations

## Estimated Effort

- **Phase 1**: ~2-3 hours (200 translations)
- **Phase 2**: ~3-4 hours (400 translations)
- **Phase 3**: ~2-3 hours (300 translations)
- **Phase 4**: ~1-2 hours (191 translations)
- **Total**: ~8-12 hours for complete bilingual coverage

## Testing Checklist

After each phase:
- [ ] Click language toggle button
- [ ] Verify NO Chinese text remains visible in English mode (except intentional code/examples)
- [ ] Verify Chinese text displays correctly in Chinese mode
- [ ] Check all updated sections work properly
- [ ] Test page navigation

## Sample Translations Provided

I've created a comprehensive translation mapping with 200+ common phrases. Would you like me to:

1. **Start with Phase 1** - Provide exact edits for critical user-facing text?
2. **Generate a complete translation file** - All 1091 translations at once (requires careful review)?
3. **Create an automated script** - That you can run and review the output?

Let me know which approach you prefer!