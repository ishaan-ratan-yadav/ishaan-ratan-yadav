// 3D scenes for X post media. Each export receives ctx (THREE + helpers) and builds the scene.
// No imports here: everything comes through ctx. Return { bloom, bloomThreshold } to tune glow.

// ---------- shared: a bottle profile (lathe) ----------
function bottleProfile(THREE) {
  const p = [[0, 0], [.50, 0], [.56, .03], [.585, .12], [.585, 1.42], [.57, 1.56], [.48, 1.74], [.33, 1.92], [.245, 2.02], [.235, 2.10], [.24, 2.22], [0, 2.22]];
  // resample so long straight runs have enough rows for the warp to bend them
  const out = [];
  for (let i = 0; i < p.length - 1; i++) {
    const [x0, y0] = p[i], [x1, y1] = p[i + 1], n = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0) / .03));
    for (let k = 0; k < n; k++) out.push(new THREE.Vector2(x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n));
  }
  out.push(new THREE.Vector2(...p[p.length - 1]));
  return out;
}

function labelTexture(ctx, crisp, accent) {
  return ctx.canvasTex(1024, 512, (g, w, h) => {
    g.fillStyle = crisp ? '#F2EEE6' : '#F1ECFF'; g.fillRect(0, 0, w, h);
    if (!crisp) { g.filter = 'blur(7px)'; }
    g.fillStyle = crisp ? '#111' : '#3b2f8f';
    g.textAlign = 'center';
    g.font = '600 30px "JetBrains Mono"'; g.fillText(crisp ? 'NO. 01  ·  STILL WATER' : 'N0. 0?  ·  STLL WTAER', w / 2, 110);
    g.font = '800 130px "Inter Tight"'; g.fillText(crisp ? 'EVOLVE' : 'EV0LEV', w / 2, 270);
    g.fillStyle = crisp ? accent : '#8f7bff'; g.fillRect(w / 2 - 70, 318, 140, 8);
    g.fillStyle = crisp ? '#111' : '#3b2f8f';
    g.font = '500 34px "Inter Tight"'; g.fillText(crisp ? '500 ml  ·  mineral' : '5O0 rnl  ·  rnineral', w / 2, 395);
    if (!crisp) { g.filter = 'none'; g.globalAlpha = .35; for (let i = 0; i < 9; i++) { g.fillStyle = i % 2 ? '#ff4fd8' : '#4ff3ff'; g.fillRect(0, Math.random() * h, w, 4 + Math.random() * 10); } }
  });
}

function warp(ctx, geo, yOff = 0) {
  const pos = geo.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), y = pos.getY(i) + yOff, z = pos.getZ(i);
    if (Math.hypot(x, z) < 1e-4) continue;
    const k = 1 + .13 * ctx.noise3(x * 3.1, y * 2.4, z * 3.1) + .05 * Math.sin(y * 9.0);
    pos.setXYZ(i, x * k + .04 * Math.sin(y * 6), pos.getY(i), z * k);
  }
  geo.computeVertexNormals();
}

