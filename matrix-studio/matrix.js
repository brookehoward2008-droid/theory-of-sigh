/* Matrix Studio — web version
 * Pure-JS multi-chain private-key derivation. Runs 100% client-side.
 * Ported from matrix_studio.py.
 */
"use strict";

/* ===========================================================================
 * SECTION 1: secp256k1 elliptic curve (BigInt)
 * ======================================================================== */
const P  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2Fn;
const N  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141n;
const Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798n;
const Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8n;

function mod(a, m) { const r = a % m; return r < 0n ? r + m : r; }

function invMod(a, m) {
  // extended euclid
  let [old_r, r] = [mod(a, m), m];
  let [old_s, s] = [1n, 0n];
  while (r !== 0n) {
    const q = old_r / r;
    [old_r, r] = [r, old_r - q * r];
    [old_s, s] = [s, old_s - q * s];
  }
  return mod(old_s, m);
}

function pointAdd(p1, p2) {
  if (p1 === null) return p2;
  if (p2 === null) return p1;
  const [x1, y1] = p1, [x2, y2] = p2;
  let s;
  if (x1 === x2) {
    if (mod(y1 + y2, P) === 0n) return null;
    s = mod(3n * x1 * x1 * invMod(2n * y1, P), P);
  } else {
    s = mod((y2 - y1) * invMod(mod(x2 - x1, P), P), P);
  }
  const x3 = mod(s * s - x1 - x2, P);
  const y3 = mod(s * (x1 - x3) - y1, P);
  return [x3, y3];
}

function scalarMult(k, point) {
  let result = null, addend = point;
  while (k > 0n) {
    if (k & 1n) result = pointAdd(result, addend);
    addend = pointAdd(addend, addend);
    k >>= 1n;
  }
  return result;
}

function privkeyToPubkeyPoint(k) { return scalarMult(k, [Gx, Gy]); }

/* ===========================================================================
 * SECTION 2: hash functions (pure JS, synchronous, byte-array based)
 * ======================================================================== */
function rotr(x, n) { return (x >>> n) | (x << (32 - n)); }

