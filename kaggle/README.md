# MiniMax-H3 × Kaggle 免费显卡部署实录（Gradio 交互面板）

> **状态：已跑通 ✅**（2026-09-09，Kaggle T4×2 实测）
> 两种形态都已验证：
> ① **全自动出片**（headless）：一条命令提交，42 分钟端到端出片，无需人工干预；
> ② **Gradio 交互面板**：上传素材 → 写提示词 → 调参数 → 在线生成 → 自行下载，可连续使用整个会话。
>
> 本文档是**实测记录**，与主 README 附录 F（理论方案）的不同之处：所有数字来自真实运行，并修正了附录 F 的两处误差（见[第 2.1 节](#21-对附录-f-的修正)）。

---

## 1. 成果一览

| 项目 | 实测值 |
|---|---|
| 平台 | Kaggle Notebook（免费 GPU 配额 30 小时/周） |
| 显卡 | **2 × Tesla T4**（各 15360 MiB，sm_75） |
| 端到端耗时（首次） | **42 分钟**（装环境 10min + 下权重 6min + 初始化 4min + 采样 30min） |
| 后续生成耗时 | 见[第 5 节参数表](#5-参数与耗时对照表)，最快 ≈8 分钟/条 |
| 首条成片 | 832×480、124 帧、24fps、5.17 秒，**H.264 + AAC 音轨**（音视频联合生成） |
| 权重总量 | **39.55 GiB**（Comfy-Org 官方公开仓库，无需 HF token） |
| 单会话时长 | 最长 9~12 小时（面板模式可连续生成多条） |

## 2. 核心思路

### 2.1 对附录 F 的修正

1. **"21G 就能跑" 是误读** —— 21GB 只是主扩散模型一个文件。完整 T2V 最小组合是四件：
   主模型 19.53 GiB + 文本编码器 14.61 GiB + 视频 VAE 4.85 GiB + 音频 VAE 0.6 GiB ≈ **39.55 GiB**。
   好消息是 Kaggle 根分区有 **1.1 TB** 空闲、HF 下载实测 **135 MB/s**，39.55 GiB 只要约 6 分钟，存储从来不是障碍。
2. **"BF16 全管线 44G+ 跑不动" 的结论对，但路径错了** —— 不需要自己量化，Comfy-Org 官方仓库已提供量化版，直接下载即可。

### 2.2 技术路线（四层）

```
┌─ 第 1 层：量化权重（Comfy-Org/MiniMax-H3，公开、免 token）
│    minimax_h3_fl2va_pruned_int8_convrot.safetensors   19.53 GiB  主扩散模型 INT8
│    qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors       14.61 GiB  文本编码器 NVFP4-AWQ
│    minimax_h3_video_vae_fp16.safetensors               4.85 GiB  视频 VAE FP16
│    minimax_h3_audio_vae_fp32.safetensors               0.60 GiB  音频 VAE FP32
├─ 第 2 层：ComfyUI v0.30.1（原生支持 H3 节点）+ torch 升级 cu130
│    Kaggle 驱动 580.159.04 ≥ 580，可升 cu130 —— 这是"30 分钟"和"1.5 小时+"
│    的分水岭：不升级时 INT8 走反量化慢速路径，5 秒视频要 1.5~3.5 小时。
├─ 第 3 层：双卡分工自定义节点（t4x2_dual_encoder）
│    文本编码器(14.6G) 固定到 GPU:1，主扩散模型(19.5G) 留在 GPU:0，
│    VAE 解码在 GPU:1 —— 单卡 16G 装不下的组合，拆到两张卡后全程无 OOM。
└─ 第 4 层：两种使用形态
     A. headless：notebook 内直接提交 workflow JSON，跑完存 /kaggle/working
     B. Gradio 面板：Web UI + cloudflared 公网隧道，人在浏览器里操作
```

ComfyUI 启动参数用 `--lowvram --reserve-vram 0.8`，模型常驻约 21.6 GB（跨双卡），实测零 OOM。

### 2.3 为什么必须 T4×2（而不是 P100）

| | T4 ×2 | P100 ×1（Kaggle 默认可能给的） |
|---|---|---|
| 架构 | Turing sm_75 | Pascal sm_60 |
| torch 2.10 支持 | ✅ | ❌ 连基础算子都不支持 |
| INT8/FP8 快速内核 | ✅（Tensor Core） | ❌ 只能反量化 → 显存回到 66GB+ |
| FP16 算力 | ~65 TFLOPS | ~19 TFLOPS |

> 2026-09-15 起 Kaggle 官方已将 P100 退役、默认切到 T4×2，此后无需关心此项。

## 3. 本目录文件清单

| 文件 | 用途 |
|---|---|
| [`gen_ui.py`](gen_ui.py) | **生成 Gradio 面板版 notebook** 的脚本：`python gen_ui.py` 产出 `h3-ui/`（notebook + 元数据），kaggle CLI 推送即得交互面板 |
| [`gen_run.py`](gen_run.py) | 生成 headless 全自动出片版 notebook（改顶部 `IMAGE_URL`/`PROMPT` 即可换素材与提示词） |
| [`h3-ui.ipynb`](h3-ui.ipynb) | 面板版 notebook 成品（与 gen_ui.py 产出一致，官方编码器） |
| [`h3-ui-her.ipynb`](h3-ui-her.ipynb) | 面板版 notebook · **Heretic 编码器变体**（文本编码器换社区 Heretic 版，其余相同） |
| [`t4x2_dual_encoder.py`](t4x2_dual_encoder.py) | 双卡分工自定义节点源码（已内嵌于上述 notebook 的 cell 中，此处单独存放便于阅读/修改） |
| [`KAGGLE_NOTEBOOK_GUIDE.md`](KAGGLE_NOTEBOOK_GUIDE.md) | 写进 Kaggle notebook 顶部的 markdown 引导页（面板用法/排障/优化） |

## 4. 从零到出片：操作步骤

### 4.1 前置条件

- Kaggle 账号（免费），手机验证后每周 30 小时 GPU 配额
- 本机装 kaggle CLI：`pip install kaggle`，并把 API Token 放到 `~/.kaggle/kaggle.json`

### 4.2 拿到 notebook（二选一）

- **A. 用本项目脚本生成**：
  ```bash
  python gen_ui.py                       # 产出 h3-ui/h3-ui.ipynb + kernel-metadata.json
  kaggle kernels push -p h3-ui --accelerator NvidiaTeslaT4
  ```
- **B. 在 Kaggle 网页直接复制**：打开 `kaggle.com/code/xwdfyx/h3-ui` → Copy & Edit，检查加速器为 GPU T4 x2 后 Run All。

### 4.3 ⚠️ 最关键的一步：加速器参数必须大写 N

`kernel-metadata.json` 里写 `"accelerator": "NvidiaTeslaT4"`。

- 小写 `nvidiaTeslaT4` **会被服务端静默忽略**并回退 P100（不报错！），torch 直接不兼容；
- 验收方法：`kaggle kernels pull <user>/<slug> -m`，看元数据里 `machine_shape`：
  - `"NvidiaTeslaT4"` → 正确拿到 2×T4
  - `"Gpu"` → 被回退了（P100/单卡），检查拼写
- 网页操作的话：Settings → Accelerator → **GPU T4 x2** → Save。

### 4.4 运行与进入面板

1. Run All（或 API 推送自动运行），等待 15~20 分钟（环境安装 + 权重下载 + ComfyUI 启动）；
2. 打开 notebook 日志，找到 cloudflared 输出的公网地址：
   `https://xxxx-xxxx-xxxx.trycloudflare.com`（每次会话地址都不同）；
3. 浏览器打开即进入面板。会话最长 9~12 小时，期间地址持续有效，关掉笔记本页面不影响。

### 4.5 面板操作

1. **① 上传素材**：支持本地上传 / 剪贴板粘贴 / 摄像头，图片即视频首帧；
2. **② 写提示词**：主体 + 动作 + 镜头语言；可在附加栏补约束（如 "no blurry face"）；默认自动追加音频描述（可关）；
3. **③ 调参数**：时长（3/5/8/10 秒）、清晰度档位、横屏/竖屏/方形、步数、Turbo LoRA 开关、种子；
   实时显示计算后的实际分辨率和预计耗时；
4. 点**生成**，进度条走完自动预览，成品区可在线播放并**直接下载**（mp4 含音轨）；
5. 历史列表保留本次会话全部成片，会话结束前记得下载（`/kaggle/working` 会随会话销毁）。

## 5. 参数与耗时对照表

实测标定（T4×2 + cu130 + Turbo LoRA 8 步）：**每步耗时 ≈ 228s × (宽×高×帧数)/(832×480×124)**。
帧数按 H3 约束对齐（`帧数 % 17 == 5`），24fps。

| 比例 | 清晰度 | 实际分辨率 | 5秒(8步) | 10秒(8步) | 5秒(4步) |
|---|---|---|---|---|---|
| 横屏 16:9 | 流畅 0.21MP | 608×352 | ≈16 分钟 | ≈32 分钟 | ≈8 分钟 |
| 横屏 16:9 | 推荐 0.40MP | 832×480 | ≈30 分钟 | ≈60 分钟 | ≈15 分钟 |
| 横屏 16:9 | 高清 0.59MP | 1024×576 | ≈45 分钟 | ≈88 分钟 | ≈22 分钟 |
| 竖屏 9:16 | 流畅 0.21MP | 352×608 | ≈16 分钟 | ≈32 分钟 | ≈8 分钟 |
| 竖屏 9:16 | 推荐 0.40MP | 480×832 | ≈30 分钟 | ≈60 分钟 | ≈15 分钟 |
| 竖屏 9:16 | 高清 0.59MP | 576×1024 | ≈45 分钟 | ≈88 分钟 | ≈22 分钟 |
| 方形 1:1 | 流畅 0.21MP | 448×448 | ≈15 分钟 | ≈30 分钟 | ≈8 分钟 |
| 方形 1:1 | 推荐 0.40MP | 640×640 | ≈31 分钟 | ≈61 分钟 | ≈16 分钟 |
| 方形 1:1 | 高清 0.59MP | 768×768 | ≈45 分钟 | ≈88 分钟 | ≈22 分钟 |

首次运行另加一次性成本 ≈20 分钟（装环境 + 下权重）。

## 6. 已踩过的坑（都是实测撞出来的）

| # | 现象 | 根因 | 解法 |
|---|---|---|---|
| 1 | 指定 T4 却分到 P100 | 元数据写成小写 `nvidiaTeslaT4`，服务端**静默**回退 | 大写 `NvidiaTeslaT4`；用 `kernels pull -m` 验收 `machine_shape` |
| 2 | 推送报 409 "title does not resolve to id" | 标题被 slugify（`MiniMax H3 Run`→`mini-max-…`）与 id 不符 | 标题与 id 保持一致的全小写 |
| 3 | torch 不兼容/量化内核缺失 | P100(sm_60) + 默认 torch cu128 | 必须 T4；升 torch cu130（驱动 ≥580 即可） |
| 4 | 探测日志显示"跑完了"其实没有 | Kaggle 的 `kernels output` **只在会话结束后**给日志 | 运行中看日志用 `GetKernelSessionLogsStream` SSE 流接口 |
| 5 | 采样巨慢（小时级） | 未升 cu130，INT8 走反量化慢路径 | pip 装 cu130 轮子（本仓库 notebook 已内置该步骤） |

## 7. 文本编码器可替换（官方 / Heretic 变体）

CLIPLoader 的类型始终是 `minimax`，换编码器只是换 `text_encoders/` 下的文件名：

| 编码器 | 仓库 | 体积 | 说明 |
|---|---|---|---|
| 官方 NVFP4-AWQ | Comfy-Org/MiniMax-H3 `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | 14.61 GiB | 默认 |
| **Heretic NVFP4** | Momoking/Qwen3-VL-32B-Heretic-MiniMax-H3-NVFP4 `qwen3vl_32b_heretic_minimax_h3_nvfp4.safetensors` | 14.61 GiB | 社区变体，与官方同规格 drop-in 替换，作者实测峰值显存 ~9.9 GB |

- **Kaggle**：`h3-ui-her.ipynb` 已内置 Heretic（下载清单走 `REPO_OVERRIDES` 指到 Momoking 仓库，工作流 `TE` 常量指向 heretic 文件名）；换回官方版只需把 SIZES 里 `text_encoders` 行与 `TE` 常量改回官方文件名。
- **本地 ComfyUI**：把 safetensors 放进 `text_encoders` 模型目录，CLIPLoader 选中该文件、类型 `minimax` 即可。
- 请遵循模型许可与当地法律法规合规创作。

## 8. 进一步优化的方向

1. **步数是线性杠杆**：Turbo LoRA 下 8 步已够看；赶时间 4 步直接减半（画质略降）。
2. **分辨率档位**：0.21MP（608×352）速度最快，适合试提示词；定稿再上 0.59MP。
3. **更小主模型**：Kijai/MiniMax-H3-experimental 有 **w4a8 版主模型仅 12.54 GB**（比现用小 40%），OOM 时或想留更多显存给高分辨率时可换。
4. **配额管理**：30 小时/周 ≈ 面板会话 2~3 个；面板空转也计时，不用时 Stop 会话；每次生成前先想好提示词，避免占着会话试错。
5. **改提示词风格**：参考本仓库 `skills/h3-prompt-writing` 的写法要点（主体/动作/镜头/音频四段式）。

## 9. FAQ

**Q: 生成时能断网/关电脑吗？**
A: headless 模式可以（云端独立跑）；面板模式会话也不受你本机影响，但成片要趁会话内下载。

**Q: 为什么每次公网地址都不一样？**
A: trycloudflare.com 是临时隧道，绑定会话生命周期。想固定域名可换成自己的 Cloudflare Tunnel token（改 notebook 里 cloudflared 启动参数）。

**Q: 480P 是上限吗？**
A: 不是。这套量化组合在 0.59MP（1024×576）下稳定；再往上受 T4 显存与耗时限制，不推荐。官方 2K 直出需要 44G+ 显存，Kaggle 免费卡跑不动。

**Q: 音频是合成的还是配的？**
A: H3 音视频联合生成，音轨由音频 VAE 从同一次采样解码而来，与画面同步。

**Q: 能商用吗？**
A: 遵循主 README 的许可证与合规要求；提示词创作须合规（本仓库已剔除越狱/审核绕过内容）。
