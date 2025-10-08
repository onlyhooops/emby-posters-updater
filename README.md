# Emby 封面更新工具 v2.0

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/onlyhooops/emby-posters-updater)
[![Emby](https://img.shields.io/badge/Emby-4.0%2B-green.svg)](https://emby.media/)
[![Python](https://img.shields.io/badge/python-3.7%2B-brightgreen.svg)](https://www.python.org/)

## 🎉 v2.0 重大更新

**已适配 Emby v4.9+ 最新API！** 同时保持对旧版本的完全兼容。

### 更新内容
- ✅ 支持 Emby v4.9+ 新版图像API
- ✅ 自动检测并回退到旧版API（兼容 v4.0+）
- ✅ 无需用户干预，自动适配服务器版本
- ✅ 所有功能测试通过

### API 变更说明
- **删除图像**: 新版使用 `POST /Items/{Id}/Images/{Type}/Delete`
- **上传图像**: 新版使用 `Type` 参数（替代 `ImageType`）
- 脚本会自动尝试新版API，失败时回退到旧版

---

> 一键运行（复制即用）

```bash
# 1) 安装依赖（仅首次）
pip install --upgrade pip requests

# 2) 下载最新脚本
curl -L -o emby-poster-updater.py   https://raw.githubusercontent.com/onlyhooops/emby-posters-updater/main/emby-poster-updater.py

# 3) 编辑脚本开头的配置（EMBY_SERVER / API_KEY / USER_ID）
# macOS: open -e emby-poster-updater.py    或    Windows: notepad emby-poster-updater.py

# 4) 运行
python3 emby-poster-updater.py
```


本说明对应脚本 `emby-poster-updater.py`。
脚本已移除敏感配置，使用前请先填写必要参数。

## 功能说明
- 批量清空并更新以下类型的封面：
  - 合集（Collections/BoxSets）
  - 流派（Genres）
  - 标签（Tags）
- 纯 Emby API 实现（不访问文件系统）
- 通过 RemoteImages API 将首个带主封面的影片图像复制为目标封面
- 交互式命令行，支持非交互场景自动化

## 填写配置
打开脚本顶部并填写：
```python
EMBY_SERVER = "http://YOUR_EMBY_HOST:8096"
API_KEY = "YOUR_EMBY_API_KEY"
USER_ID = "YOUR_USER_ID"
```

## 运行环境
- **Python**: 3.7+
- **依赖**: `pip install requests`
- **网络**: 可访问 Emby Server
- **权限**: API Key 需具备管理员权限（图像管理）
- **Emby版本**: 4.0+ (推荐 4.9+)

## 运行
交互模式：
```bash
python3 emby-poster-updater.py
```
会提示选择：
- 1) 合集 Collections
- 2) 流派 Genres
- 3) 标签 Tags
- 4) 全部 All

非交互模式（如 cron/CI）：
- 默认执行选项 1（合集）

## 使用到的 API 端点

### 查询API（所有版本通用）
- 获取合集：`GET /Users/{userId}/Items?IncludeItemTypes=BoxSet`
- 获取流派：`GET /Genres`
- 获取标签：`GET /Tags`
- 获取合集成员：`GET /Items?ParentId={collectionId}`
- 按流派名称过滤：`GET /Items?Genres={genreName}&IncludeItemTypes=Movie`
- 按标签名称过滤：`GET /Items?Tags={tagName}&IncludeItemTypes=Movie`

### 图像操作API（v2.0支持新旧版本）

#### 删除图像
- **新版 (Emby v4.9+)**: `POST /Items/{itemId}/Images/{imageType}/Delete`
- **旧版 (Emby v4.0-4.8)**: `DELETE /Items/{itemId}/Images/{imageType}`
- 脚本会自动选择合适的版本

#### 复制图像
- **新版 (Emby v4.9+)**: `POST /Items/{itemId}/RemoteImages/Download?Type=Primary&ImageUrl=...&ProviderName=Manual` (需要JSON body)
- **旧版 (Emby v4.0-4.8)**: `POST /Items/{itemId}/RemoteImages/Download?ImageType=Primary&ImageUrl=...&ProviderName=Manual`
- 脚本会自动选择合适的版本

## 安全建议
- 执行前建议备份 Emby 数据库
- 网络失败会被捕获，单项失败不会中断整体流程
- 本脚本仅通过 Emby API 上传，不会访问媒体文件

## 故障排查
- **401/403 认证失败**: 检查 API Key 与权限，确认具有管理员权限
- **404 资源未找到**: 检查服务器地址与资源 ID
- **某流派/标签无条目**: 请确认使用"名称"筛选而非"ID"
- **封面未更新**: 确认该组下存在至少一个带 Primary 图像的影片
- **API版本问题**: 脚本会自动适配，如有问题请查看日志中的"旧版API"提示
- **日志显示"旧版API"**: 说明您的Emby版本低于4.9，这是正常的兼容行为

## 许可
- 分享前请再次脱敏，勿包含任何私密信息。




## 免责声明
- 本工具会批量修改 Emby 项目的封面图像，可能影响现有外观与数据。
- 使用前请务必备份 Emby 数据库与配置（通常为 `config` 目录或容器挂载路径）。
- 任何因使用本工具导致的数据丢失、显示异常、不可预期问题，均由使用者自行承担风险与责任。
- 在生产环境使用前，建议先在测试库中进行验证。
## 零基础快速上手

### 1. 准备环境（macOS / Windows / Linux 通用）
- 安装 Python 3（官方地址或应用商店均可）。
- 打开终端（Windows 打开 PowerShell）。
- 安装依赖：
```bash
pip install --upgrade pip
pip install requests
```

### 2. 下载脚本
- 访问仓库主页，点击 Code ➜ Download ZIP
- 解压后进入目录（例如 `emby-posters-updater`）

### 3. 填写配置
用文本编辑器打开 `emby-poster-updater.py`，在开头找到：
```python
EMBY_SERVER = "http://YOUR_EMBY_HOST:8096"
API_KEY = "YOUR_EMBY_API_KEY"
USER_ID = "YOUR_USER_ID"
```
将其替换为你自己的 Emby 服务器地址、API 密钥和用户ID。

### 4. 运行脚本
```bash
python3 emby-poster-updater.py
```
- 交互模式会提示选择：合集 / 流派 / 标签 / 全部
- 非交互环境（如定时任务）将默认执行合集流程

### 5. 常见问题
- **提示认证失败**: 检查 API KEY 是否有效，**必须具有管理员权限**
- **找不到影片**: 确认媒体库已扫描且影片存在
- **封面未更新**: 该组下需至少有一个影片带 Primary 图像
- **日志显示"旧版API"**: 说明您的Emby版本 < 4.9，这是正常的兼容模式

## 版本历史

### v2.0 (2025-10-08)
- ✅ 适配 Emby v4.9+ 新版API
- ✅ 支持自动回退到旧版API
- ✅ 兼容 Emby v4.0-v4.9+
- ✅ 更新API文档说明

### v1.0
- 初始版本
- 支持合集/流派/标签封面更新