function sha256(bytes) {
  const K = [
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
    0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
    0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
    0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
  let h = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
  const l = bytes.length;
  const withOne = l + 1;
  const k = (56 - withOne % 64 + 64) % 64;
  const total = withOne + k + 8;
  const msg = new Uint8Array(total);
  msg.set(bytes);
  msg[l] = 0x80;
  const bitLenHi = Math.floor((l * 8) / 0x100000000);
  const bitLenLo = (l * 8) >>> 0;
  const dv = new DataView(msg.buffer);
  dv.setUint32(total - 8, bitLenHi);
  dv.setUint32(total - 4, bitLenLo);
  const w = new Array(64);
  for (let off = 0; off < total; off += 64) {
    for (let i = 0; i < 16; i++) w[i] = dv.getUint32(off + i * 4);
    for (let i = 16; i < 64; i++) {
      const s0 = rotr(w[i-15],7) ^ rotr(w[i-15],18) ^ (w[i-15] >>> 3);
      const s1 = rotr(w[i-2],17) ^ rotr(w[i-2],19) ^ (w[i-2] >>> 10);
      w[i] = (w[i-16] + s0 + w[i-7] + s1) >>> 0;
    }
    let [a,b,c,d,e,f,g,hh] = h;
    for (let i = 0; i < 64; i++) {
      const S1 = rotr(e,6) ^ rotr(e,11) ^ rotr(e,25);
      const ch = (e & f) ^ (~e & g);
      const t1 = (hh + S1 + ch + K[i] + w[i]) >>> 0;
      const S0 = rotr(a,2) ^ rotr(a,13) ^ rotr(a,22);
      const maj = (a & b) ^ (a & c) ^ (b & c);
      const t2 = (S0 + maj) >>> 0;
      hh=g; g=f; f=e; e=(d+t1)>>>0; d=c; c=b; b=a; a=(t1+t2)>>>0;
    }
    h[0]=(h[0]+a)>>>0; h[1]=(h[1]+b)>>>0; h[2]=(h[2]+c)>>>0; h[3]=(h[3]+d)>>>0;
    h[4]=(h[4]+e)>>>0; h[5]=(h[5]+f)>>>0; h[6]=(h[6]+g)>>>0; h[7]=(h[7]+hh)>>>0;
  }
  const out = new Uint8Array(32);
  const odv = new DataView(out.buffer);
  for (let i = 0; i < 8; i++) odv.setUint32(i * 4, h[i]);
  return out;
}

function doubleSha256(b) { return sha256(sha256(b)); }

/* RIPEMD-160 */
function ripemd160(bytes) {
  const rol = (x, n) => ((x << n) | (x >>> (32 - n))) >>> 0;
  const f = (j, x, y, z) => {
    if (j < 16) return (x ^ y ^ z) >>> 0;
    if (j < 32) return ((x & y) | (~x & z)) >>> 0;
    if (j < 48) return ((x | ~y) ^ z) >>> 0;
    if (j < 64) return ((x & z) | (y & ~z)) >>> 0;
    return (x ^ (y | ~z)) >>> 0;
  };
  const K  = [0x00000000,0x5A827999,0x6ED9EBA1,0x8F1BBCDC,0xA953FD4E];
  const KK = [0x50A28BE6,0x5C4DD124,0x6D703EF3,0x7A6D76E9,0x00000000];
  const r = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,7,4,13,1,10,6,15,3,12,0,9,5,2,14,11,8,3,10,14,4,9,15,8,1,2,7,0,6,13,11,5,12,1,9,11,10,0,8,12,4,13,3,7,15,14,5,6,2,4,0,5,9,7,12,2,10,14,1,3,8,11,6,15,13];
  const rr= [5,14,7,0,9,2,11,4,13,6,15,8,1,10,3,12,6,11,3,7,0,13,5,10,14,15,8,12,4,9,1,2,15,5,1,3,7,14,6,9,11,8,12,2,10,0,4,13,8,6,4,1,3,11,15,0,5,12,2,13,9,7,10,14,12,15,10,4,1,5,8,7,6,2,13,14,0,3,9,11];
  const s = [11,14,15,12,5,8,7,9,11,13,14,15,6,7,9,8,7,6,8,13,11,9,7,15,7,12,15,9,11,7,13,12,11,13,6,7,14,9,13,15,14,8,13,6,5,12,7,5,11,12,14,15,14,15,9,8,9,14,5,6,8,6,5,12,9,15,5,11,6,8,13,12,5,12,13,14,11,8,5,6];
  const ss= [8,9,9,11,13,15,15,5,7,7,8,11,14,14,12,6,9,13,15,7,12,8,9,11,7,7,12,7,6,15,13,11,9,7,15,11,8,6,6,14,12,13,5,14,13,13,7,5,15,5,8,11,14,14,6,14,6,9,12,9,12,5,15,8,8,5,12,9,12,5,14,6,8,13,6,5,15,13,11,11];

  let h0=0x67452301,h1=0xEFCDAB89,h2=0x98BADCFE,h3=0x10325476,h4=0xC3D2E1F0;
  const l = bytes.length;
  const withOne = l + 1;
  const k = (56 - withOne % 64 + 64) % 64;
  const total = withOne + k + 8;
  const msg = new Uint8Array(total);
  msg.set(bytes); msg[l] = 0x80;
  const dv = new DataView(msg.buffer);
  const bits = l * 8;
  dv.setUint32(total - 8, bits >>> 0, true);
  dv.setUint32(total - 4, Math.floor(bits / 0x100000000), true);

  const X = new Array(16);
  for (let off = 0; off < total; off += 64) {
    for (let i = 0; i < 16; i++) X[i] = dv.getUint32(off + i * 4, true);
    let A=h0,B=h1,C=h2,D=h3,E=h4, Ap=h0,Bp=h1,Cp=h2,Dp=h3,Ep=h4, T;
    for (let j = 0; j < 80; j++) {
      T = (rol((A + f(j,B,C,D) + X[r[j]] + K[(j/16)|0]) >>> 0, s[j]) + E) >>> 0;
      A=E; E=D; D=rol(C,10); C=B; B=T;
      T = (rol((Ap + f(79-j,Bp,Cp,Dp) + X[rr[j]] + KK[(j/16)|0]) >>> 0, ss[j]) + Ep) >>> 0;
      Ap=Ep; Ep=Dp; Dp=rol(Cp,10); Cp=Bp; Bp=T;
    }
    T = (h1 + C + Dp) >>> 0;
    h1 = (h2 + D + Ep) >>> 0;
    h2 = (h3 + E + Ap) >>> 0;
    h3 = (h4 + A + Bp) >>> 0;
    h4 = (h0 + B + Cp) >>> 0;
    h0 = T;
  }
  const out = new Uint8Array(20);
  const odv = new DataView(out.buffer);
  [h0,h1,h2,h3,h4].forEach((v,i) => odv.setUint32(i*4, v>>>0, true));
  return out;
}

