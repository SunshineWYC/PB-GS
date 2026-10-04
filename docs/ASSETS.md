# 素材、来源与公开范围

原材料放 materials/；中间转换、截图检查放 .local-preview/；准备公开的文件才放 site/assets/images/ 或 site/assets/videos/。不要把作者未授权的本地全文、原始实验数据、训练日志或素材源文件放进 site/。

site/assets/manifest.json 是公开媒体清单，每项有 path、role、public_approved。path 相对 site/，不写绝对本机路径，也不在公开清单中写私有原稿文件名。详细来源映射留在 notes/。public_approved 表示已根据用户的公开范围或公开来源核实，不等于每个文件都要重新打断用户询问。

新增 PNG、WebP、SVG、MP4 等文件都要登记。删除文件时删除对应清单项。未使用文件移到 .local-preview/ 或原材料目录；不要仅删除页面引用却留在 site/。全部示例图位于 assets/examples/，发布检查要求删除这一目录中的文件和对应清单项。

## 通用导图工具（可选）

只在需要导出时安装依赖，优先使用已有可用环境；不要更改全局 Python 配置：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-export.txt
```

从第 3 页导出局部区域，坐标为从页面左上角计算的 0–1 比例；以下坐标仅为语法示例，必须按实际页面重新检查：

```powershell
.\.venv\Scripts\python.exe scripts/export_figure.py --pdf materials/paper/latest.pdf --page 3 --crop 0.08 0.12 0.92 0.60 --name method-overview --kind diagram
```

普通图片使用 `--image materials/charts/result.png --name qualitative --kind render`。图解/表格导出 PNG，渲染图导出高质量 WebP；生成全尺寸及预览版本，原文件不变。输出已存在时不会静默覆盖；检查后用 --overwrite。工具记录 SHA256 和裁剪坐标，新增媒体默认 public_approved=false，检查后再更新清单。

必须看导出后的图片：数学符号、上标、列名、图例、曲线、文字是否清晰，裁剪是否完整，左右基线是否颠倒；确认这张图确实出现在目标版本。PDF 提取文字不能替代看图。若原表与图冲突，不擅自重画成“正确版本”。

## 视频处理

使用浏览器支持的 MP4（常见 H.264/AAC）或 WebM；先播放验证。较大的原视频保留在 materials/，展示版按可读细节合理压缩。每段视频准备明确 poster。对比视频需要帧数、视角和时间对齐后左右拼接，不能仅凭文件名假定已同步。不要给旧演示标注未经验证的新实验结果。

## 截图 vs 重绘

表格复杂且已有清晰原表时优先截图；文字密集时提供高分辨率查看。确需重绘统计图时使用标准绘图库，并保留数据来源和计算过程。不要用生成式图像工具生成或“改善”实验数据、曲线、数值和基线结果。
