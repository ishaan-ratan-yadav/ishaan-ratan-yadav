// 3D scenes for Reddit image/gallery posts (FreshLeads). Each export receives ctx (THREE + helpers) and builds the scene.
// No imports here: everything comes through ctx. Return { bloom, bloomThreshold } to tune glow.
// Text that must be readable goes in the HTML layer (title/sub/tags) or in big canvas textures, never tiny 3D text.

// ---------- shared ----------
function textPlane(ctx, text, { w = 2, h = .5, font = '800 120px "Inter Tight"', color = '#F2F5F3', bg = null, align = 'center', px = 1024 } = {}) {
  const { THREE } = ctx;
  const ph = Math.round(px * h / w);
  const tex = ctx.canvasTex(px, ph, (g, cw, ch) => {
    if (bg) { g.fillStyle = bg; g.fillRect(0, 0, cw, ch); }
    g.fillStyle = color; g.font = font; g.textAlign = align; g.textBaseline = 'middle';
    g.fillText(text, align === 'center' ? cw / 2 : 24, ch / 2 + 4);
  });
  return new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, toneMapped: false }));
}

function envelope(ctx, { paper = 0xCFCBC0, flapShade = 0xBDB8AB, glow = null, seal = null } = {}) {
  const { THREE } = ctx;
  const g = new THREE.Group();
  const body = new THREE.Mesh(new ctx.RoundedBoxGeometry(1.6, 1.0, .06, 4, .025),
    new THREE.MeshPhysicalMaterial({ color: paper, roughness: .78, sheen: .3, emissive: glow ?? 0x000000, emissiveIntensity: glow ? .18 : 0 }));
  body.castShadow = true; body.receiveShadow = true; g.add(body);
  const flap = new THREE.Shape();
  flap.moveTo(-.79, .49); flap.lineTo(.79, .49); flap.lineTo(0, -.08); flap.lineTo(-.79, .49);
  const fm = new THREE.Mesh(new THREE.ExtrudeGeometry(flap, { depth: .012, bevelEnabled: false }),
    new THREE.MeshPhysicalMaterial({ color: flapShade, roughness: .7, emissive: glow ?? 0x000000, emissiveIntensity: glow ? .12 : 0 }));
  fm.position.z = .031; fm.castShadow = true; g.add(fm);
  if (seal) {
    const s = new THREE.Mesh(new THREE.CylinderGeometry(.13, .13, .04, 48),
      new THREE.MeshPhysicalMaterial({ color: new THREE.Color(seal), metalness: .3, roughness: .25, clearcoat: 1, emissive: new THREE.Color(seal), emissiveIntensity: .35 }));
    s.rotation.x = Math.PI / 2; s.position.set(0, -.06, .05); g.add(s);
  }
  return g;
}

