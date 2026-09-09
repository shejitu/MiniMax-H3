
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
