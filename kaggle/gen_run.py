# -*- coding: utf-8 -*-
"""
MiniMax-H3 on Kaggle —— 全自动 headless 出片 notebook 生成器。
无需交互、无需公网隧道：装 ComfyUI -> 下权重 -> 起服务 -> 提交工作流 -> 出片到 /kaggle/working/videos
"""
import json, pathlib

OUT = pathlib.Path(r"E:\我的workbuddy\kaggle跑H3视频\h3-run")
OUT.mkdir(parents=True, exist_ok=True)

C = []
def add(src):
    C.append(src.strip("\n"))

# ───────────────────────── Cell 1: 配置 + 环境体检 ─────────────────────────
add(r'''
# ══════════ 配置 ══════════
# 输入图（首帧）。换成你自己的图：上传到 Kaggle Dataset 后改这里的路径或 URL
IMAGE_URL = "https://picsum.photos/seed/h3demo/864/480"

PROMPT = (
    "The scene comes alive from the still image: gentle cinematic motion, the camera "
    "slowly pushes in, subtle parallax, natural light shift, fine details breathing.\n\n"
    "Audio: soft ambient wind and distant birds.\n\n"
    "Constraints: keep the composition and colors of the first frame, no warping, "
    "no morphing, no flicker, no extra limbs, stable lighting."
)
SECONDS   = 5        # 时长（秒）
MEGAPIXEL = 0.4      # 0.4 -> 864x480（480P）；0.2 -> 608x352（更快）；0.3 -> 736x416
ASPECT    = (16, 9)
STEPS     = 8        # turbo LoRA 蒸馏步数（4 = 更快，20 = 不用 turbo 时的常规值）
USE_TURBO = True
SEED      = 12345

import os, shutil, subprocess, sys, time
from pathlib import Path
import torch

ON_KAGGLE = Path("/kaggle").exists()
WORK_ROOT = Path("/kaggle/temp/h3") if ON_KAGGLE else Path("./h3").resolve()
COMFY_HOME = WORK_ROOT / "ComfyUI"
CACHE_HOME = WORK_ROOT / "hf_cache"
GEN_DIR    = WORK_ROOT / "gen"
TMP_DIR    = WORK_ROOT / "tmp"
FINAL_DIR  = Path("/kaggle/working") if ON_KAGGLE else WORK_ROOT / "dist"
OUT_DIR    = FINAL_DIR / "videos"
LOG_FILE   = FINAL_DIR / "comfy.log"
for d in (WORK_ROOT, CACHE_HOME, GEN_DIR, TMP_DIR, FINAL_DIR, OUT_DIR):
    d.mkdir(parents=True, exist_ok=True)

def to_gib(n): return n / 1024 ** 3
def sh(c, cwd=None, check=False):
    return subprocess.run(c, shell=True, cwd=cwd, capture_output=True, text=True, check=check)

print("Python", sys.version.split()[0], "| torch", torch.__version__)
print(sh("nvidia-smi --query-gpu=index,name,memory.total,compute_cap --format=csv").stdout)

BAD = False
if not torch.cuda.is_available():
    raise RuntimeError("没有可用 GPU：请在 Settings → Accelerator 选择 GPU T4 x2。")
NAMES = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
print("GPU:", NAMES, "| 数量", torch.cuda.device_count())
for i in range(torch.cuda.device_count()):
    p = torch.cuda.get_device_properties(i)
    if (p.major, p.minor) < (7, 0):
        print(f"!! GPU{i} {p.name} compute capability {p.major}.{p.minor} 过低："
              f"当前 PyTorch 要求 sm_70+，且 H3 的 INT8/FP8 量化内核需要 sm_75+。")
        BAD = True
if torch.cuda.device_count() < 2:
    print("!! 只有 1 张卡：显存减半，OOM 风险很高，建议切到 GPU T4 x2。")
if BAD:
    raise RuntimeError(
        "当前分配到的 GPU 架构过旧（很可能是 P100 / sm_60），MiniMax H3 无法运行。\n"
        "请在 Kaggle 网页：Settings → Accelerator → 选 GPU T4 x2 → Save，再重新 Run All。\n"
        "（Kaggle 官方公告：P100 将于 2026-09-15 退役，之后会自动切到 T4x2）")

import psutil
print(f"内存 {to_gib(psutil.virtual_memory().total):.1f} GiB | 磁盘剩余 {to_gib(shutil.disk_usage(WORK_ROOT).free):.1f} GiB")
''')

