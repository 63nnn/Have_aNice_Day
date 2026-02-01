class SystemMessage:
    # ==== 系統通用訊息 ====
    PERMISSION_DENIED = "Permission denied. (wrong channel)"

    # ==== Grok 指令提示 ====
    GROK_USAGE = """```
Commands:

    Grok:
        - grok <message> : Send a message to chat with Grok.

    model:
        - grok model : Show the available models.
        - grok model refresh : Refresh the model list.
        - grok model set <model> : Set the model to use.
```"""

    # ==== 油價顯示模板 ====
    Oil_PRICE_TEMPLATE = """```
{title}: 
    92: {p92}   95: {p95}    98: {p98}

{week_adjust}

{error_message}
```"""


class SystemConst:
    # ==== Embed 顏色代表不同狀態 ====
    class EmbedColor:
        GROK = 0xB3B3B4  # 就是灰色
        PROCESSING = 0x3498DB  # 藍色 (blue)
        ERROR = 0xE74C3C  # 紅色 (red)
        WARNING = 0xF1C40F  # 黃色 (yellow)
        SUCCESS = 0x2ECC71  # 綠色 (green)

    class OilColor:
        RISE = 0xE74C3C  # 上漲 → 紅色
        FALL = 0x2ECC71  # 下跌 → 綠色
        STABLE = 0xB3B3B4  # 持平 → 灰色
        UNKNOWN = 0x95A5A6  # 狀態不明 → 淺灰
