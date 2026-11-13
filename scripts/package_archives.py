import zipfile
from pathlib import Path

def create_zip(source_dir: str, output_zip: str):
    source_path = Path(source_dir).resolve()
    zip_path = Path(output_zip).resolve()
    print(f"Zipping {source_path} into {zip_path}...")
    count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for p in sorted(source_path.rglob("*")):
            if p.is_file():
                rel_path = p.relative_to(source_path)
                zf.write(p, rel_path)
                count += 1
    print(f"Wrote {count} files to {zip_path.name} ({zip_path.stat().st_size:,} bytes).")
    with zipfile.ZipFile(zip_path, "r") as zf:
        corrupt = zf.testzip()
        if corrupt:
            raise RuntimeError(f"Corrupt file in {zip_path}: {corrupt}")
        print(f"Verification passed: {zip_path.name} is intact!")

if __name__ == "__main__":
    create_zip("dashboard_demonstration_package", "dashboard_demonstration_package.zip")
    create_zip("report_evidence_package", "report_evidence_package.zip")
