"""Local plugins for the defense deck. Lattice imports this file automatically (spec 8.1)."""
from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from lattice import Component, ComponentError, Part, RenderResult, register

HERE = Path(__file__).parent / "plugins"

NODE_STATES = {"operand", "union", "result", "past", "dim", "hidden"}
EDGE_STATES = {"union", "widen", "past", "dim", "hidden"}

_GROUP = re.compile(r'<g id="(?:node|edge)\d+" class="(node|edge)([^"]*)">\s*<title>(.*?)</title>', re.S)


class HasseAnimOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    file: str | None = None      # a .dot file, relative to the deck file
    dot: str | None = None       # or the DOT source inline
    steps: list[dict | None] = [None]
    height: int = 430


@register("hasse-anim")
class HasseAnim(Component):
    """A Graphviz diagram (a Hasse diagram of a lattice, say) whose nodes and edges change state per step.

    The drawing is laid out once by Graphviz and never moves. ``steps`` lists one entry per position:
    ``null`` (no change) or a mapping with ``nodes`` and ``edges`` (``"u->v"`` as written in the DOT,
    tail first) mapping names to a state, ``null`` to go back to the default, and an optional
    ``caption`` shown under the drawing at that position only. Entries are deltas over the previous
    position. An element whose DOT ``class`` contains ``hidden`` starts hidden.

    Arrows name its nodes and edges as parts: ``COMP.NODE`` or ``COMP.U->V`` (spec 8.9).
    """

    Options = HasseAnimOptions
    version = "2"
    body = "yaml"
    runtime = str(HERE / "hasse-anim.js")
    css = [str(HERE / "hasse-anim.css")]

    def render(self, block, opts: HasseAnimOptions, ctx) -> RenderResult:
        if (opts.file is None) == (opts.dot is None):
            raise ComponentError("give the diagram as 'file' (a .dot file) or 'dot' (its source), not both")
        source = ctx.path(opts.file).read_text(encoding="utf-8") if opts.file else opts.dot
        proc = subprocess.run(["dot", "-Tsvg"], input=source, capture_output=True, text=True, timeout=60)
        if proc.returncode != 0:
            raise ComponentError(f"graphviz failed: {proc.stderr.strip()}")
        svg = proc.stdout[proc.stdout.find("<svg"):]

        names = {"node": set(), "edge": set()}
        defaults = {"node": {}, "edge": {}}

        def tag(m: re.Match) -> str:
            kind, classes, title = m.group(1), m.group(2).split(), html.unescape(m.group(3))
            if kind == "edge":  # "u:port->v:port" is named "u->v"
                title = "->".join(end.split(":")[0] for end in re.split(r"->|--", title))
            names[kind].add(title)
            if "hidden" in classes:
                defaults[kind][title] = "hidden"
            return f'<g class="hs-{kind}" data-k="{html.escape(title, quote=True)}">'

        svg = _GROUP.sub(tag, svg)
        svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
        svg = re.sub(r"<title>.*?</title>", "", svg, flags=re.S)
        svg = re.sub(r'\swidth="[^"]*"', "", svg, count=1)
        svg = re.sub(r'\sheight="[^"]*"', "", svg, count=1)
        svg = re.sub(r'(<g id="graph0"[^>]*>\s*<polygon )fill="white"', r'\1fill="none"', svg, count=1)
        svg = re.sub(r'\sid="graph0"', "", svg, count=1)
        svg = svg.replace('stroke="black"', 'stroke="currentColor"').replace('fill="black"', 'fill="currentColor"')
        svg = svg.replace("<svg ", '<svg preserveAspectRatio="xMidYMid meet" ', 1)

        states = []
        cur = {"n": dict(defaults["node"]), "e": dict(defaults["edge"])}
        for i, step in enumerate(opts.steps):
            step = step or {}
            unknown = set(step) - {"nodes", "edges", "caption"}
            if unknown:
                raise ComponentError(f"steps[{i}]: unknown key(s) {sorted(unknown)}; use nodes, edges, caption")
            for key, kind, allowed in (("nodes", "node", NODE_STATES), ("edges", "edge", EDGE_STATES)):
                short = kind[0]
                for name, st in (step.get(key) or {}).items():
                    name = str(name)
                    if name not in names[kind]:
                        raise ComponentError(f"steps[{i}]: no {kind} {name!r}; the diagram has "
                                             f"{', '.join(sorted(names[kind]))}")
                    if st is None:
                        cur[short].pop(name, None)
                        if name in defaults[kind]:
                            cur[short][name] = defaults[kind][name]
                    elif st not in allowed:
                        raise ComponentError(f"steps[{i}]: unknown {kind} state {st!r}; use {', '.join(sorted(allowed))}")
                    else:
                        cur[short][name] = st
            states.append({"n": dict(cur["n"]), "e": dict(cur["e"]), "caption": str(step.get("caption") or "")})

        markup = (f'<div class="hasse-anim"><div class="hs-canvas" style="height:{opts.height}px">{svg}</div>'
                  f'<div class="hs-caption"></div></div>')
        return RenderResult(markup, data={"states": states, "nodes": sorted(names["node"]),
                                                "edges": sorted(names["edge"])}, positions=len(states))

    def part(self, result: RenderResult, name: str) -> Part:
        """A node (``mf1``) or an edge (``i02->mf1``), not drawn while its state is ``hidden``."""
        data = result.data or {}
        name = name.strip()
        if "->" in name:
            name = "->".join(end.strip() for end in name.split("->"))
            kind, short = "edge", "e"
        else:
            kind, short = "node", "n"
        known = data.get(f"{kind}s", [])
        if name not in known:
            raise ComponentError(f"no {kind} {name!r} in the diagram; it has {', '.join(known)}")
        drawn = [st[short].get(name) != "hidden" for st in data["states"]]
        key = name.replace("\\", "\\\\").replace('"', '\\"')
        return Part(f'.hs-{kind}[data-k="{key}"]:not([data-st=hidden])', None if all(drawn) else drawn)


class StatementOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")


_KEY = re.compile(r"\*\*(.+?)\*\*", re.S)


@register("statement")
class Statement(Component):
    """A key sentence set large on its own slide (the object of the thesis, say).

    The body is the sentence as plain text; ``**words**`` are its key phrases, set in the accent
    colour. Styled by plugins/statement.css with the theme's variables, so it follows the theme.
    """

    Options = StatementOptions
    body = "text"
    css = [str(HERE / "statement.css")]

    def render(self, block, opts: StatementOptions, ctx) -> RenderResult:
        text = " ".join(block.body.split())
        if not text:
            raise ComponentError("write the sentence in the body of the block")
        text = _KEY.sub(r'<span class="lt-statement-key">\1</span>', html.escape(text, quote=False))
        return RenderResult(f'<div class="lt-statement"><p>{text}</p></div>')
