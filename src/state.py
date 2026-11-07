"""Нигоҳдории оддии танзимот ва омор (файли JSON)."""
import datetime
import json
import os
from pathlib import Path

_path = Path(os.getenv("FLET_APP_STORAGE_DATA", ".")) / "vusto.json"

data = {
    "city": "Dushanbe",
    "country": "Tajikistan",
    "light": False,
    "bookmarks": [],
    "zikr": {},
    "last_prayer": None,
}


def load():
    try:
        if _path.exists():
            data.update(json.loads(_path.read_text(encoding="utf-8")))
    except Exception:
        pass


def save():
    try:
        _path.parent.mkdir(parents=True, exist_ok=True)
        _path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def add_zikr(n=1):
    key = datetime.date.today().isoformat()
    data["zikr"][key] = data["zikr"].get(key, 0) + n
    for old in sorted(data["zikr"])[:-60]:
        data["zikr"].pop(old, None)
    save()


DAY_LABELS = ["Дш", "Сш", "Чш", "Пш", "Ҷм", "Шб", "Яш"]


def last_days(n=7):
    today = datetime.date.today()
    out = []
    for i in range(n - 1, -1, -1):
        d = today - datetime.timedelta(days=i)
        out.append((DAY_LABELS[d.weekday()], data["zikr"].get(d.isoformat(), 0)))
    return out


def is_bookmarked(hid):
    return str(hid) in data["bookmarks"]


def toggle_bookmark(hid):
    hid = str(hid)
    if hid in data["bookmarks"]:
        data["bookmarks"].remove(hid)
        on = False
    else:
        data["bookmarks"].append(hid)
        on = True
    save()
    return on