// ---------- scene: info@ vs founder inbox ----------
export async function inbox(ctx) {
  const { THREE, scene, camera, S } = ctx;
  scene.background = ctx.backdrop('#070b09', '#121a16', 'rgba(46,204,113,.20)', .62, .34);
  ctx.floor(0, .55);
  ctx.keyLight([2.5, 6.5, 4.5], 1.8);
  ctx.rim(S.accent, [3.4, 2.6, -1.2], 34);
  ctx.rim(S.hot, [-3.6, 2.2, -1.4], 26);
  const r = ctx.rand(S.seed || 5);

  // the info@ tray: open bin + a pile that spills over
  const bin = new THREE.Group();
  const binMat = new THREE.MeshPhysicalMaterial({ color: 0x2a332e, roughness: .55, metalness: .2, clearcoat: .4 });
  const parts = [[2.0, .08, 1.3, 0, .04, 0], [2.0, .62, .07, 0, .35, .62], [2.0, .62, .07, 0, .35, -.62], [.07, .62, 1.3, .98, .35, 0], [.07, .62, 1.3, -.98, .35, 0]];
  for (const [w, h, d, x, y, z] of parts) {
    const m = new THREE.Mesh(new ctx.RoundedBoxGeometry(w, h, d, 3, .02), binMat); m.position.set(x, y, z); m.castShadow = m.receiveShadow = true; bin.add(m);
  }
  const lab = textPlane(ctx, 'info@', { w: 1.1, h: .34, font: '500 150px "JetBrains Mono"', color: '#93A39A' });
  lab.position.set(0, .36, .66); bin.add(lab);
  for (let i = 0; i < 46; i++) {
    const shade = 0x9C988E - Math.floor(r() * 4) * 0x070707;
    const env = envelope(ctx, { paper: shade, flapShade: shade - 0x0c0c0c });
    const layer = Math.floor(i / 6);
    const taper = 1 - layer * .09;
    env.scale.setScalar(.5);
    env.position.set((r() - .5) * 1.3 * taper, .3 + layer * .12 + r() * .05, (r() - .5) * .7 * taper);
    env.rotation.set(-Math.PI / 2 + (r() - .5) * .6, (r() - .5) * .5, (r() - .5) * 2.6);
    bin.add(env);
  }
  for (let i = 0; i < 6; i++) { // spill
    const env = envelope(ctx, { paper: 0x8E8A80, flapShade: 0x7F7B72 });
    env.scale.setScalar(.5);
    env.position.set(-1.0 + r() * 2.0, .05 + r() * .02, .95 + r() * .45);
    env.rotation.set(-Math.PI / 2, 0, (r() - .5) * 3); bin.add(env);
  }
  const badge = textPlane(ctx, '999+', { w: .9, h: .42, font: '800 200px "Inter Tight"', color: '#ffffff', bg: S.hot });
  badge.position.set(.7, 1.75, .2); badge.rotation.z = -.08; bin.add(badge);
  bin.position.set(-1.25, 0, 0); bin.rotation.y = .22; bin.scale.setScalar(.95); scene.add(bin);

  // the founder inbox: one envelope on a pedestal
  const ped = new THREE.Mesh(new THREE.CylinderGeometry(.55, .62, .5, 96), new THREE.MeshPhysicalMaterial({ color: 0x18201c, roughness: .3, metalness: .4, clearcoat: 1 }));
  ped.position.set(1.55, .25, .1); ped.castShadow = ped.receiveShadow = true; scene.add(ped);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(.6, .018, 16, 160), new THREE.MeshBasicMaterial({ color: new THREE.Color(S.accent), toneMapped: false }));
  ring.rotation.x = Math.PI / 2; ring.position.set(1.55, .51, .1); scene.add(ring);
  const hero = envelope(ctx, { paper: 0xDAD6CA, flapShade: 0xC8C3B6, glow: new THREE.Color(S.accent).multiplyScalar(.25).getHex(), seal: S.accent });
  hero.position.set(1.55, 1.08, .1); hero.rotation.set(-.08, -.32, .04); hero.scale.setScalar(.82); scene.add(hero);

  camera.position.set(0, 2.1, 13.4); camera.lookAt(0, .95, 0);
  if (ctx.WIDE) { camera.position.set(0, 2.2, 11.2); camera.lookAt(.1, .9, 0); }
  ctx.setTags(S.tags || [['info@ · support queue', 'hot'], ['founder · decides', 'hi']], ctx.WIDE ? 80 : 56);
  return { bloom: .18, bloomThreshold: .95 };
}

