# Case 校验

校验入口是根 `manifest.json` 中新增或修改后仍存在的条目。仅资源文件变化、删除条目、排序或 JSON 排版变化不会主动扫描其他 case。全远程条目无需本地目录，也会被选中。`name` 在整个索引中唯一；标题和目录名可独立命名。

## 字段规则

顶层是数组，每条包含 `title`、`name`、`cover`、`case`、`introduction`。三种资源使用同一结构：

| 字段 | 要求 |
| --- | --- |
| `file_name` | 实际文件名，等于 `path` 最后一段 |
| `path` | `usecases/<目录>/<文件名>`；同一 case 三种资源共用目录；远程也保留 |
| `bytes` | 非负整数字节数；布尔值、字符串均不接受 |
| `sha256` | 64 位十六进制，无空白；比较时忽略大小写 |
| `release_url` | `""` 表示本地；非空表示有效 HTTP(S) 下载 URL，不能仅含空白 |

封面扩展名须为图片类型；包为 `.science`；介绍为 `.md`。不接受重复 JSON 字段、缺失或未知字段、绝对路径、反斜杠、控制字符、空路径段和 `.` / `..`。新 manifest 必须显式提供三个 `release_url`；历史 S3 基线允许旧根目录路径，封面和介绍缺失 URL 时按空字符串比较。

## 来源与检查

| cover | case | introduction | 本地检查 | 远程检查 |
| --- | --- | --- | --- | --- |
| 本地 | 本地 | 本地 | 目录及三个文件 | 无 |
| 远程 | 本地 | 本地 | 目录、包、介绍 | 封面 HEAD |
| 本地 | 远程 | 本地 | 目录、封面、介绍；包路径不得另有本地包 | 包 HEAD |
| 本地 | 本地 | 远程 | 目录、封面、包 | 介绍 HEAD |
| 远程 | 远程 | 本地 | 目录、介绍；包路径不得另有本地包 | 封面、包 HEAD |
| 远程 | 本地 | 远程 | 目录、包 | 封面、介绍 HEAD |
| 本地 | 远程 | 远程 | 目录、封面；包路径不得另有本地包 | 包、介绍 HEAD |
| 远程 | 远程 | 远程 | 跳过目录和文件检查 | 三个资源分别 HEAD |

本地来源检查目录、普通文件、符号链接、文件名与路径、实际大小。`.science` 必须只选一个来源：采用远程来源时不要保留同路径本地包。全远程条目仅以三个 URL 为来源，按上表跳过本地检查。

远程 HEAD 必须返回 HTTP 200，且 `Content-Length` 为合法整数并与声明一致。301/302/303/307/308 重定向继续使用 HEAD。不可访问、超时、不支持 HEAD、缺失或错误的大小均失败，不回退 GET。每次连接超时为 15 秒。

check 阶段不下载正文、不重算 SHA。Git 声明检查使用已提交普通文件的 Git 对象 ID，发现资源内容改变而 SHA 声明未同步时失败；它不证明 SHA 等于实际内容。实际大小和 SHA 校验在发布准备阶段完成。

## 命令

从仓库根目录运行，checkout 必须对应待检查提交，manifest 不得有未提交变化：

```sh
CASES_JSON="$(python3 .github/scripts/check_structure.py directories --base <BASE_SHA>)" \
  python3 .github/scripts/check_structure.py manifest
python3 .github/scripts/check_structure.py declarations --base <BASE_SHA> --after <HEAD_SHA>
python3 -B -m unittest discover -s .github/tests -v
```

PR 使用 merge-base 到固定 PR head 的范围。新分支可传 `--new-branch-base`；全零 base 且无新分支基线时检查所有条目。发布流程用 `manifest --plan <计划文件>` 检查相对 S3 基线变动的条目。安全发布、暂存与失败恢复见 [PUBLISHING.md](PUBLISHING.md)。
