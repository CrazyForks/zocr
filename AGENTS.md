# ZOCR 开发指南

## 项目概述

基于百度PP-OCRv6的OCR API服务，FastAPI + Uvicorn + RapidOCR。

## 关键入口

- `app/main.py` - FastAPI应用入口
- `app/routers.py` - 路由定义（`/api/ocr/upload`, `/api/ocr/fetch`, `/api/health`）
- `app/api/ocr.py` - OCR核心逻辑（延迟初始化单例）
- `app/middleware/auth.py` - Bearer Token认证（ZOCR_TOKEN为空则跳过）
- `app/config.py` - 环境变量配置

## 开发命令

```bash
# 本地开发（热重载，端口5080）
bash run.sh dev

# 生产模式
bash run.sh

# Docker部署
docker-compose build && docker-compose up -d
```

## 模型配置

两个变体，通过`OCR_MODEL_VERSION`环境变量切换：
- `tiny` - 快速，精度较低（6904字符）
- `small` - 准确，推荐（默认，18708字符）

模型文件位置：`app/models/ppocrv6_{variant}/`

### 添加新模型版本

1. 下载模型文件（det和rec）：
```bash
# 从HuggingFace下载
wget https://huggingface.co/PaddlePaddle/PP-OCRv6_{variant}_det_onnx/resolve/main/inference.onnx
wget https://huggingface.co/PaddlePaddle/PP-OCRv6_{variant}_rec_onnx/resolve/main/inference.onnx
```

2. 提取字典文件：
```python
import yaml
import requests

# 下载rec模型的inference.yml
url = f"https://huggingface.co/PaddlePaddle/PP-OCRv6_{variant}_rec_onnx/resolve/main/inference.yml"
response = requests.get(url)
config = yaml.safe_load(response.text)

# 提取字典
char_dict = config["PostProcess"]["character_dict"]

# 保存为txt文件（每行一个字符）
with open(f"ppocrv6_{variant}_keys.txt", "w", encoding="utf-8") as f:
    for char in char_dict:
        f.write(char + "\n")
```

3. 文件命名规则：
- 检测模型：`app/models/ppocrv6_{variant}/ppocrv6_{variant}_det.onnx`
- 识别模型：`app/models/ppocrv6_{variant}/ppocrv6_{variant}_rec.onnx`
- 字典文件：`app/models/ppocrv6_{variant}_keys.txt`

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `TOKEN` | 认证密钥 | 空（无认证） |
| `WORKERS` | uvicorn进程数 | 1 |
| `OCR_MODEL_VERSION` | 模型版本(tiny/small) | small |
| `MAX_FILE_SIZE` | 最大文件(bytes) | 10485760 |

配置文件：`.env`（不提交git）

## 注意事项

- 无测试框架，无lint/typecheck配置
- OCR实例懒加载，首次请求会初始化模型
- 认证中间件排除：`/`, `/docs*`, `/api/health`
