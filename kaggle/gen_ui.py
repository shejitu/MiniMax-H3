# -*- coding: utf-8 -*-
"""生成 Kaggle 交互式 MiniMax-H3 面板 notebook。

与 gen_run.py（headless 一次性出片）的区别：
  ComfyUI 后端常驻 + Gradio 前端面板，用户自己上传素材、写提示词、下载成品。

注意：本文件内的 r'''...''' 字符串是"写进 notebook 的源码"，
      因此这些源码里绝对不能出现 ''' 序列。
"""
import base64
import json
import pathlib

OUT = pathlib.Path(r"E:\我的workbuddy\kaggle跑H3视频\h3-ui")
OUT.mkdir(parents=True, exist_ok=True)

C = []


def add(src):
    C.append(src.strip("\n"))


# ───────────────────────── Cell 1: 配置 + 环境体检 ─────────────────────────
add(r'''
# ══════════ 配置 ══════════
UI_PORT     = 7860     # Gradio 面板端口
MAX_HOURS   = 8.5      # 面板最长保活时间（Kaggle 单会话上限 ~9h）
JOB_TIMEOUT = 5 * 3600 # 单次生成超时

import os, shutil, subprocess, sys, time
from pathlib import Path
import torch

ON_KAGGLE  = Path("/kaggle").exists()
WORK_ROOT  = Path("/kaggle/temp/h3") if ON_KAGGLE else Path("./h3").resolve()
COMFY_HOME = WORK_ROOT / "ComfyUI"
CACHE_HOME = WORK_ROOT / "hf_cache"
GEN_DIR    = WORK_ROOT / "gen"        # ComfyUI 原始输出
TMP_DIR    = WORK_ROOT / "tmp"
FINAL_DIR  = Path("/kaggle/working") if ON_KAGGLE else WORK_ROOT / "dist"
OUT_DIR    = FINAL_DIR / "videos"     # 用户下载目录（Kaggle Output 面板也能看到）
UP_DIR     = FINAL_DIR / "uploads"    # 用户上传的素材
LOG_FILE   = FINAL_DIR / "comfy.log"
CF_LOG     = FINAL_DIR / "cf.log"
for d in (WORK_ROOT, CACHE_HOME, GEN_DIR, TMP_DIR, FINAL_DIR, OUT_DIR, UP_DIR):
    d.mkdir(parents=True, exist_ok=True)

def to_gib(n): return n / 1024 ** 3
def sh(c, cwd=None):
    return subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True)

print("Python", sys.version.split()[0], "| torch", torch.__version__)
print(sh("nvidia-smi --query-gpu=index,name,memory.total,compute_cap --format=csv").stdout)

if not torch.cuda.is_available():
    raise RuntimeError("没有可用 GPU：请在 Settings → Accelerator 选择 GPU T4 x2。")
NAMES = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
print("GPU:", NAMES, "| 数量", torch.cuda.device_count())
BAD = False
for i in range(torch.cuda.device_count()):
    p = torch.cuda.get_device_properties(i)
    if (p.major, p.minor) < (7, 0):
        print(f"!! GPU{i} {p.name} compute capability {p.major}.{p.minor} 过低："
              f"当前 PyTorch 要求 sm_70+，H3 的 INT8/FP8 量化内核需要 sm_75+。")
        BAD = True
if torch.cuda.device_count() < 2:
    print("!! 只有 1 张卡：显存减半，OOM 风险很高，建议切到 GPU T4 x2。")
if BAD:
    raise RuntimeError(
        "当前分配到的 GPU 架构过旧（很可能是 P100 / sm_60），MiniMax H3 无法运行。\n"
        "请在 Kaggle 网页：Settings → Accelerator → 选 GPU T4 x2 → Save，再重新 Run All。")

import psutil
print(f"内存 {to_gib(psutil.virtual_memory().total):.1f} GiB | 磁盘剩余 {to_gib(shutil.disk_usage(WORK_ROOT).free):.1f} GiB")
''')

