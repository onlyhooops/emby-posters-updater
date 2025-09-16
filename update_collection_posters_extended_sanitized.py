#!/usr/bin/env python3
"""
Emby 封面更新工具（合集 / 流派 / 标签）- 脱敏版

说明：本脚本为可分享版本，已移除服务器地址与密钥等敏感信息。
使用前请先填写脚本开头的 EMBY_SERVER、API_KEY、USER_ID。

功能：
- 通过 Emby API 清空并更新「合集」「流派」「标签」的封面
- 纯 API 实现（不访问文件系统），通过 RemoteImages API 复制封面
- 支持交互式菜单，非交互环境下自动选择默认流程
"""

import requests

# ================= 配置（使用前请先填写） =================
EMBY_SERVER = "http://YOUR_EMBY_HOST:8096"   # 例如: http://192.168.1.5:8096
API_KEY = "YOUR_EMBY_API_KEY"                # 例如: abcdef0123456789...
USER_ID = "YOUR_USER_ID"                     # 例如: 147357e3acb4...

HEADERS = {
    "X-Emby-Token": API_KEY,
    "Content-Type": "application/json"
}


# ================= 工具函数 =================
def safe_request(method, url, **kwargs):
    try:
        resp = requests.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp
    except requests.RequestException as e:
        print(f"[错误] 请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"        状态码: {e.response.status_code}")
            print(f"        响应体: {e.response.text}")
        return None

def info(msg):
    print(f"[信息] {msg}")

def ok(msg):
    print(f"[成功] {msg}")

def warn(msg):
    print(f"[警告] {msg}")

def err(msg):
    print(f"[错误] {msg}")


# ================= 查询 API =================
def get_all_collections():
    url = f"{EMBY_SERVER}/Users/{USER_ID}/Items"
    params = {"IncludeItemTypes": "BoxSet", "Recursive": "true", "Fields": "ImageTags"}
    r = safe_request("GET", url, headers=HEADERS, params=params)
    return (r.json().get("Items", []) if r else [])

def get_all_genres():
    r = safe_request("GET", f"{EMBY_SERVER}/Genres", headers=HEADERS, params={"Fields": "ImageTags"})
    return (r.json().get("Items", []) if r else [])

def get_all_tags():
    r = safe_request("GET", f"{EMBY_SERVER}/Tags", headers=HEADERS, params={"Fields": "ImageTags"})
    return (r.json().get("Items", []) if r else [])

def get_collection_items(collection_id):
    params = {"ParentId": collection_id, "Recursive": "true", "Fields": "ImageTags,Name,Type"}
    r = safe_request("GET", f"{EMBY_SERVER}/Items", headers=HEADERS, params=params)
    return (r.json().get("Items", []) if r else [])

def get_items_by_genre(genre_name):
    params = {"Genres": genre_name, "Recursive": "true", "Fields": "ImageTags,Name,Type", "IncludeItemTypes": "Movie"}
    r = safe_request("GET", f"{EMBY_SERVER}/Items", headers=HEADERS, params=params)
    return (r.json().get("Items", []) if r else [])

def get_items_by_tag(tag_name):
    params = {"Tags": tag_name, "Recursive": "true", "Fields": "ImageTags,Name,Type", "IncludeItemTypes": "Movie"}
    r = safe_request("GET", f"{EMBY_SERVER}/Items", headers=HEADERS, params=params)
    return (r.json().get("Items", []) if r else [])


# ================= 核心辅助函数 =================
def clear_item_images(item_id, item_name):
    ok_types = 0
    for t in ["Primary", "Art", "Thumb", "Banner"]:
        r = safe_request("DELETE", f"{EMBY_SERVER}/Items/{item_id}/Images/{t}", headers=HEADERS)
        if r and r.status_code in (200, 204):
            ok_types += 1
            ok(f"已清空 {item_name} 的 {t}")
        else:
            warn(f"清空 {item_name} 的 {t} 失败")
    return ok_types > 0

def pick_first_movie_with_primary(items):
    movies = [i for i in items if i.get("Type") == "Movie"]
    movies.sort(key=lambda x: x.get("Name", ""))
    for m in movies:
        tags = m.get("ImageTags") or {}
        if "Primary" in tags:
            return m
    return None

def set_poster_from_item(target_id, target_name, source_item_id):
    src_url = f"{EMBY_SERVER}/Items/{source_item_id}/Images/Primary"
    dl_url = f"{EMBY_SERVER}/Items/{target_id}/RemoteImages/Download"
    params = {"ImageUrl": src_url, "ProviderName": "Manual", "ImageType": "Primary"}
    r = safe_request("POST", dl_url, headers=HEADERS, params=params)
    if r and r.status_code in (200, 204):
        ok(f"已更新 {target_name} 的封面")
        return True
    err(f"更新 {target_name} 的封面失败")
    return False


# ================= 工作流 =================
def process_collection(col):
    cid, name = col["Id"], col["Name"]
    info(f"处理合集: {name}")
    if not clear_item_images(cid, name):
        warn(f"跳过 {name}: 清空失败")
        return False
    items = get_collection_items(cid)
    src = pick_first_movie_with_primary(items)
    if not src:
        warn(f"跳过 {name}: 未找到带主封面的影片")
        return False
    return set_poster_from_item(cid, name, src["Id"])

def process_genre(genre):
    gid, name = genre["Id"], genre["Name"]
    info(f"处理流派: {name}")
    if not clear_item_images(gid, name):
        warn(f"跳过 {name}: 清空失败")
        return False
    items = get_items_by_genre(name)
    src = pick_first_movie_with_primary(items)
    if not src:
        warn(f"跳过 {name}: 未找到带主封面的影片")
        return False
    return set_poster_from_item(gid, name, src["Id"])

def process_tag(tag):
    tid, name = tag["Id"], tag["Name"]
    info(f"处理标签: {name}")
    if not clear_item_images(tid, name):
        warn(f"跳过 {name}: 清空失败")
        return False
    items = get_items_by_tag(name)
    src = pick_first_movie_with_primary(items)
    if not src:
        warn(f"跳过 {name}: 未找到带主封面的影片")
        return False
    return set_poster_from_item(tid, name, src["Id"])


# ================= 命令行入口 =================
def main():
    import sys
    info("Emby 封面更新工具（脱敏版）")
    info(f"服务器: {EMBY_SERVER}")
    info(f"用户ID: {USER_ID}")

    # 连接性快速检查
    ping = safe_request("GET", f"{EMBY_SERVER}/System/Info", headers=HEADERS)
    if not ping:
        err("无法连接到 Emby 服务器，请检查 EMBY_SERVER/API_KEY。")
        return

    interactive = sys.stdin.isatty()
    if interactive:
        print("\n请选择要执行的流程：")
        print("1) 合集 Collections")
        print("2) 流派 Genres")
        print("3) 标签 Tags")
        print("4) 全部 All")
        print("0) 退出 Exit")
        choice = input("> ").strip()
    else:
        choice = "1"  # 非交互环境默认执行合集流程

    if choice == "0":
        info("已退出")
        return

    if choice in ("1", "4"):
        cols = get_all_collections()
        for c in cols:
            process_collection(c)

    if choice in ("2", "4"):
        for g in get_all_genres():
            process_genre(g)

    if choice in ("3", "4"):
        for t in get_all_tags():
            process_tag(t)

    ok("处理完成")


if __name__ == "__main__":
    main()


