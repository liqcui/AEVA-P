# GitHub Pages Setup Guide

**Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.**
**Watermark**: AEVA-2026-LQC-dc68e33

---

## Overview

This guide explains how to deploy the AEVA interactive demo to GitHub Pages.

**Live Demo**: https://liqcui.github.io/AEVA-P/

---

## Automatic Deployment

### GitHub Actions Workflow

A GitHub Actions workflow is configured to automatically deploy the demo when changes are pushed.

**Workflow File**: `.github/workflows/deploy-pages.yml`

**Triggers**:
- Push to `main` branch with changes in `demo/` directory
- Manual workflow dispatch

**Process**:
1. Checkout repository
2. Setup GitHub Pages
3. Upload `demo/` directory as artifact
4. Deploy to GitHub Pages

---

## Manual Setup Instructions

If you need to set up GitHub Pages manually:

### Step 1: Enable GitHub Pages

1. Go to your repository on GitHub: https://github.com/liqcui/AEVA-P
2. Click **Settings** tab
3. Scroll to **Pages** section (left sidebar)
4. Under **Source**, select:
   - Source: **GitHub Actions**

5. Click **Save**

### Step 2: Configure Repository Permissions

1. In repository **Settings**
2. Go to **Actions** → **General**
3. Scroll to **Workflow permissions**
4. Select **Read and write permissions**
5. Check **Allow GitHub Actions to create and approve pull requests**
6. Click **Save**

### Step 3: Trigger Deployment

**Option 1: Push Changes**
```bash
# Make any change to demo/ directory
cd demo
touch .trigger  # Create a trigger file
git add .
git commit -m "Trigger Pages deployment"
git push origin main
```

**Option 2: Manual Workflow Dispatch**
1. Go to **Actions** tab
2. Select **Deploy Demo to GitHub Pages**
3. Click **Run workflow**
4. Select branch: `main`
5. Click **Run workflow**

### Step 4: Verify Deployment

1. Go to **Actions** tab
2. Check latest workflow run
3. Wait for completion (usually <1 minute)
4. Visit: https://liqcui.github.io/AEVA-P/

---

## Files Structure

### Deployed Files

```
demo/
├── index.html          # Main demo page (deployed)
├── README.md           # Demo documentation (deployed)
└── .nojekyll          # Disable Jekyll processing (deployed)
```

### Workflow Configuration

```yaml
# .github/workflows/deploy-pages.yml
name: Deploy Demo to GitHub Pages

on:
  push:
    branches: [main]
    paths: ['demo/**']
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: './demo'
      - uses: actions/deploy-pages@v4
        id: deployment
```

---

## Customization

### Change Demo Content

Edit `demo/index.html`:

```bash
# Edit demo content
vim demo/index.html

# Commit changes
git add demo/index.html
git commit -m "Update demo content"
git push origin main

# Automatic deployment will trigger
```

### Custom Domain (Optional)

To use a custom domain:

1. Create `demo/CNAME` file:
```bash
echo "demo.yourdomain.com" > demo/CNAME
git add demo/CNAME
git commit -m "Add custom domain"
git push origin main
```

2. Configure DNS:
   - Add CNAME record: `demo` → `liqcui.github.io`

3. In GitHub repository settings:
   - Pages → Custom domain
   - Enter: `demo.yourdomain.com`
   - Save

---

## Troubleshooting

### Deployment Fails

**Issue**: Workflow fails with permission error

**Solution**:
1. Check repository settings → Actions → Permissions
2. Enable "Read and write permissions"
3. Re-run workflow

### Page Not Found (404)

**Issue**: https://liqcui.github.io/AEVA-P/ shows 404

**Solution**:
1. Check GitHub Pages settings
2. Ensure source is set to "GitHub Actions"
3. Verify deployment succeeded in Actions tab
4. Wait 1-2 minutes for DNS propagation

### Changes Not Reflected

**Issue**: Updated demo but changes not visible

**Solution**:
1. Hard refresh browser: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
2. Clear browser cache
3. Wait 1-2 minutes for deployment
4. Check workflow run completed successfully

### Styles Not Loading

**Issue**: Page loads but no styling

**Solution**:
1. Ensure `.nojekyll` file exists in `demo/` directory
2. Check browser console for errors
3. Verify all CSS is inline in `index.html`
4. Re-deploy workflow