function hash160(b) { return ripemd160(sha256(b)); }

/* Keccak-256 (pre-standard, as used by Ethereum) using BigInt 64-bit lanes */
function keccak256(bytes) {
  const MASK = (1n << 64n) - 1n;
  const RC = [
    0x0000000000000001n,0x0000000000008082n,0x800000000000808An,0x8000000080008000n,
    0x000000000000808Bn,0x0000000080000001n,0x8000000080008081n,0x8000000000008009n,
    0x000000000000008An,0x0000000000000088n,0x0000000080008009n,0x000000008000000An,
    0x000000008000808Bn,0x800000000000008Bn,0x8000000000008089n,0x8000000000008003n,
    0x8000000000008002n,0x8000000000000080n,0x000000000000800An,0x800000008000000An,
    0x8000000080008081n,0x8000000000008080n,0x0000000080000001n,0x8000000080008008n];
  const R = [
    [0n,36n,3n,41n,18n],
    [1n,44n,10n,45n,2n],
    [62n,6n,43n,15n,61n],
    [28n,55n,25n,21n,56n],
    [27n,20n,39n,8n,14n]];
  const rol = (x, n) => ((x << n) | (x >> (64n - n))) & MASK;

  // state[x][y]
  let state = [];
  for (let x = 0; x < 5; x++) state.push([0n,0n,0n,0n,0n]);

  const rate = 136;
  const msg = [];
  for (const b of bytes) msg.push(b);
  msg.push(0x01);
  while (msg.length % rate !== rate - 1) msg.push(0x00);
  msg.push(0x80);

  const keccakF = (st) => {
    for (let rnd = 0; rnd < 24; rnd++) {
      const C = [], D = [];
      for (let x = 0; x < 5; x++) C[x] = st[x][0]^st[x][1]^st[x][2]^st[x][3]^st[x][4];
      for (let x = 0; x < 5; x++) D[x] = C[(x+4)%5] ^ rol(C[(x+1)%5], 1n);
      for (let x = 0; x < 5; x++) for (let y = 0; y < 5; y++) st[x][y] ^= D[x];
      const B = [];
      for (let x = 0; x < 5; x++) B.push([0n,0n,0n,0n,0n]);
      for (let x = 0; x < 5; x++) for (let y = 0; y < 5; y++)
        B[y][(2*x + 3*y) % 5] = rol(st[x][y], R[x][y]);
      for (let x = 0; x < 5; x++) for (let y = 0; y < 5; y++)
        st[x][y] = (B[x][y] ^ ((~B[(x+1)%5][y] & MASK) & B[(x+2)%5][y])) & MASK;
      st[0][0] ^= RC[rnd];
    }
    return st;
  };

  for (let blockStart = 0; blockStart < msg.length; blockStart += rate) {
    for (let i = 0; i < rate / 8; i++) {
      let lane = 0n;
      for (let j = 7; j >= 0; j--) lane = (lane << 8n) | BigInt(msg[blockStart + i*8 + j]);
      const x = i % 5, y = (i / 5) | 0;
      state[x][y] ^= lane;
    }
    state = keccakF(state);
  }

  const out = [];
  while (out.length < 32) {
    for (let y = 0; y < 5 && out.length < 32; y++) {
      for (let x = 0; x < 5 && out.length < 32; x++) {
        let lane = state[x][y];
        for (let j = 0; j < 8 && out.length < 32; j++) {
          out.push(Number(lane & 0xffn)); lane >>= 8n;
        }
      }
    }
    if (out.length < 32) state = keccakF(state);
  }
  return new Uint8Array(out.slice(0, 32));
}