# ───────────────────────── Cell 2: 安装 ComfyUI + cu130 + Gradio ─────────────────────────
add(r'''
import subprocess, sys
from pathlib import Path

def sh_live(cmd, cwd=None):
    print("$", cmd if isinstance(cmd, str) else " ".join(map(str, cmd)), flush=True)
    r = subprocess.run(cmd, shell=isinstance(cmd, str), cwd=cwd, capture_output=True, text=True)
    if r.stdout: print(r.stdout[-2500:])
    if r.returncode != 0 and r.stderr: print("ERR:", r.stderr[-1500:])
    return r

COMFY_TAG = "v0.30.1"
if not (COMFY_HOME / ".git").exists():
    r = sh_live(["git", "clone", "--depth", "1", "--branch", COMFY_TAG,
                 "https://github.com/comfyanonymous/ComfyUI.git", str(COMFY_HOME)])
    if r.returncode != 0:
        print("稳定版拉取失败，退回 master")
        sh_live(["git", "clone", "--depth", "1",
                 "https://github.com/comfyanonymous/ComfyUI.git", str(COMFY_HOME)])
else:
    print("ComfyUI 已存在，跳过克隆")

sh_live([sys.executable, "-m", "pip", "install", "-q", "-r", str(COMFY_HOME / "requirements.txt")])
sh_live([sys.executable, "-m", "pip", "install", "-q", "-U",
         "huggingface_hub", "requests", "psutil", "websocket-client", "gradio", "pillow"])
subprocess.run([sys.executable, "-m", "pip", "cache", "purge"], check=False)
print("ComfyUI commit:", subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
      cwd=COMFY_HOME, text=True).strip())

# ── 升级 torch 到 cu130：启用 ComfyUI 快速量化内核（不升级则 5 秒视频要 1.5~3.5 小时）──
def driver_ok():
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
                             capture_output=True, text=True, timeout=30).stdout.strip().splitlines()
        return int(out[0].split(".")[0]) >= 580 if out else False
    except Exception:
        return False

def torch_ver():
    r = subprocess.run([sys.executable, "-c",
        "import torch;print(f'{torch.__version__}|{torch.version.cuda}')"],
        capture_output=True, text=True, timeout=90)
    if r.returncode == 0 and "|" in r.stdout:
        v, c = r.stdout.strip().split("|"); return v, c
    return "?", "?"

print("驱动 >=580 ?", driver_ok())
NEW_CUDA = "?"
if driver_ok():
    v, c = torch_ver()
    if c.startswith("13."):
        print(f"✔ torch 已是 cu130（{v} | {c}）")
        NEW_CUDA = c
    else:
        print(f"升级 torch -> cu130（当前 {v} | {c}）…")
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y",
                        "torch", "torchvision", "torchaudio"], capture_output=True, timeout=180)
        sh_live([sys.executable, "-m", "pip", "install", "-q", "--no-cache-dir",
                 "--index-url", "https://download.pytorch.org/whl/cu130",
                 "torch", "torchvision", "torchaudio"])
        _, NEW_CUDA = torch_ver()
        print("升级后:", NEW_CUDA)
    if NEW_CUDA.startswith("13."):
        sh_live([sys.executable, "-m", "pip", "install", "--force-reinstall",
                 "--no-cache-dir", "comfy-kitchen"])
else:
    print("驱动 <580，跳过 cu130 升级（速度会明显变慢）")
''')

# ───────────────────────── Cell 3: 双卡自定义节点 ─────────────────────────
NODE_PY = r'''
"""Kaggle T4x2 专用：把文本编码器 / VAE 显式加载到指定显卡。"""

import torch
import folder_paths
import comfy.sd
import comfy.utils


def _devices():
    return [f"cuda:{i}" for i in range(torch.cuda.device_count())] + ["cpu"]


class DualT4TextEncoder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip_name": (folder_paths.get_filename_list("text_encoders"),),
                "load_to": (_devices(),),
            }
        }

    RETURN_TYPES = ("CLIP",)
    FUNCTION = "load"
    CATEGORY = "loaders"

    def load(self, clip_name, load_to):
        ct = getattr(comfy.sd.CLIPType, "MINIMAX", None)
        if ct is None:
            raise RuntimeError("ComfyUI 版本过旧：MiniMax H3 需要 v0.30.0 及以上。")
        path = folder_paths.get_full_path_or_raise("text_encoders", clip_name)
        clip = comfy.sd.load_clip(
            ckpt_paths=[path],
            embedding_directory=folder_paths.get_folder_paths("embeddings"),
            clip_type=ct,
            model_options={
                "load_device": torch.device(load_to),
                "offload_device": torch.device("cpu"),
            },
        )
        return (clip,)


class DualT4VAELoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "vae_name": (folder_paths.get_filename_list("vae"),),
                "load_to": (_devices(),),
            }
        }

    RETURN_TYPES = ("VAE",)
    FUNCTION = "load"
    CATEGORY = "loaders"

    def load(self, vae_name, load_to):
        path = folder_paths.get_full_path_or_raise("vae", vae_name)
        sd = comfy.utils.load_torch_file(path)
        return (comfy.sd.VAE(sd=sd, device=torch.device(load_to)),)


NODE_CLASS_MAPPINGS = {
    "DualT4TextEncoder": DualT4TextEncoder,
    "DualT4VAELoader": DualT4VAELoader,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "DualT4TextEncoder": "Dual-T4 Text Encoder (Kaggle)",
    "DualT4VAELoader": "Dual-T4 VAE Loader (Kaggle)",
}
'''
_NODE_B64 = base64.b64encode(NODE_PY.encode("utf-8")).decode("ascii")
add('''
import base64
NODE_DIR = COMFY_HOME / "custom_nodes" / "t4x2_dual_encoder"
NODE_DIR.mkdir(parents=True, exist_ok=True)
NODE_SRC = base64.b64decode("''' + _NODE_B64 + '''").decode("utf-8")
(NODE_DIR / "__init__.py").write_text(NODE_SRC, encoding="utf-8")
print("双卡节点已写入:", NODE_DIR / "__init__.py")
''')

