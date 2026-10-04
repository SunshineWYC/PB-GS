# PB-GS project page

**Acquisition-Aware Gaussian Splatting From Native Pushbroom Imagery for Remote Sensing Scene Reconstruction**

This branch contains the static research project page. The `main` branch is reserved for research code; `project_page` has an independent commit history. Do not merge the two branches.

## Preview and checks

```powershell
python scripts/preview.py --port 49327
python scripts/check_site.py
```

Open http://127.0.0.1:49327/ to preview. The server exposes only `site/`.

- `site/`: the complete website and approved figures, tables, and comparison images.
- `scripts/`: local preview, content checks, and figure export tools.
- `release.json`: repository and publication configuration.

The website uses static HTML, CSS, and JavaScript without a build step or external runtime dependencies. It includes the original abstract, four collapsible method explanations, eight named scene comparisons, optimization efficiency, orthographic results, and limitations.

## Branch and publication boundaries

Maintain the website on `project_page`:

```powershell
git clone --single-branch --branch project_page https://github.com/SunshineWYC/PB-GS.git
```

Raw papers, source charts, private project notes, and local review files are excluded from version control. Published website assets are limited to `site/`; preserve this directory boundary when configuring hosting.

The project website is available at [https://sunshinewyc.github.io/PB-GS/](https://sunshinewyc.github.io/PB-GS/). GitHub Actions deploys only `site/` when updates are pushed to `project_page`. The `main` branch is not involved in website deployment. Run `python scripts/check_site.py --release` before publishing.

The page retains the template attribution and licenses described in [NOTICE.md](NOTICE.md). Research materials retain their respective rights.
