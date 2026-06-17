import os

from fastapi.responses import HTMLResponse


class PageHandler:
    """Web页面处理类"""

    async def index(self):
        """返回首页HTML"""
        html_path = os.path.join(os.path.dirname(__file__), "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
