"""阶段一冒烟测试：验证 GPU 可用 + 核心依赖可导入"""
import torch


def test_torch_cuda_available():
    assert torch.cuda.is_available(), "CUDA 不可用，请检查驱动和 PyTorch 安装"


def test_gpu_name():
    name = torch.cuda.get_device_name(0)
    assert "4070" in name or "NVIDIA" in name, f"未检测到预期 GPU，实际：{name}"


def test_basic_tensor_on_gpu():
    x = torch.randn(4, 3, 224, 224).cuda()
    assert x.device.type == "cuda"
    assert x.shape == (4, 3, 224, 224)


def test_import_timm():
    import timm
    model = timm.create_model("mobilenetv3_large_100", pretrained=False)
    assert model is not None


def test_import_omegaconf():
    from omegaconf import OmegaConf
    cfg = OmegaConf.create({"lr": 1e-3, "batch_size": 128})
    assert cfg.lr == 1e-3


def test_import_wandb():
    import wandb
    assert wandb.__version__ is not None
