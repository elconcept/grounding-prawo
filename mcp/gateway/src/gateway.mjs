#!/usr/bin/env node
// gateway - jeden serwer MCP (Streamable HTTP) przed wszystkimi serwerami prawnymi repozytorium.
//
//   POST /mcp              wszystkie serwery, narzedzia jako <serwer>__<narzedzie> + gateway__*
//   POST /mcp/<serwer>     jeden serwer, nazwy narzedzi bez prefiksu
//   GET  /healthz          stan dzieci i rotatora (bez sekretow)
//
// Warstwy: (1) cache plikowy = istniejacy gp-cache jako dziecko (wspolny z lexcache), (2) wbudowany rotator IP (rotator.mjs),
// (3) dzieci = serwery stdio z servers.json, uruchamiane i restartowane przez gateway.
// Uwierzytelnianie robi Cloudflare Access przed gatewayem; sam gateway slucha tylko w LAN/kontenerze.
import { spawn } from "node:child_process";
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { Rotator } from "./rotator.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const E = process.env;
const MCP_DIR = path.resolve(E.MCP_DIR || path.join(HERE, "..", ".."));
const PORT = Number(E.PORT || 8770);
const BIND = E.GATEWAY_BIND || "0.0.0.0";
const RETRIES = Number(E.GATEWAY_PROXY_RETRIES ?? E.LEXCACHE_PROXY_RETRIES ?? 3);
const CALL_TIMEOUT = Number(E.GATEWAY_CALL_TIMEOUT_MS || 180000);
const log = (m) => process.stderr.write(`[gateway ${new Date().toISOString()}] ${m}\n`);
const subst = (s) => String(s).replaceAll("{mcp}", MCP_DIR);

const registry = JSON.parse(fs.readFileSync(E.GATEWAY_SERVERS || path.join(HERE, "..", "servers.json"), "utf8")).servers;

// --- rotator IP -----------------------------------------------------------------------------------------------
const DEFAULT_HOSTS = "saos.org.pl,orzeczenia.nsa.gov.pl,orzeczenia.ms.gov.pl,orzeczenia.uzp.gov.pl,sn.pl,trybunal.gov.pl";
const hosts = (E.GATEWAY_PROXY_HOSTS || E.LEXCACHE_PROXY_HOSTS || DEFAULT_HOSTS).split(",").map((x) => x.trim()).filter(Boolean);
const pool = (E.LEXCACHE_PROXY || "").split(",").map((x) => x.trim()).filter((x) => /^https?:/i.test(x));
let torProc = null;
async function startTor() {
  // GATEWAY_TOR=socks5://host:port (zewnetrzny) albo "spawn" (domyslnie, gdy jest binarka tor i brak puli proxy)
  const want = E.GATEWAY_TOR ?? "spawn";
  if (pool.length || want === "off" || want === "") return "";
  if (want !== "spawn") return want;
  const port = Number(E.GATEWAY_TOR_PORT || 9050); // 9050 = port, na ktorym oczekuje go api-rotator-mcp
  try {
    torProc = spawn("tor", ["--SocksPort", `127.0.0.1:${port}`, "--DataDirectory", E.GATEWAY_TOR_DIR || "/tmp/gateway-tor", "--Log", "notice stderr"], { stdio: ["ignore", "ignore", "pipe"] });
  } catch { return ""; }
  const ok = await new Promise((resolve) => {
    const t = setTimeout(() => resolve(false), 90000);
    torProc.on("error", () => { clearTimeout(t); resolve(false); });
    torProc.on("exit", () => { clearTimeout(t); resolve(false); });
    torProc.stderr.on("data", (d) => { if (/Bootstrapped 100%/.test(d)) { clearTimeout(t); resolve(true); } });
  });
  if (!ok) { log("Tor nie wystartowal - rotator bez upstreamu (tryb direct)"); torProc?.kill(); return ""; }
  torProc.on("exit", (c) => log(`Tor zakonczyl dzialanie (kod ${c}) - restart gatewaya naprawi`));
  return `socks5://127.0.0.1:${port}`;
}
const rotator = new Rotator({ pool, torUrl: await startTor(), hosts, log: (m) => log(m) });
await rotator.start();
if (rotator.mode === "direct") log("UWAGA: brak LEXCACHE_PROXY i Tora - hosty blokujace IP beda dostepne tylko z wlasnego IP, rotacja niemozliwa");

// --- dzieci (serwery stdio) --------------------------------------------------------------------------------------
class Child {
  constructor(name, spec) {
    this.name = name; this.spec = spec;
    this.state = "stopped"; this.tools = []; this.instructions = ""; this.client = null;
    this.backoff = 2000; this.lastError = null; this.ready = null;
  }

