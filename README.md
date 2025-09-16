# Emby 封面更新工具 - 脱敏版使用说明

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
- Python 3.7+
- 安装依赖：`pip install requests`
- 运行机可访问 Emby Server
- API Key 具备图像管理权限

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
- 获取合集：`GET /Users/{userId}/Items?IncludeItemTypes=BoxSet`
- 获取流派：`GET /Genres`
- 获取标签：`GET /Tags`
- 获取合集成员：`GET /Items?ParentId={collectionId}`
- 按流派名称过滤：`GET /Items?Genres={genreName}&IncludeItemTypes=Movie`
- 按标签名称过滤：`GET /Items?Tags={tagName}&IncludeItemTypes=Movie`
- 清空图像：`DELETE /Items/{itemId}/Images/{imageType}`（Primary/Art/Thumb/Banner）
- 复制图像：`POST /Items/{itemId}/RemoteImages/Download?ImageUrl=...&ProviderName=Manual&ImageType=Primary`

## 安全建议
- 执行前建议备份 Emby 数据库
- 网络失败会被捕获，单项失败不会中断整体流程
- 本脚本仅通过 Emby API 上传，不会访问媒体文件

## 故障排查
- 401/403：检查 API Key 与权限
- 404：检查服务器地址与资源 ID
- 某流派/标签无条目：请确认使用“名称”筛选而非“ID”
- 封面未更新：确认该组下存在至少一个带 Primary 图像的影片

## 许可
- 分享前请再次脱敏，勿包含任何私密信息。
