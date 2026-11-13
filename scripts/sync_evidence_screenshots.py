import shutil
from pathlib import Path

root = Path(".").resolve()
demo_dir = root / "dashboard_demonstration_package"
rep_dash_dir = root / "report_evidence_package" / "06_dashboard"
rep_shots_dir = rep_dash_dir / "demonstration_screenshots"

# 1. Copy guides to demo_dir
shutil.copy2(root / "DASHBOARD_SCREENSHOT_GUIDE.md", demo_dir / "DASHBOARD_SCREENSHOT_GUIDE.md")
shutil.copy2(root / "DASHBOARD_FUNCTIONALITY_COVERAGE.md", demo_dir / "DASHBOARD_FUNCTIONALITY_COVERAGE.md")

# 2. Copy guides to report_evidence_package/06_dashboard
shutil.copy2(root / "DASHBOARD_SCREENSHOT_GUIDE.md", rep_dash_dir / "DASHBOARD_SCREENSHOT_GUIDE.md")
shutil.copy2(root / "DASHBOARD_FUNCTIONALITY_COVERAGE.md", rep_dash_dir / "DASHBOARD_FUNCTIONALITY_COVERAGE.md")

# 3. Copy all PNGs from demo_dir to rep_shots_dir
png_count = 0
for sub in [
    "01_overview_and_eda",
    "02_probability_distributions",
    "03_hypothesis_testing",
    "04_correlation_and_collinearity",
    "05_predictive_simulator",
]:
    src_sub = demo_dir / sub
    dst_sub = rep_shots_dir / sub
    dst_sub.mkdir(parents=True, exist_ok=True)
    for p in src_sub.glob("*.png"):
        shutil.copy2(p, dst_sub / p.name)
        png_count += 1

print(f"Synced {png_count} PNGs to {rep_shots_dir.relative_to(root)}.")
