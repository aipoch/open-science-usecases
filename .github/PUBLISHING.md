# Case 发布

发布从目标 S3 的 `manifest.json` 读取基线，对比固定 checkout 的 manifest。Git push 范围不作为发布基线。只有明确的 `NoSuchKey` 表示首次发布；权限、网络、无效 JSON 或不合法索引都使准备失败。

## 差异规则

索引更新与资源上传分别判断。历史 S3 索引支持旧根目录路径，封面及介绍缺失 `release_url` 时按 `""` 比较；兼容读取旧索引缺少 introduction 的条目，以便补齐升级；新索引须遵循 [CHECKING.md](CHECKING.md)。SHA 比较忽略十六进制字母大小写。

| 变化 | 发布行为 |
| --- | --- |
| 仅 `path` | 校验新来源路径，更新索引；不上传、解压或删除资源 |
| 仅 `title` | 更新索引 |
| 补充 `release_url: ""` | 更新索引，不算来源变化 |
| URL 空变非空、换 URL、非空变空 | 对应资源强制准备和上传，优先于去重 |
| `sha256`、`bytes`、`file_name` | 对应资源进入候选清单 |
| `name` | 使用新 name 查找 S3 索引记录；有记录则增量比较，无记录则视为新增 |
| 删除或排序 | 更新索引，保留已有资源对象 |
| 无相关资源声明变化 | 不 HEAD 扫描或修复对象；仍执行 FINAL_SYNC |

新 name 只有残留对象时继续正常准备：封面和介绍按候选去重规则验证目标，包仍准备、上传和解压。不得因前缀存在就跳过。旧 name 移出索引后旧对象保留。

S3 键始终由 `name` 和 `file_name` 决定，不采用仓库 `path`：

```text
<AWS_TARGET_FOLDER>/<name>/<file_name>
<AWS_TARGET_FOLDER>/<name>/extracted/...
<AWS_TARGET_FOLDER>/manifest.json
```

## 候选与去重

仅候选清单内、未强制上传的封面和介绍执行目标 S3 `HeadObject`。目标 `Metadata.sha256` 和 `ContentLength` 都匹配才跳过上传。缺对象、缺 metadata、SHA 或大小不匹配都准备并上传。403、网络和其他错误失败，不冒充缺对象；HeadObject 的明确 404/NoSuchKey/NotFound 才表示缺对象。

来源变化对三类资源一致：即使目标 metadata 相同也强制上传；`.science` 同时选择解压和替换。包不进行 metadata 去重。源下载 URL 的 metadata 不作为目标 S3 证据。

计划保存候选原因、`force_upload`、HEAD 证据、上传或跳过决定及原因。执行前再次 HEAD 所有跳过项；若此时不匹配，整个批次在写入前失败，应重新生成计划。

## 准备与解压

Action 分别控制条目校验、资源准备、包解压、manifest 发布。无资源上传时仍发布所需索引并执行 `FINAL_SYNC`。

本地来源读取固定 checkout 中的 `path`，复制到本次运行的临时目录；远程来源下载到该目录。所有选中文件都必须与声明的实际大小和 SHA 一致。所有文件准备成功、所有选中包解压成功后才允许任何 S3 写入。包上传和解压复用同一暂存文件，远程包只下载一次。封面、介绍、标题或路径变化不会选择包解压。

`.science` 是 gzip tar；解压保留 `session.json`、`records.json`、包内 `manifest.json`、`README.md` 原始字节。inventory 中资源通过 `storageKey` 恢复至 `extracted/` 对应路径，支持 `content-dedupe`；不发布中间 `objects/` 目录，不重写 `$DATA/` 历史数据。客户端需把 `$DATA/<storageKey>` 解析为对应 extracted URL，并对各路径段编码。

