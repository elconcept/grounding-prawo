#!/usr/bin/env node
// gp-refresh - utrzymanie bazy GROUNDING-PRAWO po stronie konektorow MCP.
//
//   node gp-refresh.mjs [--all] [--source saos] [--limit N] [--dry-run]
//       G4: ponawia wywolania z wygaslych wpisow CACHE/**/mcp-*.md (z --all: wszystkich)
//   node gp-refresh.mjs --cite-check [--limit N] [--dry-run]
//       G5: saos_cite_check dla orzeczen z ORZECZENIA/ (source: saos); werdykt trafia
//       do ich frontmattera (pola cite_check, cite_check_at) przez gp-cache.
//
// Wywolania ida przez gp-cache.mjs, wiec wynik laduje w tych samych plikach cache.
// Baza: GROUNDING_ROOT albo katalog nadrzedny z CACHE/ i INDEX/.
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const flag = (f) => args.includes(f);
const opt = (f) => { const i = args.indexOf(f); return i >= 0 ? args[i + 1] : undefined; };
const LIMIT = Number(opt("--limit") || 0);
const DRY = flag("--dry-run");

// Podkatalog bez wzgledu na wielkosc liter (GROUNDING-PRAWO: CACHE/, abogada: mcp/cache/).
function sub(d, name) {
  try {
    const hit = fs.readdirSync(d).find((n) => n.toLowerCase() === name.toLowerCase() && fs.statSync(path.join(d, n)).isDirectory());
    if (hit) return path.join(d, hit);
  } catch { /* brak katalogu */ }
  return path.join(d, name);
}
function findRoot() {
  const isRoot = (d) => d && fs.existsSync(sub(d, "CACHE")) && fs.existsSync(sub(d, "INDEX"));
  if (isRoot(process.env.GROUNDING_ROOT)) return process.env.GROUNDING_ROOT;
  for (let d = HERE; d !== path.dirname(d); d = path.dirname(d)) if (isRoot(d)) return d;
  for (const d of [path.join(process.cwd(), "mcp"), process.cwd()]) if (isRoot(d)) return d;
  return null;
}
const ROOT = findRoot();
if (!ROOT) {
  console.error("gp-refresh: nie znaleziono bazy GROUNDING-PRAWO (ustaw GROUNDING_ROOT)");
  process.exit(2);
}

function frontmatter(file) {
  const t = fs.readFileSync(file, "utf8").replace(/\r\n/g, "\n"); // checkout z core.autocrlf
  const fm = /^---\n([\s\S]*?)\n---\n/.exec(t);
  if (!fm) return null;
  return Object.fromEntries(fm[1].split("\n").map((l) => {
    const i = l.indexOf(":");
    return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^"(.*)"$/, "$1").replace(/\\"/g, '"')];
  }));
}
function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.startsWith("mcp-") && e.name.endsWith(".md")) out.push(p);
  }
  return out;
}

// Zadania: [serwer, narzedzie, argumenty, etykieta]
const jobs = [];
const now = new Date().toISOString();
if (flag("--cite-check")) {
  const dir = [sub(ROOT, "ORZECZENIA"), sub(sub(ROOT, "CACHE"), "orzeczenia")].find((d) => fs.existsSync(d));
  for (const f of (dir ? fs.readdirSync(dir) : []).filter((x) => x.endsWith(".md"))) {
    const m = frontmatter(path.join(dir, f));
    if (m && m.source === "saos" && m.sygnatura) jobs.push(["saos", "saos_cite_check", { caseNumber: m.sygnatura }, m.sygnatura]);
  }
} else {
  for (const f of walk(sub(ROOT, "CACHE"))) {
    const m = frontmatter(f);
    if (!m || !m.tool?.startsWith("mcp:")) continue;
    const [server, tool] = m.tool.slice(4).split(".");
    if (opt("--source") && server !== opt("--source")) continue;
    if (!flag("--all") && m.expires_at > now) continue;
    let a;
    try { a = JSON.parse(m.query || "{}"); } catch { continue; }
    jobs.push([server, tool, a, m.identyfikator || f]);
  }
}
const todo = LIMIT ? jobs.slice(0, LIMIT) : jobs;
console.error(`gp-refresh: ${todo.length} wywolan (baza ${ROOT})`);
if (DRY) {
  for (const [s, t, , label] of todo) console.log(`[dry-run] ${s}.${t} ${label}`);
  process.exit(0);
}

// Minimalny klient MCP po stdio.
function client(server) {
  const env = { ...process.env, GROUNDING_ROOT: ROOT, GP_CACHE: flag("--cite-check") ? "" : "refresh" };
  const child = spawn(process.execPath, [path.join(HERE, "gp-cache.mjs"), server], { stdio: ["pipe", "pipe", "ignore"], env });
  const waiting = new Map();
  let id = 0;
  readline.createInterface({ input: child.stdout }).on("line", (l) => {
    try {
      const m = JSON.parse(l);
      if (waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); }
    } catch { /* nie-JSON */ }
  });
  const request = (method, params) => new Promise((resolve) => {
    const i = ++id;
    waiting.set(i, resolve);
    child.stdin.write(JSON.stringify({ jsonrpc: "2.0", id: i, method, params }) + "\n");
  });
  return {
    async init() {
      await request("initialize", { protocolVersion: "2025-06-18", capabilities: {}, clientInfo: { name: "gp-refresh", version: "1" } });
      child.stdin.write(JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized" }) + "\n");
    },
    call: (name, a) => request("tools/call", { name, arguments: a }),
    close: () => child.stdin.end(),
  };
}

const byServer = new Map();
for (const j of todo) (byServer.get(j[0]) || byServer.set(j[0], []).get(j[0])).push(j);
let ok = 0, bad = 0;
for (const [server, list] of byServer) {
  const c = client(server);
  await c.init();
  for (const [, tool, a, label] of list) {
    const r = await c.call(tool, a);
    const failed = r.error || r.result?.isError;
    failed ? bad++ : ok++;
    const verdict = r.result?.structuredContent?.verdict;
    console.log(`${failed ? "BLAD" : "ok  "} ${server}.${tool} ${label}${verdict ? ` -> ${verdict}` : ""}`);
    await new Promise((res) => setTimeout(res, 300));
  }
  c.close();
}
console.error(`gp-refresh: ${ok} ok, ${bad} bledow`);
process.exit(bad ? 1 : 0);
