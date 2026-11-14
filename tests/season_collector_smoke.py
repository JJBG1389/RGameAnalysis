"""Offline collector tests; no API credentials or network calls."""
import importlib.util,tempfile
from pathlib import Path
spec=importlib.util.spec_from_file_location("collector","scripts/collect_2026_season.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Session:
    def __init__(self):self.headers={}
    def get(self,url,params=None,timeout=None):
        class Response:
            status_code=200
            def raise_for_status(self):pass
            def json(self):
                if "/events/search/2026" in url:return [{"code":"ABC","dateStart":"2026-11-01"}]
                if url.endswith("/matches"):return [{"id":1,"scores":{}}]
                if url.endswith("/teams"):return [{"teamNumber":123}]
                return {}
        return Response()
with tempfile.TemporaryDirectory() as d:
    root=Path(d)
    result=m.collect_ftc(Session(),root,10)
    assert result["events_saved"]==1 and not result["errors"]
    payload=(root/"ftc"/"ABC.json").read_text()
    assert '"matches"' in payload and '"teams"' in payload
print("2026 FTC collector offline fixture passed")