# ───────────────────────── Cell 4: 下载权重 ─────────────────────────
add(r'''
import os
from pathlib import Path
from huggingface_hub import hf_hub_download

os.environ["HF_HOME"] = str(CACHE_HOME)
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"

REPO = "Comfy-Org/MiniMax-H3"
SIZES = {
 "diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors": 20970379616,
 "text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors":        15687142551,
 "vae/minimax_h3_video_vae_fp16.safetensors":                          5207808496,
 "vae/minimax_h3_audio_vae_fp32.safetensors":                           605254808,
}
MODELS = COMFY_HOME / "models"
print(f"共 {sum(SIZES.values())/1024**3:.2f} GiB（公开仓库，无需 token）")

for rel, size in SIZES.items():
    dst = MODELS / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_size == size:
        print("[跳过]", rel); continue
    if dst.exists():
        print("[重下] 大小不符:", rel); dst.unlink()
    print("[下载]", rel, flush=True)
    got = Path(hf_hub_download(repo_id=REPO, filename=rel, local_dir=MODELS))
    if got.stat().st_size != size:
        raise RuntimeError(f"校验失败 {rel}: {got.stat().st_size} != {size}")
    print(f"[完成] {rel} ({got.stat().st_size/1024**3:.2f} GiB)", flush=True)

ldir = MODELS / "loras"; ldir.mkdir(parents=True, exist_ok=True)
LF = "minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors"
if not (ldir / LF).exists():
    print("[下载] Turbo LoRA …", flush=True)
    hf_hub_download(repo_id="lightx2v/Minimax-h3-Turbo", filename=LF, local_dir=ldir)
LORA_NAME = LF
print("Turbo LoRA 就绪:", (ldir / LF).stat().st_size / 1024 ** 2, "MiB")
print("\n权重全部就绪")
''')

# ───────────────────────── Cell 5: 启动 ComfyUI（常驻后台） ─────────────────────────
add(r'''
import os, signal, subprocess, sys, time, requests

PORT = 8188
BASE = f"http://127.0.0.1:{PORT}"
PID_FILE = WORK_ROOT / "server.pid"
if PID_FILE.exists():
    try: os.kill(int(PID_FILE.read_text().strip()), signal.SIGTERM); time.sleep(2)
    except Exception: pass
    PID_FILE.unlink(missing_ok=True)

env = os.environ.copy()
env["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
env["HF_HOME"] = str(CACHE_HOME)
env["PYTHONUNBUFFERED"] = "1"

args = [sys.executable, "main.py",
        "--listen", "127.0.0.1", "--port", str(PORT),
        "--lowvram",
        "--preview-method", "none",
        "--output-directory", str(GEN_DIR),
        "--temp-directory", str(TMP_DIR)]
help_out = subprocess.run([sys.executable, "main.py", "--help"], cwd=COMFY_HOME,
                          env=env, capture_output=True, text=True).stdout
if "--reserve-vram" in help_out:
    args += ["--reserve-vram", "0.8"]

print("$", " ".join(args), flush=True)
log_fp = open(LOG_FILE, "w", encoding="utf-8")
SERVER = subprocess.Popen(args, cwd=COMFY_HOME, env=env,
                          stdout=log_fp, stderr=subprocess.STDOUT)
PID_FILE.write_text(str(SERVER.pid))

def log_tail(n=25):
    if not LOG_FILE.exists(): return "(无日志)"
    return "\n".join(LOG_FILE.read_text(encoding="utf-8", errors="replace").splitlines()[-n:])

t0 = time.time()
while time.time() - t0 < 600:
    try:
        r = requests.get(f"{BASE}/system_stats", timeout=5)
        if r.status_code == 200:
            print("ComfyUI 就绪，用时", round(time.time() - t0), "秒")
            for d in r.json().get("devices", [])[:2]:
                print("  ", d.get("name"), round(d.get("vram_total", 0) / 1e9, 1), "GB")
            break
    except Exception:
        pass
    if SERVER.poll() is not None:
        print("!! ComfyUI 进程退出，日志：\n", log_tail(60)); raise RuntimeError("ComfyUI 启动失败")
    time.sleep(10)
else:
    print(log_tail(60)); raise RuntimeError("ComfyUI 启动超时")
''')

