#!/usr/bin/env node
// gp-cache - posrednik MCP (stdio) z cache w bazie GROUNDING-PRAWO.
//
//   node gp-cache.mjs <serwer>                   uruchamia servers/<serwer>.cjs obok tego pliku
//   node gp-cache.mjs <serwer> -- <cmd> [args]   dowolny serwer MCP jako zrodlo
//
// Kazde udane wywolanie narzedzia trafia do CACHE/<zrodlo>/mcp-<narzedzie>-<klucz>.md
// (frontmatter jak w lexcache + pelna odpowiedz w bloku ```json). To samo wywolanie
// przed uplywem TTL nie idzie do sieci. Gdy zrodlo nie odpowiada albo zwraca blad,
// a w cache jest wpis - nawet wygasly - wraca on z jawnym ostrzezeniem o dacie.
// Wynik z cache zawsze niesie na poczatku linie z data pobrania: cache jest widocznym
// poziomem hierarchii zrodel, nie ukryta optymalizacja (DOKUMENTACJA/03, P1).
//
// Zmienne: GROUNDING_ROOT - baza (domyslnie szukana: cwd, OneDrive, /mnt/e, /sessions/*/mnt/*);
//          GP_CACHE=off (bez cache) | refresh (zawsze pobierz, zapisz);
//          GP_CACHE_TTL_<SERWER>_<NARZEDZIE>=dni (np. GP_CACHE_TTL_SAOS_SEARCH=1).
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const SERVER = argv[0];
if (!SERVER) {
  process.stderr.write("uzycie: gp-cache.mjs <serwer> [-- <polecenie> ...]\n");
  process.exit(2);
}
const sep = argv.indexOf("--");
const CHILD = sep >= 0 ? argv.slice(sep + 1) : [process.execPath, path.join(HERE, "servers", `${SERVER}.cjs`)];

// TTL w dniach (DOKUMENTACJA/04 §2). 0 = bez cache. Nieznane narzedzie: 7 dni.
const TTL = {
  saos: { search: 3, search_by_case: 30, get_judgment: 180, saos_cite_check: 7 },
  nsa: { search: 7, search_by_case: 30, get_judgment: 180 },
  isap: { search_acts: 7, get_act: 30, get_act_text: 90 },
  krs: { get_entity: 1, get_entity_full: 1, get_board: 1 },
  "eu-sparql": { search_by_celex: 30, search_by_date_range: 7, search_cjeu: 7, search_cjeu_by_ecli: 180, search_gdprhub: 7 },
  eureka: { search: 7, search_by_signature: 30, get_interpretation: 180, list_categories: 30 },
  "eu-compliance": { "*": 0 }, // korpus offline - nie ma czego cache'owac
};
// Katalog w CACHE/ - zgodny z lexcache (NSA to CBOSA, EUR-Lex to eurlex).
const SOURCE_DIR = { nsa: "cbosa", "eu-sparql": "eurlex" };
const QUERY_TYPE = {
  get_judgment: "orzeczenie", search_by_case: "orzeczenie", saos_cite_check: "citator",
  search_cjeu_by_ecli: "orzeczenie_ue", get_act: "akt", get_act_text: "akt", search_by_celex: "akt_ue",
  get_entity: "podmiot", get_entity_full: "podmiot", get_board: "podmiot",
  get_interpretation: "interpretacja", search_by_signature: "interpretacja",
};
const ID_KEYS = ["caseNumber", "case_number", "signature", "eli", "celex", "ecli", "krs", "krsNumber",
  "krs_number", "id", "doc_id", "judgmentId", "query", "phrase", "title", "sector"];

function ttlDays(tool) {
  const env = process.env[`GP_CACHE_TTL_${SERVER}_${tool}`.toUpperCase().replace(/[^A-Z0-9_]/g, "_")];
  if (env !== undefined && env !== "") return Number(env);
  const t = TTL[SERVER] || {};
  return tool in t ? t[tool] : ("*" in t ? t["*"] : 7);
}

