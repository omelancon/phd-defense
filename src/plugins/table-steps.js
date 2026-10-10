// Runtime for the `table-steps` local component: each position hides some columns of the table and
// highlights the best number of each row. A single step animates: the cells that stay glide from
// their old place (FLIP), the cells that appear fade in, the highlight fades to its new cell.
Lattice.component("table-steps", {
  mount(el, data) {
    const root = el.querySelector(".lt-table-steps");
    const cells = [...root.querySelectorAll("th, td")];
    const byKey = {};
    for (const td of root.querySelectorAll("td")) byKey[td.parentNode.dataset.r + "," + td.dataset.c] = td;
    return { root, cells, byKey, positions: data.positions, timer: 0 };
  },
  show(inst, position, info) {
    const p = inst.positions[Math.min(position, inst.positions.length - 1)];
    const off = new Set(p.hidden.map(String));
    const best = new Set(p.best.map(([r, c]) => r + "," + c));
    const animate = !!(info && info.animate);
    clearTimeout(inst.timer);
    for (const c of inst.cells) { c.style.transition = ""; c.style.transform = ""; c.classList.remove("ts-in"); }
    const scale = inst.root.getBoundingClientRect().width / (inst.root.offsetWidth || 1) || 1;
    const before = new Map();
    if (animate) for (const c of inst.cells) if (!c.classList.contains("ts-off")) before.set(c, c.getBoundingClientRect().left);
    inst.root.classList.toggle("ts-animate", animate);
    for (const c of inst.cells) c.classList.toggle("ts-off", off.has(c.dataset.c));
    for (const [k, td] of Object.entries(inst.byKey)) td.classList.toggle("ts-best", best.has(k));
    if (!animate) return;
    const moved = [];
    for (const c of inst.cells) {
      if (c.classList.contains("ts-off")) continue;
      if (!before.has(c)) { c.classList.add("ts-in"); continue; }
      const dx = (before.get(c) - c.getBoundingClientRect().left) / scale;
      if (Math.abs(dx) > 0.5) { c.style.transform = `translateX(${dx}px)`; moved.push(c); }
    }
    void inst.root.offsetWidth;
    for (const c of moved) { c.style.transition = "transform .5s cubic-bezier(.3,.7,.2,1)"; c.style.transform = ""; }
    inst.timer = setTimeout(() => {
      for (const c of inst.cells) { c.style.transition = ""; c.classList.remove("ts-in"); }
    }, 1100);
  },
  leave(inst) {
    clearTimeout(inst.timer);
  },
});
