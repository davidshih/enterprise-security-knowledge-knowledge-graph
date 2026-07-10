# Enterprise Security Knowledge Graph

這是一個以金融業 AppSec／Cloud Security 為背景的「企業安全知識圖譜」起始專案。第一版先把最容易被忽略、但日後最難補救的東西釘死：canonical ID、實體／關係契約、來源證據、資料品質閘門，以及可解釋的風險分數。

完整設計與執行計畫請看 [`docs/PLAN.md`](docs/PLAN.md)。

## 目前可執行內容

- 將 source-neutral JSONL 轉成 canonical graph JSON。
- 每個節點與關係都必須帶 evidence。
- 使用 deterministic ID，避免同一資產每次匯入都長出分身。
- 拒絕指向不存在節點的 dangling relationship。
- 提供可解釋、可版本化的 0–100 MVP risk score。
- 使用 Python standard library 即可跑 demo 與測試。

## 快速開始

需求：Python 3.11+、Make。

```bash
make test
make lint
make demo
```

輸出會寫入：

```text
data/out/canonical_graph.json
```

不使用 Make 也可直接執行：

```bash
PYTHONPATH=src python3 -m security_graph ingest \
  --input data/sample/records.jsonl \
  --output data/out/canonical_graph.json
```

## 專案結構

```text
enterprise-security-knowledge-graph/
├── config/                 # Sources, access policy, and risk policy
├── data/sample/            # Safe synthetic input data
├── docs/PLAN.md            # Full implementation plan
├── examples/queries.cypher # Analyst and attack-path queries
├── schema/graph-model.yaml # Canonical entity/relationship contract
├── src/security_graph/     # Runnable Python normalization core
└── tests/                  # Contract and risk-model tests
```

## 下一個工程步驟

先完成 AWS Organizations／AWS Config／Security Hub、Snyk Enterprise、Entra ID 四個 read-only adapter，再依 `docs/PLAN.md` 的 Phase 1 驗收標準做一條端到端薄切。不要一開始就接十幾套 SaaS；那樣通常只會得到一座資料很豐富、答案不可信的圖資料垃圾山。

## GitHub Pages 知識庫

`website/` 提供 dependency-free 的靜態知識庫首頁，並由 `.github/workflows/pages.yml` 自動部署。每次 build 都會從目前版本的 plan、schema、queries、OpenAPI 與 policies 產生 knowledge bundle，避免網站內容和 repository 各自活在平行宇宙。

```bash
make site
make site-serve
```

本機預覽網址為 `http://localhost:8000`。推送 `main` 後，GitHub Actions 會自動發布最新版本。