/* ===========================================================================
 * SECTION 3: Base58 + Bech32
 * ======================================================================== */
const B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
function base58encode(bytes) {
  let x = 0n;
  for (const b of bytes) x = (x << 8n) | BigInt(b);
  let out = "";
  while (x > 0n) { out = B58[Number(x % 58n)] + out; x /= 58n; }
  for (const b of bytes) { if (b === 0) out = "1" + out; else break; }
  return out;
}
function base58check(versionBytes, payload) {
  const data = concat(versionBytes, payload);
  const checksum = doubleSha256(data).slice(0, 4);
  return base58encode(concat(data, checksum));
}

const BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l";
function bech32Polymod(values) {
  const GEN = [0x3b6a57b2,0x26508e6d,0x1ea119fa,0x3d4233dd,0x2a1462b3];
  let chk = 1;
  for (const v of values) {
    const b = chk >> 25;
    chk = ((chk & 0x1ffffff) << 5) ^ v;
    for (let i = 0; i < 5; i++) if ((b >> i) & 1) chk ^= GEN[i];
  }
  return chk >>> 0;
}
function bech32HrpExpand(hrp) {
  const a = [], b = [];
  for (const c of hrp) a.push(c.charCodeAt(0) >> 5);
  for (const c of hrp) b.push(c.charCodeAt(0) & 31);
  return a.concat([0], b);
}
function bech32CreateChecksum(hrp, data) {
  const values = bech32HrpExpand(hrp).concat(data);
  const polymod = bech32Polymod(values.concat([0,0,0,0,0,0])) ^ 1;
  const out = [];
  for (let i = 0; i < 6; i++) out.push((polymod >> (5 * (5 - i))) & 31);
  return out;
}
function bech32Encode(hrp, data) {
  const combined = data.concat(bech32CreateChecksum(hrp, data));
  return hrp + "1" + combined.map(d => BECH32_CHARSET[d]).join("");
}
function convertBits(data, from, to, pad) {
  let acc = 0, bits = 0; const ret = []; const maxv = (1 << to) - 1;
  for (const value of data) {
    if (value < 0 || (value >> from)) return null;
    acc = (acc << from) | value; bits += from;
    while (bits >= to) { bits -= to; ret.push((acc >> bits) & maxv); }
  }
  if (pad) { if (bits) ret.push((acc << (to - bits)) & maxv); }
  else if (bits >= from || ((acc << (to - bits)) & maxv)) return null;
  return ret;
}
function segwitEncode(hrp, witver, witprog) {
  return bech32Encode(hrp, [witver].concat(convertBits(witprog, 8, 5, true)));
}

/* ===========================================================================
 * SECTION 4: helpers + multi-chain derivation
 * ======================================================================== */
function concat(...arrs) {
  let len = 0; for (const a of arrs) len += a.length;
  const out = new Uint8Array(len); let o = 0;
  for (const a of arrs) { out.set(a, o); o += a.length; }
  return out;
}
function intToBytes32(n) {
  const out = new Uint8Array(32);
  let x = n;
  for (let i = 31; i >= 0; i--) { out[i] = Number(x & 0xffn); x >>= 8n; }
  return out;
}
function toHex(bytes) {
  let s = ""; for (const b of bytes) s += b.toString(16).padStart(2, "0"); return s;
}
function bigToHex64(n) { return n.toString(16).padStart(64, "0"); }