// --- baza GROUNDING-PRAWO --------------------------------------------------
function looksLikeRoot(d) {
  return d && fs.existsSync(path.join(d, "CACHE")) && fs.existsSync(path.join(d, "INDEX"));
}
function writable(d) {
  // Realny zapis i odczyt: na uszkodzonym udziale SMB stat i touch przechodza (lexcache).
  try {
    const probe = path.join(d, "CACHE", `.gp-probe-${process.pid}`);
    fs.writeFileSync(probe, "ok");
    const ok = fs.readFileSync(probe, "utf8") === "ok";
    fs.unlinkSync(probe);
    return ok;
  } catch {
    return false;
  }
}
function resolveRoot() {
  const h = os.homedir();
  const c = [process.env.GROUNDING_ROOT, process.cwd(), process.env.CLAUDE_PROJECT_DIR];
  for (const od of ["OneDrive", "Library/CloudStorage/OneDrive-Personal", "Library/CloudStorage/OneDrive-Osobisty"]) {
    c.push(path.join(h, od, "LEGAL", "GROUNDING-PRAWO"), path.join(h, od, "GROUNDING-PRAWO"));
  }
  c.push("E:\\OneDrive\\LEGAL\\GROUNDING-PRAWO", "/mnt/e/OneDrive/LEGAL/GROUNDING-PRAWO", "/Volumes/GROUNDING-PRAWO");
  try { // Cowork: podpiety folder w maszynie wirtualnej
    for (const s of fs.readdirSync("/sessions")) {
      const mnt = path.join("/sessions", s, "mnt");
      if (fs.existsSync(mnt)) for (const m of fs.readdirSync(mnt)) c.push(path.join(mnt, m));
    }
  } catch { /* brak /sessions */ }
  for (const d of c) if (looksLikeRoot(d) && writable(d)) return { root: d, cache: path.join(d, "CACHE") };
  const fb = path.join(h, ".cache", "grounding-prawo", "CACHE");
  fs.mkdirSync(fb, { recursive: true });
  return { root: null, cache: fb };
}
const { root: ROOT, cache: CACHE } = resolveRoot();
process.stderr.write(`[gp-cache ${SERVER}] cache: ${CACHE}${ROOT ? "" : " (brak bazy GROUNDING-PRAWO - cache lokalny)"}\n`);

// --- zapis i odczyt wpisow ------------------------------------------------------
function canonical(v) {
  if (Array.isArray(v)) return v.map(canonical);
  if (v && typeof v === "object") return Object.fromEntries(Object.keys(v).sort().map((k) => [k, canonical(v[k])]));
  return v;
}
function entryPath(tool, args) {
  const key = createHash("sha256").update(JSON.stringify([SERVER, tool, canonical(args || {})])).digest("hex").slice(0, 16);
  const dir = path.join(CACHE, SOURCE_DIR[SERVER] || SERVER);
  return { key, file: path.join(dir, `mcp-${tool}-${key}.md`) };
}
function yamlStr(s) {
  return JSON.stringify(String(s));
}
function readEntry(file) {
  try {
    const t = fs.readFileSync(file, "utf8");
    const fm = /^---\n([\s\S]*?)\n---\n/.exec(t);
    const js = /```json\n([\s\S]*)\n```\s*$/.exec(t);
    if (!fm || !js) return null;
    const meta = Object.fromEntries(fm[1].split("\n").map((l) => {
      const i = l.indexOf(":");
      return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^"(.*)"$/, "$1")];
    }));
    return { meta, result: JSON.parse(js[1]) };
  } catch {
    return null;
  }
}
function writeEntry(file, key, tool, args, result, ttl) {
  const now = new Date();
  const exp = new Date(now.getTime() + ttl * 86400000);
  const iso = (d) => d.toISOString().replace(/\.\d{3}Z$/, "Z");
  const id = ID_KEYS.map((k) => args?.[k]).find((v) => v !== undefined && v !== "");
  const text = (result.content || []).filter((c) => c.type === "text").map((c) => c.text).join("\n\n");
  const md = [
    "---",
    "status: FOUND",
    `query_type: ${QUERY_TYPE[tool] || "wyszukiwanie"}`,
    `source: ${SOURCE_DIR[SERVER] || SERVER}`,
    `tool: ${yamlStr(`mcp:${SERVER}.${tool}`)}`,
    `query: ${yamlStr(JSON.stringify(args || {}))}`,
    ...(id !== undefined ? [`identyfikator: ${yamlStr(id)}`] : []),
    "origin: mcp-cache",
    `retrieved_at: ${yamlStr(iso(now))}`,
    `expires_at: ${yamlStr(iso(exp))}`,
    `ttl_days: ${ttl}`,
    "confidence: deterministic",
    `cache_key: ${key}`,
    "---",
    text,
    "",
    "```json",
    JSON.stringify(result, null, 1),
    "```",
    "",
  ].join("\n");
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = `${file}.tmp-${process.pid}`;
  fs.writeFileSync(tmp, md);
  fs.renameSync(tmp, file);
}
// G5: werdykt citatora trafia do frontmattera orzeczenia w korpusie i w cache SAOS,
// zeby `lexcache find --field cite_check=przelamanie_wykryte` odpowiadalo, ktore
// orzeczenia, na ktorych stoja pisma, przestaly zyc.
function markCiteCheck(caseNumber, result) {
  const verdict = result?.structuredContent?.verdict;
  if (!verdict || !caseNumber) return 0;
  const norm = (s) => String(s || "").replace(/\s+/g, " ").trim().toUpperCase();
  const target = norm(caseNumber);
  const now = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
  const dirs = [path.join(CACHE, "saos"), ...(ROOT ? [path.join(ROOT, "ORZECZENIA")] : [])];
  let marked = 0;
  for (const d of dirs) {
    let files = [];
    try { files = fs.readdirSync(d).filter((f) => f.endsWith(".md") && !f.startsWith("mcp-saos_cite_check-")); } catch { continue; }
    for (const f of files) {
      const p = path.join(d, f);
      let t;
      try { t = fs.readFileSync(p, "utf8"); } catch { continue; }
      const fm = /^---\n([\s\S]*?)\n---\n/.exec(t);
      if (!fm) continue;
      const sigs = [...fm[1].matchAll(/^(?:sygnatura|identyfikator):\s*"?([^"\n]*)"?\s*$/gm)].map((x) => norm(x[1]));
      if (!sigs.includes(target)) continue;
      const meta = fm[1].replace(/^cite_check(?:_at)?:.*(?:\n|$)/gm, "").replace(/\n+$/, "");
      fs.writeFileSync(p, `---\n${meta}\ncite_check: ${verdict}\ncite_check_at: "${now}"\n---\n` + t.slice(fm[0].length));
      marked++;
    }
  }
  return marked;
}

