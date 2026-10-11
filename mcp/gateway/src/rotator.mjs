// rotator - wbudowany rotator IP gatewaya.
//
// Lokalny proxy HTTP (CONNECT) na 127.0.0.1, przez ktory serwery-dzieci (HTTPS_PROXY) wychodza do hostow
// blokujacych IP za CGNAT. Dla hostow spoza listy ruch idzie bezposrednio (nie liczymy GB u dostawcy).
// Upstream, w kolejnosci: (1) pula LEXCACHE_PROXY (http/https, "{session}" = id sesji u dostawcy,
// np. rezydencjalne PL), (2) Tor (SOCKS5, kazda sesja = osobne dane logowania = nowy obwod),
// (3) bezposrednio (rotacja niemozliwa - status to pokazuje).
// rotate() zmienia sesje i zrywa otwarte tunele, wiec kolejne polaczenia dostaja nowe IP.
import crypto from "node:crypto";
import http from "node:http";
import net from "node:net";
import tls from "node:tls";

const sid = () => crypto.randomBytes(8).toString("hex");

export class Rotator {
  constructor({ pool = [], torUrl = "", hosts = [], log = () => {} }) {
    this.pool = pool;
    this.tor = torUrl ? new URL(torUrl) : null;
    this.hosts = hosts.map((h) => h.toLowerCase());
    this.log = log;
    this.mode = pool.length ? "pool" : this.tor ? "tor" : "direct";
    this.rotations = 0;
    this.conns = new Set();
    this.port = 0;
    this.#newSession();
  }

