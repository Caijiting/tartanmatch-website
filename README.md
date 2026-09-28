# TartanMatch 项目网站

本地静态论文网站，参考 MAC-I² 项目页的深色学术展示风格。页面内容为英文，使用提供的论文与 PPT 原始素材，无运行时第三方依赖。

## 本地预览

```bash
git clone https://github.com/Caijiting/tartanmatch-website.git
cd tartanmatch-website
npm run dev
```

需要 Node.js 18 或更新版本，无需安装 npm 依赖。私有仓库克隆需要 GitHub 账号授权。

打开 http://localhost:3000 。更换端口：`npm run dev -- --port 3001`。

若通过 SSH 连接到这台机器，请在本机转发远端的 3000 端口，或使用编辑器的 Ports / 端口转发功能，然后在本机浏览器访问该地址。

## 页面内容

- 首屏背景展示 8 组同模态与跨模态匹配，配有 Source / Target 输入与双向 Warp 标签；首屏后直接展示完整 Abstract。
- 5 × 5 模态矩阵：25 个配对均可切换并播放原 PPT 动画。
- DSERT-RoLL 真实场景：6 个配对，MINIMA / MatchAnything / TartanMatch 对比及同步重播。
- 论文架构图（支持放大）、模态表示、两阶段训练与数据混合。
- Cross-modal / Same-modal / Relative pose 结果图表与精确数值表格。
- 重雪传感器输入（单独说明其含义）、视网膜与卫星的双向 Warp 对照与 BibTeX 复制。
- 深浅主题、移动端布局、键盘导航、减弱动态效果支持。

## 文件

- `index.html`：页面结构与论文介绍。
- `styles.css`：样式、主题与响应式布局。
- `app.js`：视频选择、交互图表、引用复制。
- `assets/`：已提取和压缩的素材（约 39 MB，含 PDF），直接用于部署。
- `scripts/serve.mjs`：支持视频 Range 请求的 Node 本地服务。
- `scripts/build.mjs`：复制静态站点到 `dist/`。
- `scripts/prepare_assets.py`：从原始 PPT / PDF 提取并转换素材；通常无需重新运行。
- `.work/`：本地提取文件、检查记录与页面截图，不属于网站发布内容。

`npm run build` 可生成独立 `dist/`，适合以后部署到 GitHub Pages 等静态托管服务。当前仅本地预览，未部署。

仓库包含运行和构建所需的全部网页素材。原始 PPT、根目录论文副本、`.work/` 和 `dist/` 不进入版本管理；重新提取素材时需要自行将原始文件放回项目根目录。

## 素材与数据依据

1. `mmufm_paper (18).pdf`：正式页面标题、作者顺序、摘要、Fig. 2 架构图、Table II 跨模态结果、Table III 位姿结果、Table IV 重雪结果、Table V 同模态结果、Table VII 联合训练结果。
2. `Modality_pairs_demo_video_new2 (2).pptx`：第 9 页的 25 配对动画，以及第 11–14 页真实传感器对比。原始 GIF 转为 H.264 MP4；移除原动画顶端文字后，网页提供清晰的列标题。
3. `tartanmatch_pre_final (4) (1).pptx`：作者单位、重雪多传感器观测和未见图像域定性示例。
4. 字体 DM Sans / Space Grotesk 已下载到本地，预览不依赖 Google Fonts 网络请求。

61.9% / 49.6% 为论文摘要报告值。图表中的 strongest baseline 按每个评测设置从 dense baselines 选取，并保留 TartanMatch 并非最优的设置。运行时间使用 Table II 的 27.8 / 27.6 / 206.4 / 262.4 ms，因此页面速度比写为 7.4×。定性迁移例子不作定量性能声明。

提供的 PDF 含投稿模板占位信息。网站未填写未确认的会议、DOI、arXiv 编号或代码仓库；BibTeX 使用 manuscript 条目。公开发布前可替换为最终出版信息。

若需重新提取素材，使用 Python 3.11，安装 `Pillow pymupdf imageio-ffmpeg` 后运行 `python3.11 scripts/prepare_assets.py`。常规运行与构建只需 Node.js。

## 素材方向核对（修订）

- 原固定图像对讲解区已由完整论文 Abstract 替换；25 配对与真实场景交互演示保留。
- 25 配对与真实场景视频：保留原始完整三栏，左为固定 source，中间为变化的 target，右为 source warped 到当前 target。网页明确提示比较第 3 栏与第 2 栏。
- 第二份 PPT 第 82 页：retina image98/99 为输入，image101 为 target→source，image100 为 source→target；satellite image102/103 为输入，image104 为 target→source，image105 为 source→target。网页按原 PPT 展示两幅输入及两个方向，不再将 image104 错标为 warped source。
- 静态图像对的 GIF 是从原图到预测对齐的过渡演示，不是时间序列；页面已区分这两类动画。暂停或减少动态效果时，首屏使用最终对齐帧作封面。
- 移除页头、页脚的放射状星号，保留 TartanMatch 文字标识。

## 论文标题背景视频

背景使用 `tartanmatch_talk_finalized.pptx` 第 1、81、82 页的 8 组 matching，保留连续铺满的现有排版。

- 同模态：Depth/Depth、稀疏 Depth/Depth。
- 跨模态：RGB/Depth、RGB/Thermal、Depth/RGB、RGB/Event、LiDAR/RGB、稀疏 RGB/Depth。
- 每组上方为 Source / Target 原图，下方为 Target → Source / Source → Target 动画；第 81 页的 Depth→RGB 组已按 source/target 语义重新排列。
- 桌面视频 1920×960，4 列 × 2 行；手机视频 900×1800，2 列 × 4 行。静音循环 12 秒。
- `scripts/prepare_hero_video.py` 直接读取指定 finalized PPT，合成视频与最终对齐帧封面。素材和原幻灯片的对应关系保存在 `assets/hero-media-sources.json`。
- 作者字号为桌面 18px、手机 14px；机构移动到贡献说明下方，字号分别为 18px / 16px。
- 支持暂停、离屏暂停、减少动态效果时显示静态封面。
