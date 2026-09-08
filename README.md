<div align="center">
  <img width="100%" src="assets/minimax-h3-header.gif" alt="MiniMax H3">
</div>

<p align="center">
  <a href="https://hailuoai.video" target="_blank"><img src="https://img.shields.io/badge/Hailuo%20AI-FF6C37?logo=minimax&logoColor=white" alt="Hailuo AI"></a>
  <a href="https://platform.minimax.io/docs/guides/text-generation" target="_blank"><img src="https://img.shields.io/badge/API-FF6C37?logo=minimax&logoColor=white" alt="API"></a>
  <a href="https://www.minimax.io" target="_blank"><img src="https://img.shields.io/badge/MiniMax%20Website-FF6C37?logo=minimax&logoColor=white" alt="MiniMax Website"></a>
  <a href="https://github.com/MiniMax-AI/MiniMax-H3" target="_blank"><img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white" alt="GitHub"></a>
  <a href="https://huggingface.co/MiniMaxAI/MiniMax-H3" target="_blank"><img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=black" alt="Hugging Face"></a>
  <br>
  <a href="https://modelscope.cn/organization/minimax" target="_blank" rel="noopener noreferrer"><img alt="ModelScope MiniMax AI" src="https://img.shields.io/badge/ModelScope-MiniMax%20AI-white?labelColor=%23EF3D5D"></a>
  <a href="https://platform.minimaxi.com/docs/faq/contact-us" target="_blank"><img src="https://img.shields.io/badge/WeChat-07C160?logo=wechat&logoColor=white" alt="WeChat"></a>
  <a href="https://discord.com/invite/dbMxutw7tP" target="_blank"><img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE"><img src="https://img.shields.io/badge/LICENSE-4CAF50?logo=creativecommons&logoColor=white" alt="LICENSE"></a>
</p>

<p align="center">
  <a href="README.en.md">English</a> |
  <a href="README.md"><strong>简体中文</strong></a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.ja.md">日本語</a>
</p>

# MiniMax H3

## 提示词撰写技巧（Prompt Writing Skill）

安装 H3 提示词撰写技能 —— 本仓库随附的九项技能之一：

```bash
npx skills add https://github.com/MiniMax-AI/MiniMax-H3 --skill h3-prompt-writing
```

它附带两份提示词指南，位于 `skills/h3-prompt-writing/references/`：`base-en.txt` 用于文本/关键帧模式，`ref-en.txt` 用于全参考（Ref2VA）模式。