  #newSession() {
    this.session = sid();
    this.poolEntry = this.pool.length ? this.pool[Math.floor(Math.random() * this.pool.length)] : null;
  }

  matches(host) {
    const h = String(host).toLowerCase();
    return this.hosts.some((x) => h === x || h.endsWith("." + x));
  }

  get proxyUrl() {
    return `http://127.0.0.1:${this.port}`;
  }

  describe() {
    const masked = this.poolEntry ? this.poolEntry.replace(/\/\/[^@]*@/, "//***@") : null;
    return { mode: this.mode, session: this.session, rotations: this.rotations, hosts: this.hosts,
      upstream: masked || (this.tor ? `${this.tor.protocol}//${this.tor.host}` : null), activeTunnels: this.conns.size };
  }

  rotate(reason = "") {
    this.#newSession();
    this.rotations++;
    for (const s of this.conns) s.destroy();
    this.conns.clear();
    this.log(`rotacja IP #${this.rotations} (${reason || "zadanie"}), tryb ${this.mode}, sesja ${this.session}`);
  }

  // Tunel TCP do host:port - wybor upstreamu wg trybu; dla hostow spoza listy bezposrednio.
  async tunnel(host, port) {
    if (this.mode === "direct" || !this.matches(host)) return this.#direct(host, port);
    const sock = this.mode === "pool" ? await this.#viaHttpProxy(host, port) : await this.#viaSocks(host, port);
    this.conns.add(sock);
    sock.on("close", () => this.conns.delete(sock));
    return sock;
  }

  #direct(host, port) {
    return new Promise((resolve, reject) => {
      const s = net.connect(port, host);
      s.once("connect", () => resolve(s));
      s.once("error", reject);
    });
  }

  async #viaHttpProxy(host, port) {
    const u = new URL(this.poolEntry.replace("{session}", this.session));
    const up = await new Promise((resolve, reject) => {
      const s = u.protocol === "https:"
        ? tls.connect({ host: u.hostname, port: Number(u.port) || 443, servername: u.hostname })
        : net.connect(Number(u.port) || 80, u.hostname);
      s.once(u.protocol === "https:" ? "secureConnect" : "connect", () => resolve(s));
      s.once("error", reject);
    });
    const auth = u.username
      ? `Proxy-Authorization: Basic ${Buffer.from(`${decodeURIComponent(u.username)}:${decodeURIComponent(u.password)}`).toString("base64")}\r\n`
      : "";
    up.write(`CONNECT ${host}:${port} HTTP/1.1\r\nHost: ${host}:${port}\r\n${auth}\r\n`);
    const head = await readUntil(up, "\r\n\r\n");
    const code = Number(/^HTTP\/1\.[01] (\d{3})/.exec(head.toString("latin1"))?.[1]);
    if (code !== 200) { up.destroy(); throw new Error(`proxy upstream odrzucilo CONNECT (${code || "brak odpowiedzi"})`); }
    return up;
  }

  // SOCKS5 z uwierzytelnieniem user/haslo (RFC 1929). Tor izoluje obwody po danych logowania.
  async #viaSocks(host, port) {
    const t = this.tor;
    const s = await new Promise((resolve, reject) => {
      const c = net.connect(Number(t.port) || 9050, t.hostname);
      c.once("connect", () => resolve(c));
      c.once("error", reject);
    });
    const user = Buffer.from(`gw${this.session}`), pass = Buffer.from(sid());
    s.write(Buffer.from([5, 1, 2]));
    let r = await readN(s, 2);
    if (r[0] !== 5 || r[1] !== 2) { s.destroy(); throw new Error("SOCKS5: serwer nie przyjal uwierzytelnienia"); }
    s.write(Buffer.concat([Buffer.from([1, user.length]), user, Buffer.from([pass.length]), pass]));
    r = await readN(s, 2);
    if (r[1] !== 0) { s.destroy(); throw new Error("SOCKS5: odrzucone dane logowania"); }
    const h = Buffer.from(host);
    s.write(Buffer.concat([Buffer.from([5, 1, 0, 3, h.length]), h, Buffer.from([port >> 8, port & 255])]));
    r = await readN(s, 4);
    if (r[1] !== 0) { s.destroy(); throw new Error(`SOCKS5: CONNECT nieudany (kod ${r[1]})`); }
    // adres zwrotny (ATYP 1 = IPv4, 4 = IPv6, 3 = nazwa) + port - do odrzucenia
    const rest = r[3] === 1 ? 6 : r[3] === 4 ? 18 : (await readN(s, 1))[0] + 2;
    await readN(s, rest);
    return s;
  }

  // Zewnetrzne IP widziane przez rotator (diagnostyka, gateway__status).
  async egressIp() {
    const sock = await this.tunnel("api.ipify.org", 443);
    const t = tls.connect({ socket: sock, servername: "api.ipify.org" });
    t.write("GET / HTTP/1.1\r\nHost: api.ipify.org\r\nConnection: close\r\n\r\n");
    const chunks = [];
    for await (const c of t) chunks.push(c);
    return Buffer.concat(chunks).toString().split("\r\n\r\n").pop().trim();
  }

  start() {
    const srv = http.createServer((req, res) => {
      // zwykly HTTP (rzadki): bez rotacji, prosto do celu
      let u;
      try { u = new URL(req.url); } catch { res.writeHead(400).end(); return; }
      const up = http.request({ host: u.hostname, port: u.port || 80, path: u.pathname + u.search, method: req.method, headers: req.headers },
        (r) => { res.writeHead(r.statusCode, r.headers); r.pipe(res); });
      up.on("error", () => res.writeHead(502).end());
      req.pipe(up);
    });
    srv.on("connect", async (req, client, head) => {
      const [host, p] = req.url.split(":");
      try {
        const up = await this.tunnel(host, Number(p) || 443);
        client.write("HTTP/1.1 200 Connection Established\r\n\r\n");
        if (head?.length) up.write(head);
        up.pipe(client); client.pipe(up);
        const end = () => { up.destroy(); client.destroy(); };
        up.on("error", end); client.on("error", end); up.on("close", end); client.on("close", end);
      } catch (e) {
        this.log(`tunel ${host}: ${e.message}`);
        client.end("HTTP/1.1 502 Bad Gateway\r\n\r\n");
      }
    });
    return new Promise((resolve) => srv.listen(0, "127.0.0.1", () => {
      this.port = srv.address().port;
      this.server = srv;
      this.log(`rotator: tryb ${this.mode}, proxy ${this.proxyUrl}, hosty: ${this.hosts.join(", ") || "(brak)"}`);
      resolve(this);
    }));
  }
}

function readN(sock, n) {
  return new Promise((resolve, reject) => {
    let buf = Buffer.alloc(0);
    const on = (d) => {
      buf = Buffer.concat([buf, d]);
      if (buf.length >= n) { cleanup(); if (buf.length > n) sock.unshift(buf.subarray(n)); resolve(buf.subarray(0, n)); }
    };
    const err = (e) => { cleanup(); reject(e); };
    const end = () => { cleanup(); reject(new Error("polaczenie zamkniete")); };
    const cleanup = () => { sock.off("data", on); sock.off("error", err); sock.off("close", end); };
    sock.on("data", on); sock.once("error", err); sock.once("close", end);
  });
}

function readUntil(sock, marker) {
  return new Promise((resolve, reject) => {
    let buf = Buffer.alloc(0);
    const on = (d) => {
      buf = Buffer.concat([buf, d]);
      const i = buf.indexOf(marker);
      if (i >= 0) { cleanup(); if (buf.length > i + marker.length) sock.unshift(buf.subarray(i + marker.length)); resolve(buf.subarray(0, i + marker.length)); }
    };
    const err = (e) => { cleanup(); reject(e); };
    const end = () => { cleanup(); reject(new Error("polaczenie zamkniete")); };
    const cleanup = () => { sock.off("data", on); sock.off("error", err); sock.off("close", end); };
    sock.on("data", on); sock.once("error", err); sock.once("close", end);
  });
}