解压拒绝路径穿越、绝对路径、符号链接、硬链接、特殊文件、重复或跨平台冲突路径、不支持的格式/特性、缺失或未声明文件、错误大小/SHA、损坏或截断 gzip。执行前再次验证暂存内容，并从已验证包审计完整解压上传清单（不再次落盘解压），拒绝缺项、额外文件或改写 metadata。固定提交重新推导候选和 checkpoint，拒绝遗漏强制上传项、伪造跳过项或篡改计划。

## checkpoint 与写入

每个新增/更新 case 完成自身资源后才提交该步 manifest。顺序为：

1. 确认 S3 基线未变化；若包被选中，清理且仅清理 `<name>/extracted/`。
2. 上传本 case 的选中资源和解压文件，写入从实际上传字节计算的 `sha256` metadata，再 HEAD 验证大小和 metadata。
3. 条件写入根 manifest：已有对象使用 `If-Match` ETag，首次使用 `If-None-Match: *`。
4. 回读验证 manifest 原始文本一致，等待本步 CDN 刷新完成，然后进入下一步。
5. 最后 `FINAL_SYNC` 写入固定提交的 manifest 原始字节，回读并刷新整个发布前缀。

删除、排序及仅索引变化步骤没有资源清理。清理前缀的末尾 `/` 防止误删相似名称。条件冲突失败且不降级无条件写；只有不确定的传输失败允许通过回读确认 PUT 是否已完成。ETag 用于版本条件，不是内容 SHA。

串行 workflow 锁覆盖读取基线到最终发布。锁不使多对象写入原子化：包替换期间可能短暂缺文件；失败前成功上传的对象仍然存在。所有发布者都必须遵守同一锁。

## 证据、失败与恢复

`publication-plan.json` 及同名目录保存基线、候选、决定、完整计划、各步 manifest、文件清单、前后条目、`status.json`、`events.jsonl` 和 `summary.md`。Actions 始终保存证据 artifact，保留 14 天，不上传暂存正文。日志也显示去重证据；URL 不应携带凭据。

步骤状态为 `waiting`、`uploading`、`completed` 或 `failed`，分别记录 manifest 是否提交、回读验证和 CDN 状态。任何校验、准备、解压、删除、上传、回读或 CDN 失败立即停止，失败后不补跑 FINAL_SYNC。进程被终止时状态可能停留在 uploading，恢复仍以 S3 为准。

例如前两个 case 完成、第三个上传后索引写入失败：新运行读取前两个 case 的 checkpoint，只处理未完成的差异。第三个封面/介绍可经目标 metadata 去重，来源切换仍强制上传；包仍重新准备和解压。索引已提交但 CDN 失败时，新运行的 FINAL_SYNC 刷新整个前缀。

修复原因后在 main 发起新的 `workflow_dispatch`，不要使用原生 Re-run jobs；脚本和 Action 拒绝 `GITHUB_RUN_ATTEMPT != 1`。每次新运行使用新固定 SHA、新暂存和新 S3 基线。禁止复用完成解压的旧计划来重试解压。并发队列不保证提交祖先顺序，旧目标排队发布后可再 dispatch 当前 main。

没有主动对象修复或垃圾回收。声明未变时不会发现手动删除的对象，回退声明也不保证修复失败批次留下的对象变化。需要时单独安排明确的资源修复。

## usecases 迁移验收

目录整体迁移，资源内容、文件名、大小、SHA、name 和 title 不变；只修改 `path` 并补充空 URL 字段。以迁移前索引作为 fake S3 基线，必须证明资源候选/上传、包解压和 S3 删除清单均为空，新的 manifest 写入后回读一致，已有资源键及字节保持原状。

## 本地验证

```sh
python3 -B -m unittest discover -s .github/tests -v
```

测试使用临时 Git、本地 HTTP 和 fake S3，不访问正式 AWS。覆盖 HEAD 无 GET、来源组合/切换、增量候选、metadata 去重、准备完整性、解压安全、计划篡改、清理范围、逐 case 失败恢复和路径迁移的索引写入。真实 Actions 权限、AWS/CDN、线上消费者兼容性仍需合并后另行验证；本地通过不代表真实发布已执行。
