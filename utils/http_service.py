# utils/http_service.py
import aiohttp
import asyncio
from typing import Optional


class HttpService:
    _instance: Optional["HttpService"] = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HttpService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # 防止重複初始化
            self.session = None  # aiohttp ClientSession
            self.initialized = True

    async def initialize(self):
        """初始化 aiohttp 會話"""
        async with self._lock:
            if self.session is None or self.session.closed:
                self.session = aiohttp.ClientSession()

    async def close(self):
        """關閉 aiohttp 會話"""
        if self.session and not self.session.closed:
            await self.session.close()

    async def get(self, endpoint: str) -> str:
        """執行非同步 GET 請求"""
        if self.session is None:
            await self.initialize()
        async with self.session.get(f"{endpoint}") as response:
            return await response.text()

    async def post(self, endpoint: str, data: dict) -> str:
        """執行非同步 POST 請求"""
        if self.session is None:
            await self.initialize()
        async with self.session.post(
            f"{self.base_url}/{endpoint}", json=data
        ) as response:
            return await response.text()


async def get_http_service() -> HttpService:
    """獲取 HttpService 單例實例"""
    if HttpService._instance is None:
        HttpService._instance = HttpService()
        await HttpService._instance.initialize()
    return HttpService._instance
