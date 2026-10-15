# herta-data

崩坏：星穹铁道 深渊类玩法（混沌回忆 / 虚构叙事 / 末日幻影 / 异相仲裁）低配通关记录数据，供 [game-toolbox](https://github.com/Ca5tor1ce-vesna/game-toolbox) 的「角色顶分」模块读取。

- 数据来自 **The Herta**（https://theherta.com ），每天 **12:00（北京时间）** 更新。
- 只保留阵容与配置信息，不包含上传者账号、视频链接。

## 文件

| 路径 | 说明 |
|---|---|
| `data/latest.json` | 最新数据 |
| `data/latest.sha256` | latest.json 的 SHA-256（`<hex>  latest.json`），客户端下载后校验 |
| `data/history/YYYYMMDD.json` | 每日存档 |
| `scripts/publish.py` | 校验并发布新数据：`python scripts/publish.py herta_zh.json` |

## 选取规则

对每个模式的当前关卡/分类，把记录按「阵容组」（主C）分组，每组取 **限定五星数最少** 的一条；同数取 **常驻五星更少** 的，再同数取 **更早** 的。

## 字段说明

顶层：`source` 来源页面，`collected_at` 采集时间（UTC+8），`selection_rule` 选取规则，`targets` 列表。

`targets[]`：
- `mode` 模式：混沌回忆 / 虚构叙事 / 末日幻影 / 异相仲裁
- `season` 版本期数，`stage` 关卡名（中文），`stage_en` 英文原名
- `category` 分类（如 0轮次、满分）
- `total_runs` 该分类原始记录总数
- `records[]`：
  - `group` 阵容组名，`runs_in_group` 该组记录数
  - `lineup[]`：`name` 角色，`eidolon` 星魂（E0–E6），`superimposition` 光锥叠影（S1–S5），`lightcone` 光锥中文名（可选，可能为 null）
  - `tag` 分类标签，`cycle` 轮次，`score` 积分（虚构/末日），`av` 行动值（如有）
  - `ltd` / `std` 限定 / 常驻五星数量
  - `date` 记录时间