# ───────────────────────── Cell 2: 安装 ComfyUI + cu130 torch ─────────────────────────
add(r'''
import subprocess, sys
from pathlib import Path

def sh_live(cmd, cwd=None):
    print("$", cmd if isinstance(cmd, str) else " ".join(map(str, cmd)))
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
         "huggingface_hub", "requests", "psutil", "websocket-client"])
subprocess.run([sys.executable, "-m", "pip", "cache", "purge"], check=False)
print("ComfyUI commit:", subprocess.check_output(["git","rev-parse","--short","HEAD"],
      cwd=COMFY_HOME, text=True).strip())

# ── 升级 torch 到 cu130：启用 ComfyUI 快速量化内核（不升级则 5 秒视频要 1.5~3.5 小时）──
def driver_ok():
    try:
        out = subprocess.run(["nvidia-smi","--query-gpu=driver_version","--format=csv,noheader"],
                             capture_output=True, text=True, timeout=30).stdout.strip().splitlines()
        return int(out[0].split(".")[0]) >= 580 if out else False
    except Exception:
        return False

def sub_torch():
    r = subprocess.run([sys.executable, "-c",
        "import torch;print(f'{torch.__version__}|{torch.version.cuda}')"],
        capture_output=True, text=True, timeout=90)
    if r.returncode == 0 and "|" in r.stdout:
        v, c = r.stdout.strip().split("|"); return v, c
    return "?", "?"

print("驱动 >=580 ?", driver_ok())
if driver_ok():
    v, c = sub_torch()
    if c.startswith("13."):
        print(f"✔ 子进程 torch 已是 cu130（{v} | {c}）")
        NEW_CUDA = c
    else:
        print(f"升级 torch -> cu130（当前 {v} | {c}）…")
        subprocess.run([sys.executable,"-m","pip","uninstall","-y","torch","torchvision","torchaudio"],
                       capture_output=True, timeout=180)
        sh_live([sys.executable,"-m","pip","install","-q","--no-cache-dir",
                 "--index-url","https://download.pytorch.org/whl/cu130",
                 "torch","torchvision","torchaudio"])
        _, NEW_CUDA = sub_torch()
        print("升级后:", NEW_CUDA)
    if NEW_CUDA.startswith("13."):
        sh_live([sys.executable,"-m","pip","install","--force-reinstall","--no-cache-dir","comfy-kitchen"])
else:
    print("驱动 <580，跳过 cu130 升级（速度会明显变慢）")
''')

# ───────────────────────── Cell 3: 双卡自定义节点 ─────────────────────────
# 节点源码用 base64 内嵌，彻底避免引号嵌套问题
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
import base64 as _b64
_NODE_B64 = _b64.b64encode(NODE_PY.encode("utf-8")).decode("ascii")
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
NEED = list(SIZES)
MODELS = COMFY_HOME / "models"
print(f"共 {sum(SIZES.values())/1024**3:.2f} GiB（公开仓库，无需 token）")

for rel in NEED:
    dst = MODELS / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_size == SIZES[rel]:
        print("[跳过]", rel); continue
    if dst.exists():
        print("[重下] 大小不符:", rel); dst.unlink()
    print("[下载]", rel, flush=True)
    got = Path(hf_hub_download(repo_id=REPO, filename=rel, local_dir=MODELS))
    if got.stat().st_size != SIZES[rel]:
        raise RuntimeError(f"校验失败 {rel}: {got.stat().st_size} != {SIZES[rel]}")
    print(f"[完成] {rel} ({got.stat().st_size/1024**3:.2f} GiB)", flush=True)

LORA = None
if USE_TURBO:
    ldir = MODELS / "loras"; ldir.mkdir(parents=True, exist_ok=True)
    LF = "minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors"
    lp = ldir / LF
    if not lp.exists():
        print("[下载] Turbo LoRA …", flush=True)
        hf_hub_download(repo_id="lightx2v/Minimax-h3-Turbo", filename=LF, local_dir=ldir)
    LORA = LF
    print("Turbo LoRA 就绪:", lp.stat().st_size/1024**2, "MiB")
print("\n权重全部就绪 ✔")
''')

# ───────────────────────── Cell 5: 启动 ComfyUI ─────────────────────────
add(r'''
import os, signal, subprocess, sys, time, json, requests

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
        "--lowvram",                       # 39.5G 权重 > 32G 显存，必须分层卸载
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
            print("✔ ComfyUI 就绪，用时", round(time.time()-t0), "秒")
            print(json.dumps(r.json().get("devices", [{}])[0], ensure_ascii=False)[:400]
                  if (json := __import__("json")) else "")
            break
    except Exception:
        pass
    if SERVER.poll() is not None:
        print("!! ComfyUI 进程退出，日志：\n", log_tail(60)); raise RuntimeError("ComfyUI 启动失败")
    time.sleep(10)
else:
    print(log_tail(60)); raise RuntimeError("ComfyUI 启动超时")
