import asyncio
import os
import time
import functools  # 裝飾器用來維持傳入 function id
import json
from dataclasses import dataclass
from typing import Optional, Union, Callable
from openai import (
    AsyncOpenAI,
    OpenAIError,
    RateLimitError,
    AuthenticationError,
)


class GrokService:
    """
    ### Singleton class to manage the Grok API client.

    Usage:
    ```python
    from utils.grok_service import GrokService
    grok_service = GrokService()
    ```

    Methods:
    - `fetch_client_info()`: Fetches the client information.
    - `set_api_key(new_api_key: str)`: Sets a new API key.
    - `set_model(new_model: str)`: Sets a new model.
    - `chat_completion(messages: list)`: Sends a chat completion request.
    - `generate_image(prompt: str, **kwargs)`: Generates an image based on the prompt.
    - `get_models_list()`: Fetches the list of available models.
    - `close()`: Closes the client connection.

    """

    _instance: Optional["GrokService"] = None
    _lock = asyncio.Lock()  # Create a lock for thread safety
    _semaphore = asyncio.Semaphore(1)  # Semaphore to limit concurrent access

    def __new__(cls) -> "GrokService":
        if cls._instance is None:
            cls._instance = super(GrokService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self._api_key = os.getenv("grokApiKey")
            self.base_url = "https://api.x.ai/v1"
            self.client = None
            self.initialized = False
            self.model = "grok-3-fast-latest"
            self.last_request_time: float = time.time() - 1
            self.timeout = 30
            asyncio.create_task(self._initialize())

    # Singleton instance
    async def _initialize(self) -> None:
        async with self._lock:
            if not self.initialized:
                if not self._api_key:
                    raise ValueError("API key is missing")
                self.client = AsyncOpenAI(api_key=self._api_key, base_url=self.base_url)
                self.initialized = True

    # Fetch client Information
    async def fetch_client_info(self) -> dict:
        if self.client is None or not self.initialized:
            return None
        else:
            client_info = {
                "model": self.model,
                "base_url": self.base_url,
                "last_request_time": time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(self.last_request_time)
                ),
            }
            return client_info

    # Set the API key
    async def set_api_key(self, new_api_key: str) -> Union[str, None]:
        if not new_api_key:
            return "API key 不能為空"
        async with self._lock:
            if self.client is not None and not self.client.is_closed:
                await self.client.close()
            self._api_key = new_api_key
            self.client = None
            self.initialized = False
            await self._initialize()
            return None

    # Set the model
    async def set_model(self, new_model: str) -> Union[str, None]:
        # 檢查模型名稱是否為空
        if not new_model:
            return "模型名稱不能為空"

        # 檢查模型名稱是否符合格式
        with open("./data/docs/grok_data.json", "r") as f:
            data = json.load(f)
            models_list = data["grok_models"].keys()
            if new_model not in models_list:
                return "模型名稱不存在，請嘗試重新取得模型列表"

        # 都成功後
        # async with self._lock:
        #     if self.client is not None and not self.client.is_closed:
        #         await self.client.close()
        #     self.model = new_model
        #     self.client = None
        #     self.initialized = False
        #     await self._initialize()
        #     return None
        async with self._lock:
            self.model = new_model
            return None

    # 使用前確保初始化
    async def _ensure_initialized(self) -> None:
        if self.client is None or not self.initialized:
            await self._initialize()

    # 裝飾器處理 API 錯誤
    def handle_api_errors(endpoint: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            async def wrapper(*args, **kwargs) -> Union[object, str]:
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        return await func(*args, **kwargs)
                    except RateLimitError:
                        if attempt < max_retries - 1:
                            await asyncio.sleep(1)
                            continue
                        raise Exception("速率限制，請稍後重試。")
                    except AuthenticationError:
                        raise Exception("API 密鑰無效，請檢查 API key。")
                    except OpenAIError as e:
                        raise Exception(f"API 錯誤 ({endpoint}): {str(e)}")
                else:
                    raise Exception("請求失敗，請稍後重試。")

            return wrapper

        return decorator

    # 裝飾器處理 API 請求限制 # 這裡的請求限制是每秒 1 次
    def api_request_limit(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs) -> Union[object, str]:
            async with self._semaphore:
                current_time = time.time()
                next_available_time = self.last_request_time + 1
                if current_time < next_available_time:
                    await asyncio.sleep(next_available_time - current_time)
                send_time = time.time()
                result = await func(self, *args, **kwargs)
                self.last_request_time = send_time
                return result

        return wrapper

    # 普通對話
    @handle_api_errors("chat_completion")
    @api_request_limit
    async def chat_completion(
        self,
        messages: list,
    ):
        await self._ensure_initialized()
        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            timeout=self.timeout,
        )
        return completion

    # 圖片生成
    @handle_api_errors("generate_image")
    @api_request_limit
    async def generate_image(self, prompt: str):
        await self._ensure_initialized()
        completion = await self.client.images.generate(prompt=prompt)
        return completion

    # 獲取可用模型列表
    @handle_api_errors("get_models_list")
    @api_request_limit
    async def get_models_list(self) -> list:
        await self._ensure_initialized()
        models = await self.client.models.list()
        if models is {}:
            return None

        # 把模型資料寫入 JSON 文件資料
        with open("./data/docs/grok_data.json", "r+") as f:
            data = json.load(f)
            model_data = {}
            for model in models.data:
                model_name = model.id
                model_data[model_name] = vars(model)
            data["grok_models"] = model_data

            # 回到檔案開頭
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)

            # 刪除多餘的舊內容（如果有）
            f.truncate()
        return model_data

    async def close(self) -> None:
        async with self._lock:
            if self.client is not None and not self.client.is_closed:
                await self.client.close()
                self.client = None
                self.initialized = False
