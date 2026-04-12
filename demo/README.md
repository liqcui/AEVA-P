# AEVA Interactive Demo

[![Deploy to GitHub Pages](https://github.com/liqcui/AEVA-P/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/liqcui/AEVA-P/actions/workflows/deploy-pages.yml)

**Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.**
**License**: Dual License (Personal/Academic Free, Commercial Requires Permission)
**Watermark**: AEVA-2026-LQC-dc68e33

**🌐 Live Demo**: https://liqcui.github.io/AEVA-P/

---

## Overview

This is a **fully offline-capable** interactive demo page for the AEVA platform. It showcases all core features with pre-loaded mock data, requiring no network connection or API access.

## Features

- ✅ **Fully Offline** - No network or API required
- ✅ **Interactive UI** - Modern, responsive design
- ✅ **Complete Functionality** - All 8 pages with mock data
- ✅ **Fast Loading** - Instant page switching
- ✅ **Cross-Browser** - Works on Chrome, Safari, Firefox, Edge

---

## Quick Start

### Method 1: Direct Open (Recommended)

```bash
# Navigate to demo directory
cd demo

# Open with browser
open index.html

# Or use any browser: Chrome/Safari/Firefox/Edge
```

### Method 2: Local Server (Optional)

```bash
# Using Python HTTP server
cd demo
python3 -m http.server 8000

# Open browser
open http://localhost:8000
```

### Method 3: VS Code Live Server (Optional)

```bash
# If VS Code Live Server extension installed
# Right-click index.html -> Open with Live Server
```

---

## Page Structure

The demo includes 8 interactive pages:

### 1. Architecture (Default)

**Content**:
- System architecture overview
- 15 core modules introduction
- Technology stack
- Code statistics and maturity metrics

**Key Points**:
- 5 core components: Guard, Bench, Auto, Brain, Report/Comparison
- Full ML lifecycle coverage
- 23K+ lines of code, 95% production maturity

### 2. Dashboard

**Content**:
- Overall evaluation metrics
- Recent evaluation records
- Accuracy trend charts
- Performance distribution

**Key Points**:
- 15 core modules, 68 test cases
- 95% maturity, 65% test coverage
- Dual interface support (CLI + Web)

### 3. Interfaces ⭐ NEW

**Content**:
- CLI vs Web comparison
- 11 CLI command reference
- 7 Web dashboard pages
- Feature comparison matrix
- Usage recommendations

**Key Points**:
- CLI for automation and CI/CD
- Web for exploration and collaboration
- 100% functional equivalence

### 4. Guard (Quality Gates)

**Content**:
- 5 quality gate configurations
- Real-time gate check status
- Blocking/Non-blocking strategies
- Gate history timeline

**Key Points**:
- Multi-dimensional quality checks
- Accuracy ≥90% (Blocking)
- Performance ≤100ms (Blocking)

### 5. Bench (Benchmarks)

**Content**:
- 4 benchmark test suites
- Detailed test results
- Radar chart for model comparison
- Performance comparison charts

**Key Points**:
- Standardized evaluation benchmarks
- Industry-standard test datasets
- Visual model comparison

### 6. Auto (Pipeline)

**Content**:
- Pipeline visualization timeline
- 5 execution stages
- Stage status monitoring
- Execution logs

**Key Points**:
- End-to-end automation
- Data prep → Load → Bench → Guard → Brain
- Distributed execution support

### 7. Brain (Intelligence) ⭐ CORE

**Content**:
- AI-powered analysis results
- Root cause identification
- Optimization recommendations
- Risk predictions

**Key Points**:
- Claude API integration
- Intelligent diagnostics
- 96% efficiency improvement
- From 2 hours to 5 minutes

### 8. Enhancements

**Content**:
- Report generation features
- Model comparison capabilities
- Dataset management
- Performance profiling

**Key Points**:
- HTML/PDF/Markdown reports
- Champion/Challenger management
- Dataset versioning
- Production integrations

---

## Technical Details

### Architecture

- **Frontend**: Pure HTML/CSS/JavaScript
- **Charts**: Chart.js for visualizations
- **Data**: Pre-loaded mock data in JavaScript
- **No Dependencies**: Self-contained single file

### File Size

- `index.html`: ~2,900 lines
- Total size: ~150KB
- Load time: <1 second

### Browser Compatibility

- ✅ Chrome 90+
- ✅ Safari 14+
- ✅ Firefox 88+
- ✅ Edge 90+

---

## Usage Scenarios

### 1. Product Demonstration

Show AEVA's capabilities to stakeholders:
- System architecture and design
- Core features and functionality
- User interface and experience

### 2. Technical Presentation

Present technical details to engineering teams:
- Module structure
- Technology stack
- Code quality metrics

### 3. Offline Showcase

Demo in environments without network:
- Conference presentations
- Customer meetings
- Training sessions

### 4. Quick Preview

Quickly preview AEVA without installation:
- Evaluate features
- Understand workflow
- Check UI/UX

---

## Customization

### Modify Data

Edit the mock data in `index.html`:

```javascript
// Find the data section (around line 2000+)
const mockData = {
    evaluations: [...],
    gates: [...],
    // Modify as needed
};
```

### Change Styling

Modify CSS variables:

```css
:root {
    --primary: #2563eb;
    --success: #10b981;
    /* Customize colors */
}
```

---

## Limitations

### What Works

- ✅ All page navigation
- ✅ Interactive charts
- ✅ Mock data display
- ✅ Responsive design

### What Doesn't Work

- ❌ Real API calls (uses mock data)
- ❌ File upload (display only)
- ❌ Data persistence (no backend)
- ❌ Live updates (static content)

---

## Development

### Adding New Pages

1. Add navigation link:
```html
<a href="#" class="nav-link" data-page="newpage">New Page</a>
```

2. Add page section:
```html
<div id="newpage" class="page-section">
    <!-- Page content -->
</div>
```

### Adding New Charts

Use Chart.js:

```javascript
const ctx = document.getElementById('myChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: { /* ... */ },
    options: { /* ... */ }
});
```

---

## Troubleshooting

### Charts Not Displaying

**Issue**: Charts don't render

**Solution**: Ensure Chart.js CDN is loaded
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

### Page Navigation Not Working

**Issue**: Clicking tabs doesn't switch pages

**Solution**: Check JavaScript console for errors
- Ensure all page sections have correct IDs
- Verify navigation event listeners

### Styling Issues

**Issue**: Layout broken

**Solution**: Check CSS
- Verify all CSS variables defined
- Check for conflicting styles
- Test in different browsers

---

## Performance

### Optimization Tips

1. **Minimize Images**: Use SVG for icons
2. **Lazy Load Charts**: Initialize only when page visible
3. **Compress Data**: Minify mock data
4. **Cache Assets**: Use browser caching

### Metrics

- **Load Time**: <1 second
- **Page Switch**: <100ms
- **Chart Render**: <500ms
- **Memory Usage**: <50MB

---

## License

**Dual License**:
- ✅ FREE for personal and academic use
- ⚠️ Commercial use requires explicit permission

**Contact**: liquan_cui@126.com

See [LICENSE](../LICENSE) for details.

---

## Support

- **GitHub**: https://github.com/liqcui/AEVA-P
- **Issues**: https://github.com/liqcui/AEVA-P/issues
- **Email**: liquan_cui@126.com

---

*AEVA v2.0 - Interactive Offline Demo*
*Copyright © 2024-2026 AEVA Development Team*
*Watermark: AEVA-2026-LQC-dc68e33*