# ───────────────────────── Cell 6: Gradio 面板 ─────────────────────────
add(r'''
import base64, json, os, re, shutil, time, uuid
from datetime import datetime
from pathlib import Path
import requests, gradio as gr
from PIL import Image

# ── 与 ComfyUI 对话的工具 ───────────────────────────────────────────────
OBJ = requests.get(f"{BASE}/object_info", timeout=180).json()

def declared(cls):
    v = OBJ.get(cls)
    return set((v or {}).get("input", {}).get("required", {})) | \
           set((v or {}).get("input", {}).get("optional", {}))

def check(cls, payload):
    d = declared(cls)
    if not d: return
    bad = [k for k in payload if k not in d]
    if bad: print(f"  注意: {cls} 未声明 {bad} -> 已剔除")
    for k in bad: payload.pop(k, None)

def align_frames(sec, fps=24):
    n = max(5, int(round(sec * fps)))
    return n + (5 - (n % 17)) % 17          # H3 硬约束：帧数 % 17 == 5

def canvas(aspect, mp, multiple=32):
    ar = aspect[0] / aspect[1]
    h = (mp * 1e6 / ar) ** 0.5
    w = ar * h
    cap = 768 * 1344                        # H3 面积上限
    if w * h > cap:
        s = (cap / (w * h)) ** 0.5; w *= s; h *= s
    r = lambda v: max(multiple, int(round(v / multiple)) * multiple)
    return r(w), r(h)

DIT  = "minimax_h3_fl2va_pruned_int8_convrot.safetensors"
TE   = "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors"
VVAE = "minimax_h3_video_vae_fp16.safetensors"
AVAE = "minimax_h3_audio_vae_fp32.safetensors"
DEV1 = "cuda:1" if torch.cuda.device_count() > 1 else "cuda:0"

# 画面比例：横屏 / 竖屏 / 方形
ORIENT = {
    "横屏 16:9":  (16, 9),
    "竖屏 9:16":  (9, 16),
    "方形 1:1":   (1, 1),
    "宽屏 4:3":   (4, 3),
    "竖版 3:4":   (3, 4),
}
# 清晰度档（单位：百万像素）。步数与时长固定时，耗时近似与像素数成正比
QUALITY = {
    "流畅 0.21MP（最快）": 0.21,
    "标清 0.31MP":         0.31,
    "推荐 0.40MP":         0.40,
    "高清 0.59MP（慢）":    0.59,
    "超清 0.85MP（很慢）":  0.85,
}
SEC_PER_STEP_K = 0.0   # 下面用实测样本标定

def _calibrate_step_sec():
    """由 832x480 / 124 帧 / 0.40MP -> 228 秒/步 标定：
       单步耗时 ∝ 像素数 × 帧数
       sec/step = k * (W*H) * L
    """
    w, h, frames, sec = 832, 480, 124, 228.0
    return sec / (w * h * frames)

SEC_PER_STEP_K = _calibrate_step_sec()

def estimate_step_sec(wh, frames):
    return SEC_PER_STEP_K * wh * frames

def estimate_minutes(mp, steps, frames):
    """粗估单次生成分钟数（不含首次约 4 分钟的权重加载）。"""
    return estimate_step_sec(mp * 1e6, frames) * steps / 60.0

AUDIO_HINT = "Audio: soft ambient sound matching the scene."

# ── 构建 ComfyUI 工作流 ────────────────────────────────────────────────
def build_graph(prompt, img_name, W, H, L, steps, seed, use_turbo):
    g = {}
    if img_name:
        g["0"] = {"class_type": "LoadImage", "inputs": {"image": img_name}}
        check("LoadImage", g["0"]["inputs"])
    g["1"] = {"class_type": "UNETLoader",
              "inputs": {"unet_name": DIT, "weight_dtype": "default"}}
    check("UNETLoader", g["1"]["inputs"])
    model = ["1", 0]
    if use_turbo:
        g["2"] = {"class_type": "LoraLoaderModelOnly",
                  "inputs": {"model": model, "lora_name": LORA_NAME, "strength_model": 1.0}}
        check("LoraLoaderModelOnly", g["2"]["inputs"])
        model = ["2", 0]
    g["3"] = {"class_type": "DualT4TextEncoder",
              "inputs": {"clip_name": TE, "load_to": DEV1}}
    check("DualT4TextEncoder", g["3"]["inputs"])
    g["4"] = {"class_type": "DualT4VAELoader",
              "inputs": {"vae_name": VVAE, "load_to": "cuda:0"}}
    check("DualT4VAELoader", g["4"]["inputs"])
    g["5"] = {"class_type": "DualT4VAELoader",
              "inputs": {"vae_name": AVAE, "load_to": "cuda:0"}}
    check("DualT4VAELoader", g["5"]["inputs"])
    h3 = {"clip": ["3", 0], "vae": ["4", 0], "prompt": prompt,
          "width": W, "height": H, "length": L}
    if img_name:
        h3["first_frame"] = ["0", 0]        # 传首帧 = 图生视频；不传 = 文生视频
    g["6"] = {"class_type": "MiniMaxH3ImageToVideo", "inputs": h3}
    check("MiniMaxH3ImageToVideo", g["6"]["inputs"])
    g["7"] = {"class_type": "BasicGuider",
              "inputs": {"model": model, "conditioning": ["6", 0]}}
    check("BasicGuider", g["7"]["inputs"])
    g["8"] = {"class_type": "RandomNoise", "inputs": {"noise_seed": int(seed)}}
    check("RandomNoise", g["8"]["inputs"])
    g["9"] = {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "res_multistep"}}
    check("KSamplerSelect", g["9"]["inputs"])
    g["10"] = {"class_type": "BasicScheduler",
               "inputs": {"model": model, "scheduler": "simple",
                          "steps": int(steps), "denoise": 1.0}}
    check("BasicScheduler", g["10"]["inputs"])
    g["11"] = {"class_type": "SamplerCustomAdvanced",
               "inputs": {"noise": ["8", 0], "guider": ["7", 0], "sampler": ["9", 0],
                          "sigmas": ["10", 0], "latent_image": ["6", 1]}}
    check("SamplerCustomAdvanced", g["11"]["inputs"])
    g["12"] = {"class_type": "VAEDecode", "inputs": {"samples": ["11", 0], "vae": ["4", 0]}}
    check("VAEDecode", g["12"]["inputs"])
    g["13"] = {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["11", 0], "vae": ["5", 0]}}
    check("VAEDecodeAudio", g["13"]["inputs"])
    g["14"] = {"class_type": "CreateVideo",
               "inputs": {"images": ["12", 0], "audio": ["13", 0], "fps": 24}}
    check("CreateVideo", g["14"]["inputs"])
    g["15"] = {"class_type": "SaveVideo",
               "inputs": {"video": ["14", 0], "filename_prefix": "h3",
                          "format": "auto", "codec": "auto"}}
    check("SaveVideo", g["15"]["inputs"])
    missing = [k for k, v in g.items() if v["class_type"] not in OBJ]
    if missing:
        raise RuntimeError(f"ComfyUI 缺少节点 {[g[k]['class_type'] for k in missing]}，请升级 ComfyUI")
    return g

# ── 提交并等待（带实时步数）─────────────────────────────────────────────
def run_until_done(pid, cid, state, timeout):
    ws = None
    try:
        import websocket
        ws = websocket.WebSocket()
        ws.connect(f"ws://127.0.0.1:{PORT}/ws?clientId={cid}", timeout=5)
    except Exception as e:
        state["ws_err"] = repr(e)[:120]
    t0 = time.time()
    while True:
        if ws is not None:
            try:
                ws.settimeout(1.0)
                msg = ws.recv()
                if msg:
                    d = json.loads(msg)
                    t = d.get("type")
                    if t == "progress":
                        state["cur"] = d.get("data", {}).get("value", 0)
                        state["max"] = d.get("data", {}).get("max", 1)
                    elif t == "execution_error":
                        state["error"] = json.dumps(d, ensure_ascii=False)[:900]
            except Exception:
                pass
        try:
            h = requests.get(f"{BASE}/history/{pid}", timeout=15).json()
            if pid in h:
                state["done"] = True; state["hist"] = h[pid]; break
        except Exception:
            pass
        if state.get("error"):
            break
        if time.time() - t0 > timeout:
            state["timeout"] = True; break
        time.sleep(1)
    try:
        if ws is not None: ws.close()
    except Exception:
        pass
    return state

def collect_output(hist, tag):
    files = []
    for node_out in (hist.get("outputs") or {}).values():
        for key in ("video", "images", "audio", "gifs"):
            for item in (node_out.get(key) or []):
                fn = item.get("filename")
                if not fn: continue
                sub = item.get("subfolder", "") or ""
                src = (GEN_DIR / sub / fn) if sub else (GEN_DIR / fn)
                if not src.exists():
                    cands = list(GEN_DIR.rglob(fn))
                    if cands: src = cands[0]
                if src.exists() and src.suffix.lower() in (".mp4", ".webm", ".mov", ".mkv"):
                    stamp = datetime.now().strftime("%m%d_%H%M%S")
                    dst = OUT_DIR / f"h3_{stamp}_{tag}{src.suffix}"
                    shutil.copy2(src, dst)
                    files.append(str(dst))
    return files

# ── 主处理函数 ─────────────────────────────────────────────────────────
def do_generate(image, prompt, extra, add_audio, seconds, orient_label, quality_label,
                steps, seed, use_turbo, progress=gr.Progress()):
    lines = []
    def say(s):
        lines.append(f"[{datetime.now():%H:%M:%S}] {s}")
        return "\n".join(lines)

    try:
        progress(0.02, desc="准备参数")
        if SERVER.poll() is not None:
            yield None, None, say("ComfyUI 已退出，请重新运行 Cell 5")
            return
        if not (prompt or "").strip():
            yield None, None, say("请填写提示词")
            return

        mp = QUALITY[quality_label]
        W, H = canvas(ORIENT[orient_label], mp)
        L = align_frames(float(seconds))
        say(f"分辨率 {W}x{H} | 帧数 {L}（{seconds}s @24fps）| 步数 {steps}")
        yield None, None, say("参数就绪")

        # 素材
        img_name = None
        if image is not None:
            src = image if isinstance(image, str) else str(image)
            tag = uuid.uuid4().hex[:8]
            img_name = f"up_{tag}.png"
            im = Image.open(src).convert("RGB")
            im = im.resize((W, H))
            im.save(COMFY_HOME / "input" / img_name)
            UP_DIR.mkdir(parents=True, exist_ok=True)
            im.save(UP_DIR / img_name)
            say(f"素材已载入并缩放到 {W}x{H}（图生视频）")
        else:
            say("未上传素材 -> 文生视频")
        yield None, None, say("素材就绪")
        # 组织最终提示词
        body = prompt.strip()
        if (extra or "").strip():
            body = body + "\n\nConstraints: " + extra.strip()
        if add_audio and "audio" not in body.lower():
            body = body + "\n\n" + AUDIO_HINT

        g = build_graph(body, img_name, W, H, L, steps, int(seed), bool(use_turbo))
        say("工作流校验通过，提交中…")

        cid = uuid.uuid4().hex
        res = requests.post(f"{BASE}/prompt",
                            json={"prompt": g, "client_id": cid}, timeout=180).json()
        if "prompt_id" not in res:
            yield None, None, say("提交失败：" + json.dumps(res, ensure_ascii=False)[:900])
            return
        pid = res["prompt_id"]
        say("已排队，首次生成需加载约 39G 权重（约 4 分钟），之后约 228 秒/步")

        state = {"cur": 0, "max": max(1, int(steps)), "done": False}
        import threading
        th = threading.Thread(target=run_until_done,
                              args=(pid, cid, state, JOB_TIMEOUT), daemon=True)
        th.start()

        t0 = time.time()
        while th.is_alive():
            elapsed = time.time() - t0
            cur = int(state.get("cur", 0)); mx = int(state.get("max", 1))
            frac = min(0.98, 0.05 + 0.9 * (cur / mx))
            head = say(f"运行中 {int(elapsed//60)}m{int(elapsed%60):02d}s | 步 {cur}/{mx}")
            progress(frac, desc=f"步 {cur}/{mx}")
            yield None, None, head
            time.sleep(3)

        if state.get("timeout"):
            yield None, None, say(f"超时（{JOB_TIMEOUT//3600}h）未完成")
            return
        if state.get("error"):
            yield None, None, say("生成出错：" + state["error"])
            return

        files = collect_output(state.get("hist") or {}, uuid.uuid4().hex[:6])
        cost = (time.time() - t0) / 60
        if not files:
            say(f"完成但未找到视频文件（{cost:.1f} 分钟），请查看 Kaggle Output")
        else:
            say(f"生成完成，用时 {cost:.1f} 分钟")
            for f in files:
                say("成品：" + f)
        yield (files[0] if files else None), (files or None), say("就绪")
    except Exception as e:
        import traceback
        yield None, None, say("异常：" + repr(e) + "\n" + traceback.format_exc()[-1200:])
def refresh_list():
    fs = sorted(OUT_DIR.glob("h3_*"), key=lambda p: p.stat().st_mtime, reverse=True)[:30]
    return gr.update(value=[str(p) for p in fs])

def compute_spec(seconds, orient_label, quality_label, steps):
    mp = QUALITY[quality_label]
    W, H = canvas(ORIENT[orient_label], mp)
    L = align_frames(float(seconds))
    est = estimate_minutes(mp, int(steps), L)
    return (f"分辨率 {W} x {H}　|　帧数 {L}（{seconds} 秒 @24fps）　|　"
            f"预计 {est:.0f} 分钟（首次额外 +4 分钟加载权重）")

def gpu_status():
    try:
        st = requests.get(f"{BASE}/system_stats", timeout=10).json()
        out = []
        for d in st.get("devices", [])[:2]:
            out.append(f"{d.get('name')} 显存 {d.get('vram_free',0)/1e9:.1f}/{d.get('vram_total',0)/1e9:.1f} GB")
        q = requests.get(f"{BASE}/queue", timeout=10).json()
        out.append(f"队列：运行 {len(q.get('queue_running',[]))} 等待 {len(q.get('queue_pending',[]))}")
        return "\n".join(out)
    except Exception as e:
        return f"读取失败：{e}"

# ── 界面布局 ───────────────────────────────────────────────────────────
CSS = ".download-wrap .file-preview{background:#111}"
with gr.Blocks(title="MiniMax-H3 视频工坊 (Kaggle T4x2)", css=CSS) as demo:
    gr.Markdown(
        "# MiniMax-H3 视频工坊\n"
        "**左边导入素材 → 写提示词 → 选参数 → 生成 → 右边下载成品。**\n\n"
        "提示：首次生成要加载约 39G 权重（约 4 分钟）；之后约 **228 秒/步**（8 步 ≈ 30 分钟）。"
        "生成期间可以关掉本页面，任务在服务器端继续跑。"
    )
    with gr.Row():
        # ---------- 左：输入 ----------
        with gr.Column(scale=5):
            gr.Markdown("### 1. 导入素材")
            in_image = gr.Image(
                label="首帧图片（可拖拽 / 点击上传）",
                type="filepath", height=260,
                sources=["upload", "clipboard"],
            )
            gr.Markdown(
                "<div style='font-size:12px;color:#888'>"
                "传图 = <b>图生视频</b>（画面从这张图开始动起来）；不传 = 文生视频。"
                "图片会自动缩放到所选分辨率。</div>"
            )

            gr.Markdown("### 2. 提示词")
            in_prompt = gr.Textbox(
                label="画面描述（英文效果最好）",
                placeholder="A golden retriever puppy running through a sunlit meadow "
                            "at golden hour, handheld camera, shallow depth of field…",
                lines=4,
            )
            in_extra = gr.Textbox(
                label="约束 / 负面要求（可选，会拼到提示词后面）",
                placeholder="no body distortion, no blurry face, stable lighting, no flicker",
                lines=2,
            )
            in_add_audio = gr.Checkbox(value=True, label="自动补充 Audio 描述（生成环境音）")

            gr.Markdown("### 3. 参数")
            with gr.Row():
                in_seconds = gr.Radio([3, 5, 8, 10], value=5, label="时长（秒）")
                in_orient = gr.Dropdown(list(ORIENT), value="横屏 16:9", label="画面比例")
            with gr.Row():
                in_quality = gr.Dropdown(list(QUALITY), value="推荐 0.40MP", label="清晰度")
                in_steps = gr.Slider(4, 20, value=8, step=1, label="步数（越多越精、越慢）")
            in_spec = gr.Textbox(
                label="实际规格与预计耗时（随上面参数自动更新）",
                value=compute_spec(5, "横屏 16:9", "推荐 0.40MP", 8),
                interactive=False, lines=2)
            with gr.Row():
                in_turbo = gr.Checkbox(value=True, label="Turbo LoRA（8 步即可，建议开）")
                in_add_audio = gr.Checkbox(value=True, label="自动生成环境音")
            in_seed = gr.Number(value=12345, label="随机种子")
            btn_random = gr.Button("随机种子", size="sm")
            btn_random.click(lambda: int(time.time()) % 99999999, None, in_seed)

            btn_gen = gr.Button("生成视频", variant="primary", size="lg")
            btn_refresh = gr.Button("刷新成品列表", size="sm")

        # ---------- 右：输出 ----------
        with gr.Column(scale=6):
            gr.Markdown("### 成品")
            out_video = gr.Video(label="预览", height=340)
            out_files = gr.File(label="下载成品（可多选）", file_count="multiple",
                                elem_classes=["download-wrap"])
            out_status = gr.Textbox(label="运行状态", lines=12, max_lines=20, interactive=False)
            btn_gpu = gr.Button("查看 GPU 状态", size="sm")
            btn_gpu.click(gpu_status, None, out_status)

    # 参数变化时实时更新「实际规格与预计耗时」
    for _c in (in_seconds, in_orient, in_quality, in_steps):
        _c.change(compute_spec, [in_seconds, in_orient, in_quality, in_steps], in_spec)

    btn_gen.click(
        do_generate,
        inputs=[in_image, in_prompt, in_extra, in_add_audio, in_seconds, in_orient,
                in_quality, in_steps, in_seed, in_turbo],
        outputs=[out_video, out_files, out_status],
    )
    btn_refresh.click(refresh_list, None, out_files)

print("Gradio 面板构建完成")
''')

