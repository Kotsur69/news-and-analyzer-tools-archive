# News & Analyzer Tools — Archive

Early experiments (Jan 2026) in **local-LLM market analysis**: scraping steel-industry news,
parsing PDF/Excel price reports, and asking a locally hosted model (LM Studio / Ollama) to
summarize the market and forecast price direction, then checking its own predictions.

These seven tools were separate repos, built iteratively. Each one is the next step from
the one before it. They're merged here with their commit history so the progression stays visible.

> **Archived — not maintained.** Sample input reports (PDF/Excel) and generated analysis output
> are included in each folder so you can see what the tools consumed and produced.

| Folder | What it does |
|---|---|
| [`steel-news-crawler`](steel-news-crawler) | Crawls configured news sites, picks random links, keeps the ones that look like articles, and sends them to a local LLM for a market summary. |
| [`steel-news-crawler-gui`](steel-news-crawler-gui) | The same crawler with a simple GUI and an editable URL list. |
| [`steel-news-predictor`](steel-news-predictor) | Scrapes price-action news, forecasts from historical values, and tracks how accurate its own past predictions were. |
| [`steel-news-pdf-excel-analyzer`](steel-news-pdf-excel-analyzer) | Combines scraped news with PDF and Excel reports to forecast steel prices. URLs and prompts can be swapped for any domain. |
| [`pdf-excel-llm-analyzer`](pdf-excel-llm-analyzer) | Bulk analysis of PDF and Excel price data with a configurable analyst prompt. |
| [`pdf-excel-price-forecaster`](pdf-excel-price-forecaster) | Month-by-month analysis of the report history: forecasts, validates each forecast against the next month, explains hits and misses, and adds a risk assessment. |
| [`excel-sales-analyzer`](excel-sales-analyzer) | Analyzes multi-year sales from Excel, draws charts, and writes an LLM commentary (top products, trends). |

**Stack:** Python · web scraping · PDF/Excel parsing · pandas · matplotlib ·
local LLMs via LM Studio / Ollama.