function pubkeyCompressed(x, y) {
  const prefix = new Uint8Array([(y % 2n === 0n) ? 0x02 : 0x03]);
  return concat(prefix, intToBytes32(x));
}
function pubkeyUncompressed(x, y) {
  return concat(new Uint8Array([0x04]), intToBytes32(x), intToBytes32(y));
}

const V0 = new Uint8Array([0x00]);
const V5 = new Uint8Array([0x05]);
const V30 = new Uint8Array([0x30]);

function btcLegacyUncompressed(x, y) { return base58check(V0, hash160(pubkeyUncompressed(x, y))); }
function btcLegacyCompressed(x, y)   { return base58check(V0, hash160(pubkeyCompressed(x, y))); }
function btcP2shSegwit(x, y) {
  const h = hash160(pubkeyCompressed(x, y));
  const redeem = concat(new Uint8Array([0x00, 0x14]), h);
  return base58check(V5, hash160(redeem));
}
function btcNativeSegwit(x, y) { return segwitEncode("bc", 0, Array.from(hash160(pubkeyCompressed(x, y)))); }
function bchLegacy(x, y) { return base58check(V0, hash160(pubkeyCompressed(x, y))); }
function ltcLegacy(x, y) { return base58check(V30, hash160(pubkeyCompressed(x, y))); }
function ethAddress(x, y) {
  const hashed = keccak256(concat(intToBytes32(x), intToBytes32(y)));
  return "0x" + toHex(hashed.slice(12));
}
function trxAddress(x, y) {
  const hashed = keccak256(concat(intToBytes32(x), intToBytes32(y)));
  const tron = concat(new Uint8Array([0x41]), hashed.slice(12));
  const checksum = doubleSha256(tron).slice(0, 4);
  return base58encode(concat(tron, checksum));
}
function intToWif(n, compressed) {
  const raw = intToBytes32(n);
  const payload = compressed
    ? concat(new Uint8Array([0x80]), raw, new Uint8Array([0x01]))
    : concat(new Uint8Array([0x80]), raw);
  return base58encode(concat(payload, doubleSha256(payload).slice(0, 4)));
}

/* ===========================================================================
 * SECTION 5: famous keys library
 * ======================================================================== */
const FAMOUS_KEYS = {
  "Private Key = 1 (the most famous weak key)": 1n,
  "Private Key = 2": 2n,
  "Private Key = 3": 3n,
  "Private Key = 4": 4n,
  "Private Key = 5": 5n,
  "Private Key = 7 (lucky 7)": 7n,
  "Private Key = 10": 10n,
  "Private Key = 13": 13n,
  "Private Key = 21 (Bitcoin max supply digit)": 21n,
  "Private Key = 42 (the answer)": 42n,
  "Private Key = 100": 100n,
  "Private Key = 1000": 1000n,
  "Private Key = 2^8 = 256": 2n**8n,
  "Private Key = 2^16 = 65,536": 2n**16n,
  "Private Key = 2^32": 2n**32n,
  "Private Key = 2^64": 2n**64n,
  "Private Key = 2^128 (halfway point)": 2n**128n,
  "Private Key = 2^224": 2n**224n,
  "Private Key = N - 1 (maximum valid key)": N - 1n,
  "Private Key = N - 2": N - 2n,
  "Private Key = N / 2 (true midpoint)": N / 2n,
  "Bitcoin Puzzle #1 (1 bit)": 1n,
  "Bitcoin Puzzle #2 (2 bit range, min)": 2n,
  "Bitcoin Puzzle #3 (3 bit range, min)": 4n,
  "Bitcoin Puzzle #4 (4 bit range, min)": 8n,
  "Bitcoin Puzzle #5 (5 bit range, min)": 16n,
  "Bitcoin Puzzle #10 (10 bit range, min)": 2n**9n,
  "Bitcoin Puzzle #20 (20 bit range, min)": 2n**19n,
  "Bitcoin Puzzle #32 (32 bit range, min)": 2n**31n,
};