# ───────────────────────── Cell 7: 启动 + 公网 URL + 保活 ─────────────────────────
add(r'''
import os, re, subprocess, threading, time
from datetime import datetime

def start_cloudflared(port, timeout=180):
    """快速隧道，无需注册，返回 https://xxx.trycloudflare.com"""
    binp = "/usr/local/bin/cloudflared"
    try:
        if not os.path.exists(binp):
            print("[隧道] 下载 cloudflared …", flush=True)
            subprocess.run(
                f"curl -sL --ssl-no-revoke -o {binp} "
                "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64",
                shell=True, timeout=300)
            subprocess.run(f"chmod +x {binp}", shell=True, check=False)
        if CF_LOG.exists(): CF_LOG.unlink()
        subprocess.Popen(f"{binp} tunnel --url http://127.0.0.1:{port} --no-autoupdate "
                         f"> {CF_LOG} 2>&1", shell=True)
        t0 = time.time()
        while time.time() - t0 < timeout:
            time.sleep(3)
            if CF_LOG.exists():
                txt = CF_LOG.read_text(encoding="utf-8", errors="replace")
                m = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", txt)
                if m:
                    return m.group(0)
    except Exception as e:
        print("[隧道] cloudflared 失败:", e)
    return None

local_url, share_url, urls = None, None, []
try:
    demo.queue(max_size=8)
    _, local_url, share_url = demo.launch(
        server_name="0.0.0.0", server_port=UI_PORT, share=True, show_error=True,
        prevent_thread_lock=True,
        allowed_paths=[str(OUT_DIR), str(GEN_DIR), str(UP_DIR)])
except Exception as e:
    print("[面板] 主启动方式异常:", repr(e)[:300], flush=True)
    threading.Thread(target=lambda: demo.queue(max_size=8).launch(
        server_name="0.0.0.0", server_port=UI_PORT, share=True), daemon=True).start()
    time.sleep(30)
    local_url = f"http://127.0.0.1:{UI_PORT}"
    share_url = None

print("\n" + "=" * 70, flush=True)
print("本地地址 :", local_url, flush=True)
if share_url:
    print("Gradio 公网地址 :", share_url, flush=True)
    urls.append(share_url)

cf = start_cloudflared(UI_PORT)
if cf:
    print("Cloudflare 公网地址:", cf, flush=True)
    urls.append(cf)

if not urls:
    print("!! 两种隧道都没起来。备用办法：在本 notebook 右上角查看，或改用 Kaggle Output 面板取成品。", flush=True)
else:
    print("\n>>> 请用浏览器打开上面任意一个公网地址，即可操作面板 <<<", flush=True)
print("=" * 70 + "\n", flush=True)

# ── 保活：防止 Kaggle 因空闲回收会话 ──────────────────────────────────
FINAL_DIR.mkdir(parents=True, exist_ok=True)
urls_file = FINAL_DIR / "ui_urls.txt"
urls_file.write_text("\n".join(u for u in urls if u) or local_url or "", encoding="utf-8")

t0 = time.time(); beat = 0
try:
    while time.time() - t0 < MAX_HOURS * 3600:
        time.sleep(300)
        beat += 1
        try:
            st = requests.get(f"{BASE}/system_stats", timeout=10).json()
            devs = " | ".join(
                f"{d.get('name','?')} {d.get('vram_free',0)/1e9:.1f}/{d.get('vram_total',0)/1e9:.1f}GB"
                for d in st.get("devices", [])[:2])
        except Exception as e:
            devs = f"服务异常 {e}"
        try:
            n_out = len(list(OUT_DIR.glob("h3_*")))
        except Exception:
            n_out = -1
        print(f"[心跳 {beat}] {datetime.now():%H:%M:%S} "
              f"已运行 {(time.time()-t0)/3600:.2f}h | 成品 {n_out} 个 | {devs}", flush=True)
except KeyboardInterrupt:
    pass
finally:
    print("保活结束，共运行", round((time.time()-t0)/3600, 2), "小时", flush=True)
''')


def code_cell(src):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": src.splitlines(keepends=True)}


nb = {
    "cells": [code_cell(c) for c in C],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
        "kaggle": {"accelerator": "NvidiaTeslaT4", "dataSources": [],
                   "isGpuEnabled": True, "isInternetEnabled": True,
                   "language": "python", "sourceType": "notebook"},
    },
    "nbformat": 4, "nbformat_minor": 4,
}
(OUT / "h3-ui.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

meta = {
    "id": "xwdfyx/h3-ui", "title": "h3 ui", "code_file": "h3-ui.ipynb",
    "language": "python", "kernel_type": "notebook", "is_private": True,
    "enable_gpu": True, "enable_internet": True,
    # 必须大写 N：NvidiaTeslaT4 = T4 x2 (2x16GB, sm_75)
    "accelerator": "NvidiaTeslaT4", "machine_shape": "NvidiaTeslaT4",
    "dataset_sources": [], "competition_sources": [], "kernel_sources": [],
}
(OUT / "kernel-metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                                          encoding="utf-8")
print("written:", OUT, "| cells:", len(C))
