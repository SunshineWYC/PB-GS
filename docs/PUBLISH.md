# PB-GS 网站发布与维护

仓库：https://github.com/SunshineWYC/PB-GS 。正式网站：https://sunshinewyc.github.io/PB-GS/ 。

- `main`：默认分支，预留研究代码，与网站历史独立。
- `project_page`：网站及维护文件；不要与 main 合并，不强推。
- GitHub Pages 使用 GitHub Actions，工作流只上传 `./site`。
- 推送 project_page 会触发发布；main 不参与网站发布。部署环境只允许 project_page 分支。

## 修改和发布

1. 核对当前分支为 project_page、origin 为 SunshineWYC/PB-GS，且没有未处理的本地修改。干净工作区可用 `git pull --ff-only origin project_page` 同步。
2. 根据材料修改网页，本地预览并按变化范围验收；更新素材 manifest。私有 materials、notes、PROJECT_BRIEF.md、.local-preview 及本地工具配置始终忽略。
3. 执行 `python scripts/check_site.py --release`。若更换正式 URL，同步 release.json、canonical、og:url 和分享图片绝对地址。
4. 核对暂存差异和文件清单，确认没有原始论文或私有记录；在用户授权后提交并推送 project_page。
5. 在 Actions 检查该提交的 Publish project page 成功，再核对正式网页及资源。部署成功与线上验证完成后，将提交、工作流 URL 和网站 URL 写入本地 notes/deployment.md。

GitHub Pages 的 build_type 为 workflow，实际发布内容由上传的 Actions artifact 决定，不使用分支根目录直接发布。不要改成 Deploy from a branch，不要上传仓库根目录。

本目录保持 project_page；研究代码使用独立检出。保留既有 Git 身份和凭据。认证失败时使用正常登录，不索取聊天中的令牌；分歧通过分析与正常提交解决，不强推。回退使用 git revert 生成撤销提交并重新发布。