/* ===========================================================================
 * SECTION 6: optional balance lookups
 * ======================================================================== */
async function queryBtcBalance(address) {
  try {
    const r = await fetch(`https://blockchain.info/rawaddr/${address}?limit=0&cors=true`);
    if (!r.ok) return `HTTP ${r.status}`;
    const d = await r.json();
    const bal = (d.final_balance || 0) / 1e8;
    return `${bal.toFixed(8)} BTC (${d.n_tx || 0} tx)`;
  } catch (e) { return "lookup failed"; }
}
async function queryEthBalance(address) {
  try {
    // public no-key endpoint (rate limited)
    const r = await fetch(`https://api.etherscan.io/api?module=account&action=balance&address=${address}&tag=latest`);
    const d = await r.json();
    if (d.status === "1") return `${(Number(d.result) / 1e18).toFixed(6)} ETH`;
    return `api: ${d.message || "error"}`;
  } catch (e) { return "lookup failed"; }
}

/* ===========================================================================
 * SECTION 7: UI wiring
 * ======================================================================== */
const $ = (id) => document.getElementById(id);
let currentKey = 1n;
let sessionLog = [];

const PK_FIELDS = [
  ["Decimal (integer)", "decimal", null],
  ["Hexadecimal (64 chars)", "hex", null],
  ["Bit length", "bits", null],
  ["WIF uncompressed (starts 5…)", "wif_u", null],
  ["WIF compressed (starts K/L…)", "wif_c", null],
];
const PUB_FIELDS = [
  ["X coordinate", "x"],
  ["Y coordinate", "y"],
  ["Compressed (33 bytes, 02/03 + x)", "compressed"],
  ["Uncompressed (65 bytes, 04 + x + y)", "uncompressed"],
];
const CHAINS = [
  ["BTC Legacy uncompressed (1…)", "btc_u"],
  ["BTC Legacy compressed (1…)", "btc_c"],
  ["BTC P2SH-SegWit (3…)", "btc_p2sh"],
  ["BTC Native SegWit (bc1…)", "btc_bech32"],
  ["Ethereum (0x…)", "eth"],
  ["Bitcoin Cash (1…)", "bch"],
  ["Litecoin (L…)", "ltc"],
  ["Tron (T…)", "trx"],
];

const pkVars = {}, pubVars = {}, addrVars = {}, balVars = {};

function makeField(labelText, hasBalance) {
  const wrap = document.createElement("div");
  wrap.className = "field";
  const fl = document.createElement("div");
  fl.className = "fl";
  const lab = document.createElement("label");
  lab.textContent = labelText;
  lab.style.margin = "0";
  fl.appendChild(lab);
  wrap.appendChild(fl);
  const ir = document.createElement("div");
  ir.className = "ir";
  const input = document.createElement("input");
  input.type = "text"; input.readOnly = true; input.spellcheck = false;
  const btn = document.createElement("button");
  btn.className = "copy"; btn.textContent = "Copy";
  btn.addEventListener("click", () => copyText(input.value));
  ir.appendChild(input); ir.appendChild(btn);
  wrap.appendChild(ir);
  let bal = null;
  if (hasBalance) {
    bal = document.createElement("div");
    bal.className = "addr-balance";
    wrap.appendChild(bal);
  }
  return { wrap, input, bal };
}

