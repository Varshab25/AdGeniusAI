from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AdGenius AI | Marketing Intelligence</title>
<style>
:root {
  --bg: #0b1020; --panel: #131b30; --line: #27324b;
  --text: #eef2ff; --muted: #9ba9c6; --accent: #8b7cff;
  --green: #50dfb0;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--text);
  font-family: Arial, sans-serif;
}
header {
  padding: 24px 6%; border-bottom: 1px solid var(--line);
  display: flex; justify-content: space-between; align-items: center;
}
.logo { font-size: 22px; font-weight: 800; }
.logo span { color: var(--accent); }
.tag { color: var(--muted); font-size: 12px; }
main { max-width: 1100px; margin: auto; padding: 34px 20px; }
.hero { margin-bottom: 28px; }
h1 { font-size: clamp(30px, 5vw, 48px); margin: 8px 0; }
p { color: var(--muted); line-height: 1.6; }
.eyebrow { color: var(--green); font-weight: bold; font-size: 12px; }
.stats { display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; }
.card, .panel {
  background: var(--panel); border: 1px solid var(--line);
  border-radius: 15px; padding: 20px;
}
.stat { color: var(--muted); font-size: 13px; }
.value { font-size: 25px; font-weight: bold; margin-top: 12px; }
.layout { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 22px; }
h2 { font-size: 19px; margin-top: 0; }
label { display: block; font-size: 13px; margin: 15px 0 7px; }
input, select, textarea {
  width: 100%; padding: 12px; border-radius: 9px;
  border: 1px solid var(--line); background: #0b1020;
  color: var(--text); font: inherit;
}
textarea { min-height: 85px; resize: vertical; }
button {
  border: 0; border-radius: 9px; padding: 12px 17px;
  background: var(--accent); color: white; font-weight: bold;
  cursor: pointer; margin-top: 16px;
}
button:hover { opacity: .88; }
.output { white-space: pre-wrap; line-height: 1.7; }
.note { font-size: 12px; }
footer { text-align: center; padding: 30px; color: var(--muted); font-size: 12px; }
@media(max-width:700px) {
  .stats, .layout { grid-template-columns: 1fr; }
  header { padding: 20px; }
}
</style>
</head>
<body>
<header>
  <div class="logo">AdGenius <span>AI</span></div>
  <div class="tag">MARKETING INTELLIGENCE</div>
</header>
<main>
  <section class="hero">
    <div class="eyebrow">YOUR CAMPAIGN WORKSPACE</div>
    <h1>Turn marketing ideas<br>into measurable growth.</h1>
    <p>Create campaign copy and calculate advertising performance in one workspace.</p>
  </section>

  <section class="stats">
    <div class="card"><div class="stat">Campaign spend</div><div class="value" id="spend">₹0</div></div>
    <div class="card"><div class="stat">Attributed revenue</div><div class="value" id="revenue">₹0</div></div>
    <div class="card"><div class="stat">ROAS</div><div class="value" id="roas">—</div></div>
  </section>

  <section class="layout">
    <div class="panel">
      <h2>Campaign creator</h2>
      <form id="campaignForm">
        <label>Business or product name</label>
        <input name="product" placeholder="e.g. Handmade skincare" required>
        <label>Campaign objective</label>
        <select name="goal">
          <option>Increase sales</option>
          <option>Generate leads</option>
          <option>Build brand awareness</option>
          <option>Drive website traffic</option>
        </select>
        <label>Target audience</label>
        <textarea name="audience" placeholder="Who do you want to reach?" required></textarea>
        <label>Advertising platform</label>
        <select name="platform">
          <option>Instagram</option><option>Google</option>
          <option>Facebook</option><option>LinkedIn</option>
        </select>
        <label>Campaign budget (₹)</label>
        <input name="budget" type="number" min="1" step="0.01" required>
        <button type="submit">Create campaign draft</button>
      </form>
    </div>

    <div class="panel">
      <h2>Campaign draft</h2>
      <p id="draftHint">Your campaign draft will appear here.</p>
      <div id="draft" class="output"></div>
      <p class="note">This starter creates a structured draft, not verified AI-generated recommendations.</p>
    </div>

    <div class="panel">
      <h2>Performance calculator</h2>
      <form id="analyticsForm">
        <label>Advertising spend (₹)</label>
        <input name="spend" type="number" min="0" step="0.01" required>
        <label>Revenue attributed to ads (₹)</label>
        <input name="revenue" type="number" min="0" step="0.01" required>
        <label>Other campaign costs (₹)</label>
        <input name="costs" type="number" min="0" step="0.01" value="0" required>
        <button type="submit">Calculate performance</button>
      </form>
    </div>

    <div class="panel">
      <h2>Performance results</h2>
      <div id="results" class="output">Enter campaign figures to calculate ROAS and estimated profit.</div>
      <p class="note">Results depend on the accuracy of your entered figures. They do not prove that ads caused a sales increase.</p>
    </div>
  </section>
</main>
<footer>AdGenius AI · Marketing workspace starter</footer>
<script>
const money = n => new Intl.NumberFormat('en-IN', {
  style: 'currency', currency: 'INR', maximumFractionDigits: 2
}).format(n);

document.getElementById('campaignForm').addEventListener('submit', e => {
  e.preventDefault();
  const d = Object.fromEntries(new FormData(e.target));
  document.getElementById('draftHint').textContent = 'Draft created locally';
  document.getElementById('draft').textContent =
    'PRODUCT: ' + d.product + '\\n\\n' +
    'OBJECTIVE: ' + d.goal + '\\n\\n' +
    'AUDIENCE: ' + d.audience + '\\n\\n' +
    'PLATFORM: ' + d.platform + '\\n\\n' +
    'BUDGET: ' + money(Number(d.budget)) + '\\n\\n' +
    'SAMPLE HEADLINE: Discover ' + d.product + '\\n\\n' +
    'SAMPLE DESCRIPTION: Explore our offer and discover how it may suit your needs. Learn more today.';
});

document.getElementById('analyticsForm').addEventListener('submit', async e => {
  e.preventDefault();
  const d = Object.fromEntries(new FormData(e.target));
  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(d)
    });
    const r = await response.json();
    if (!response.ok) throw new Error(r.error || 'Calculation failed');
    document.getElementById('results').textContent =
      'ROAS: ' + r.roas + '\\n' +
      'Estimated profit: ' + money(r.profit) + '\\n' +
      'Profit margin: ' + r.profit_margin + '\\n' +
      'Break-even note: ' + r.note;
    document.getElementById('spend').textContent = money(Number(d.spend));
    document.getElementById('revenue').textContent = money(Number(d.revenue));
    document.getElementById('roas').textContent = r.roas;
  } catch (err) {
    document.getElementById('results').textContent = err.message;
  }
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    try:
        spend = float(data.get("spend", 0))
        revenue = float(data.get("revenue", 0))
        costs = float(data.get("costs", 0))
        if not all(map(lambda n: n >= 0 and n < float("inf"), [spend, revenue, costs])):
            raise ValueError()
        if spend <= 0:
            return jsonify(error="Advertising spend must be greater than zero."), 400
    except (ValueError, TypeError):
        return jsonify(error="Enter valid, non-negative numbers."), 400

    profit = revenue - spend - costs
    return jsonify({
        "roas": f"{revenue / spend:.2f}x",
        "profit": round(profit, 2),
        "profit_margin": f"{profit / revenue * 100:.1f}%" if revenue else "N/A",
        "note": "Revenue covers spend and other costs." if profit >= 0 else "Campaign is below break-even based on these inputs."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
