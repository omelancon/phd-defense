// Runtime for the `hasse-anim` local component: the drawing is static, each position sets the
// state of its nodes and edges (data-st) and the caption.
Lattice.component("hasse-anim", {
  mount(el, data) {
    const root = el.querySelector(".hasse-anim");
    const groups = { n: {}, e: {} };
    for (const g of root.querySelectorAll(".hs-node")) groups.n[g.dataset.k] = g;
    for (const g of root.querySelectorAll(".hs-edge")) groups.e[g.dataset.k] = g;
    return { root, groups, states: data.states, caption: root.querySelector(".hs-caption") };
  },
  show(inst, position, info) {
    const s = inst.states[Math.min(position, inst.states.length - 1)] || { n: {}, e: {}, caption: "" };
    inst.root.classList.toggle("hs-animate", !!(info && info.animate));
    for (const kind of ["n", "e"]) {
      for (const [k, g] of Object.entries(inst.groups[kind])) {
        const st = s[kind][k];
        if (st) g.setAttribute("data-st", st);
        else g.removeAttribute("data-st");
      }
    }
    inst.caption.textContent = s.caption || "";
  },
});
