# PB-GS 仓库与后续发布

当前仓库为 https://github.com/SunshineWYC/PB-GS 。

- `main`：默认分支，目前只有简短 README，供后续研究代码使用。
- `project_page`：当前网站及维护文件，使用独立的初始提交，与 main 没有共同提交历史。
- 不把网站分支合并到 main，不强推，不把 main 内容复制进网站分支。

本轮只授权建立分支和提交推送，没有启用 GitHub Pages。现有工作流只有手动入口，不会因本轮推送自动部署；正式 URL 及分享元数据尚未配置。

## 维护网站

在当前目录或单独的 project_page 分支检出中工作。先确认 `git branch --show-current` 为 `project_page`，以及 origin 为上述仓库。工作区干净时使用 `git pull --ff-only origin project_page`；有本地改动先保留，不覆盖分歧。

只跟踪网站及必要维护文件。`materials/`、`notes/`、`PROJECT_BRIEF.md`、`.local-preview/` 和本地工具配置始终忽略；不上传论文全文，不把令牌写入任何文件。保留现有 Git 身份和凭据管理。

修改后运行 `python scripts/check_site.py` 并按变化范围检查浏览器。提交前检查暂存差异、文件清单及私有路径；只推送 `project_page`。不要在含私有工作材料的当前目录切换到 main；研究代码使用单独检出。

## 未来获授权后启用 Pages

1. 核对 Pages 实际设置，确定正式 URL；在 release.json、canonical、og:url、分享图绝对地址中同步。不要把推导出的候选地址当成已上线地址。
2. 运行 `python scripts/check_site.py --release`，并复查实际浏览器显示与素材公开范围。
3. 使用 GitHub Actions 发布，上传路径必须为 `./site`，不能上传整个仓库根目录。
4. 依据实际 Actions 发现情况，为 `project_page` 显式配置推送触发并启用 Pages；不要为手动入口可见性把工作流加到 main。空代码分支不负责网站部署。
5. 只有远端目标提交、成功的部署工作流、正式 URL 和资源内容均核对通过后，才能报告上线。记录于本地 notes/deployment.md。

遇到登录或权限错误时报告准确原因，使用正常 Git/GitHub 登录；不能因为读取仓库成功就假定能够推送，也不能以强推解决分歧。