function makeBottle(ctx, { crisp, accent }) {
  const { THREE } = ctx;
  const grp = new THREE.Group();
  let geo = new THREE.LatheGeometry(bottleProfile(THREE), 160);
  if (!crisp) warp(ctx, geo);
  const body = new THREE.Mesh(geo, crisp
    ? new THREE.MeshPhysicalMaterial({ color: 0x0d0d12, metalness: .15, roughness: .32, clearcoat: 1, clearcoatRoughness: .08 })
    : new THREE.MeshPhysicalMaterial({ color: 0xb9a8ff, metalness: .55, roughness: .18, iridescence: 1, iridescenceIOR: 1.6, iridescenceThicknessRange: [200, 900], clearcoat: .6 }));
  body.castShadow = true; grp.add(body);
  const lgeo = new THREE.CylinderGeometry(.594, .594, .86, 128, crisp ? 1 : 24, true, -Math.PI / 2, Math.PI);
  if (!crisp) warp(ctx, lgeo, .78);
  const label = new THREE.Mesh(lgeo,
    new THREE.MeshPhysicalMaterial({ map: labelTexture(ctx, crisp, accent), roughness: crisp ? .55 : .3, metalness: 0, transparent: false, side: THREE.DoubleSide }));
  label.position.y = .78;
  grp.add(label);
  const cap = new THREE.Mesh(new THREE.CylinderGeometry(.255, .255, .34, 96),
    new THREE.MeshPhysicalMaterial({ color: crisp ? new THREE.Color(accent) : 0x9a8cff, metalness: crisp ? .9 : .4, roughness: crisp ? .22 : .35, clearcoat: 1 }));
  cap.position.y = 2.22 + .17; cap.castShadow = true; grp.add(cap);
  if (!crisp) {
    const wire = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: 0x8f7bff, wireframe: true, transparent: true, opacity: .14 }));
    wire.scale.setScalar(1.012); grp.add(wire);
    for (const [c, dx] of [[0xff3fd2, -.07], [0x3ff6ff, .07]]) {
      const ghost = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: .13, blending: THREE.AdditiveBlending, depthWrite: false }));
      ghost.position.x = dx; grp.add(ghost);
    }
  }
  return grp;
}

// ---------- scene: AI vs 3D ----------
export async function ai_vs_3d(ctx) {
  const { THREE, scene, camera, S } = ctx;
  scene.background = ctx.backdrop('#08080c', '#15131d', 'rgba(124,108,255,.28)', .5, .34);
  ctx.floor(0, .6);
  ctx.keyLight([2.5, 6, 4], 1.7);
  ctx.rim(S.accent, [-3.4, 2.4, -1.6], 30);
  ctx.rim(0xffa36b, [3.6, 2.6, -1.4], 22);
  const ai = makeBottle(ctx, { crisp: false, accent: S.accent }); ai.position.set(-1.05, 0, 0); ai.rotation.y = .35; scene.add(ai);
  const real = makeBottle(ctx, { crisp: true, accent: S.accent }); real.position.set(1.05, 0, 0); real.rotation.y = -.18; scene.add(real);
  camera.position.set(0, 1.9, 12.2); camera.lookAt(0, 1.0, 0);
  ctx.setTags([['AI · a vibe', 'lo'], ['3D · the product', 'hi']], ctx.W > ctx.H ? 70 : 57);
  return { bloom: .22, bloomThreshold: .92 };
}

// ---------- scene: logo from memory ----------
export async function logo_memory(ctx) {
  const { THREE, scene, camera, S } = ctx;
  scene.background = ctx.backdrop('#08080c', '#16141c', 'rgba(124,108,255,.22)', .62, .34);
  ctx.floor(-.02, .5);
  ctx.keyLight([3, 7, 5], 1.7);
  ctx.rim(S.accent, [2.5, 3, -2], 40);
  ctx.rim(0x6be4ff, [-3, 2.5, -1], 26);
  const r = ctx.rand(7);
  const chrome = new THREE.MeshPhysicalMaterial({ color: 0xd4d4de, metalness: 1, roughness: .16, clearcoat: 1 });
  const tangle = new THREE.Group();
  for (let k = 0; k < 7; k++) {
    const pts = []; for (let i = 0; i < 9; i++) pts.push(new THREE.Vector3((r() - .5) * 1.9, .25 + r() * 1.9, (r() - .5) * 1.4));
    const tube = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, false, 'catmullrom', .5), 220, .045 + r() * .03, 24), chrome);
    tube.castShadow = true; tangle.add(tube);
  }
  tangle.scale.setScalar(.72); tangle.position.set(-1.2, .05, -.2); scene.add(tangle);
  // the memorable mark: rounded square with a circle cut, extruded and bevelled
  const s = 1.05, rr = .32, shape = new THREE.Shape();
  shape.moveTo(-s + rr, -s); shape.lineTo(s - rr, -s); shape.quadraticCurveTo(s, -s, s, -s + rr);
  shape.lineTo(s, s - rr); shape.quadraticCurveTo(s, s, s - rr, s); shape.lineTo(-s + rr, s);
  shape.quadraticCurveTo(-s, s, -s, s - rr); shape.lineTo(-s, -s + rr); shape.quadraticCurveTo(-s, -s, -s + rr, -s);
  const hole = new THREE.Path(); hole.absarc(0, 0, .48, 0, Math.PI * 2, true); shape.holes.push(hole);
  const mark = new THREE.Mesh(new THREE.ExtrudeGeometry(shape, { depth: .42, bevelEnabled: true, bevelThickness: .09, bevelSize: .07, bevelSegments: 10, curveSegments: 96 }),
    new THREE.MeshPhysicalMaterial({ color: new THREE.Color(S.accent), metalness: .25, roughness: .2, clearcoat: 1, clearcoatRoughness: .05, sheen: .4 }));
  mark.geometry.center(); mark.scale.setScalar(.5); mark.position.set(1.25, .82, 0); mark.rotation.set(-.12, -.42, .05); mark.castShadow = true; scene.add(mark);
  camera.position.set(0, 1.7, 12.4); camera.lookAt(0, .85, 0);
  ctx.setTags([['decoration', 'lo'], ['a logo', 'hi']], ctx.W > ctx.H ? 70 : 55);
  return { bloom: .2, bloomThreshold: .93 };
}

