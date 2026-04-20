import gradio as gr
import re

def encode(prompt: str) -> str:
    ACTIONS = {
        "summarize": "sum", "summarise": "sum",
        "generate": "gen", "write": "gen", "create": "gen", "draft": "gen",
        "fix": "fix", "debug": "fix", "correct": "fix",
        "explain": "xpl", "describe": "xpl",
        "compare": "cmp", "contrast": "cmp",
        "extract": "ext", "review": "rev",
        "translate": "lang", "analyse": "anl", "analyze": "anl",
        "plan": "pln", "rewrite": "ref", "rephrase": "ref",
        "classify": "cls", "format": "fmt",
    }
    MODIFIERS = {
        "bullet points": "fmt:bullets", "bullets": "fmt:bullets",
        "numbered list": "fmt:list", "table": "fmt:table",
        "json": "fmt:json", "markdown": "fmt:md",
        "formal": "tone:formal", "professional": "tone:professional",
        "casual": "tone:casual", "friendly": "tone:friendly",
        "academic": "tone:academic", "persuasive": "tone:persuasive",
        "simple": "lvl:simple", "technical": "lvl:technical",
        "python": "code:py", "javascript": "code:js",
        "typescript": "code:ts", "rust": "code:rs",
        "go": "code:go", "java": "code:java", "sql": "code:sql",
    }
    FILLERS = [
        "please", "could you", "can you", "i want you to",
        "i would like you to", "i need you to", "make sure to",
        "ensure that", "you should", "try to", "attempt to",
        "the following", "as follows", "given the", "provided",
        "kindly", "i'd like", "would you", "help me",
    ]
    CONSTRAINTS = {
        "focus on": "+", "emphasise": "+", "emphasize": "+",
        "prioritise": "+", "prioritize": "+", "especially": "+",
        "ignore": "-", "exclude": "-", "avoid": "-",
        "without": "-", "leave out": "-",
    }
    text = prompt.lower().strip()
    action = None
    modifiers = []
    constraints = []
    for filler in sorted(FILLERS, key=len, reverse=True):
        text = re.sub(rf'\b{re.escape(filler)}\b', '', text)
    for word, code in sorted(ACTIONS.items(), key=lambda x: len(x[0]), reverse=True):
        if word in text:
            action = code
            text = text.replace(word, '', 1).strip()
            break
    for word, code in sorted(MODIFIERS.items(), key=lambda x: len(x[0]), reverse=True):
        if word in text:
            modifiers.append(code)
            text = text.replace(word, '').strip()
    for word, symbol in sorted(CONSTRAINTS.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = rf'{re.escape(word)}\s+([\w\s]+?)(?=[,.\n]|$)'
        matches = re.findall(pattern, text)
        for match in matches:
            topic = '_'.join(match.strip().split()[:2])
            constraints.append(f"{symbol}{topic}")
        text = re.sub(pattern, '', text).strip()
    text = re.sub(r'\b(\d+)\s*(bullet|point|item|word|sentence|line)s?', r'#\1', text)
    text = re.sub(r'\s+', ' ', text).strip().strip('.,; ')
    artha = action or 'gen'
    if text: artha += f'[{text}]'
    if modifiers: artha += f'({", ".join(modifiers)})'
    if constraints: artha += f' {" ".join(constraints)}'
    return artha


def compress(prompt: str):
    if not prompt.strip():
        return "", "", "", ""
    compressed = encode(prompt)
    en_t = len(prompt.strip().split())
    ar_t = len(compressed.strip().split())
    saved = max(0, en_t - ar_t)
    pct = round((saved / en_t) * 100) if en_t > 0 else 0
    cost = round((saved / 1000) * 0.01 * 1_000_000, 2)
    return compressed, str(en_t), str(ar_t), f"{pct}%", f"${cost:,.0f}"


HTML = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;600;700&family=Kalam:wght@300;400&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Kalam', cursive; background: #fdfcf7; padding: 24px; }
.title { font-family: 'Caveat', cursive; font-size: 42px; font-weight: 700; color: #1a1a1a; text-align: center; margin-bottom: 4px; }
.sub { font-size: 14px; color: #555; text-align: center; font-style: italic; margin-bottom: 8px; }
.links { display: flex; gap: 16px; justify-content: center; margin-bottom: 24px; }
.links a { font-family: 'Caveat', cursive; font-size: 16px; color: #1a1a1a; text-decoration: none; border-bottom: 2px solid #333; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 960px; margin: 0 auto; }
.box { background: #fff; border: 2px solid #1a1a1a; border-radius: 3px 12px 4px 10px; padding: 16px; box-shadow: 4px 4px 0 #1a1a1a; }
.box-label { font-family: 'Caveat', cursive; font-size: 18px; font-weight: 600; color: #1a1a1a; margin-bottom: 8px; display: block; }
textarea { width: 100%; border: 2px solid #1a1a1a; border-radius: 2px 8px 3px 6px; padding: 10px 12px; font-family: 'Kalam', cursive; font-size: 14px; background: #fffef5; color: #1a1a1a; resize: vertical; min-height: 90px; outline: none; }
textarea:focus { box-shadow: 2px 2px 0 #000; }
button.main-btn { background: #1a1a1a; color: #fdfcf7; border: 2px solid #000; border-radius: 2px 8px 3px 6px; padding: 10px 20px; font-family: 'Caveat', cursive; font-size: 18px; font-weight: 600; cursor: pointer; width: 100%; margin-top: 10px; box-shadow: 3px 3px 0 #555; }
button.main-btn:hover { background: #333; }
.examples-label { font-family: 'Caveat', cursive; font-size: 15px; color: #555; margin: 14px 0 6px; display: block; }
.chip { font-size: 12px; padding: 5px 10px; border: 1.5px solid #555; border-radius: 1px 6px 2px 5px; cursor: pointer; color: #333; background: #fffef5; font-family: 'Kalam', cursive; margin: 0 4px 6px 0; display: inline-block; }
.chip:hover { background: #1a1a1a; color: #fdfcf7; }
.output-box { font-family: 'Caveat', cursive; font-size: 20px; color: #1a1a1a; min-height: 60px; background: #fffef5; border: 2px dashed #333; border-radius: 2px 8px 3px 6px; padding: 14px; margin-bottom: 14px; word-break: break-word; }
.stats { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 14px; }
.stat { background: #fffef5; border: 2px solid #333; border-radius: 2px 8px 3px 6px; padding: 10px; text-align: center; box-shadow: 2px 2px 0 #aaa; }
.stat-num { font-family: 'Caveat', cursive; font-size: 28px; font-weight: 700; color: #1a1a1a; display: block; }
.stat-num.green { color: #2d6a2d; }
.stat-lbl { font-size: 11px; color: #666; }
.bar-row { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.bar-lbl { font-size: 12px; color: #555; width: 55px; text-align: right; }
.bar-track { flex: 1; height: 16px; border: 2px solid #333; border-radius: 2px; background: #fffef5; overflow: hidden; }
.bar-en { height: 100%; background: repeating-linear-gradient(45deg,#555,#555 2px,transparent 2px,transparent 6px); transition: width 0.4s; }
.bar-ar { height: 100%; background: repeating-linear-gradient(45deg,#2d6a2d,#2d6a2d 2px,transparent 2px,transparent 6px); transition: width 0.4s; }
.cost-line { font-size: 13px; color: #555; text-align: center; border-top: 1px dashed #ccc; padding-top: 10px; margin-top: 8px; }
.why { max-width: 960px; margin: 24px auto 0; border-top: 2px dashed #ccc; padding-top: 20px; }
.why-title { font-family: 'Caveat', cursive; font-size: 22px; font-weight: 600; color: #1a1a1a; margin-bottom: 8px; }
.why p { font-size: 14px; color: #444; line-height: 1.8; margin-bottom: 8px; }
</style>
</head>
<body>
<div class="title">⟁ Artha</div>
<div class="sub">a math-based language for AI — type english, get artha</div>
<div class="links">
  <a href="https://github.com/sidvsukhi/artha" target="_blank">github</a>
  <a href="https://huggingface.co/siddsukh/artha-1.1b" target="_blank">model</a>
  <a href="https://github.com/sidvsukhi/artha/blob/main/SPEC.md" target="_blank">spec</a>
</div>

<div class="grid">
  <div>
    <div class="box">
      <span class="box-label">english prompt</span>
      <textarea id="inp" placeholder="type your prompt here..." oninput="compress()"></textarea>
      <button class="main-btn" onclick="compress()">⟁ compress to artha</button>
    </div>
    <span class="examples-label">try an example:</span>
    <div id="chips"></div>
  </div>

  <div class="box">
    <span class="box-label">artha output</span>
    <div class="output-box" id="out">your compressed prompt appears here...</div>
    <div class="stats">
      <div class="stat"><span class="stat-num" id="en-t">—</span><span class="stat-lbl">english tokens</span></div>
      <div class="stat"><span class="stat-num" id="ar-t">—</span><span class="stat-lbl">artha tokens</span></div>
      <div class="stat"><span class="stat-num green" id="pct">—</span><span class="stat-lbl">reduction</span></div>
    </div>
    <div class="bar-row"><span class="bar-lbl">english</span><div class="bar-track"><div class="bar-en" id="bar-en" style="width:100%"></div></div><span id="en-lbl" style="font-size:12px;color:#555;width:30px"></span></div>
    <div class="bar-row"><span class="bar-lbl">artha</span><div class="bar-track"><div class="bar-ar" id="bar-ar" style="width:30%"></div></div><span id="ar-lbl" style="font-size:12px;color:#2d6a2d;width:30px"></span></div>
    <div class="cost-line">at 1M calls/day → saves <strong id="cost" style="color:#2d6a2d">—</strong>/year</div>
  </div>
</div>

<div class="why">
  <div class="why-title">why does this work?</div>
  <p>English was chosen for AI by accident — it's what the training data was in. But math is truly universal. Artha strips every prompt to pure intent.</p>
  <p>A standard tokenizer sees <code>fmt:bullets</code> as <strong>4 tokens</strong>. An Artha tokenizer sees it as <strong>1</strong>. The model doesn't translate — it <em>thinks</em> in Artha.</p>
</div>

<script>
const EXAMPLES = [
  "Please summarise this article in 3 bullet points, focus on key facts, ignore opinions",
  "Fix the bug in this Python code and explain what was wrong",
  "Write a formal email to a client about the project delay, under 150 words",
  "Compare React and Vue for a beginner, format as table, focus on performance",
  "Explain machine learning to a 10 year old in simple language",
  "Translate this text to French, keep it professional, under 200 words",
];

const chips = document.getElementById('chips');
EXAMPLES.forEach(ex => {
  const c = document.createElement('span');
  c.className = 'chip';
  c.textContent = ex.slice(0,40) + '...';
  c.onclick = () => { document.getElementById('inp').value = ex; compress(); };
  chips.appendChild(c);
});

const ACTIONS = {"summarize":"sum","summarise":"sum","generate":"gen","write":"gen","create":"gen","draft":"gen","fix":"fix","debug":"fix","explain":"xpl","describe":"xpl","compare":"cmp","contrast":"cmp","extract":"ext","review":"rev","translate":"lang","analyse":"anl","analyze":"anl","plan":"pln","rewrite":"ref","rephrase":"ref","classify":"cls"};
const MODIFIERS = {"bullet points":"fmt:bullets","bullets":"fmt:bullets","numbered list":"fmt:list","table":"fmt:table","json":"fmt:json","markdown":"fmt:md","formal":"tone:formal","professional":"tone:professional","casual":"tone:casual","simple":"lvl:simple","technical":"lvl:technical","python":"code:py","javascript":"code:js","typescript":"code:ts","rust":"code:rs","java":"code:java","sql":"code:sql"};
const FILLERS = ["please","could you","can you","i want you to","i would like you to","i need you to","make sure to","ensure that","you should","try to","the following","kindly","i'd like","would you","help me"];
const CONSTRAINTS = {"focus on":"+","emphasise":"+","emphasize":"+","prioritise":"+","prioritize":"+","ignore":"-","exclude":"-","avoid":"-","without":"-"};

function encode(prompt) {
  let text = prompt.toLowerCase().trim();
  let action = null, mods = [], cons = [];
  FILLERS.slice().sort((a,b)=>b.length-a.length).forEach(f => { text = text.replace(new RegExp('\\b'+f.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\b','gi'),''); });
  for(const [w,c] of Object.entries(ACTIONS).sort((a,b)=>b[0].length-a[0].length)) { if(text.includes(w)){action=c;text=text.replace(w,'').trim();break;} }
  for(const [w,c] of Object.entries(MODIFIERS).sort((a,b)=>b[0].length-a[0].length)) { if(text.includes(w)){mods.push(c);text=text.replace(w,'').trim();} }
  for(const [w,s] of Object.entries(CONSTRAINTS).sort((a,b)=>b[0].length-a[0].length)) { const re=new RegExp(w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\s+([\\w\\s]+?)(?=[,.\\n]|$)','gi'); const ms=[...text.matchAll(re)]; ms.forEach(m=>cons.push(s+m[1].trim().split(/\s+/).slice(0,2).join('_'))); text=text.replace(re,'').trim(); }
  text = text.replace(/\b(\d+)\s*(bullet|point|item|word|line)s?/gi,'#$1').replace(/\s+/g,' ').trim().replace(/^[.,; ]+|[.,; ]+$/g,'');
  let artha = action||'gen';
  if(text) artha+=`[${text}]`;
  if(mods.length) artha+=`(${mods.join(', ')})`;
  if(cons.length) artha+=` ${cons.join(' ')}`;
  return artha;
}

function compress() {
  const prompt = document.getElementById('inp').value.trim();
  if(!prompt) return;
  const artha = encode(prompt);
  const en = prompt.split(/\s+/).length;
  const ar = artha.split(/\s+/).length;
  const saved = Math.max(0, en-ar);
  const pct = Math.round((saved/en)*100);
  const cost = Math.round((saved/1000)*0.01*1000000);
  const max = Math.max(en,ar);
  document.getElementById('out').textContent = artha;
  document.getElementById('en-t').textContent = en;
  document.getElementById('ar-t').textContent = ar;
  document.getElementById('pct').textContent = pct+'%';
  document.getElementById('bar-en').style.width = Math.round(en/max*100)+'%';
  document.getElementById('bar-ar').style.width = Math.round(ar/max*100)+'%';
  document.getElementById('en-lbl').textContent = en+'t';
  document.getElementById('ar-lbl').textContent = ar+'t';
  document.getElementById('cost').textContent = '$'+cost.toLocaleString();
}

document.getElementById('inp').value = EXAMPLES[0];
compress();
</script>
</body>
</html>
"""

with gr.Blocks(title="Artha") as demo:
    gr.HTML(HTML)

if __name__ == "__main__":
    demo.launch()