function withNote(result, note) {
  return { ...result, content: [{ type: "text", text: note }, ...(result.content || [])] };
}
function relToRoot(file) {
  return ROOT ? path.relative(ROOT, file).split(path.sep).join("/") : file;
}

// --- posrednik ----------------------------------------------------------------
const MODE = (process.env.GP_CACHE || "").toLowerCase();
const childEnv = { ...process.env };
if (SERVER === "eu-compliance" && ROOT && !childEnv.EU_COMPLIANCE_DB) {
  const db = path.join(ROOT, "CACHE", "eu-compliance", "regulations.db");
  if (fs.existsSync(db)) childEnv.EU_COMPLIANCE_DB = db;
}
const child = spawn(CHILD[0], CHILD.slice(1), { stdio: ["pipe", "pipe", "inherit"], env: childEnv });
const pending = new Map(); // id -> { tool, args, key, file, ttl, stale }
const send = (msg) => process.stdout.write(JSON.stringify(msg) + "\n");

function answerStale(id, p, reason) {
  const note = `[GROUNDING-PRAWO cache] ${reason} - zwracam wpis pobrany ${p.stale.meta.retrieved_at}` +
    `${p.stale.meta.expires_at < new Date().toISOString() ? " (WYGASLY - zweryfikuj w zrodle przed cytowaniem)" : ""}; ` +
    `plik ${relToRoot(p.file)}`;
  send({ jsonrpc: "2.0", id, result: withNote(p.stale.result, note) });
}

readline.createInterface({ input: process.stdin, crlfDelay: Infinity }).on("line", (line) => {
  if (!line.trim()) return;
  let msg;
  try { msg = JSON.parse(line); } catch { child.stdin.write(line + "\n"); return; }
  if (msg && msg.method === "tools/call" && msg.id !== undefined && MODE !== "off") {
    const tool = msg.params?.name;
    const args = msg.params?.arguments || {};
    const ttl = ttlDays(tool);
    if (ttl > 0) {
      const { key, file } = entryPath(tool, args);
      const entry = readEntry(file);
      const fresh = entry && entry.meta.expires_at > new Date().toISOString();
      if (fresh && MODE !== "refresh") {
        send({ jsonrpc: "2.0", id: msg.id, result: withNote(entry.result,
          `[GROUNDING-PRAWO cache] wynik pobrany ${entry.meta.retrieved_at}, wazny do ${entry.meta.expires_at}; plik ${relToRoot(file)}`) });
        return;
      }
      pending.set(msg.id, { tool, args, key, file, ttl, stale: entry });
    }
  }
  child.stdin.write(line + "\n");
});
process.stdin.on("end", () => child.stdin.end());

readline.createInterface({ input: child.stdout, crlfDelay: Infinity }).on("line", (line) => {
  let msg;
  try { msg = JSON.parse(line); } catch { process.stdout.write(line + "\n"); return; }
  const p = msg && msg.id !== undefined ? pending.get(msg.id) : undefined;
  if (!p) { process.stdout.write(line + "\n"); return; }
  pending.delete(msg.id);
  const failed = msg.error || msg.result?.isError;
  if (failed && p.stale) { answerStale(msg.id, p, "zrodlo zwrocilo blad"); return; }
  if (!failed && msg.result) {
    try {
      writeEntry(p.file, p.key, p.tool, p.args, msg.result, p.ttl);
      if (SERVER === "saos" && p.tool === "saos_cite_check") markCiteCheck(p.args.caseNumber, msg.result);
    } catch (e) { process.stderr.write(`[gp-cache ${SERVER}] zapis nieudany: ${e.message}\n`); }
  }
  process.stdout.write(line + "\n");
});

child.on("exit", (code) => {
  for (const [id, p] of pending) {
    if (p.stale) answerStale(id, p, "serwer zrodla nie dziala");
    else send({ jsonrpc: "2.0", id, error: { code: -32000, message: `serwer ${SERVER} zakonczyl dzialanie (kod ${code})` } });
  }
  pending.clear();
  process.exit(code ?? 0);
});
