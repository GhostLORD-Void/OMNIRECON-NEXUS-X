"""Small dependency-free dashboard served by FastAPI."""
DASHBOARD_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OMNIRECON NEXUS X</title><style>
:root{color-scheme:dark;font-family:system-ui;background:#0b1020;color:#e7ecff}
body{max-width:980px;margin:40px auto;padding:0 20px}p{color:#aab5d2}
.panel{background:#141d33;border:1px solid #293858;border-radius:14px;padding:18px;margin:16px 0}
pre{white-space:pre-wrap;overflow-wrap:anywhere;color:#b9d8ff}
button{background:#526dff;color:white;border:0;border-radius:8px;padding:10px 16px;cursor:pointer}
</style></head><body><h1>OMNIRECON NEXUS X</h1><p>Agent operations console · planning mode · autonomous actions disabled</p>
<div class="panel"><h2>System</h2><pre id="health">Loading...</pre></div>
<div class="panel"><h2>Agent registry</h2><pre id="agents">Loading...</pre></div>
<div class="panel"><h2>Recent task plans</h2><pre id="tasks">Loading...</pre><button onclick="refresh()">Refresh</button></div>
<script>
async function show(path,id){const r=await fetch(path);document.getElementById(id).textContent=r.ok?JSON.stringify(await r.json(),null,2):("HTTP "+r.status);}
async function refresh(){await Promise.all([show('/health','health'),show('/v1/agents','agents'),show('/v1/tasks','tasks')]);}refresh();
</script></body></html>"""
