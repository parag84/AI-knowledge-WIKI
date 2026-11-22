// AI Video Knowledge Hub dashboard: renders data.json; no framework, no build step.
(() => {
  "use strict";
  const $ = (s, el = document) => el.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fmtTs = (s) => { s = Math.floor(s); const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = String(s % 60).padStart(2, "0"); return h ? `${h}:${String(m).padStart(2, "0")}:${x}` : `${m}:${x}`; };

  // Minimal, safe Markdown: headings, bold/italic/strike, links, lists, paragraphs. Input is escaped first.
  function md(src) {
    const inline = (t) => esc(t)
      .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (m, t, h) => /^\s*javascript:/i.test(h) ? t : `<a href="${h}" rel="noopener">${t}</a>`)
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/~~([^~]+)~~/g, "<del>$1</del>")
      .replace(/(^|\W)_([^_]+)_(?=\W|$)/g, "$1<em>$2</em>")
      .replace(/`([^`]+)`/g, "<code>$1</code>");
    const out = []; let list = null;
    const close = () => { if (list) { out.push(`</${list}>`); list = null; } };
    for (const raw of String(src || "").split("\n")) {
      const line = raw.trimEnd();
      let m;
      if ((m = line.match(/^(#{1,4})\s+(.*)/))) { close(); out.push(`<h${m[1].length + 1}>${inline(m[2])}</h${m[1].length + 1}>`); }
      else if (list === "ol" && (m = line.match(/^\s{2,}[-*]\s+(.*)/))) { out[out.length - 1] = out[out.length - 1].replace(/<\/li>$/, `<br><span class="facts">${inline(m[1])}</span></li>`); }
      else if ((m = line.match(/^\s*[-*]\s+(.*)/))) { if (list !== "ul") { close(); out.push("<ul>"); list = "ul"; } out.push(`<li>${inline(m[1])}</li>`); }
      else if ((m = line.match(/^\s*\d+\.\s+(.*)/))) { if (list !== "ol") { close(); out.push("<ol>"); list = "ol"; } out.push(`<li>${inline(m[1])}</li>`); }
      else if (!line.trim()) { close(); }
      else { close(); out.push(`<p>${inline(line)}</p>`); }
    }
    close();
    return out.join("");
  }

  let D = null, view = "new", query = "";
  const byId = {}, insightsByVideo = {}, topicName = {};

  const badge = (st) => st && st !== "active" ? ` <span class="badge ${st}">${st}</span>` : "";
  const chips = (topics) => `<div class="chips">${(topics || []).map((t) => `<span class="chip">${esc(topicName[t] || t)}</span>`).join("")}</div>`;

  function matches(text) {
    if (!query) return true;
    const hay = text.toLowerCase();
    return query.split(/\s+/).every((w) => hay.includes(w));
  }
  const videoText = (v) => [v.title, v.channel, v.summary, v.applies, (v.topics || []).join(" "),
    (v.tools || []).map((t) => `${t.name} ${t.version}`).join(" "),
    (insightsByVideo[v.id] || []).map((i) => `${i.text} ${(i.facts || []).join(" ")}`).join(" ")].join(" ");

  function videoCard(v) {
    const ins = insightsByVideo[v.id] || [];
    const insList = ins.map((i) => {
      const gone = i.status === "superseded" || i.status === "archived";
      let extra = "";
      if (i.status === "superseded" && i.superseded_by && byId.ins[i.superseded_by]) {
        const nv = byId.video[byId.ins[i.superseded_by].video_id];
        extra = ` <span class="facts">→ replaced by ${esc(nv ? nv.title : i.superseded_by)}: ${esc(i.status_reason || "")}</span>`;
      }
      const facts = (i.facts || []).length ? `<div class="facts">Relies on: ${esc(i.facts.join("; "))} (as of ${esc(i.date)})</div>` : "";
      return `<li><span class="${gone ? "struck" : ""}">${esc(i.text)}</span>${badge(i.status)}${extra}${facts}</li>`;
    }).join("");
    const tools = (v.tools || []).map((t) => `<li><strong>${esc(t.name)}</strong>${t.version ? " " + esc(t.version) : ""} <span class="facts">(${esc(t.kind)})</span></li>`).join("");
    const moments = (v.moments || []).map((m) => `<li><a href="${esc(v.url)}&t=${m.seconds}s" rel="noopener">${fmtTs(m.seconds)}</a>: ${esc(m.note)}</li>`).join("");
    const frames = (v.frames || []).map((f) => `<img src="${esc(f)}" alt="Keyframe from ${esc(v.title)}" loading="lazy">`).join("");
    return `<details class="card">
      <summary>
        ${v.thumb ? `<img class="thumb" src="${esc(v.thumb)}" alt="" loading="lazy">` : `<div class="thumb"></div>`}
        <div>
          <h3>${esc(v.title)}${badge(v.status)}</h3>
          <div class="byline"><span class="rel" title="Relevance to your work">${v.relevance ?? "?"}/5</span> · ${esc(v.channel)} · ${esc(v.published)} · ${fmtTs(v.duration_s)}</div>
          <p class="sum">${esc(v.summary)}</p>
          ${chips(v.topics)}
        </div>
      </summary>
      <div class="body">
        <h4>Key insights</h4><ul>${insList}</ul>
        <h4>How this applies to AX / design systems</h4><p>${esc(v.applies)}</p>
        ${v.relevance_reason ? `<p class="facts">Relevance ${v.relevance}/5: ${esc(v.relevance_reason)}</p>` : ""}
        ${tools ? `<h4>Tools, models &amp; APIs</h4><ul>${tools}</ul>` : ""}
        ${moments ? `<h4>Best moments</h4><ul>${moments}</ul>` : ""}
        ${frames ? `<h4>Keyframes</h4><div class="frames">${frames}</div>` : ""}
        <p><a href="${esc(v.url)}" rel="noopener">Watch on YouTube ↗</a></p>
      </div>
    </details>`;
  }

  function insightRow(i) {
    const v = byId.video[i.video_id] || {};
    const why = i.status_reason ? ` <span class="facts">· ${esc(i.status_reason)}</span>` : "";
    return `<div class="ins"><p>${esc(i.text)}${badge(i.status)}</p>
      <div class="src">${esc(v.title || i.video_id)} · ${esc(i.date)}${why} · <a href="${esc(v.url || "#")}" rel="noopener">video ↗</a></div></div>`;
  }

  const videos = () => D.videos.filter((v) => matches(videoText(v)));
  const empty = (msg) => `<p class="empty">${esc(msg)}</p>`;

  const views = {
    new() {
      const r = D.last_run || {};
      const latest = D.videos.length ? D.videos.map((v) => v.analyzed_at).sort().pop() : null;
      const list = videos().filter((v) => !query ? v.analyzed_at === latest : true);
      const active = D.insights.filter((i) => i.status === "active").length;
      return `<div class="stats">
          <div class="stat"><b>${D.videos.length}</b><span>videos analysed</span></div>
          <div class="stat"><b>${active}</b><span>active insights</span></div>
          <div class="stat"><b>${r.analyzed ?? 0}</b><span>new in last run</span></div>
          <div class="stat"><b>${r.superseded ?? 0}</b><span>superseded last run</span></div>
        </div>
        <h2>${query ? "Search results" : `Added in the latest run${latest ? ` (${esc(latest)})` : ""}`}</h2>
        ${list.map(videoCard).join("") || empty(query ? "No matches." : "Nothing analysed yet. Run the weekly workflow.")}`;
    },
    topics() {
      return D.topics.map((t) => {
        const ins = D.insights.filter((i) => i.status === "active" && (i.topics || []).includes(t.slug) && matches(i.text + " " + (i.facts || []).join(" ")))
          .sort((a, b) => b.date.localeCompare(a.date));
        if (query && !ins.length) return "";
        const qs = (t.open_questions || []).map((q) => `<li>${esc(q)}</li>`).join("");
        return `<section class="topic" id="topic-${esc(t.slug)}">
          <h3>${esc(t.name)}</h3><p class="lede">${esc(t.description || "")}${t.updated ? ` · updated ${esc(t.updated)}` : ""}</p>
          <div class="md">${t.synthesis ? md(t.synthesis) : "<p class='facts'>No synthesis yet.</p>"}</div>
          ${ins.length ? `<h4 class="facts">Latest active insights (${ins.length})</h4>${ins.slice(0, 8).map(insightRow).join("")}` : ""}
          ${qs ? `<h4 class="facts">Open questions</h4><ul>${qs}</ul>` : ""}
        </section>`;
      }).join("") + (D.proposed_topics?.length ? `<h2>Proposed topics awaiting approval</h2><ul>${D.proposed_topics.map((p) => `<li><code>${esc(p.slug)}</code> ${esc(p.why || "")}</li>`).join("")}</ul>` : "");
    },
    weeks() {
      const groups = {};
      for (const v of videos()) (groups[v.week] ||= []).push(v);
      const weeks = Object.keys(groups).sort().reverse();
      return weeks.map((w) => `<h2>${esc(w)} <span class="facts">(${groups[w].length})</span></h2>${groups[w].map(videoCard).join("")}`).join("") || empty("No videos.");
    },
    relevance() {
      const list = videos().sort((a, b) => (b.relevance - a.relevance) || b.published.localeCompare(a.published));
      let out = "", cur = null;
      for (const v of list) { if (v.relevance !== cur) { cur = v.relevance; out += `<h2>Relevance ${cur}/5</h2>`; } out += videoCard(v); }
      return out || empty("No videos.");
    },
    outdated() {
      const pick = (st) => D.insights.filter((i) => i.status === st && matches(i.text)).sort((a, b) => (b.status_changed || "").localeCompare(a.status_changed || ""));
      const sec = (title, lede, list) => `<h2>${title} <span class="facts">(${list.length})</span></h2><p class="lede">${lede}</p>${list.map(insightRow).join("") || empty("None.")}`;
      const log = D.changelog.filter((e) => matches(`${e.reason} ${e.insight_id}`)).slice(0, 40)
        .map((e) => `<li><code>${esc(e.date)}</code> <strong>${esc(e.action)}</strong> ${esc(e.insight_id)}: ${esc(e.reason)}</li>`).join("");
      return sec("Stale: needs review", "Not reinforced by any newer video for 90+ days.", pick("stale")) +
        sec("Superseded", "Replaced by a newer claim, model or practice.", pick("superseded")) +
        sec("Archived", "Unreinforced for 180+ days. Kept for history.", pick("archived")) +
        `<h2>Changelog</h2><ul>${log || "<li>No changes yet.</li>"}</ul>`;
    },
    digests() {
      const list = D.digests.filter((d) => matches(d.markdown));
      return list.map((d, n) => `<details class="card" ${n === 0 ? "open" : ""}><summary style="display:block"><h3>${esc(d.week)}</h3></summary><div class="body md">${md(d.markdown)}</div></details>`).join("") || empty("No digests yet.");
    },
  };

  function render() {
    document.querySelectorAll(".tabs button").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.view === view)));
    $("#main").innerHTML = views[view]();
  }

  function setView(v) {
    if (!views[v]) v = "new";
    view = v;
    try { localStorage.setItem("hub.view", v); } catch (e) { /* storage unavailable */ }
    if (location.hash !== `#${v}`) history.replaceState(null, "", `#${v}`);
    render();
  }

  async function init() {
    try {
      D = await (await fetch("data.json", { cache: "no-cache" })).json();
    } catch (e) {
      $("#main").innerHTML = empty("Couldn't load data.json.");
      return;
    }
    byId.video = Object.fromEntries(D.videos.map((v) => [v.id, v]));
    byId.ins = Object.fromEntries(D.insights.map((i) => [i.id, i]));
    for (const i of D.insights) (insightsByVideo[i.video_id] ||= []).push(i);
    for (const t of D.topics) topicName[t.slug] = t.name;
    document.title = D.title;
    $("#site-title").textContent = D.title;
    const r = D.last_run || {};
    $("#run-meta").textContent = r.week ? `Last run ${r.date} (${r.week}): ${r.analyzed} new videos, ${r.superseded} superseded` : "No runs yet";
    $("#generated").textContent = D.generated;

    document.querySelectorAll(".tabs button").forEach((b) => b.addEventListener("click", () => setView(b.dataset.view)));
    let t;
    $("#q").addEventListener("input", (e) => { clearTimeout(t); t = setTimeout(() => { query = e.target.value.trim().toLowerCase(); render(); }, 120); });
    window.addEventListener("hashchange", () => { const h = location.hash.slice(1); if (h && h !== view) setView(h); });
    let saved = location.hash.slice(1);
    if (!saved) { try { saved = localStorage.getItem("hub.view") || ""; } catch (e) { saved = ""; } }
    setView(saved || "new");
  }
  init();
})();
