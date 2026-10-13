# AIPOCH Open-Science 案例

本仓库收集完成的 Open-Science 会话导出、封面和介绍，根 `manifest.json` 是案例索引。

案例统一放在 `usecases/<目录>/`。每个条目包含 `title`、唯一 kebab-case `name`，以及 `cover`、`case`、`introduction` 三种资源；每种资源都提供 `file_name`、`path`、`bytes`、`sha256`、`release_url`。URL 为空时采用本地文件，非空时采用远程资源；全远程条目可不创建本地目录，但仍保留规范 path。

```text
usecases/示例目录/
  cover.png
  session.science
  introduction.md
```

目录、标题与 name 可独立命名。S3 始终使用 `<name>/<file_name>`，包解压内容位于 `<name>/extracted/`，目录迁移不改变 S3 资源键。

原始 `.science` 会话内容保持不变。案例中标明的模拟演示和未解决结论仍以源会话为准，收录不代表模型的一般性能保证。

- [新增和修改案例](AGENTS.md)
- [校验规则与命令](.github/CHECKING.md)
- [发布、去重与恢复](.github/PUBLISHING.md)

本地测试：`python3 -B -m unittest discover -s .github/tests -v`。测试使用临时数据及 fake S3，不执行真实发布。
