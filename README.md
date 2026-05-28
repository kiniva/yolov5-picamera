# YOLOv5 客製化修改版本

本專案包含基於 [YOLOv5](https://github.com/ultralytics/yolov5/tree/master)（由 Ultralytics 開發）所修改的檔案。

以下檔案為客製化修改版本，用於**覆蓋**原始 YOLOv5 儲存庫中的對應檔案：

| 檔案 | 覆蓋目標路徑 |
|------|-------------|
| `dataloader.py` | `./yolov5/utils/dataloader.py` |
| `detect.py` | `./yolov5/detect.py` |

---

## 環境需求

- [Git](https://git-scm.com/)
- Python 3.8+
- YOLOv5 `requirements.txt` 中所列之相依套件

---

## 使用方式

**步驟一 — 克隆 YOLOv5 儲存庫**

```bash
git clone https://github.com/ultralytics/yolov5.git
```

**步驟二 — 下載本專案的檔案**

下載或克隆本儲存庫以取得修改後的檔案：

```bash
git clone <本專案的儲存庫網址>
```

**步驟三 — 覆蓋 `dataloader.py`**

將修改後的 `dataloader.py` 複製至 YOLOv5 的 `utils` 資料夾：

```bash
cp dataloader.py ./yolov5/utils/dataloader.py
```

**步驟四 — 覆蓋 `detect.py`**

將修改後的 `detect.py` 複製至 YOLOv5 的根目錄：

```bash
cp detect.py ./yolov5/detect.py
```

---

## 注意事項

- 本專案的修改基於原始 YOLOv5 程式碼，請確認使用相容的 YOLOv5 版本。
- 一般使用方式請參閱原始 [YOLOv5 文件](https://docs.ultralytics.com/)。

---

## 致謝

原始 YOLOv5 專案由 [Ultralytics](https://github.com/ultralytics/yolov5) 開發。本專案僅包含修改後的檔案，並未重新發布完整的 YOLOv5 原始碼。
