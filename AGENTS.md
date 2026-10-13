# 新增与修改 case

- 根 `manifest.json` 是数组。每个新 case 恰好新增一条，包含 `title`、唯一 kebab-case `name`、`cover`、`case`、`introduction`，不要修改 schema 来容纳缺失数据。
- `title` 是展示标题，`name` 是稳定标识及 S3 前缀，二者不强制等于目录名。目录统一为 `usecases/<目录>/`，同一 case 的三个资源共享目录。
- 三种资源均须包含下表五个字段，包括全远程资源。封面须是图片，包为 `.science`，介绍为 `.md`。

| 字段 | 含义 |
| --- | --- |
| `file_name` | 真实文件名，与 path 最后一段一致 |
| `path` | 仓库相对路径 `usecases/<目录>/<文件名>`，远程来源也保留 |
| `bytes` | 实际字节数，非负整数 |
| `sha256` | 实际文件 SHA-256，恰好 64 位十六进制，无空白 |
| `release_url` | 空字符串选本地文件；非空选 HTTP(S) 远程资源 |

- 任意本地来源要求目录及对应普通文件存在，不接受符号链接。全远程条目不要求本地目录。`.science` 只提供一个来源，远程包不要同时放同路径本地文件。
- 介绍必须非空并准确说明 case。完成新增前阅读真实介绍内容，不使用空文档、占位文字或 README 替代；远程介绍也须在上传前完成内容检查。
- 内容最终确定后，从用户设备上的真实文件计算三个资源的大小和 SHA。远程资源上传前也从本地原文件计算，不复用其他文件摘要、不猜测值；内容变更后重新计算。

```sh
wc -c < 'usecases/目录/文件名'
shasum -a 256 'usecases/目录/文件名'
```

# 提交前检查

检查字段及类型、唯一 name、资源类型、安全路径、文件名、真实大小、SHA 和来源选择。目录迁移只更新 path，保持资源内容及其他 metadata 不变。提交遵循 Conventional Commits。

运行 `python3 -B -m unittest discover -s .github/tests -v`。对准备提交的目标运行 [校验命令](.github/CHECKING.md#命令)。check 不下载正文、不重算 SHA，仅检查格式、远程 HEAD、大小及 Git 对象与声明一致性；实际 SHA 验证由发布准备阶段完成。

复杂的来源组合与 HEAD 行为见 [.github/CHECKING.md](.github/CHECKING.md)；S3 基线、差异、强制上传、去重、暂存、解压、checkpoint、失败恢复及迁移验收见 [.github/PUBLISHING.md](.github/PUBLISHING.md)。测试只用临时 Git、本地 HTTP、fake S3，未经用户授权不得真实发布。
