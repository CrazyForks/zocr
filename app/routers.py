from fastapi import APIRouter

from app.api.ocr import OcrHandler
from app.api.page import PageHandler

ocr_handler = OcrHandler()
page_handler = PageHandler()

router = APIRouter()

# 首页
router.get("/")(page_handler.index)

# 健康检查接口
router.get("/api/health")(ocr_handler.health)

# OCR识别接口
router.post("/api/ocr")(ocr_handler.recognize)
