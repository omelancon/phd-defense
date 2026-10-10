// Runtime for the `takeaway` local component: position 0 shows the key on a pending rule,
// position 1 fills the node, draws the rule in the accent colour and shows the figure and caption.
Lattice.component("takeaway", {
  mount(el) {
    return { root: el.querySelector(".lt-takeaway") };
  },
  show(inst, position, info) {
    inst.root.classList.toggle("tk-animate", !!(info && info.animate));
    inst.root.classList.toggle("tk-done", position >= 1);
  },
});