// ---------- scene: unpaid invoice ----------
export async function invoice(ctx) {
  const { THREE, scene, camera, S } = ctx;
  scene.background = ctx.backdrop('#08080c', '#18141a', 'rgba(255,170,90,.18)', .5, .3);
  ctx.keyLight([-2.5, 6, 5], 1.5);
  ctx.rim(0xffb36b, [2.8, 2.5, -1.5], 30);
  ctx.rim(S.accent, [-3, 1.5, -1], 30);
  const tex = ctx.canvasTex(1024, 1400, (g, w, h) => {
    g.fillStyle = '#F4F1EA'; g.fillRect(0, 0, w, h);
    g.fillStyle = '#121212'; g.font = '800 92px "Inter Tight"'; g.fillText('INVOICE', 80, 170);
    g.font = '500 30px "JetBrains Mono"'; g.fillStyle = '#6b6b6b'; g.fillText('NO. 0047   ·   NET 30', 84, 225);
    g.fillStyle = '#121212'; g.fillRect(80, 270, w - 160, 3);
    const rows = [['3D product film · 15s', '1,800.00'], ['Social cutdowns · x4', '400.00'], ['Revisions (round 6)', '0.00'], ['"Quick small change"', '0.00']];
    g.font = '500 36px "Inter Tight"';
    rows.forEach(([a, b], i) => { const y = 360 + i * 92; g.fillStyle = '#222'; g.fillText(a, 84, y); g.textAlign = 'right'; g.fillText(b, w - 84, y); g.textAlign = 'left'; g.fillStyle = '#ddd8cc'; g.fillRect(84, y + 30, w - 168, 2); });
    g.fillStyle = '#121212'; g.font = '800 54px "Inter Tight"'; g.fillText('TOTAL', 84, 820); g.textAlign = 'right'; g.fillText('$2,200.00', w - 84, 820); g.textAlign = 'left';
    g.font = '500 28px "JetBrains Mono"'; g.fillStyle = '#7a7a7a'; g.fillText('SENT: DAY 1     SEEN: DAY 3', 84, 900); g.fillText('PAID: ...', 84, 945);
    g.save(); g.translate(w * .62, 1130); g.rotate(-.2);
    g.strokeStyle = '#E2463C'; g.lineWidth = 12; g.strokeRect(-250, -85, 500, 170);
    g.fillStyle = '#E2463C'; g.font = '800 104px "Inter Tight"'; g.textAlign = 'center'; g.fillText('UNPAID', 0, 38); g.restore();
    for (let i = 0; i < 2500; i++) { g.fillStyle = `rgba(0,0,0,${Math.random() * .035})`; g.fillRect(Math.random() * w, Math.random() * h, 2, 2); }
  });
  const geo = new THREE.PlaneGeometry(2.2, 3.0, 80, 110), pos = geo.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), y = pos.getY(i);
    const curl = Math.max(0, -y - .55); const side = Math.max(0, x - .6);
    pos.setZ(i, .12 * Math.sin(y * 1.4) + .55 * curl * curl + .35 * side * side * Math.max(0, -y + .2));
  }
  geo.computeVertexNormals();
  const paper = new THREE.Mesh(geo, new THREE.MeshPhysicalMaterial({ map: tex, color: 0xcfcac2, roughness: .85, side: THREE.DoubleSide }));
  paper.scale.setScalar(.82); paper.position.set(0, 1.5, 0); paper.rotation.set(-.3, .36, .1); paper.castShadow = true; scene.add(paper);
  const gold = new THREE.MeshPhysicalMaterial({ color: 0xf2c46b, metalness: 1, roughness: .2, clearcoat: .8 });
  const r = ctx.rand(11);
  [[-1.5, 2.15, .5], [1.4, 2.2, .6], [-1.2, .6, .9], [1.3, .45, 1.0], [.75, 2.55, -.6]].forEach(([x, y, z], i) => {
    const c = new THREE.Mesh(new THREE.CylinderGeometry(.27, .27, .045, 96), gold);
    c.position.set(x, y, z); c.rotation.set(r() * 3, r() * 3, r() * 3); c.castShadow = true; scene.add(c);
  });
  ctx.floor(-.9, .45);
  camera.position.set(0, 1.5, 11.6); camera.lookAt(0, 1.2, 0);
  return { bloom: .15, bloomThreshold: .96 };
}