---

## Monitoring

### Check Deployment Status

**Via GitHub UI**:
1. Go to **Actions** tab
2. View recent workflow runs
3. Click run for details/logs

**Via Command Line**:
```bash
# View workflow status
gh run list --workflow=deploy-pages.yml

# View specific run details
gh run view <run-id>
```

### View Deployment Logs

1. Actions tab → Select workflow run
2. Click **deploy** job
3. Expand steps to view logs
4. Check "Deploy to GitHub Pages" step

---

## Performance

### Optimization Tips

1. **Minimize File Size**:
   - Inline critical CSS
   - Minimize JavaScript
   - Use SVG for icons

2. **Enable Caching**:
   - Browser caches static assets
   - GitHub Pages auto-enables caching

3. **CDN Benefits**:
   - GitHub Pages uses CDN
   - Global distribution
   - Fast loading worldwide

### Metrics

- **Page Load**: <1 second
- **Deployment Time**: <1 minute
- **Availability**: 99.9%+
- **Global CDN**: Yes

---

## Security

### HTTPS

- ✅ Automatic HTTPS enabled
- ✅ Certificate auto-renewed
- ✅ HTTP → HTTPS redirect

### Content Security

- Keep sensitive data out of demo
- Use mock data only
- No API keys in demo
- Watermark protection (AEVA-2026-LQC-dc68e33)

---

## Best Practices

### Development Workflow

1. **Local Testing**:
```bash
cd demo
python3 -m http.server 8000
open http://localhost:8000
```

2. **Commit Changes**:
```bash
git add demo/
git commit -m "Update demo: [description]"
```

3. **Push & Deploy**:
```bash
git push origin main
# Auto-deployment triggers
```

4. **Verify**:
   - Wait 1-2 minutes
   - Visit: https://liqcui.github.io/AEVA-P/
   - Test all features

### Version Control

- Tag releases:
```bash
git tag -a demo-v1.0 -m "Demo version 1.0"
git push origin demo-v1.0
```

- Track demo changes separately
- Use meaningful commit messages

---

## Updating Demo

### Regular Updates

```bash
# 1. Make changes
vim demo/index.html

# 2. Test locally
cd demo
python3 -m http.server 8000

# 3. Commit
git add demo/
git commit -m "Update demo: add new feature showcase"

# 4. Push
git push origin main

# 5. Verify deployment
# Check Actions tab for workflow status
# Visit https://liqcui.github.io/AEVA-P/
```

### Emergency Updates

If critical fix needed:

```bash
# 1. Quick fix
vim demo/index.html

# 2. Fast commit
git add demo/index.html
git commit -m "Hotfix: critical demo issue"
git push origin main

# 3. Manual trigger (if needed)
gh workflow run deploy-pages.yml
```

---

## URLs

### Production

- **Live Demo**: https://liqcui.github.io/AEVA-P/
- **Repository**: https://github.com/liqcui/AEVA-P
- **Workflow**: https://github.com/liqcui/AEVA-P/actions

### Badges (Optional)

Add to README:

```markdown
[![Deploy](https://github.com/liqcui/AEVA-P/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/liqcui/AEVA-P/actions/workflows/deploy-pages.yml)
```

---

## FAQ

### Q: How long does deployment take?

**A**: Usually <1 minute. Check Actions tab for exact time.

### Q: Can I use custom domain?

**A**: Yes, add `CNAME` file to `demo/` directory and configure DNS.

### Q: Is HTTPS supported?

**A**: Yes, automatic HTTPS with auto-renewed certificate.

### Q: How to rollback?

**A**:
```bash
git revert <commit-hash>
git push origin main
```

### Q: Can I preview before deployment?

**A**: Test locally with `python3 -m http.server 8000` in `demo/` directory.

---

## Support

- **GitHub Issues**: https://github.com/liqcui/AEVA-P/issues
- **Email**: liquan_cui@126.com
- **Documentation**: [docs/](.)

---

## License

**Dual License**:
- ✅ FREE for personal and academic use
- ⚠️ Commercial use requires explicit permission

Contact: liquan_cui@126.com

---

*AEVA v2.0 - GitHub Pages Deployment*
*Copyright © 2024-2026 AEVA Development Team*
*Watermark: AEVA-2026-LQC-dc68e33*
