# ⭐ starsnapshot

GitHub 星标快照工具 —— 自动抓取某个用户的 starred 仓库，生成 Markdown 统计报告。

纯 Python 标准库实现，**零依赖**，配 GitHub Actions 可**每天自动更新报告**。

## 功能

- 抓取用户所有 starred 仓库（自动分页）
- 按语言聚合统计
- Top 10 高星仓库 & 最近 star 的仓库
- 输出 Markdown 报告
- 未认证限速 60 次/小时；设置 `GH_TOKEN` 后 5000 次/小时

## 用法

```bash
python starsnapshot.py <username> [--out stars.md]
```

示例：

```bash
GH_TOKEN=ghp_xxx python starsnapshot.py Miku-3993 --out stars.md
```

## 自动化

`.github/workflows/daily.yml` 每天 08:00 UTC 自动生成报告并提交回仓库：

- 每次 push 会看到机器人提交（`chore: update stars report`）
- 也可以手动触发：仓库 → Actions → **Daily Stars Report** → Run workflow

## 测试

```bash
python -m unittest discover -v
```

## 许可

[MIT](LICENSE)