''')

# ───────────────────────── Cell 6: 构建工作流 + 提交 + 监控 ─────────────────────────
add(r'''
import json, math, time, uuid, requests

OBJ = requests.get(f"{BASE}/object_info", timeout=180).json()
def declared(cls):
    v = OBJ.get(cls)
    return set((v or {}).get("input", {}).get("required", {})) | set((v or {}).get("input", {}).get("optional", {}))
def check(cls, payload):
    d = declared(cls)
    if not d: return
    bad = [k for k in payload if k not in d]
    if bad: print(f"  注意: {cls} 未声明 {bad} -> 已剔除")
    for k in bad: payload.pop(k, None)

def align_frames(sec, fps=24):
    n = max(5, int(round(sec * fps)))
    return n + (5 - (n % 17)) % 17
def canvas(aspect, mp=MEGAPIXEL, multiple=32):
    ar = aspect[0] / aspect[1]
    h = (mp * 1e6 / ar) ** 0.5
    w = ar * h
    cap = 768 * 1344
    if w * h > cap:
        s = (cap / (w * h)) ** 0.5; w *= s; h *= s
    r = lambda v: max(multiple, int(round(v / multiple)) * multiple)
    return r(w), r(h)

W, H = canvas(ASPECT)
L = align_frames(SECONDS)
print(f"分辨率 {W}x{H} | 帧数 {L}（{SECONDS}s @24fps，已按 n%17==5 对齐）| 步数 {STEPS}")

# ── 准备输入图（图生视频首帧）──
import urllib.request
from PIL import Image
inp_dir = COMFY_HOME / "input"
inp_dir.mkdir(parents=True, exist_ok=True)
IMG_NAME = "h3_input.png"
img_path = inp_dir / IMG_NAME
try:
    if not img_path.exists():
        print("下载输入图:", IMAGE_URL, flush=True)
        urllib.request.urlretrieve(IMAGE_URL, img_path)
    im = Image.open(img_path).convert("RGB").resize((W, H))
    im.save(img_path)
    print("输入图就绪:", img_path, im.size, flush=True)
    HAVE_IMAGE = True
except Exception as e:
    print("输入图准备失败，回退为文生视频:", repr(e))
    HAVE_IMAGE = False

DIT = "minimax_h3_fl2va_pruned_int8_convrot.safetensors"
TE  = "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors"
VVAE = "minimax_h3_video_vae_fp16.safetensors"
AVAE = "minimax_h3_audio_vae_fp32.safetensors"
dev1 = "cuda:1" if torch.cuda.device_count() > 1 else "cuda:0"

g = {}
if HAVE_IMAGE:
    g["0"] = {"class_type": "LoadImage", "inputs": {"image": IMG_NAME}}
    check("LoadImage", g["0"]["inputs"])
g["1"] = {"class_type": "UNETLoader",
          "inputs": {"unet_name": DIT, "weight_dtype": "default"}}
check("UNETLoader", g["1"]["inputs"])
model = ["1", 0]
if LORA:
    g["2"] = {"class_type": "LoraLoaderModelOnly",
              "inputs": {"model": model, "lora_name": LORA, "strength_model": 1.0}}
    check("LoraLoaderModelOnly", g["2"]["inputs"])
    model = ["2", 0]
g["3"] = {"class_type": "DualT4TextEncoder", "inputs": {"clip_name": TE, "load_to": dev1}}
check("DualT4TextEncoder", g["3"]["inputs"])
g["4"] = {"class_type": "DualT4VAELoader", "inputs": {"vae_name": VVAE, "load_to": "cuda:0"}}
check("DualT4VAELoader", g["4"]["inputs"])
g["5"] = {"class_type": "DualT4VAELoader", "inputs": {"vae_name": AVAE, "load_to": "cuda:0"}}
check("DualT4VAELoader", g["5"]["inputs"])
_h3 = {"clip": ["3", 0], "vae": ["4", 0], "prompt": PROMPT,
       "width": W, "height": H, "length": L}
if HAVE_IMAGE:
    _h3["first_frame"] = ["0", 0]      # 首帧 -> 图生视频（不传则为文生视频）
g["6"] = {"class_type": "MiniMaxH3ImageToVideo", "inputs": _h3}
check("MiniMaxH3ImageToVideo", g["6"]["inputs"])
g["7"] = {"class_type": "BasicGuider", "inputs": {"model": model, "conditioning": ["6", 0]}}
check("BasicGuider", g["7"]["inputs"])
g["8"] = {"class_type": "RandomNoise", "inputs": {"noise_seed": SEED}}
check("RandomNoise", g["8"]["inputs"])
g["9"] = {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "res_multistep"}}
check("KSamplerSelect", g["9"]["inputs"])
g["10"] = {"class_type": "BasicScheduler",
           "inputs": {"model": model, "scheduler": "simple", "steps": STEPS, "denoise": 1.0}}