**智能体兼容性：** `h3-prompt-writing` 是一个纯 Markdown + 参考文件的技能，不调用任何外部 API，因此可在 Claude Code、Claude Agent SDK、Cursor、Windsurf、基于 OpenAI 的 agents/Codex、LangChain，或任何能读取 `SKILL.md` 与本地文件的 harness 中使用。随附的 `skills/h3-prompt-writing/agents/openai.yaml` 仅为 ChatGPT/Codex 技能界面提供可选的 UI 元数据（显示名、描述、默认提示词），遵循 [OpenAI 的技能规范](https://learn.chatgpt.com/docs/build-skills)——它并不将该技能限定于 OpenAI agents。

其余八项是面向 MiniMax Hub 画布工作流（`hub_generate_video`、`hub_generate_image`、画布节点、选择卡片等）构建的、特定风格的视频生成技能，无法移植到通用 agent harness：

<table align="center">
  <tr>
    <td align="center"><img src="assets/minimalist-product-ad-generator.gif" alt="minimalist-product-ad-generator" width="240"><br><a href="skills/minimalist-product-ad-generator/SKILL.md">minimalist-product-ad-generator</a></td>
    <td align="center"><img src="assets/3d-animation-short-generator.gif" alt="3d-animation-short-generator" width="240"><br><a href="skills/3d-animation-short-generator/SKILL.md">3d-animation-short-generator</a></td>
    <td align="center"><img src="assets/papercraft-stop-motion-explainer.gif" alt="papercraft-stop-motion-explainer" width="240"><br><a href="skills/papercraft-stop-motion-explainer/SKILL.md">papercraft-stop-motion-explainer</a></td>
    <td align="center"><img src="assets/brand-promo-video-generator.gif" alt="brand-promo-video-generator" width="240"><br><a href="skills/brand-promo-video-generator/SKILL.md">brand-promo-video-generator</a></td>
  </tr>
  <tr>
    <td align="center"><img src="assets/music-video-subtitle-generator.gif" alt="music-video-subtitle-generator" width="240"><br><a href="skills/music-video-subtitle-generator/SKILL.md">music-video-subtitle-generator</a></td>
    <td align="center"><img src="assets/co-op-game-intro-generator.gif" alt="co-op-game-intro-generator" width="240"><br><a href="skills/co-op-game-intro-generator/SKILL.md">co-op-game-intro-generator</a></td>
    <td align="center"><img src="assets/paper-collage-explainer-generator.gif" alt="paper-collage-explainer-generator" width="240"><br><a href="skills/paper-collage-explainer-generator/SKILL.md">paper-collage-explainer-generator</a></td>
    <td align="center"><img src="assets/handdrawn-live-video-generator.gif" alt="handdrawn-live-video-generator" width="240"><br><a href="skills/handdrawn-live-video-generator/SKILL.md">handdrawn-live-video-generator</a></td>
  </tr>
</table>

## 在线 API

通过 API 直接使用 MiniMax-H3。
- 国际版：[platform.minimax.io](https://platform.minimax.io/docs/api-reference/video-generation-v2-create) | 国内版：[platform.minimaxi.com](https://platform.minimaxi.com/docs/api-reference/video-generation-v2-create)

## 在线 App

通过 App 直接使用 MiniMax-H3。
- WebApp 国际版：[hailuoai.video](https://hailuoai.video/tools/minimax-h3) | 国内版：[hailuoai.com](https://hailuoai.com/)
- 桌面端 国际版：[hub.minimax.io](https://hub.minimax.io/) | 国内版：[hub.minimaxi.com](https://hub.minimaxi.com/)

## 系统概述

MiniMax H3 是一套通用的全模态生成系统。它支持对由文本、图像、视频和音频组成的多模态上下文进行统一理解，并能生成最高 2K 分辨率、最长 15 秒、且带有原生立体声的视频。得益于以任务泛化为导向的系统设计，H3 在预训练阶段就已具备广泛的多模态上下文理解与生成能力，在遵循复杂多模态指令时表现出色。

H3 支持以下输入与输出规格：

| 类别 | 规格 |
|---|---|
| 输出时长 | 4–15 秒 |
| 输出宽高比 | 支持多种宽高比，包括但不限于 21:9、16:9、4:3、1:1、3:4、9:16 |
| 输出分辨率 | 支持多种分辨率尺寸。默认短边设为 768 像素。2K 分辨率可通过 H3-Regenerate-2K 生成 |
| 输出帧率 | 24 FPS |
| 输出音频 | 32 kHz 立体声 |
| 支持的对白语言 | 稳定支持 11 种语言：阿拉伯语、中文、英语、法语、德语、意大利语、日语、韩语、葡萄牙语、俄语、西班牙语。其它语言也有不同程度的支持 |

### 模型变体与输入规格

| 模型变体 | 输入模式 | 规格 |
|---|---|---|
| H3-Base-FL2VA | 首帧-末帧模式 | 支持零张、一张或两张输入图像。<br><br>- 无图像输入：文生视频模式<br>- 一张图像输入：首帧生视频或末帧生视频<br>- 两张图像输入：首帧-末帧生视频 |
| H3-Base-Ref2VA | 全参考模式 | 支持多模态参考输入：<br><br>- **图像：** ≤ 9 张<br>- **视频：** ≤ 3 段；每段须 2–15 秒；总时长 ≤ 15 秒<br>- **音频：** ≤ 3 段；每段须 2–15 秒；总时长 ≤ 15 秒<br>- **混合输入：** 所有输入类型合计文件数最多 12 个 |

![Image](assets/overview.png)

完整的 H3 系统由以下三个模块组成：
- **H3-Context-IR**：随着输入愈发复杂，我们构建了一套专用系统来深度理解并精修输入的多模态指令，再将其转换为 H3 易于理解的形式——上下文中间表示（Context Intermediate Representation）——用于生成。**H3-Context-IR 对最终输出质量至关重要，因此我们强烈建议将其纳入你的生成管线，或遵循"提示词指引"自行构建上下文处理系统。**
- **H3-Base**：基于 H3-Context-IR 的输出生成音视频，输出 768p 分辨率结果。
- **H3-Regenerate-2K**：将 768p 结果与原始上下文一起回填进 H3，重新生成 2K 分辨率输出。该过程同时利用了 H3 强大的生成能力与原始上下文中蕴含的丰富信息，从而产出细节更精确、视觉保真度更高的高分辨率结果。

## 模型架构

### H3-Context-IR

H3-Context-IR 是一套面向自由形式多模态输入、托管式的预处理与编排系统。

它解析文本、图像、音频与参考视频之间的关系，以及这些素材与预期生成结果之间的关联。其内部流程包含指令解析、跨模态关联、时序理解与复杂逻辑推理。

H3-Context-IR 将其对上下文的理解序列化成一个 H3-Base 可接收的结构化表示。在不偏离用户原始意图的前提下，它也会在适当处补充缺失或欠明确的语义细节。

由于 H3-Context-IR 依赖多阶段流程及多个托管模型与服务，它未包含在本开源版本中。我们提供一套 API，使用户能复现官方流程的行为。我们也提供详细教程，开发者可遵循**提示词指引**自行构建预处理系统。

详见**推荐工作流 — 完整 2K 工作流**。

**安全护栏**

用户提交的文本、图像和视频，以及增强后的提示词，都会经过自动化审核。疑似违法、色情或侵犯第三方权利的内容可能被拦截。我们采用业界标准的过滤措施，但无法消除误判（误报/漏报）。这些护栏不影响被许可方在《MiniMax H3 社区许可协议》下的义务，特别是与合法使用和使用限制相关的部分。

### H3-Base

![Image](assets/full-arch.png)

#### 架构概述

- H3-Base 使用对应的编码器或 VAE 对不同模态进行编码，并将编码后的表示组织为统一的打包多模态序列。在整段序列送入 H3-Omni-Transformer 之前，使用 RoPE 捕获 token 之间必要的时空关系。
- 具体而言，文本由 H3-Encoder 编码；视觉输入由 H3-Encoder 与 H3-VisualVAE 共同编码；音频仅由 H3-AudioVAE 编码。
- H3-Omni-Transformer 联合预测视频与音频的潜变量，随后分别解码为视频与立体声音频。
- 为降低长多模态序列的计算开销，H3 原生支持稀疏注意力训练与推理。首个开源版本仅提供全注意力推理。我们的稀疏注意力实现将在后续更新中发布。

#### H3-Encoder

- H3-Encoder 使用 Qwen3-VL-32B 的完整预训练权重，并将其第 50 层的隐藏状态提供给 H3-Omni-Transformer。
- 我们在分词器配置中添加了若干特殊 token，例如 `<d>`。使用 H3 时需要 H3 仓库中提供的分词器及配套配置文件。

#### H3-VAE

H3 使用相互独立的视觉与音频潜变量来分别表示各自模态。

##### H3-VisualVAE

- H3-VisualVAE 是一个时间因果的视频自编码器，空间压缩因子 16×、时间压缩因子 4×、24 个潜通道，记作 f16t4d24。我们应用了多种潜空间优化技术，在提升重建质量的同时改善潜变量的可学习性。
- 在送入 H3-Omni-Transformer 之前，视觉潜变量会沿 `(时间, 高, 宽)` 维度以 `1 × 2 × 2` 的 patch 尺寸进一步分块（patchify）。因此进入 Transformer 的视觉 token 有效空间下采样因子为 32×，而时间下采样因子仍为 4×。
- H3-VisualVAE 的潜空间同时针对重建质量与生成模型的可学习性进行了优化。在训练完编码器后，我们还额外训练了一个基于 ViT 的解码器，以降低解码开销并进一步提升重建质量。

##### H3-AudioVAE

- H3-AudioVAE 对左右两个音频声道使用相同的编码器与解码器，但各自独立处理。解码后的声道随后重新组合，从而实现立体声音频的输入与输出。
- 对每个声道，H3-AudioVAE 将 32 kHz 音频压缩为时间速率 40 Hz 的潜 token 序列。
- 受 VA-VAE 启发，我们优化潜空间以在保留音频重建质量的同时，使其更易于被生成模型学习。

#### H3-Omni-Transformer

- 为兼顾可扩展性与泛化能力，我们采用了相对简洁的 Transformer 块设计。H3-Omni-Transformer 是一个 33B 参数的稠密、单流 Transformer，其中约 13B 参数位于 AdaLN 相关分支中。由于 AdaLN 调制输出可预计算并缓存，推理部署时无需加载这些参数。我们发布完整模型权重以支持进一步开发，包括微调。
- 注意力层与 FFN 层均不含模态专属结构。模态专属参数仅限于输入/输出层与 AdaLN 分支。特别地，模态专属的 AdaLN 以较低的额外训练与推理开销提升了生成质量。
- 模型使用三维多模态旋转位置嵌入（MM-RoPE）来表示跨越时间与两个空间维度 `(t, h, w)` 的位置关系。
- 在训练的最后阶段，我们引入了原生稀疏注意力以降低长序列的计算开销。稀疏注意力实现未包含在首个开源版本中，将在后续更新中单独发布。

### H3-Regenerate-2K

- 对于 H3 的 2K 分辨率输出，我们没有使用传统的专用超分模块，而是采用 H3 基础模型，以"上下文内（in-context）"方式重新生成其自身的低分辨率结果。
- 该方法有两个优势：（1）重生成过程能最大程度复用 H3 基础模型的生成能力；（2）上下文内格式能在产出高分辨率结果时复用原始多模态上下文，从而恢复出传统超分方法不得不"猜测"的信息，例如小文字与精细细节。
- 上下文内重生成也是任务泛化的一个例证。
- **由于系统复杂度较高，该模块尚未开源。待准备就绪后将予以发布。** 我们提供一套 API 用于验证官方结果；见下方"完整 2K 工作流"。

## 推荐工作流

为帮助社区正确部署 MiniMax H3，我们提供两种验证方式。

由于完整的 H3 系统由三个模块组成——H3-Context-IR、H3-Base 与 H3-Regenerate-2K——"完整 2K 工作流"通过结合开放平台 API 与本地部署的 H3-Base，提供了一条面向 2K 输出的端到端验证管线。"本地部署 H3-Base"章节则提供一种仅用本地部署的 H3-Base 验证 768p 输出的方法。

此外，"提示词指引"章节提供了详细教程，帮助社区开发自己的提示词系统。

### 本地部署 H3-Base

MiniMax H3 以两个面向特定任务的检查点形式发布。每个检查点包含一个专用的 Omni Transformer 模型，以及所需的 processor、tokenizer、文本编码器、Visual VAE 与独立的 Audio VAE 组件。

| 检查点 | 支持任务 | 输入条件 | 输出 | 精度 |
|---|---|---|---|---|
| MiniMax-H3 Base FL2VA | 文生音视频（`t2va`）、首/末帧生音视频（`fl2va`） | 文本；可选首帧、末帧或二者皆有 | 视频与音频 | BF16 |
| MiniMax-H3 Base Ref2VA | 参考生音视频（`ref2va`） | 带参考图像、视频和/或音频的文本 | 视频与音频 | BF16 |

发布的检查点为 CFG 蒸馏后的 Omni Transformer 模型权重。

每个检查点作为一个自包含的 Hugging Face 风格仓库分发，包含以下组件：

```text
<TASK>/
├── model_index.json
├── processor/
├── tokenizer/
├── text_encoder/
├── transformer/
├── visual_vae/
└── audio_vae/
```

下载模型。仓库并列托管了原始检查点（`FL2VA/`、`Ref2VA/`）与 diffusers 格式，因此请按需限定下载范围：

`model_index.json` 是仓库级的公共入口。任务族特定的 diffusers 索引仍位于 `FL2VA/model_index.json` 与 `Ref2VA/model_index.json`。

```bash
# 原始检查点，两个任务族（SGLang、vLLM）：
hf download MiniMaxAI/MiniMax-H3 --include "model_index.json" "FL2VA/*" "Ref2VA/*" --local-dir MiniMax-H3

# 或仅单个任务族：
hf download MiniMaxAI/MiniMax-H3 --include "model_index.json" "FL2VA/*" --local-dir MiniMax-H3
```

diffusers 用户无需手动下载：`ModularPipeline.from_pretrained("MiniMaxAI/MiniMax-H3")` 会精确获取所需组件。加载方式参见 [diffusers 文档](https://github.com/huggingface/diffusers/blob/minimax-h3/docs/source/en/api/pipelines/minimax_h3.md)。

我们推荐以下推理框架来服务该模型：

- [SGLang](https://docs.sglang.io/) - 参见 [cookbook](https://docs.sglang.io/cookbook/diffusion/MiniMax/MiniMax-H3)
- [vLLM](https://github.com/vllm-project/vllm) - 参见 [vllm recipes](https://recipes.vllm.ai/MiniMaxAI/MiniMax-H3)
- [diffusers](https://github.com/huggingface/diffusers) - 参见 [diffusers 文档](https://github.com/huggingface/diffusers/blob/minimax-h3/docs/source/en/api/pipelines/minimax_h3.md)
- [ComfyUI](https://github.com/Comfy-Org/ComfyUI) - 参见 [Comfy 教程](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)；使用 [R2V 模板](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_minimax_h3_r2v.json) / [T2V 模板](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/video_minimax_h3_t2v.json)

#### Sglang 部署

此处以 sglang 作为部署示例。更多部署配置参见 [MiniMax-H3 部署指南](https://docs.sglang.io/cookbook/diffusion/MiniMax/MiniMax-H3#3-serve-minimax-h3)。

FL2VA：

```bash
sglang serve \
  --model-path MiniMaxAI/MiniMax-H3 \
  --num-gpus 4 \
  --ulysses-degree 4 \
  --performance-mode speed \
  --host 0.0.0.0 \
  --port 30010 \
  --model-variant fl2va
```

Ref2VA：

```bash
sglang serve \
  --model-path MiniMaxAI/MiniMax-H3 \
  --num-gpus 4 \
  --ulysses-degree 4 \
  --performance-mode speed \
  --host 0.0.0.0 \
  --port 30011 \
  --model-variant ref2va
```

#### 可复现的 768p 案例

以下 T2VA、FL2VA 与 Ref2VA 三个用例演示了如何复现 MiniMax-H3 的视频-音频生成。

| 用例 | 请求 | 结果 |
|---|---|---|
| T2VA | [查看脚本](scripts/readme/reproducible-768p-t2va-request.sh) | [t2va.mp4](assets/t2va.mp4) |
| FL2VA | [查看脚本](scripts/readme/reproducible-768p-fl2va-request.sh) | [fl2va.mp4](assets/fl2va.mp4) |
| Ref2VA | [查看脚本](scripts/readme/reproducible-768p-ref2va-request.sh) | [ref2va.mp4](assets/ref2va.mp4) |

#### 使用本地图片/视频代替远程 URL

上述可复现脚本引用了托管在公共 CDN 上的 `conditions[].uri` 值，因此开箱即用，但 `uri` 并不限于 `http(s)://`。本地测试时可将其指向 `file://` 路径——例如，把 FL2VA 的关键帧换成你自己的图片：

```json
"conditions": [
  {
    "type": "image",
    "uri": "file:///data/minimax-h3/my-keyframe.png",
    "role": "keyframe",
    "frame_index": 0
  }
]
```

该路径由 SGLang 服务端进程解析，而非运行 `curl` 的机器，因此它必须指向服务端实际可见的文件：

- 若 `sglang serve` 原生运行在宿主机上，该进程可读的任何绝对路径均可。
- 若在容器中运行，文件必须位于你挂载进容器的目录内（例如将宿主机文件夹挂载到 `/data/minimax-h3`，并引用 `file:///data/minimax-h3/...`）。

完整受支持的 condition/media 选项列表参见 [MiniMax-H3 SGLang cookbook](https://docs.sglang.io/cookbook/diffusion/MiniMax/MiniMax-H3)。

### 完整 2K 工作流

本节讲解如何组合本地部署的 SGLang 服务与官方 **H3-Context-IR**、**H3-Regenerate-2K** API，以复现由 MiniMax API 直接生成的 2K 视频质量。开始之前，请先配置 SGLang 端点与你的 MiniMax API 凭据：

```bash
# 你的 SGLang 部署地址
SGLANG_DEPLOYMENT_URL="<sglang-deployment-url>"

# MiniMax API 端点（二选一）
# 国内版
MINIMAX_API_BASE="https://api.minimaxi.com"
# 国际版
# MINIMAX_API_BASE="https://api.minimax.io"

# 从 MiniMax 平台获取的 API token
TOKEN="<token>"
```

MiniMax 平台：

API 文档：
- 创建 H3-2K：使用 /video-generation-v2-create [EN 文档](https://platform.minimax.io/docs/api-reference/video-generation-v2-create) / [CN 文档](https://platform.minimaxi.com/docs/api-reference/video-generation-v2-create)
- H3-Context-IR：使用 /video-generation-v2-h3-context-ir [EN 文档](https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir) / [CN 文档](https://platform.minimaxi.com/docs/api-reference/video-generation-v2-h3-context-ir)
- H3-Regenerate-2K：使用 /video-generation-v2-regeneration [EN 文档](https://platform.minimax.io/docs/api-reference/video-generation-v2-regeneration) / [CN 文档](https://platform.minimaxi.com/docs/api-reference/video-generation-v2-regeneration)

下方各示例将本地 H3-Base 输出文件编码为 Base64 Data URL。生产环境建议将视频上传到公开可访问的 URL，并将该 URL 作为 `base_video` 传入。

对于每个用例，我们均提供通过开放平台 API 直接生成的 2K 与 768p 参考输出，便于校验结果。

#### case-T2VA

- 类型：文本生视频
- 时长：10 秒
- 宽高比：16:9

<table>
  <thead>
    <tr><th>阶段</th><th>请求</th><th>结果</th></tr>
  </thead>
  <tbody>
    <tr><td>H3-Context-IR</td><td><a href="scripts/readme/full-2k-t2va-h3-context-ir.sh">查看脚本</a></td><td><pre><code class="language-json">{
  "task": {
    "id": "&lt;task_id&gt;",
    "model": "MiniMax-H3",
    "status": "succeeded",
    "created_at": "&lt;created_at&gt;",
    "updated_at": "&lt;updated_at&gt;",
    "content": {
      "prompt": "integrated_multimodal_description: [Shot 1] Cinematic, medium wide shot, pushing in slowly. In the cavernous, dimly lit bridge of a starship, sleek metallic consoles with glowing amber displays flank a massive, curved observation window. A female captain, in her late 40s with an athletic build and short silver-streaked black hair, stands in the center midground. She wears a structured, high-collared dark navy military tunic with silver chest insignias. Her back is to the camera, silhouetted against the cool, ambient starlight pouring through the thick glass. She stands perfectly still with her hands clasped tightly behind her back. Outside the window, a massive armada of jagged, dark grey dreadnoughts hovers in tight formation against a deep purple space nebula. The fleet's massive rear thrusters begin to glow with an intense, escalating bright blue light. [Shot 2] At 00:04.500, the camera cuts to a close-up of the captain's face and shakes strongly. The brilliant blue-white light from the fleet's gathering energy reflects vividly in her dark eyes. Suddenly, a blinding white flash floods through the window, completely washing out the background as the fleet jumps to hyperspace. The sheer spatial force violently jolts the bridge, causing the captain from Shot 1 to stagger slightly forward, her shoulders tensing as she visibly braces herself against the physical tremors. As the intense white light fades abruptly, leaving only the dim, empty expanse of the purple nebula reflected on her starkly lit skin, her jaw clenches, and she slowly closes her eyes in the newly emptied space.\noverall_soundscape: A low, resonant hum of the ship's ambient life support systems serves as the baseline, soon drowned out by an audible, escalating, high-pitched electronic whine as the fleet outside charges its hyperdrives. A massive, deafening, bass-heavy boom and sharp crackle erupts during the blinding flash, accompanied by the loud metall... [truncated]
    },
    "duration": 10,
    "usage": {
      "total_tokens": 8565,
      "prompt_tokens": 5650,
      "completion_tokens": 2915
    },
    "ratio": "16:9",
    "task_type": "h3_context_ir",
    "modality": "text"
  }
}</code></pre></td></tr>
    <tr><td>H3-Base</td><td><a href="scripts/readme/full-2k-t2va-h3-base.sh">查看脚本</a></td><td><a href="assets/t2va.mp4">t2va.mp4</a></td></tr>
    <tr><td>H3-Regenerate-2K</td><td><a href="scripts/readme/full-2k-t2va-h3-regenerate-2k.sh">查看脚本</a></td><td><a href="assets/t2va_2k.mp4">t2va_2k.mp4</a></td></tr>
    <tr><td>直接调用开放平台 API 得到的参考 2K 结果</td><td><a href="scripts/readme/full-2k-t2va-reference-2k-result-by-directly-calling-open-platform-api.sh">查看脚本</a></td><td><a href="assets/h3_direct_2k.mp4">h3_direct_2k.mp4</a></td></tr>
    <tr><td>直接调用开放平台 API 得到的参考 768P 结果</td><td><a href="scripts/readme/full-2k-t2va-reference-768p-result-by-directly-calling-open-platform-api.sh">查看脚本</a></td><td><a href="assets/h3_direct_768p.mp4">h3_direct_768p.mp4</a><br></td></tr>
  </tbody>
</table>

#### case-I2VA

- 类型：首帧图生视频
- 时长：8 秒
- 宽高比：自适应

<table>
  <thead>
    <tr><th>阶段</th><th>请求</th><th>结果</th></tr>
  </thead>
  <tbody>
    <tr><td>H3-Context-IR</td><td><a href="scripts/readme/full-2k-i2va-h3-context-ir.sh">查看脚本</a></td><td><pre><code class="language-json">{
  "task": {
    "id": "&lt;task_id&gt;",
    "model": "MiniMax-H3",
    "status": "succeeded",
    "created_at": "&lt;created_at&gt;",
    "updated_at": "&lt;updated_at&gt;",
    "content": {
      "prompt": "For the target video, at 0.00 seconds into the target video, &lt;Picture 1&gt; (from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: [Shot 1] This is a live-action, cinematic shot with a shallow depth of field. The camera holds a perfectly static shot throughout the entire eight-second duration, capturing a cozy family gathering in a traditional Japanese dining room. The scene opens with a large, intricately patterned blue and white ceramic bowl of ramen in the immediate foreground, rendered in crisp, sharp focus. The bowl sits on a smooth, polished long wooden table. Inside the bowl, a rich, oily golden-brown broth surrounds yellow wavy noodles, topped with two thick, round slices of chashu pork featuring visible fat marbling and a distinct spiral meat pattern. A generous mound of freshly chopped, bright green scallions rests in the center, and a crisp, dark green rectangular sheet of nori seaweed is tucked into the right edge. To the left of the bowl, a pair of light brown wooden chopsticks rests horizontally on a small, dark rectangular chopstick rest, near a small cylindrical ceramic teacup with blue painted patterns. On the right side of the table, a spherical paper lantern with a ribbed bamboo frame sits on a black wooden base. In the background, a large family of seven is gathered around the table, initially appearing as a soft, blurred presence. Behind them, traditional Japanese sliding shoji screens with wooden lattice frames are open, revealing a bright outdoor scene with lush green trees. Early in the clip, the thick, white steam rising from the hot ramen broth immediately intensifies, billowing upwards in thick, swirling clouds that dance continuously above the bowl. As the clip progresses into the middle seconds, the camera maintains its static position while the focus begins a deliberate, smooth shift deeper into the room. The foreground ramen bowl, its vibrant ingredients, and the rising steam gradu... [truncated]
    },
    "duration": 8,
    "usage": {
      "total_tokens": 22822,
      "prompt_tokens": 12800,
      "completion_tokens": 10022
    },
    "ratio": "16:9",
    "task_type": "h3_context_ir",
    "modality": "text"
  }
}</code></pre></td></tr>
    <tr><td>H3-Base</td><td><a href="scripts/readme/full-2k-i2va-h3-base.sh">查看脚本</a></td><td><a href="assets/i2va.mp4">i2va.mp4</a></td></tr>
    <tr><td>H3-Regenerate-2K</td><td><a href="scripts/readme/full-2k-i2va-h3-regenerate-2k.sh">查看脚本</a></td><td><a href="assets/i2va_2k.mp4">i2va_2k.mp4</a><br></td></tr>
    <tr><td>直接调用开放平台 API 得到的参考 2K 结果</td><td><a href="scripts/readme/full-2k-i2va-reference-2k-result-by-directly-calling-open-platform-api.sh">查看脚本</a></td><td><a href="assets/i2va_direct_2k.mp4">i2va_direct_2k.mp4</a></td></tr>
    <tr><td>直接调用开放平台 API 得到的参考 768P 结果</td><td><a href="scripts/readme/full-2k-i2va-reference-768p-result-by-directly-calling-open-platform-api.sh">查看脚本</a></td><td><a href="assets/i2va_direct_768p.mp4">i2va_direct_768p.mp4</a></td></tr>
  </tbody>
</table>

#### case-Ref2VA

- 类型：多模态参考生视频（视频 + 音频）
- 时长：5 秒
- 宽高比：自适应

<table>
  <thead>
    <tr><th>阶段</th><th>请求</th><th>结果</th></tr>
  </thead>
  <tbody>
    <tr><td>H3-Context-IR</td><td><a href="scripts/readme/full-2k-ref2va-h3-context-ir.sh">查看脚本</a></td><td><pre><code class="language-json">{
  "task": {
    "id": "&lt;task_id&gt;",
    "model": "MiniMax-H3",
    "status": "succeeded",
    "created_at": "&lt;created_at&gt;",
    "updated_at": "&lt;updated_at&gt;",
    "content": {
      "prompt": "subject_definitions:\n&lt;Subject 1&gt; is the young man with short wavy blonde hair, wearing a bright pink suit jacket, matching pink trousers, an unbuttoned white shirt, and silver rings, holding a small black lamb in his arms in &lt;Video 1&gt;.\n&lt;Video 1&gt; is the source video for the editing task.\n&lt;Audio 1&gt; is the synchronized audio track of &lt;Video 1&gt;, providing the background music.\n&lt;Audio 2&gt; is the voice timbre reference for &lt;Subject 1&gt;'s voice, containing a spoken male voiceover.\n\nsummary:\n[video editing + audio reference + audio reuse] The target video is an edited version of &lt;Video 1&gt;. &lt;Subject 1&gt;, wearing a bright pink suit and holding a black lamb, stands in a grassy field with other white lambs in the background. The edit animates &lt;Subject 1&gt;'s face to speak the user-provided dialogue. &lt;Audio 1&gt; is partially reused as the continuous background music, while the target references the calm male voice timbre of &lt;Audio 2&gt; for &lt;Subject 1&gt;'s spoken lines.\n\nretention_analysis:\n&lt;Subject 1&gt; (appears in [Shot 1]): fully_preserved - the man retains his identity, wavy blonde hair, pink suit, white shirt, accessories, and the black lamb he holds, with his mouth newly animated to speak.\n&lt;Video 1&gt; (source video editing): fully_preserved - the original camera framing, warm golden hour lighting, grassy hill setting, and background white lambs are maintained while the central character is edited.\n&lt;Audio 1&gt;: partially_copy - the atmospheric background music from &lt;Audio 1&gt; is reused in the target video, mixed beneath the newly added spoken dialogue.\n&lt;Audio 2&gt;: reference - the target audio references the male voice timbre from &lt;Audio 2&gt; to generate &lt;Subject 1&gt;'s spoken dialogue.\n\ndetailed_description:\nThe target video is in realistic photographic style.\n[Shot 1] The shot begins from the source &lt;Video 1&gt;... [truncated]
    },
    "duration": 5,
    "usage": {
      "total_tokens": 39299,
      "prompt_tokens": 33323,
      "completion_tokens": 5976
    },
    "ratio": "16:9",
    "task_type": "h3_context_ir",
    "modality": "text"
  }
}</code></pre></td></tr>
    <tr><td>H3-Base</td><td><a href="scripts/readme/full-2k-ref2va-h3-base.sh">查看脚本</a></td><td><a href="assets/r2va.mp4">r2va.mp4</a><br></td></tr>
    <tr><td>直接调用开放平台 API 得到的参考 2K 结果</td><td><a href="scripts/readme/full-2k-ref2va-reference-2k-result-by-directly-calling-open-platform-api.sh">查看脚本</a></td><td><a href="assets/r2va_2k.mp4">r2va_2k.mp4</a></td></tr>
    <tr><td>开放平台中供参考的 H3 API 2K 结果</td><td><a href="scripts/readme/full-2k-ref2va-h3-api-2k-in-open-platform-for-reference.sh">查看脚本</a></td><td><a href="assets/r2va_direct_2k.mp4">r2va_direct_2k.mp4</a><br></td></tr>
    <tr><td>直接调用开放平台 API 得到的参考 768P 结果</td><td><a href="scripts/readme/full-2k-ref2va-reference-768p-result-by-directly-calling-open-platform-api.sh">查看脚本</a></td><td><a href="assets/r2va_direct_768p.mp4">r2va_direct_768p.mp4</a><br></td></tr>
  </tbody>
</table>

### 提示词指引

来自 HuggingFace 发布的提示词指引文档未复制进本仓库，以保持 markdown 布局简洁。

## 许可证

MiniMax H3 依据 [MiniMax H3 社区许可协议](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE) 发布。

## 联系我们

联系我们： [model@minimax.io](mailto:model@minimax.io)。

---

# 附录：社区部署参考（融合自零度解说等第三方教程，已剔除越狱/审核绕过内容）

> **合规说明**：以下内容整理自第三方社区教程（如"零度解说"等）中**可公开讨论的技术事实**，用于帮助理解模型构成与本地部署思路。已**剔除**其中的"无审查/越狱版"下载链接、绕过内容审核的说明，以及不当的提示词示例。
>
> **重要**：MiniMax 官方开源仓库分发的是 **BF16 精度权重**，并内置**安全护栏**（用户输入文本/图像/视频及增强提示词均经过自动化审核）。社区对权重进行 INT8 / NVFP4 等量化、或以 4 步加速、或从第三方获取修改版权重，**不改变模型能力本质，但可能绕过官方安全审核**——请务必遵守《MiniMax H3 社区许可协议》与所在地法律法规，仅用于合规创作。

## A. 21G 体积由什么构成

社区常提到的"21G 包"通常包含 H3 本地运行所需的三大类文件：

| 组件 | 作用 | 说明 |
|---|---|---|
| 主扩散模型（diffusion_models） | 核心生成网络，负责把条件（文本/图/参考）映射到视频-音频潜变量 | 官方原生为 BF16；社区"加速版"多为 INT8 量化（如 `turbo-int8-convrot`）以压缩体积、降低显存 |
| VAE 自编码器（vae） | 视觉潜变量 ↔ 像素帧 的解码/编码 | 与官方 VisualVAE 对应，负责把潜变量还原成视频画面 |
| 文本编码器（text_encoders） | 把提示词文本编码为 H3 可理解的向量 | 基于 **Qwen3-VL-32B**，能力最强但最占显存；社区常用 NVFP4（4-bit）量化版把它压到约 16G 左右 |

要点：
- **文本编码器是显存大户**：Qwen3-VL-32B 即使量化也需约 16G 显存。主扩散模型 INT8 量化后约 8G，二者叠加才能跑通，所以"8G 显存可跑"的说法成立的前提是——**文本编码器也做了 NVFP4 之类的低比特量化**，否则单靠 8G 装不下完整管线。
- 官方仓库（HF `MiniMaxAI/MiniMax-H3`）本身只提供 BF16 权重 + 部署指引，**并不承诺 8G 显存**；"8G 能跑"是社区把官方权重量化、并配合分层显存卸载实现的。

## B. ComfyUI 本地部署目录结构（社区通用做法）

最新版 ComfyUI 已内置 MiniMax H3 的文生视频 / 图生视频节点，部署要点如下（路径以 Windows 默认安装为例）：

```text
ComfyUI-Shared/
└── models/
    ├── diffusion_models/   ← 放入主扩散模型（如 *.safetensors / 量化版）
    ├── vae/                ← 放入 VAE 自编码器
    └── text_encoders/      ← 放入文本编码器（Qwen3-VL-32B 或其量化版）
```

工作流（workflow）JSON 文件则在 ComfyUI 中直接"加载"使用。官方 Comfy 教程与 T2V/R2V 模板见正文"本地部署 H3-Base"章节的链接。

## C. 工作流类型速查（社区加速版常见命名）

社区发布的加速工作流通常按"任务类型 + 步数"命名，常见 5 类（去掉越狱模型依赖、仅保留用途说明）：

| 工作流 | 用途 | 说明 |
|---|---|---|
| `01_reference_4step_sla` | 文本 → 视频（4 步加速） | 最常用，直接由提示词生成视频 |
| `02_derope_4plus4_sla` | 去除视频运动抖动/拖影 | 后处理，提升画面稳定性 |
| `03_derope_dyrope…` | 更高级的运动修复 | 进阶版运动修正 |
| `04_i2v_fl2v_4step_sla` | 图片 → 视频 | 图生视频，需提供首帧/关键帧图像 |
| `05_ref2va_4step_sla` | 参考图 → 视频 | 多参考生视频，对应官方的 Ref2VA |

> 官方原生工作流以 API / SGLang 为主（见正文）；上述带 `4step` 的是社区把去噪步数压缩到 4 步的加速变体。

## D. 实测生成速度参考（社区 RTX 4090 数据）

下表为社区在 **RTX 4090（24G）** 上的实测，供估算硬件需求（Kaggle 等云平台的 GPU 算力/显存不同，实际耗时会有差异）：

| 分辨率 | 条件 | 单条约耗时 |
|---|---|---|
| 864×480（480P） | pruned fp8 + SageAttention + EasyCache | 4–5 分钟 |
| 1280×736（720P） | pruned fp8 | 14–15 分钟 |
| 1280×736（720P） | bf16 + 8 步 | ~10 分钟（20 步约 22 分钟） |

换算到 Kaggle（详见此前可行性分析）：T4×2（32G 显存）跑 480P 约 5–10 分钟/条、720P 约 15–25 分钟/条；P100（16G）因显存不足文本编码器而易 OOM，不推荐。

## E. 提示词写法要点（合规创作）

- **结构化描述**：把"镜头语言、人物/物体外观、动作时序（按 0–N 秒分段）、环境动态、声音、限制项"分块写清，质量远高于一句话。
- **时序分段**：例如"0–2 秒：…；2–5 秒：…"，让模型理解镜头推进与动作节奏。
- **限制项（negative 思路）**：明确写出"不要……"（如不要面部漂移、不要肢体畸形、不要比例变化），可显著减少常见瑕疵。
- 官方还提供 `h3-prompt-writing` 技能与 `base-en.txt` / `ref-en.txt` 两份指南（见正文"提示词撰写技巧"），建议优先参考官方写法。

## F. Kaggle 云端部署方案

本地没有大显存显卡时，Kaggle Notebook 的免费 GPU 是成本最低的试跑途径。核心结论：**能跑通，`/kaggle/working` 的 20G 限制不是障碍**。

### F.1 为什么 20G 不是障碍（存储机制）

Kaggle 的磁盘配额是**分区独立**的，关键在于模型根本不进 `working`：

| 路径 | 配额 | 用途 | 占 20G 吗 |
|---|---|---|---|
| `/kaggle/input` | 独立（Dataset/Model 配额，私有约 200G+） | **只读挂载**模型权重 | ❌ 不占 |
| `/kaggle/working` | **20G** | 代码、依赖、生成的视频 | ✅ 占 |
| `/kaggle/temp` | 较大 | 临时中转 | ❌ 不计入 |

模型作为 Private Dataset 挂在 `/kaggle/input` 后，ComfyUI / diffusers 通过 **mmap 直接读取**，全程不需要把 21G 复制进 `working`。`working` 里只放几百 MB 的代码与依赖，加上生成的视频（单条 10 秒 768p 通常几十 MB），远低于 20G。

### F.2 GPU 选型（决定能否跑起来）

| 加速器 | 显存 | 算力 | 结论 |
|---|---|---|---|
| **T4 ×2** | 16G + 16G（合计 32G） | ~65 TFLOPS/卡（FP16，有 Tensor Core） | ✅ **推荐**，唯一稳妥选项 |
| P100 | 16G | ~18 TFLOPS（无 Tensor Core） | ❌ 不推荐，显存不够且算力低，极易 OOM |

> **显存是硬门槛**：4090 跑 10 秒 720P 实测约需 44G 显存（含 Qwen3-VL-32B 文本编码器）。Kaggle 最高只有 32G，因此**必须使用量化权重**——主扩散模型用 INT8（约 8G）+ 文本编码器用 NVFP4（约 16G），才能塞进 32G。官方原生 BF16 权重在 Kaggle 上跑不动完整管线。

### F.3 操作步骤

**① 上传模型到 Private Dataset**

Kaggle → Datasets → New Dataset，按组件上传，文件名保持原样（ComfyUI 按路径查找）：

```text
minimax-h3/
├── diffusion_models/   ← 主扩散模型（INT8 量化版，如 turbo-int8-convrot）
├── vae/                ← VAE 自编码器
└── text_encoders/      ← 文本编码器（Qwen3-VL-32B NVFP4 量化版）
```

> ⚠️ Kaggle Dataset **单文件上限约 50G**。21G 总量没问题；若某个权重文件超限，需先 `split` 分片再传，加载时 `cat` 合并。

**② 创建 Notebook 并挂载**

新建 Notebook → 右侧 *Add Data* 选择刚建的 Private Dataset → 打开 **Internet** 与 **Accelerator：GPU T4 ×2**。

```python
import os
for root, dirs, files in os.walk('/kaggle/input'):
    if files:
        print(root, '->', files[:3])
```

**③ 安装运行环境**

Kaggle 预装了 torch/transformers，但**没有 ComfyUI**，需自行安装（约 10–20 分钟）：

```bash
!git clone https://github.com/Comfy-Org/ComfyUI.git /kaggle/working/ComfyUI
%cd /kaggle/working/ComfyUI
!pip install -q -r requirements.txt
# 可选加速：SageAttention
!pip install -q sageattention
```

> 💡 **省时技巧**：第一次装好后，把 `site-packages` 打包成第二个 Dataset，下次直接本地安装，可省约 15 分钟。

**④ 把模型软链到 ComfyUI**

不要复制 21G，用软链（或在 `extra_model_paths.yaml` 中直接指向 input 路径）：

```bash
!mkdir -p /kaggle/working/ComfyUI/models
!ln -s /kaggle/input/minimax-h3/diffusion_models /kaggle/working/ComfyUI/models/diffusion_models
!ln -s /kaggle/input/minimax-h3/vae            /kaggle/working/ComfyUI/models/vae
!ln -s /kaggle/input/minimax-h3/text_encoders  /kaggle/working/ComfyUI/models/text_encoders
```

**⑤ 启动并生成**

```bash
!cd /kaggle/working/ComfyUI && nohup python main.py --listen 0.0.0.0 --port 8188 > comfy.log 2>&1 &
```

在 ComfyUI 中加载工作流（官方 T2V / R2V 模板，或社区 4 步加速版），生成结果默认落在 `ComfyUI/output/`，即 `/kaggle/working/` 下，**Commit 后可在 Output 面板直接下载**。

### F.4 耗时与产能预估

| 项目 | T4 ×2 预估 |
|---|---|
| 首条额外开销（模型加载 + 量化 + CUDA warmup，一次性） | 3–6 分钟 |
| 480P（864×480）单条 10 秒视频 | 5–10 分钟 |
| 720P（1280×736）单条 10 秒视频 | 15–25 分钟（开 SageAttention + EasyCache 可压到 ~15 分钟） |

**产能账**：免费 GPU **30 小时/周**、单次会话最长 **9 小时**。按 15 分钟/条（含环境重建）估算，一周约可产出 **30–40 条** 10 秒视频。

### F.5 常见坑与对策

| 坑 | 对策 |
|---|---|
| **OOM（显存爆掉）** | 换 T4×2；必须用 INT8 主模型 + NVFP4 文本编码器；降到 480P；启用分层卸载 |
| **ComfyUI 每次重启都要重装** | 把装好的依赖打包成 Dataset 复用（见 ③） |
| **交互式会话 20 分钟无操作被断** | 长时间生成改用 **Save & Run All（Commit）** 后台跑，输出落 `/kaggle/working` 后下载 |
| **CUDA 版本不匹配** | Kaggle 为 CUDA 12.x，装 torch 选 `cu121` 及以上，**勿装 cu118** |
| **忘记开 Internet** | 装依赖必须开联网；挂载 Dataset 本身不需要联网 |
| **单文件超 50G 上限** | 先 `split` 分片上传，Notebook 里 `cat` 合并到 `/kaggle/working` 再加载 |

> 若坚持用**官方原版 BF16 权重**配合 SGLang / diffusers 部署，显存需求远高于 32G，Kaggle 免费档基本不可行，需改用付费 GPU（如 A100 80G）或本地多卡。

> 再次提醒：请只用于合规、正当的内容创作，遵守 MiniMax H3 社区许可协议与相关法律。
