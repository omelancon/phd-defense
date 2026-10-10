// Runtime for the `related-work-note` local component with `flash: true`: the note is shown at
// position 1 only, laid over the blocks that follow it (see related-work-note.css).
Lattice.component("related-work-note", {
  mount(el) {
    return { el, slot: el.querySelector(".lt-related-work-slot") };
  },
  show(inst, position, info) {
    const on = position === 1;
    if (inst.slot.classList.contains("rw-on") === on) return;
    inst.slot.classList.toggle("rw-animate", !!(info && info.animate));
    inst.slot.classList.toggle("rw-on", on);
    inst.el.dispatchEvent(new CustomEvent("lt-relayout", { bubbles: true, detail: { animate: false } }));
  },
});