function buildFields() {
  for (const [label, key] of PK_FIELDS) {
    const f = makeField(label, false); pkVars[key] = f.input; $("pkFields").appendChild(f.wrap);
  }
  for (const [label, key] of PUB_FIELDS) {
    const f = makeField(label, false); pubVars[key] = f.input; $("pubFields").appendChild(f.wrap);
  }
  for (const [label, key] of CHAINS) {
    const f = makeField(label, true); addrVars[key] = f.input; balVars[key] = f.bal; $("addrFields").appendChild(f.wrap);
  }
  const sel = $("famous");
  for (const name of Object.keys(FAMOUS_KEYS)) {
    const o = document.createElement("option");
    o.value = name; o.textContent = name; sel.appendChild(o);
  }
}

function deriveAndDisplay(k) {
  if (!(k >= 1n && k < N)) { toast("Key must be in range [1, N−1]"); return; }
  currentKey = k;
  const hex = bigToHex64(k);
  pkVars.decimal.value = k.toString();
  pkVars.hex.value = hex;
  pkVars.bits.value = `${k.toString(2).length} bits (out of 256 max)`;
  pkVars.wif_u.value = intToWif(k, false);
  pkVars.wif_c.value = intToWif(k, true);

  const [x, y] = privkeyToPubkeyPoint(k);
  pubVars.x.value = bigToHex64(x);
  pubVars.y.value = bigToHex64(y);
  pubVars.compressed.value = toHex(pubkeyCompressed(x, y));
  pubVars.uncompressed.value = toHex(pubkeyUncompressed(x, y));

  addrVars.btc_u.value = btcLegacyUncompressed(x, y);
  addrVars.btc_c.value = btcLegacyCompressed(x, y);
  addrVars.btc_p2sh.value = btcP2shSegwit(x, y);
  addrVars.btc_bech32.value = btcNativeSegwit(x, y);
  addrVars.eth.value = ethAddress(x, y);
  addrVars.bch.value = bchLegacy(x, y);
  addrVars.ltc.value = ltcLegacy(x, y);
  addrVars.trx.value = trxAddress(x, y);

  for (const key of Object.keys(balVars)) if (balVars[key]) balVars[key].textContent = "";

  updateExplanation(k);
  if ($("live").checked) startBalanceLookups();
}

function updateExplanation(k) {
  const bits = k.toString(2).length;
  let sizeNote = "";
  if (bits < 20) sizeNote = "Very small key — a known weak-key pattern.";
  else if (bits < 50) sizeNote = "Medium-small key — still well within scanning range.";
  else if (bits < 128) sizeNote = "Medium key — starts becoming practically unreachable by brute force.";
  else sizeNote = "Large key — well within the secure range for real wallets.";
  const text =
`Step by step, with private key = ${k}:

1. Your secret number in 256-bit hex is:
   ${bigToHex64(k)}

2. It has ${bits} significant bits (of 256 max).
   ${sizeNote}

3. Public key = ${k} × G, where G is the secp256k1 generator point.
   The result is a point (x, y) on the curve — fast one way, infeasible to reverse.

4. Bitcoin addresses: serialize the public key, hash with SHA-256 then RIPEMD-160,
   add a version byte + checksum, and Base58-encode.

5. Ethereum: take the uncompressed public key (no 04 prefix), Keccak-256 it,
   and keep the last 20 bytes prefixed with 0x.

6. The SAME private key yields DIFFERENT addresses per chain — the differences are
   just different encoding rules over the same underlying public key.`;
  $("explain").textContent = text;
}

async function startBalanceLookups() {
  const btc = addrVars.btc_c.value, eth = addrVars.eth.value;
  balVars.btc_c.textContent = "looking up…";
  balVars.eth.textContent = "looking up…";
  queryBtcBalance(btc).then(r => {
    balVars.btc_c.textContent = r;
    appendNote(`[btc lookup] ${btc.slice(0,12)}… → ${r}`);
  });
  queryEthBalance(eth).then(r => {
    balVars.eth.textContent = r;
    appendNote(`[eth lookup] ${eth.slice(0,12)}… → ${r}`);
  });
}

