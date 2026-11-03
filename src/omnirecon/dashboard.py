"""Local dashboard with task submission and agent-run controls."""
DASHBOARD_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OMNIRECON NEXUS X</title><style>
:root{color-scheme:dark;font-family:system-ui;background:#0b1020;color:#e7ecff}
body{max-width:980px;margin:32px auto;padding:0 18px}p{color:#aab5d2}
.panel{background:#141d33;border:1px solid #293858;border-radius:14px;padding:18px;margin:16px 0}
pre{white-space:pre-wrap;overflow-wrap:anywhere;color:#b9d8ff;max-height:480px;overflow:auto}
input,textarea{box-sizing:border-box;width:100%;margin:8px 0;padding:12px;border:1px solid #354666;border-radius:8px;background:#0b1020;color:#e7ecff}
textarea{min-height:110px}button{background:#526dff;color:white;border:0;border-radius:8px;padding:10px 16px;cursor:pointer;margin:5px 5px 5px 0}
button:disabled{opacity:.5;cursor:wait}.muted{font-size:.9rem;color:#aab5d2}
</style></head><body><h1>OMNIRECON NEXUS X</h1>
<p>MAXPOWER · Hybrid model routing · Local-first control panel · No autonomous tool actions</p>
<div class="panel"><h2>System status</h2><pre id="health">Loading...</pre><h3>Configured providers</h3><pre id="providers">Loading...</pre></div>
<div class="panel"><h2>Run the agent team</h2>
<p class="muted">Submits your objective to the coordinator, research and engineering agents, then requests a synthesis. Security specialist analysis is included for relevant objectives. No shell, scanning or external tools are executed.</p>
<textarea id="objective" maxlength="4000" placeholder="Describe the objective (at least 8 characters)"></textarea>
<textarea id="context" maxlength="12000" placeholder="Optional context, constraints, or requirements"></textarea>
<label><input id="authorized" type="checkbox" style="width:auto"> I confirm I am authorized for any named assets in this request</label><br>
<button id="run" onclick="runAgents()">Run agent team</button><pre id="result">Results will appear here.</pre></div>
<div class="panel"><h2>Agent registry</h2><pre id="agents">Loading...</pre></div>
<div class="panel"><h2>Recent task plans</h2><pre id="tasks">Loading...</pre><button onclick="refresh()">Refresh</button></div>
<script>
async function show(path,id){const r=await fetch(path);const e=document.getElementById(id);e.textContent=r.ok?JSON.stringify(await r.json(),null,2):("HTTP "+r.status);}
async function refresh(){await Promise.all([show('/health','health'),show('/v1/providers','providers'),show('/v1/agents','agents'),show('/v1/tasks','tasks')]);}
async function runAgents(){
 const objective=document.getElementById('objective').value.trim();
 const result=document.getElementById('result');
 const button=document.getElementById('run');
 if(objective.length<8){result.textContent='Please enter an objective of at least 8 characters.';return;}
 button.disabled=true;result.textContent='Agents are working...';
 try{
  const response=await fetch('/v1/agents/run',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({objective,context:document.getElementById('context').value,
    authorized:document.getElementById('authorized').checked})});
  const data=await response.json();
  result.textContent=JSON.stringify(data,null,2);
 }catch(error){result.textContent='Request failed: '+String(error);}
 finally{button.disabled=false;}
}
refresh();
</script></body></html>"""