// ---------- scene: bar comparison (reply rates etc.) ----------
// --data "Industry:2.5:2-3%,Our outreach:8:8%"  (label:value[:display]); the last bar or one marked with ! is the hero
export async function bars(ctx) {
  const { THREE, scene, camera, S } = ctx;
  scene.background = ctx.backdrop('#070b09', '#111915', 'rgba(46,204,113,.22)', .6, .3);
  ctx.floor(0, .5);
  ctx.keyLight([-2.5, 7, 5], 1.7);
  ctx.rim(S.accent, [2.8, 3, -1.5], 40);
  ctx.rim(0x7fd8ff, [-3, 2, -1], 18);
  const data = (S.data && S.data.length ? S.data : [{ label: 'Industry', value: 2.5, display: '2-3%' }, { label: 'Ours', value: 8, display: '8%', hero: true }]);
  if (!data.some(d => d.hero)) data[data.length - 1].hero = true;
  const max = Math.max(...data.map(d => d.value)), n = data.length, gap = 1.35, x0 = -(n - 1) * gap / 2;
  const base = new THREE.Mesh(new ctx.RoundedBoxGeometry(n * gap + .6, .16, 1.5, 4, .05), new THREE.MeshPhysicalMaterial({ color: 0x18201c, roughness: .35, metalness: .3, clearcoat: 1 }));
  base.position.y = .08; base.receiveShadow = base.castShadow = true; scene.add(base);
  data.forEach((d, i) => {
    const h = Math.max(.12, 2.2 * d.value / max);
    const mat = d.hero
      ? new THREE.MeshPhysicalMaterial({ color: new THREE.Color(S.accent), roughness: .16, metalness: .1, clearcoat: 1, clearcoatRoughness: .05, emissive: new THREE.Color(S.accent), emissiveIntensity: .18 })
      : new THREE.MeshPhysicalMaterial({ color: 0x55605a, roughness: .5, metalness: .1, clearcoat: .3 });
    const bar = new THREE.Mesh(new ctx.RoundedBoxGeometry(.85, h, .85, 6, .08), mat);
    bar.position.set(x0 + i * gap, .16 + h / 2, 0); bar.castShadow = true; scene.add(bar);
    const val = textPlane(ctx, d.display || String(d.value), { w: 1.3, h: .5, font: '800 230px "Inter Tight"', color: d.hero ? '#ffffff' : '#C7D2CC' });
    val.position.set(x0 + i * gap, .16 + h + .38, .1); scene.add(val);
    const lab = textPlane(ctx, d.label.toUpperCase(), { w: 1.3, h: .2, font: '500 70px "JetBrains Mono"', color: d.hero ? S.accent : '#93A39A' });
    lab.position.set(x0 + i * gap, .08, .78); lab.rotation.x = -.35; scene.add(lab);
  });
  camera.position.set(0, 2.0, 13.0); camera.lookAt(0, 1.3, 0);
  if (ctx.WIDE) { camera.position.set(0, 2.0, 11.6); camera.lookAt(0, 1.2, 0); }
  if (S.tags) ctx.setTags(S.tags, ctx.WIDE ? 84 : 62);
  return { bloom: .3, bloomThreshold: .86 };
}

// ---------- scene: a lead sold to 5 buyers, then retired ----------
export async function five_buyers(ctx) {
  const { THREE, scene, camera, S } = ctx;
  scene.background = ctx.backdrop('#070b09', '#131a16', 'rgba(46,204,113,.18)', .5, .3);
  ctx.floor(0, .5);
  ctx.keyLight([2, 7, 5], 1.8);
  ctx.rim(S.accent, [-3, 2.4, -1.2], 34);
  ctx.rim(S.hot, [3.2, 2.6, -1], 24);
  const tex = ctx.canvasTex(1400, 840, (g, w, h) => {
    g.fillStyle = '#B9B5AB'; g.fillRect(0, 0, w, h);
    g.fillStyle = '#0f1512'; g.font = '800 92px "Inter Tight"'; g.fillText('LEAD', 80, 150);
    g.font = '500 34px "JetBrains Mono"'; g.fillStyle = '#6b746f'; g.fillText('D2C BRAND  ·  FOUNDER', 330, 145);
    g.fillStyle = '#0f1512'; g.fillRect(80, 190, w - 160, 4);
    const rows = [['inbox', 'founder, SMTP-verified'], ['why now', 'dated trigger: launch / raise / retail'], ['copy', 'cold email + DM'], ['buyers', '5 of 5']];
    g.font = '500 44px "Inter Tight"';
    rows.forEach(([a, b], i) => { const y = 290 + i * 105; g.fillStyle = '#4a534e'; g.fillText(a.toUpperCase(), 84, y); g.fillStyle = '#0f1512'; g.fillText(b, 420, y); g.fillStyle = '#9a968c'; g.fillRect(84, y + 32, w - 168, 2); });
    g.save(); g.translate(w * .7, h * .86); g.rotate(-.12);
    g.strokeStyle = S.hot; g.lineWidth = 14; g.strokeRect(-250, -62, 500, 124);
    g.fillStyle = S.hot; g.font = '800 92px "Inter Tight"'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('RETIRED', 0, 6); g.restore();
  });
  const card = new THREE.Mesh(new ctx.RoundedBoxGeometry(2.8, 1.68, .06, 4, .04), [
    new THREE.MeshPhysicalMaterial({ color: 0xCFCBC2, roughness: .8 }), new THREE.MeshPhysicalMaterial({ color: 0xCFCBC2, roughness: .8 }),
    new THREE.MeshPhysicalMaterial({ color: 0xCFCBC2, roughness: .8 }), new THREE.MeshPhysicalMaterial({ color: 0xCFCBC2, roughness: .8 }),
    new THREE.MeshPhysicalMaterial({ map: tex, roughness: .7 }), new THREE.MeshPhysicalMaterial({ color: 0xCFCBC2, roughness: .8 })]);
  card.position.set(0, 1.75, -.2); card.scale.setScalar(.88); card.rotation.set(-.16, .0, .03); card.castShadow = true; scene.add(card);
  // five buyer tokens in an arc, all filled
  const tokMat = new THREE.MeshPhysicalMaterial({ color: new THREE.Color(S.accent), roughness: .14, clearcoat: 1, metalness: .15, emissive: new THREE.Color(S.accent), emissiveIntensity: .12 });
  for (let i = 0; i < 5; i++) {
    const a = (-2 + i) * .38;
    const tok = new THREE.Group();
    const head = new THREE.Mesh(new THREE.SphereGeometry(.17, 48, 48), tokMat); head.position.y = .52; tok.add(head);
    const body = new THREE.Mesh(new THREE.CapsuleGeometry(.2, .22, 8, 32), tokMat); body.position.y = .2; tok.add(body);
    tok.children.forEach(c => c.castShadow = true);
    tok.position.set(Math.sin(a) * 2.0, 0, Math.cos(a) * 1.2 - .1); scene.add(tok);
  }
  // the sixth seat: empty and dim, nobody else gets it
  const six = new THREE.Mesh(new THREE.TorusGeometry(.2, .03, 16, 64), new THREE.MeshBasicMaterial({ color: 0x3a4540 }));
  six.rotation.x = Math.PI / 2; six.position.set(Math.sin(1.25) * 2.0, .02, Math.cos(1.25) * 1.2 - .1); scene.add(six);
  camera.position.set(0, 2.2, 12.6); camera.lookAt(0, 1.2, 0);
  if (ctx.WIDE) { camera.position.set(0, 2.2, 10.8); camera.lookAt(0, 1.2, 0); }
  ctx.setTags(S.tags || [['5 buyers max', 'hi'], ['then retired', 'hot']], ctx.WIDE ? 88 : 64);
  return { bloom: .18, bloomThreshold: .96 };
}