// ---------- scene: generic statement (abstract hero, use for any post) ----------
export async function statement(ctx) {
  const { THREE, scene, camera, S } = ctx;
  scene.background = ctx.backdrop('#07070b', '#14121b', 'rgba(124,108,255,.26)', .55, .32);
  ctx.keyLight([3, 6, 5], 2.0);
  ctx.rim(S.accent, [-2.8, 2.4, -1.4], 36);
  ctx.rim(0xff9a62, [2.8, 1.2, -1], 30);
  const seed = S.seed || 3, r = ctx.rand(seed);
  const geo = new THREE.IcosahedronGeometry(1.15, 96), pos = geo.attributes.position, v = new THREE.Vector3();
  const f = 1.2 + r() * .8;
  for (let i = 0; i < pos.count; i++) { v.fromBufferAttribute(pos, i); const n = ctx.noise3(v.x * f + seed, v.y * f, v.z * f); v.multiplyScalar(1 + .22 * n); pos.setXYZ(i, v.x, v.y, v.z); }
  geo.computeVertexNormals();
  const blob = new THREE.Mesh(geo, new THREE.MeshPhysicalMaterial({ color: new THREE.Color(S.accent), metalness: .3, roughness: .1, clearcoat: 1, clearcoatRoughness: .04, iridescence: 1, iridescenceIOR: 1.5, iridescenceThicknessRange: [180, 820] }));
  blob.position.set(.25, 1.55, 0); blob.castShadow = true; scene.add(blob);
  const glass = new THREE.Mesh(new THREE.SphereGeometry(.52, 96, 96), new THREE.MeshPhysicalMaterial({ transmission: 1, thickness: .9, roughness: .02, ior: 1.45, color: 0xffffff }));
  glass.position.set(-1.5, 2.2, .6); scene.add(glass);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(.62, .07, 48, 160), new THREE.MeshPhysicalMaterial({ color: 0xe8e8f0, metalness: 1, roughness: .12 }));
  ring.position.set(1.55, .35, .7); ring.rotation.set(1.1, .3, .4); ring.castShadow = true; scene.add(ring);
  ctx.floor(-.25, .45);
  camera.position.set(0, 1.6, 13.2); camera.lookAt(0, 1.25, 0);
  return { bloom: .25, bloomThreshold: .9 };
}
