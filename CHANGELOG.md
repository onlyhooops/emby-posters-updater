# 更新日志 (Changelog)

## [v2.0] - 2025-10-08

### 🎉 重大更新

**适配 Emby v4.9+ 最新API规范，同时保持对旧版本的完全兼容！**

### ✨ 新增功能

- **新版API支持**: 完整支持 Emby v4.9+ 的新版图像操作API
- **自动版本检测**: 脚本自动检测并使用合适的API版本
- **向后兼容**: 自动回退到旧版API，支持 Emby v4.0-v4.8

### 🔧 API 变更详情

#### 删除图像API
- **新版** (Emby v4.9+): `POST /Items/{Id}/Images/{Type}/Delete`
- **旧版** (Emby v4.0-4.8): `DELETE /Items/{Id}/Images/{Type}`
- 脚本优先使用新版API，失败时自动回退到旧版

#### 上传图像API
- **新版** (Emby v4.9+): 
  - 参数名从 `ImageType` 改为 `Type`
  - 需要发送JSON请求体（空对象 `{}`）
  - `POST /Items/{Id}/RemoteImages/Download?Type=Primary&...`
- **旧版** (Emby v4.0-4.8):
  - 使用 `ImageType` 参数
  - `POST /Items/{Id}/RemoteImages/Download?ImageType=Primary&...`
- 脚本优先使用新版API，失败时自动回退到旧版

### 📝 更新的函数

#### `clear_item_images()`
```python
# v2.0: 新增新版API支持和自动回退机制
def clear_item_images(item_id, item_name):
    # 优先尝试新版API (POST method)
    # 失败时自动回退到旧版API (DELETE method)
```

#### `set_poster_from_item()`
```python
# v2.0: 新增Type参数支持和JSON body
def set_poster_from_item(target_id, target_name, source_item_id):
    # 优先尝试新版API (Type参数 + JSON body)
    # 失败时自动回退到旧版API (ImageType参数)
```

### 🎯 兼容性

- ✅ Emby v4.9+ (新版API)
- ✅ Emby v4.0-v4.8 (旧版API)
- ✅ Python 3.7+
- ✅ 所有功能测试通过

### 📚 文档更新

- ✅ README.md - 添加v2.0更新说明
- ✅ README.md - 更新API端点文档
- ✅ README.md - 添加版本历史
- ✅ README.md - 更新故障排查指南
- ✅ 脚本注释 - 添加v2.0更新说明

### 🧪 测试

- ✅ Emby v4.9.1.80 - 新版API测试通过
- ✅ 向后兼容测试通过
- ✅ 合集封面更新测试通过
- ✅ 流派封面更新测试通过
- ✅ 标签封面更新测试通过

### 💡 使用建议

1. **首次升级**: 建议在测试环境验证
2. **日志提示**: 如果看到"旧版API"提示，说明您的Emby < v4.9，这是正常的
3. **权限要求**: 确保API密钥具有管理员权限
4. **备份数据**: 执行前建议备份Emby数据库

---

## [v1.0] - 2024

### ✨ 初始发布

- 支持合集(BoxSet)封面更新
- 支持流派(Genres)封面更新
- 支持标签(Tags)封面更新
- 纯API实现，不依赖文件系统
- 交互式菜单
- 非交互模式支持

---

## 反馈与支持

如遇到问题或有建议，欢迎：
- 提交 Issue
- 发起 Pull Request
- 查看 README.md 故障排查章节

**感谢使用 Emby 封面更新工具！** 🎉