  start() {
    if (this.ready) return this.ready;
    this.state = "starting";
    this.ready = (async () => {
      const env = { ...E };
      for (const [k, v] of Object.entries(this.spec.env || {})) env[k] = subst(v);
      if (this.spec.proxy && rotator.mode !== "direct") {
        // gp-cache bierze proxy z LEXCACHE_PROXY (tylko dla saos,nsa); kio i inne dostaja standardowe zmienne
        Object.assign(env, { LEXCACHE_PROXY: rotator.proxyUrl, HTTPS_PROXY: rotator.proxyUrl, HTTP_PROXY: rotator.proxyUrl, https_proxy: rotator.proxyUrl,
          http_proxy: rotator.proxyUrl, NODE_USE_ENV_PROXY: "1", NO_PROXY: "localhost,127.0.0.1", no_proxy: "localhost,127.0.0.1" });
      } else {
        delete env.LEXCACHE_PROXY;
      }
      const transport = new StdioClientTransport({ command: subst(this.spec.command), args: (this.spec.args || []).map(subst), env, stderr: "pipe" });
      transport.stderr?.on("data", (d) => String(d).trimEnd().split("\n").forEach((l) => log(`${this.name}: ${l}`)));
      const client = new Client({ name: "abogada-gateway", version: "0.1.0" });
      transport.onclose = () => this.#down("proces zakonczony");
      await client.connect(transport);
      const tools = [];
      let cursor;
      do { const r = await client.listTools({ cursor }); tools.push(...r.tools); cursor = r.nextCursor; } while (cursor);
      Object.assign(this, { client, tools, instructions: client.getInstructions() || "", state: "ready", backoff: 2000, lastError: null });
      log(`${this.name}: gotowy, ${tools.length} narzedzi`);
    })().catch((e) => { this.#down(e.message); });
    return this.ready;
  }

  #down(why) {
    if (this.state === "stopped") return;
    this.state = "down"; this.lastError = why; this.client = null; this.ready = null;
    log(`${this.name}: niedostepny (${why}); ponowna proba za ${this.backoff / 1000}s`);
    const wait = this.backoff;
    this.backoff = Math.min(this.backoff * 2, 60000);
    setTimeout(() => { if (this.state === "down") this.start(); }, wait).unref();
  }

  async call(tool, args) {
    if (this.state !== "ready") await Promise.race([this.start(), new Promise((r) => setTimeout(r, 30000))]);
    if (this.state !== "ready" || !this.client) throw new Error(`serwer ${this.name} niedostepny: ${this.lastError || this.state}`);
    return this.client.callTool({ name: tool, arguments: args }, undefined, { timeout: CALL_TIMEOUT });
  }
}

const children = new Map();
for (const [name, spec] of Object.entries(registry)) children.set(name, new Child(name, spec));
await Promise.allSettled([...children.values()].map((c) => c.start()));

// --- wywolanie narzedzia: cache robi gp-cache (dziecko); gateway tylko rotuje IP po blokadzie -------------------------
const textOf = (r) => (r?.content || []).filter((c) => c.type === "text").map((c) => c.text || "").join("\n");
const errRes = (t) => ({ isError: true, content: [{ type: "text", text: t }] });
const BLOCK = /captcha|access denied|request rejected|too many requests|zbyt wiele zapyta|unusual traffic|forbidden|\b(403|429)\b|timeout|timed out|ETIMEDOUT|ECONNRESET|fetch failed|socket hang up/i;

async function callThrough(child, tool, args) {
  const rotating = child.spec.proxy && rotator.mode !== "direct";
  let res;
  for (let attempt = 0; attempt <= (rotating ? RETRIES : 0); attempt++) {
    try { res = await child.call(tool, args); } catch (e) { res = errRes(e.message); }
    const blocked = rotating && res.isError && BLOCK.test(textOf(res).slice(0, 3000));
    if (!blocked) return res;
    if (attempt < RETRIES) rotator.rotate(`blokada/blad zrodla ${child.name}.${tool}, proba ${attempt + 1}/${RETRIES}`);
  }
  return errRes(`[BLOKADA] ${child.name}.${tool}: zrodlo odrzuca ruch mimo ${RETRIES} zmian IP (tryb ${rotator.mode}). To nie jest "brak wyniku". ` +
    `Powiedz uzytkownikowi, ze trzeba zmienic proxy (LEXCACHE_PROXY) albo odczekac.\n${textOf(res).slice(0, 500)}`);
}

// --- narzedzia wlasne gatewaya ------------------------------------------------------------------------------------
const OWN = [
  { name: "gateway__status", description: "Stan gatewaya: serwery (gotowe/niedostepne), rotator IP (tryb, sesja, liczba rotacji, zewnetrzne IP).",
    inputSchema: { type: "object", properties: { check_ip: { type: "boolean", description: "sprawdz zewnetrzne IP widziane przez rotator (api.ipify.org)" } } } },
  { name: "gateway__rotate_ip", description: "Wymusza zmiane IP rotatora (nowa sesja proxy / nowy obwod Tor). Uzyj po stwierdzeniu blokady zrodla.",
    inputSchema: { type: "object", properties: {} } },
];
async function callOwn(name, args) {
  const json = (o) => ({ content: [{ type: "text", text: JSON.stringify(o, null, 1) }], structuredContent: o });
  if (name === "gateway__status") {
    const o = { rotator: rotator.describe(), servers: Object.fromEntries([...children].map(([n, c]) => [n, { state: c.state, tools: c.tools.length, error: c.lastError }])) };
    if (args.check_ip) o.egressIp = await rotator.egressIp().catch((e) => `blad: ${e.message}`);
    return json(o);
  }
  if (name === "gateway__rotate_ip") { rotator.rotate("reczne"); return json(rotator.describe()); }
  return errRes(`nieznane narzedzie ${name}`);
}

// --- serwer MCP ---------------------------------------------------------------------------------------------------
function buildServer(only) {
  const list = only ? [children.get(only)] : [...children.values()];
  const instructions = list.filter((c) => c.instructions).map((c) => `## ${c.name}\n${c.instructions}`).join("\n\n");
  const header = only ? "" : "Gateway MCP repozytorium abogada: narzedzia maja prefiks <serwer>__. Cache plikowy (wspolny z lexcache: mcp/cache) robi gp-cache; odswiezenie = GP_CACHE=refresh po stronie gatewaya. Wyniki z cache niosa linie [GROUNDING-PRAWO cache] z data pobrania; blokada zrodla to [BLOKADA], nie brak wyniku.\n\nKolejnosc pracy: (0) `lexcache find` / cache; (1) repertorium__szukaj_repertorium - wyszukiwanie semantyczne, zwraca tylko skrocone fragmenty i odesylacze (limit dzienny, wynik trafia do cache); (2) pelny tekst z zrodla wskazanego przez repertorium: saos__get_judgment / saos__search_by_case, nsa__*, isap__get_act_text, eu-sparql__*, kio__*, eureka__*. Repertorium nie jest zrodlem cytowalnosci - cytuje sie zrodlo.\n\n";
  const s = new Server({ name: "abogada-mcp-gateway", version: "0.1.0" }, { capabilities: { tools: {} }, instructions: header + instructions });
  const prefix = (c, t) => (only ? t : `${c.name}__${t}`);
  s.setRequestHandler(ListToolsRequestSchema, async () => {
    const tools = [];
    for (const c of list) {
      for (const t of c.tools) {
        const schema = { type: "object", ...(t.inputSchema || {}) };
        tools.push({ ...t, name: prefix(c, t.name), inputSchema: schema });
      }
    }
    return { tools: only ? tools : [...tools, ...OWN] };
  });
  s.setRequestHandler(CallToolRequestSchema, async (req) => {
    const { name } = req.params;
    const args = { ...(req.params.arguments || {}) };
    if (!only && name.startsWith("gateway__")) return callOwn(name, args);
    let child, tool;
    if (only) { child = children.get(only); tool = name; }
    else { const i = name.indexOf("__"); child = children.get(name.slice(0, i)); tool = name.slice(i + 2); }
    if (!child || !child.tools.some((t) => t.name === tool)) return errRes(`nieznane narzedzie ${name}`);
    return callThrough(child, tool, args);
  });
  return s;
}

const readBody = (req) => new Promise((resolve, reject) => {
  const chunks = []; let n = 0;
  req.on("data", (c) => { n += c.length; if (n > 4e6) { reject(new Error("body za duze")); req.destroy(); } else chunks.push(c); });
  req.on("end", () => { try { resolve(chunks.length ? JSON.parse(Buffer.concat(chunks).toString()) : undefined); } catch (e) { reject(e); } });
  req.on("error", reject);
});

http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://x");
  if (url.pathname === "/healthz") {
    const o = { ok: [...children.values()].some((c) => c.state === "ready"), rotator: rotator.describe().mode,
      servers: Object.fromEntries([...children].map(([n, c]) => [n, c.state])) };
    res.writeHead(o.ok ? 200 : 503, { "content-type": "application/json" }).end(JSON.stringify(o));
    return;
  }
  const m = /^\/mcp(?:\/([\w-]+))?\/?$/.exec(url.pathname);
  if (!m || (m[1] && !children.has(m[1]))) { res.writeHead(404).end("not found"); return; }
  if (req.method !== "POST") {
    res.writeHead(405, { allow: "POST", "content-type": "application/json" }).end(JSON.stringify({ jsonrpc: "2.0", error: { code: -32000, message: "Method not allowed (stateless)" }, id: null }));
    return;
  }
  try {
    const body = await readBody(req);
    const server = buildServer(m[1]);
    const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
    res.on("close", () => { transport.close(); server.close(); });
    await server.connect(transport);
    await transport.handleRequest(req, res, body);
  } catch (e) {
    log(`blad zadania: ${e.message}`);
    if (!res.headersSent) res.writeHead(500, { "content-type": "application/json" }).end(JSON.stringify({ jsonrpc: "2.0", error: { code: -32603, message: e.message }, id: null }));
  }
}).listen(PORT, BIND, () => log(`nasluchuje ${BIND}:${PORT}, serwerow: ${children.size}`));

for (const sig of ["SIGINT", "SIGTERM"]) {
  process.on(sig, () => { for (const c of children.values()) { c.state = "stopped"; c.client?.close().catch(() => {}); } torProc?.kill(); process.exit(0); });
}
