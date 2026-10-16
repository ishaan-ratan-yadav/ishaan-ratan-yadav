// Grey clay BLOCKOUT previz for a 6-shot product film (label macro, base, drop on petal,
// falling botanicals with a speed ramp, spinning hero close-up, calm ending). Pure seek(T):
// edit the shot windows / camera paths, render with blockout_capture.cjs, encode with ffmpeg.
// Use the MP4 as @video1 ("camera, timing and blocking only"). Every clay shape is a placeholder.
import * as THREE from 'three';
const W = 960, H = 540;
const r = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
r.setSize(W, H); r.setPixelRatio(1); document.body.appendChild(r.domElement);
r.toneMapping = THREE.ACESFilmicToneMapping; r.outputColorSpace = THREE.SRGBColorSpace;
const scene = new THREE.Scene(); scene.background = new THREE.Color(0xb9b4ae);
const cam = new THREE.PerspectiveCamera(30, W / H, 0.01, 100);
scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8580, 1.6));
const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(-3, 4, 3); scene.add(key);
const clay = (c) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.85, metalness: 0 });
// --- bottle (clay): lathe body + label band + art panel + cap
function makeBottle() {
  const g = new THREE.Group(), spin = new THREE.Group(); g.add(spin);
  const pts = [[0, 0], [0.47, 0], [0.5, 0.04], [0.5, 1.15], [0.47, 1.3], [0.36, 1.42], [0.2, 1.5], [0.17, 1.56], [0.17, 1.8], [0, 1.8]].map(p => new THREE.Vector2(p[0], p[1]));
  spin.add(new THREE.Mesh(new THREE.LatheGeometry(pts, 64), clay(0x9a8f86)));
  const label = new THREE.Mesh(new THREE.CylinderGeometry(0.507, 0.507, 0.78, 64, 1, true, -1.1, 2.2), clay(0xe6e1d8)); label.position.y = 0.58; spin.add(label);
  const panel = new THREE.Mesh(new THREE.CylinderGeometry(0.51, 0.51, 0.5, 64, 1, true, -0.55, 1.1), clay(0x6f625a)); panel.position.y = 0.6; spin.add(panel);
  const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.26, 48), clay(0xcfc6b6)); cap.position.y = 1.9; spin.add(cap);
  const base = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.06, 16, 64), clay(0xa79c92)); base.rotation.x = Math.PI / 2; base.position.y = 0.04; spin.add(base);
  g.userData.spin = spin; return g;
}
const bottle = makeBottle(); scene.add(bottle);
// --- petal (curved plane) and drop
const petalGeo = new THREE.PlaneGeometry(3, 2, 60, 40);
{ const p = petalGeo.attributes.position; for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i); p.setZ(i, -0.25 * x * x - 0.12 * y * y); } petalGeo.computeVertexNormals(); }
const petal = new THREE.Mesh(petalGeo, clay(0xc9b3ab)); petal.material.side = THREE.DoubleSide; scene.add(petal);
const drop = new THREE.Mesh(new THREE.SphereGeometry(0.045, 32, 16), clay(0xa08d7d)); drop.scale.y = 0.7; scene.add(drop);
// --- falling botanicals (clay shapes, seeded)
let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
const bits = new THREE.Group(); scene.add(bits);
const shapes = [
  () => { const m = new THREE.Mesh(new THREE.CircleGeometry(0.11, 20), clay(0xc4aaa0)); m.scale.set(1, 1.4, 1); m.material.side = THREE.DoubleSide; return m; }, // petal
  () => new THREE.Mesh(new THREE.TorusGeometry(0.09, 0.025, 8, 24, 4.2), clay(0xd09a6a)),       // peel curl
  () => { const m = new THREE.Mesh(new THREE.PlaneGeometry(0.06, 0.26), clay(0xa7aea0)); m.material.side = THREE.DoubleSide; return m; }, // leaf
  () => new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.02, 12), clay(0xd8c48c)),       // chamomile
  () => { const m = new THREE.Mesh(new THREE.OctahedronGeometry(0.07), clay(0x6e5a4c)); m.scale.set(1, 1, 0.3); return m; }, // star anise
  () => new THREE.Mesh(new THREE.SphereGeometry(0.035, 12, 8), clay(0x4f4c55)),                 // juniper
];
const P = [];
for (let i = 0; i < 260; i++) {
  const m = shapes[Math.floor(rnd() * shapes.length)](); bits.add(m);
  m.scale.multiplyScalar(1.45); P.push({ m, x: (rnd() - 0.5) * 7, z: (rnd() - 0.5) * 4, y0: 3.2 + rnd() * 2.2, rx: rnd() * 6, ry: rnd() * 6, wx: (rnd() - 0.5) * 3, wy: (rnd() - 0.5) * 3, sway: rnd() * 6 });
}
// --- glass + table for the ending
const glassPts = [[0, 0], [0.42, 0], [0.45, 0.02], [0.45, 1.0], [0.42, 1.0], [0.42, 0.12], [0, 0.12]].map(p => new THREE.Vector2(p[0], p[1]));
const glass = new THREE.Mesh(new THREE.LatheGeometry(glassPts, 64), new THREE.MeshStandardMaterial({ color: 0xd8d2ca, roughness: 0.3, transparent: true, opacity: 0.55 })); scene.add(glass);
const liquid = new THREE.Mesh(new THREE.CylinderGeometry(0.41, 0.41, 0.7, 48), clay(0xb08870)); scene.add(liquid);
const table = new THREE.Mesh(new THREE.PlaneGeometry(20, 12), clay(0x7c6a5c)); table.rotation.x = -Math.PI / 2; scene.add(table);
const bub = []; for (let i = 0; i < 40; i++) { const b = new THREE.Mesh(new THREE.SphereGeometry(0.012 + rnd() * 0.015, 8, 6), clay(0xeee8e0)); scene.add(b); bub.push({ b, a: rnd() * 6.28, rr: rnd() * 0.35, ph: rnd(), sp: 0.15 + rnd() * 0.25 }); }
const ease = (x) => x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x);
const look = (p, t, fov) => { cam.position.set(...p); cam.lookAt(...t); cam.fov = fov; cam.updateProjectionMatrix(); };
function vis(o) { for (const k in o) o[k].visible = true; }
function seek(T) {
  for (const o of [bottle, petal, drop, bits, glass, liquid, table]) o.visible = false; bub.forEach(b => b.b.visible = false);
  const spin = bottle.userData.spin; bottle.position.set(0, 0, 0); bottle.rotation.set(0, 0, 0);
  if (T < 2.5) {               // S1 label macro, slow rotation
    const t = T; bottle.visible = true; bottle.rotation.z = -0.95; spin.rotation.y = -0.45 + t * 0.3;
    look([0.5 + 0.12 * t / 2.5, 0.62, 1.55], [0.42, 0.42, 0], 30);
  } else if (T < 4.5) {        // S2 base from below, rotating
    const t = T - 2.5; bottle.visible = true; bottle.rotation.set(-1.0, 0, -0.7); spin.rotation.y = t * 0.35;
    look([-0.75 - 0.08 * t, -1.1, 1.45], [0.05, 0.2, 0], 34);
  } else if (T < 7.0) {        // S3 drop on petal, slides, falls, camera tips down
    const t = T - 4.5; petal.visible = drop.visible = true; petal.rotation.set(-1.15, 0, 0.55); petal.position.set(0, 0, 0);
    const s = Math.min(t / 2.0, 1);                            // slide along petal toward edge
    const local = new THREE.Vector3(-0.35 + 1.25 * ease(s), 0.15 - 0.55 * ease(s), 0); local.z = -0.25 * local.x * local.x - 0.12 * local.y * local.y + 0.035;
    petal.updateMatrixWorld(); const wp = local.applyMatrix4(petal.matrixWorld);
    if (t > 2.0) { const f = t - 2.0; wp.y -= 4.9 * f * f; }
    drop.position.copy(wp);
    const tilt = ease((t - 2.05) / 0.45);                         // fast tilt down after the drop
    const tgt = new THREE.Vector3(wp.x * 0.6 + 0.1, 0.0 - tilt * 1.6 + wp.y * 0.3, wp.z * 0.6);
    look([tgt.x - 0.2, 0.9 - tilt * 1.3, tgt.z + 1.6], [tgt.x, tgt.y, tgt.z], 30);
  } else if (T < 9.5) {        // S4 botanicals fall: fast then slow-mo ramp, bottle spinning inside
    const t = T - 7.0; bits.visible = true; bottle.visible = true;
    const tau = t < 0.45 ? t * 2.2 : 0.99 + (t - 0.45) * 0.35;       // speed ramp
    P.forEach(p => { p.m.position.set(p.x + 0.15 * Math.sin(p.sway + tau), p.y0 - tau * 2.6, p.z); p.m.rotation.set(p.rx + p.wx * tau, p.ry + p.wy * tau, 0); });
    bottle.position.set(0.1, 1.5 - tau * 0.75, 0); bottle.scale.setScalar(1.15); bottle.rotation.z = -0.45; spin.rotation.y = -2.0 + tau * 0.9;
    const push = ease(t / 2.5);
    look([0, 1.9 - 0.25 * t, 7.5 - 1.8 * push], [0, 1.3 - 0.3 * t, 0], 30);
  } else if (T < 12.0) {       // S5 close-up, same spin direction, push in eases to stop
    const t = T - 9.5; bottle.visible = true; bits.visible = true; bottle.scale.setScalar(1); bottle.rotation.z = -0.45;
    spin.rotation.y = -0.46 + 0.46 * (1 - Math.pow(1 - Math.min(t / 2.5, 1), 2));
    P.forEach((p, i) => { const k = i % 25 === 0; p.m.visible = k; p.m.position.set(p.x * 0.18 + 0.1, 1.9 - ((t * 0.35 + p.y0 * 0.7) % 1.9), p.z * 0.2 + (i % 2 ? 1.3 : -0.6)); p.m.rotation.set(p.rx + t * 0.6, p.ry, 0); });
    const push = 1 - Math.pow(1 - Math.min(t / 2.5, 1), 3);
    look([0.15, 1.0, 3.4 - 0.9 * push], [0.05, 0.85, 0], 30);
  } else {                     // S6 calm ending: glass right, bottle back-left, fizz, slow push
    const t = T - 12.0; table.visible = glass.visible = liquid.visible = bottle.visible = true; bottle.scale.setScalar(1);
    bottle.position.set(-1.6, 0, -1.8); spin.rotation.y = 0.2; glass.position.set(0.6, 0, 0); liquid.position.set(0.6, 0.47, 0);
    bub.forEach(o => { o.b.visible = true; const y = 0.15 + ((o.ph + t * o.sp) % 1) * 0.65; o.b.position.set(0.6 + Math.cos(o.a) * o.rr, y, Math.sin(o.a) * o.rr); });
    const push = ease(t / 3);
    look([0.1, 0.75, 4.2 - 0.35 * push], [0.0, 0.55, -0.4], 30);
  }
  P.forEach(p => { if (T >= 7.0 && T < 9.5) p.m.visible = true; });
  r.render(scene, cam);
}
window.__seek = seek; seek(0); window.__ready = true;