// ---------- scene: generic statement (abstract hero, any post) ----------
export async function statement(ctx) {
  const { THREE, scene, camera, S } = ctx;
  scene.background = ctx.backdrop('#060a08', '#111813', 'rgba(46,204,113,.22)', .55, .32);
  ctx.keyLight([3, 6, 5], 2.0);
  ctx.rim(S.accent, [-2.8, 2.4, -1.4], 36);
  ctx.rim(S.hot, [2.8, 1.2, -1], 26);
  const seed = S.seed || 3, r = ctx.rand(seed);
  const geo = new THREE.IcosahedronGeometry(1.15, 96), pos = geo.attributes.position, v = new THREE.Vector3();
  const f = 1.2 + r() * .8;
  for (let i = 0; i < pos.count; i++) { v.fromBufferAttribute(pos, i); const n = ctx.noise3(v.x * f + seed, v.y * f, v.z * f); v.multiplyScalar(1 + .22 * n); pos.setXYZ(i, v.x, v.y, v.z); }
  geo.computeVertexNormals();
  const blob = new THREE.Mesh(geo, new THREE.MeshPhysicalMaterial({ color: new THREE.Color(S.accent), metalness: .3, roughness: .1, clearcoat: 1, clearcoatRoughness: .04, iridescence: 1, iridescenceIOR: 1.5, iridescenceThicknessRange: [180, 820] }));
  blob.position.set(.25, 1.55, 0); blob.castShadow = true; scene.add(blob);
  const glass = new THREE.Mesh(new THREE.SphereGeometry(.52, 96, 96), new THREE.MeshPhysicalMaterial({ transmission: 1, thickness: .9, roughness: .02, ior: 1.45, color: 0xffffff }));
  glass.position.set(-1.5, 2.2, .6); scene.add(glass);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(.62, .07, 48, 160), new THREE.MeshPhysicalMaterial({ color: 0xe8ece9, metalness: 1, roughness: .12 }));
  ring.position.set(1.55, .35, .7); ring.rotation.set(1.1, .3, .4); ring.castShadow = true; scene.add(ring);
  ctx.floor(-.25, .45);
  camera.position.set(0, 1.6, 13.2); camera.lookAt(0, 1.25, 0);
  if (ctx.WIDE) { camera.position.set(0, 1.6, 10.8); camera.lookAt(0, 1.3, 0); }
  if (S.tags) ctx.setTags(S.tags, ctx.WIDE ? 80 : 57);
  return { bloom: .25, bloomThreshold: .9 };
}
