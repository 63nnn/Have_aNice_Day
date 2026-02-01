# Python 命名規範（繁體中文）

本表格整理了基於 **PEP 8** 的 Python 命名規範，確保程式碼與檔案名稱的一致性和可讀性，方便作為專案筆記。

| **物件類型** | **命名風格** | **範例** | **備註** |
| --- | --- | --- | --- |
| **變數** | `snake_case`（小寫） | `user_name`, `total_count` | 使用描述性名稱；避免單字母變數，除非是迴圈計數器（如 `i`）。 |
| **常數** | `UPPER_SNAKE_CASE`（全大寫） | `MAX_CONNECTIONS`, `PI` | 定義於模組層級，程式執行期間不應修改。 |
| **函數/方法** | `snake_case`（小寫） | `calculate_total_price`, `get_user_data` | 使用動詞描述功能，名稱需清晰簡潔。 |
| **類別** | `CamelCase`（駝峰式） | `UserProfile`, `DataProcessor` | 使用名詞或名詞短語，每個單詞首字母大寫。 |
| **模組（檔案）** | `lowercase` 或 `snake_case` | `user_utils.py`, `data_processing.py` | 保持簡短；避免連字符（`-`）和 `camelCase`（如 `userUtils.py`），以符合慣例和跨平台相容性。 |
| **套件** | `lowercase` | `mypackage/` | 簡短命名，必要時避免底線。 |
| **私有名稱** | `_snake_case` | `_internal_data`, `_private_method` | 單底線表示「受保護」（僅為約定），實際上仍可訪問。 |
| **強私有名稱** | `__snake_case` | `__secret_value` | 雙底線用於名稱改進，防止子類別覆蓋。 |
| **特殊方法** | `__dunder__` | `__init__`, `__str__` | 保留給特殊方法（魔術方法），避免在自訂名稱中使用雙底線。 |

## 其他建議

- **避免保留字**：不要使用 Python 關鍵字（例如 `class`、`def`、`if`）作為名稱。
- **使用英文命名**：在公開或協作專案中，建議以英文命名以保持一致性。
- **名稱描述性**：在簡潔與清晰間取得平衡（例如數學相關程式碼使用 `matrix` 而非 `array`）。
- **檔案命名注意**：模組和套件檔案名稱應避免 `camelCase` 或連字符，優先使用全小寫或 `snake_case`，以確保跨平台相容性和符合 Python 慣例。
- **使用工具檢查**：使用 `pylint`、`flake8` 或 `black` 等工具確保符合 PEP 8 規範。

本表格可作為 Python 專案的快速命名參考，確保程式碼與檔案名稱的一致性與可維護性。