check("BasicScheduler", g["10"]["inputs"])
g["11"] = {"class_type": "SamplerCustomAdvanced",
           "inputs": {"noise": ["8", 0], "guider": ["7", 0], "sampler": ["9", 0],
                      "sigmas": ["10", 0], "latent_image": ["6", 1]}}
check("SamplerCustomAdvanced", g["11"]["inputs"])
g["12"] = {"class_type": "VAEDecode", "inputs": {"samples": ["11", 0], "vae": ["4", 0]}}
check("VAEDecode", g["12"]["inputs"])
g["13"] = {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["11", 0], "vae": ["5", 0]}}
check("VAEDecodeAudio", g["13"]["inputs"])
g["14"] = {"class_type": "CreateVideo", "inputs": {"images": ["12", 0], "audio": ["13", 0], "fps": 24}}
check("CreateVideo", g["14"]["inputs"])
g["15"] = {"class_type": "SaveVideo",
           "inputs": {"video": ["14", 0], "filename_prefix": "h3_t2v", "format": "auto", "codec": "auto"}}
check("SaveVideo", g["15"]["inputs"])

missing = [k for k, v in g.items() if v["class_type"] not in OBJ]
if missing:
    raise RuntimeError(f"ComfyUI 缺少节点 {[g[k]['class_type'] for k in missing]}，请升级 ComfyUI")

cid = uuid.uuid4().hex
r = requests.post(f"{BASE}/prompt", json={"prompt": g, "client_id": cid}, timeout=120)
res = r.json()
if "prompt_id" not in res:
    print(json.dumps(res, ensure_ascii=False)[:2000]); raise RuntimeError("提交失败，见上")
pid = res["prompt_id"]
print("已提交 prompt_id:", pid, flush=True)

# 轮询等待（首次会加载 ~39G 权重，可能十几分钟）
t0 = time.time(); last = 0
while True:
    h = requests.get(f"{BASE}/history/{pid}", timeout=30).json()
    if pid in h:
        print("\n✔ 生成完成，用时", round((time.time()-t0)/60, 1), "分钟")
        break
    if time.time() - t0 > 5 * 3600:
        print(log_tail(80)); raise RuntimeError("超时 5 小时未完成")
    if time.time() - last > 120:
        last = time.time()
        try:
            q = requests.get(f"{BASE}/queue", timeout=10).json()
            print(f"[{round((time.time()-t0)/60)}min] 运行 {len(q.get('queue_running',[]))} "
                  f"等待 {len(q.get('queue_pending',[]))}", flush=True)
            print("   ", log_tail(4).replace("\n", " | ")[:400], flush=True)
        except Exception as e:
            print("轮询异常", e)
    time.sleep(20)
''')

# ───────────────────────── Cell 7: 收尾输出 ─────────────────────────
add(r'''
import shutil, subprocess, time
from pathlib import Path
time.sleep(10)
EXT = {".mp4", ".webm", ".mov", ".mkv"}
found = [p for p in GEN_DIR.rglob("*") if p.is_file() and p.suffix.lower() in EXT]
if not found:
    found = [p for p in Path("/kaggle/temp").rglob("*.mp4")] if Path("/kaggle/temp").exists() else []
print("找到成片:", len(found))
for f in found:
    dst = OUT_DIR / f.name
    shutil.copy2(f, dst)
    print(f"  {dst}  {dst.stat().st_size/1024**2:.1f} MiB")
print("\n输出目录:", OUT_DIR)
try:
    os.kill(int(PID_FILE.read_text().strip()), signal.SIGTERM); print("已关闭 ComfyUI 服务")
except Exception: pass
sh_live(f"ls -lh {OUT_DIR}")
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
(OUT / "h3-run.ipynb").write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

meta = {
    "id": "xwdfyx/h3-i2v-480p", "title": "h3 i2v 480p", "code_file": "h3-run.ipynb",
    "language": "python", "kernel_type": "notebook", "is_private": True,
    "enable_gpu": True, "enable_internet": True,
    # 注意大小写：必须是 NvidiaTeslaT4（T4 x2，2x16GB，sm_75）。
    # 小写 nvidiaTeslaT4 会被服务端静默忽略并回退到 P100（sm_60，torch2.x 不支持）。
    "accelerator": "NvidiaTeslaT4", "machine_shape": "NvidiaTeslaT4",
    "dataset_sources": [], "competition_sources": [], "kernel_sources": [],
}
(OUT / "kernel-metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print("written:", OUT, "| cells:", len(C))