/* notes */
function nowStr() {
  const d = new Date();
  return d.toTimeString().slice(0, 8);
}
function appendNote(note) {
  const line = note ? `${nowStr()} | ${note}` : "";
  sessionLog.push(line);
  const ta = $("notes");
  ta.value += line + "\n";
  ta.scrollTop = ta.scrollHeight;
}

/* clipboard */
function copyText(text) {
  if (!text) return;
  const done = () => { toast("Copied"); appendNote(`[copy] ${text.slice(0,50)}${text.length>50?"…":""}`); };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
  } else fallbackCopy(text, done);
}
function fallbackCopy(text, done) {
  const t = document.createElement("textarea");
  t.value = text; t.style.position = "fixed"; t.style.opacity = "0";
  document.body.appendChild(t); t.focus(); t.select();
  try { document.execCommand("copy"); done(); } catch (e) {}
  document.body.removeChild(t);
}

let toastTimer = null;
function toast(msg) {
  const el = $("toast");
  el.textContent = msg; el.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove("show"), 1400);
}

/* parse manual input */
function parseKey(raw) {
  raw = raw.trim();
  if (!raw) return null;
  try {
    if (raw.toLowerCase().startsWith("0x")) return BigInt(raw);
    return BigInt(raw);
  } catch (e) { return null; }
}

function init() {
  buildFields();

  $("famous").addEventListener("change", (e) => {
    const name = e.target.value;
    if (name && FAMOUS_KEYS[name] !== undefined) {
      const k = FAMOUS_KEYS[name];
      $("manual").value = k.toString();
      deriveAndDisplay(k);
      appendNote(`[library] Loaded '${name}' → key = ${k}`);
    }
  });

  $("deriveBtn").addEventListener("click", () => {
    const k = parseKey($("manual").value);
    if (k === null) { toast("Enter an integer or 0x-hex"); return; }
    deriveAndDisplay(k);
    appendNote(`[manual] Derived key = ${k}`);
  });
  $("manual").addEventListener("keydown", (e) => { if (e.key === "Enter") $("deriveBtn").click(); });

  document.querySelectorAll("[data-step]").forEach(b => b.addEventListener("click", () => {
    const nk = currentKey + BigInt(b.dataset.step);
    if (nk < 1n || nk >= N) { toast("Out of range"); return; }
    $("manual").value = nk.toString(); deriveAndDisplay(nk);
    appendNote(`[step] ${b.dataset.step} → key = ${nk}`);
  }));
  document.querySelectorAll("[data-mul]").forEach(b => b.addEventListener("click", () => {
    const m = b.dataset.mul;
    let nk;
    if (m === "0.5") nk = currentKey / 2n; else nk = currentKey * BigInt(m);
    if (nk < 1n || nk >= N) { toast("Out of range"); return; }
    $("manual").value = nk.toString(); deriveAndDisplay(nk);
    appendNote(`[step] ×${m} → key = ${nk}`);
  }));

  $("addNote").addEventListener("click", () => {
    const n = prompt("Your note:");
    if (n) appendNote(`[note] ${n}`);
  });
  $("saveNote").addEventListener("click", () => {
    const blob = new Blob(
      ["Matrix Studio Session Log\n" + "=".repeat(60) + "\nSaved: " + new Date().toISOString() + "\n\n" + sessionLog.join("\n") + "\n"],
      { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `matrix_studio_session_${new Date().toISOString().replace(/[:.]/g,"-")}.txt`;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    appendNote("[saved] Session log downloaded");
  });
  $("clearNote").addEventListener("click", () => {
    if (confirm("Clear the session log?")) {
      sessionLog = []; $("notes").value = ""; appendNote("Session log cleared.");
    }
  });

  appendNote("Matrix Studio opened. Session started " + new Date().toISOString().slice(0,19).replace("T"," "));
  appendNote("Pick a key from the library, enter one manually, or use the steppers.");
  appendNote("");

  deriveAndDisplay(1n);
}

document.addEventListener("DOMContentLoaded", init);
