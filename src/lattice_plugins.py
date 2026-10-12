"""Local plugins for the defense deck. Lattice imports this file automatically (spec 8.1)."""
from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path

from markdown_it import MarkdownIt
from pydantic import BaseModel, ConfigDict, Field

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


class RelatedWorkNoteOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    comment: str = ""     # a sentence on how the works relate, between the heading and the items
    items: list[str] = Field(min_length=1)
    flash: bool = False   # shown for one position only, laid over what follows it
    inline: bool = False  # the comment and the items run on as one sentence (no bullets), to save height


_INLINE = MarkdownIt("commonmark", {"html": False})


@register("related-work-note")
class RelatedWorkNote(Component):
    """A box pointing out related work, the same on every slide that has one.

    Every note has the same layout: a bold "Related work" heading at the top, then the optional
    ``comment`` (a sentence on how the works relate), then the ``items``, one work per entry
    (``Name (Author year)``); both take inline Markdown (`code`, *emphasis*). Styled by
    plugins/related-work-note.css, a light blue box built from the theme's variables.

    Two ways to show it:

    - a note that stays: put a ``{.reveal}`` line before the block. Like any fragment, its room is
      kept from the first step of the slide, so the slide must have space for it.
    - a note that flashes, for a slide without that space: ``flash: true`` and an ``#id``. The block
      is then a track of three positions, hidden (0), shown (1) and hidden again (2), moved in the
      timeline (``rw 1``, then ``rw end``). It takes no room: shown, it is laid over the blocks that
      follow it in its column, at its own place, so it belongs where the next blocks are not yet
      revealed (they appear in that space once it is gone).

    ``inline: true`` runs the comment and the items on as one sentence under the heading, without
    bullets (items are separated by semicolons), to save height for a note citing one work.
    """

    Options = RelatedWorkNoteOptions
    version = "4"
    body = "yaml"
    runtime = str(HERE / "related-work-note.js")
    css = [str(HERE / "related-work-note.css")]

    def render(self, block, opts: RelatedWorkNoteOptions, ctx) -> RenderResult:
        items = "".join(f"<li>{_INLINE.renderInline(item)}</li>" for item in opts.items)
        cls = "lt-related-work rw-inline" if opts.inline else "lt-related-work"
        comment = f'<p class="rw-comment">{_INLINE.renderInline(opts.comment)}</p> ' if opts.comment else ""
        note = (f'<aside class="{cls}"><p class="rw-head"><strong>Related work</strong></p>'
                f"{comment}<ul>{items}</ul></aside>")
        if not opts.flash:
            return RenderResult(note)
        return RenderResult(f'<div class="lt-related-work-slot">{note}</div>', data={"flash": True}, positions=3)


class TakeawayOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    key: str              # the phrase of the thesis question it answers, quoted
    figure: str           # one big number or word
    caption: str          # what the figure means, one short sentence


@register("takeaway")
class Takeaway(Component):
    """One answer on the closing slide: a quoted key phrase, then a big figure and a caption.

    The YAML body gives ``key`` (the phrase of the thesis question it answers), ``figure`` (a number
    or a short word, set large in the accent colour) and ``caption``; ``key`` and ``caption`` take
    inline Markdown. Two positions: at 0 only the key shows, on a grey rule with a hollow node; at 1
    the node fills, the rule turns to the accent colour and the figure and caption appear. The rule
    runs into the gap after its column, so that takeaways side by side in columns read as one path.
    Give it an ``#id`` and move it in a timeline. Styled by plugins/takeaway.css, which uses the
    theme's variables.
    """

    Options = TakeawayOptions
    version = "1"
    body = "yaml"
    runtime = str(HERE / "takeaway.js")
    css = [str(HERE / "takeaway.css")]

    def render(self, block, opts: TakeawayOptions, ctx) -> RenderResult:
        markup = ('<div class="lt-takeaway"><span class="tk-rule"></span>'
                  f'<p class="tk-key">{_INLINE.renderInline(opts.key)}</p>'
                  f'<p class="tk-figure">{html.escape(opts.figure, quote=False)}</p>'
                  f'<p class="tk-caption">{_INLINE.renderInline(opts.caption)}</p></div>')
        return RenderResult(markup, data={"positions": 2}, positions=2)


class ThanksOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    lines: list[str] = Field(min_length=1)
    image: str            # a PNG whose alpha channel is the drawing, relative to the deck file
    alt: str = ""
    caption: str = ""


@register("thanks")
class Thanks(Component):
    """The acknowledgements slide: lines of thanks beside a black and white drawing and its credit.

    The YAML body gives ``lines`` (one sentence each; ``**words**`` mark who is thanked, set in ink
    while the rest of the sentence is muted), ``image`` (a PNG drawn as an alpha mask, so that the
    drawing takes the theme's ink colour; it is embedded in the deck), ``alt`` and ``caption`` (the
    credit, in inline Markdown). Styled by plugins/thanks.css with the theme's variables.
    """

    Options = ThanksOptions
    body = "yaml"
    css = [str(HERE / "thanks.css")]

    def render(self, block, opts: ThanksOptions, ctx) -> RenderResult:
        import base64
        import struct

        data = ctx.path(opts.image).read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            raise ComponentError(f"{opts.image}: give a PNG with an alpha channel")
        w, h = struct.unpack(">II", data[16:24])
        url = "data:image/png;base64," + base64.b64encode(data).decode("ascii")
        lines = "".join(f"<p>{_INLINE.renderInline(line)}</p>" for line in opts.lines)
        caption = f"<figcaption>{_INLINE.renderInline(opts.caption)}</figcaption>" if opts.caption else ""
        figure = (f'<figure class="th-figure"><div class="th-drawing" role="img" '
                  f'aria-label="{html.escape(opts.alt, quote=True)}" '
                  f"style=\"aspect-ratio:{w}/{h};--th-src:url('{url}')\"></div>{caption}</figure>")
        return RenderResult(f'<div class="lt-thanks"><div class="th-lines">{lines}</div>{figure}</div>')


class TableStepsOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    table: str                                  # a GFM table, as it would be written in the slide
    best: str = "none"                          # min, max or none: which number of each row is highlighted
    steps: list[dict | None] = [None]


_NUM = re.compile(r"[-+]?\d+(?:[.,]\d+)*(?:[eE][-+]?\d+)?")


def _table_cells(line: str) -> list[str]:
    """The cells of one row of a GFM table (a `\\|` stays in its cell)."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line)]


@register("table-steps")
class TableSteps(Component):
    """A table whose columns appear or disappear step by step, the best number of each row highlighted.

    The YAML body gives ``table`` (a GFM table, cells in inline Markdown, alignment from its
    separator row), ``best`` (``min`` or ``max``: in each row, the smallest or largest number among
    the columns shown at that position is highlighted in light yellow, all of them on a tie; ``none``, the default,
    leaves the cells as written) and ``steps``, one entry per position: ``null`` (no change) or a
    mapping with ``hide`` and ``show``, lists of column headers as written in the table. Entries
    are deltas over the previous position, so the first one hides what the slide opens without.
    With ``best``, write the numbers without ``**``: the highlight is computed.

    A single step animates: the columns that stay glide to their new places, the columns shown
    fade in, the highlight moves. Give it an ``#id`` when the slide has another track. Styled by
    plugins/table-steps.css; the table itself keeps the theme's table style.
    """

    Options = TableStepsOptions
    version = "2"
    body = "yaml"
    runtime = str(HERE / "table-steps.js")
    css = [str(HERE / "table-steps.css")]

    def render(self, block, opts: TableStepsOptions, ctx) -> RenderResult:
        lines = [ln for ln in opts.table.strip().splitlines() if ln.strip()]
        if len(lines) < 2 or not re.fullmatch(r"\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*", lines[1]):
            raise ComponentError("'table' must be a GFM table: a header row, then a separator row (| --- | ---: |)")
        head = _table_cells(lines[0])
        aligns = []
        for sep in _table_cells(lines[1]):
            left, right = sep.startswith(":"), sep.endswith(":")
            aligns.append("center" if left and right else "right" if right else "left" if left else None)
        rows = [_table_cells(ln) for ln in lines[2:]]
        ncols = len(head)
        if len(aligns) != ncols or any(len(r) != ncols for r in rows):
            raise ComponentError(f"every row of the table must have {ncols} cells, as its header")
        if opts.best not in ("min", "max", "none"):
            raise ComponentError(f"best: {opts.best!r}; use min, max or none")

        def value(cell: str) -> float | None:
            plain = cell.replace("*", "").replace("`", "").strip()
            m = _NUM.fullmatch(plain)
            return float(m.group(0).replace(",", "")) if m else None

        values = [[value(c) for c in r] for r in rows]
        if opts.best != "none" and any("**" in c for r in rows for c in r):
            raise ComponentError("with 'best', write the numbers without ** : the highlight is computed")

        hidden: set[int] = set()
        positions = []
        for i, step in enumerate(opts.steps):
            step = step or {}
            unknown = set(step) - {"hide", "show"}
            if unknown:
                raise ComponentError(f"steps[{i}]: unknown key(s) {sorted(unknown)}; use hide, show")
            for key in ("hide", "show"):
                for name in step.get(key) or []:
                    name = str(name).strip()
                    if name not in head:
                        raise ComponentError(f"steps[{i}].{key}: no column {name!r}; the table has "
                                             f"{', '.join(repr(h) for h in head)}")
                    (hidden.add if key == "hide" else hidden.discard)(head.index(name))
            best = []
            if opts.best != "none":
                for r, row in enumerate(values):
                    shown = [v for c, v in enumerate(row) if c not in hidden and v is not None]
                    if shown:
                        target = min(shown) if opts.best == "min" else max(shown)
                        best += [[r, c] for c, v in enumerate(row) if c not in hidden and v == target]
            positions.append({"hidden": sorted(hidden), "best": best})

        def cell(tag: str, text: str, c: int) -> str:
            style = f' style="text-align:{aligns[c]}"' if aligns[c] else ""
            return f'<{tag} data-c="{c}"{style}><span class="ts-v">{_INLINE.renderInline(text)}</span></{tag}>'

        thead = "<tr>" + "".join(cell("th", h, c) for c, h in enumerate(head)) + "</tr>"
        tbody = "".join(f'<tr data-r="{r}">' + "".join(cell("td", t, c) for c, t in enumerate(row)) + "</tr>"
                        for r, row in enumerate(rows))
        markup = (f'<div class="lt-table-steps"><table><thead>{thead}</thead>'
                  f"<tbody>{tbody}</tbody></table></div>")
        return RenderResult(markup, data={"positions": positions}, positions=len(positions))


class JuryMember(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    role: str             # président, directeur de recherche...
    affiliation: str = ""


class TitlePageOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = None      # defaults to the front matter's title
    author: str | None = None     # defaults to the front matter's author
    kicker: str = ""              # a short line above the title (the occasion)
    date: str | None = None       # defaults to the front matter's date, if any
    logo: str | None = None       # an SVG, relative to the deck file, inlined
    logo_alt: str = ""
    jury: list[JuryMember] = Field(default_factory=list)
    motif: bool = True            # a large, faint lattice in the background


_SVG_HEAD = re.compile(r"^.*?(?=<svg\b)", re.S)


def _inline_svg(source: str, alt: str) -> str:
    """An SVG file as inline markup: shapes without a fill take the text colour (``currentColor``),
    so that the black parts of a logo follow the theme's ink while its coloured parts keep their colour."""
    svg = _SVG_HEAD.sub("", source, count=1)
    svg = re.sub(r"<!--.*?-->|<metadata\b.*?</metadata>", "", svg, flags=re.S)
    svg = re.sub(r"<(path|polygon|rect|circle|ellipse)\b(?![^>]*\bfill=)", r'<\1 fill="currentColor"', svg)
    end = svg.find(">") + 1                     # the root tag loses its size: CSS sets it
    svg = re.sub(r'\s(?:width|height)="[^"]*"', "", svg[:end]) + svg[end:]
    label = f'role="img" aria-label="{html.escape(alt, quote=True)}"' if alt else 'aria-hidden="true"'
    return svg.replace("<svg ", f'<svg class="tp-logo" {label} preserveAspectRatio="xMinYMid meet" ', 1)


def _lattice_motif(half: int = 4, dx: float = 60, dy: float = 52, r: float = 6) -> str:
    """A Hasse diagram for the background: a diamond lattice from a bottom element to a top one, each
    node joined to the nodes just above it. ``half`` is the number of rows from the bottom to the
    widest row. Styled faint by plugins/title-page.css."""
    rows = [i + 1 for i in range(half + 1)] + [half - i for i in range(half)]   # 1 2 3 4 5 4 3 2 1

    def pos(i, j):
        return (j - (rows[i] - 1) / 2) * dx, -i * dy

    lines, dots = [], []
    for i, n in enumerate(rows):
        for j in range(n):
            x, y = pos(i, j)
            dots.append((x, y))
            if i + 1 < len(rows):
                above = (j, j + 1) if rows[i + 1] > n else (j - 1, j)
                lines += [(x, y, *pos(i + 1, k)) for k in above if 0 <= k < rows[i + 1]]
    w, h = half * dx + 2 * r + 4, (len(rows) - 1) * dy + 2 * r + 4
    ox, oy = w / 2, h - r - 2
    edges = "".join(f'<line x1="{x1 + ox:.1f}" y1="{y1 + oy:.1f}" x2="{x2 + ox:.1f}" y2="{y2 + oy:.1f}"/>'
                    for x1, y1, x2, y2 in lines)
    nodes = "".join(f'<circle cx="{x + ox:.1f}" cy="{y + oy:.1f}" r="{r}"/>' for x, y in dots)
    return (f'<svg class="tp-motif" viewBox="0 0 {w:.0f} {h:.0f}" aria-hidden="true">'
            f'<g class="tp-motif-edges">{edges}</g><g class="tp-motif-nodes">{nodes}</g></svg>')


_HYPHENATED = re.compile(r"\S+-\S+")


@register("title-page")
class TitlePage(Component):
    """The opening slide of a defense: the institution, the title, the author and the jury.

    The YAML body gives ``kicker`` (a short line naming the occasion), ``logo`` (an SVG file, inlined so
    that its uncoloured shapes take the theme's ink), ``logo_alt`` and ``jury``, a list of
    ``{name, role, affiliation}`` in the order of the defense; ``motif: false`` removes the faint
    lattice drawn in the background. ``title``, ``author`` and ``date`` default
    to the front matter. The slide's own ``#`` heading is hidden (it still names the slide in the
    overview and the go-to list), so the block owns the whole slide. Styled by plugins/title-page.css
    with the theme's variables: the jury hangs from a rule with a node per member, the vertical
    counterpart of the takeaways on the Conclusion slide.
    """

    Options = TitlePageOptions
    version = "2"
    body = "yaml"
    css = [str(HERE / "title-page.css")]

    def render(self, block, opts: TitlePageOptions, ctx) -> RenderResult:
        title = opts.title or ctx.meta.title
        author = opts.author or ctx.meta.author
        if not title:
            raise ComponentError("give a 'title', or a title in the front matter")
        date = opts.date if opts.date is not None else (ctx.meta.date or "")
        esc = lambda s: html.escape(str(s), quote=False)

        top = ""
        if opts.logo or opts.kicker:
            logo = _inline_svg(ctx.path(opts.logo).read_text(encoding="utf-8"), opts.logo_alt) if opts.logo else ""
            kicker = f'<p class="tp-kicker">{esc(opts.kicker)}</p>' if opts.kicker else ""
            top = f'<div class="tp-top">{logo}{kicker}</div>'

        byline = ""
        if author or date:
            byline = ('<div class="tp-byline">'
                      + (f'<p class="tp-author">{esc(author)}</p>' if author else "")
                      + (f'<p class="tp-date">{esc(date)}</p>' if date else "") + "</div>")
        # a hyphenated word (Ahead-of-Time) never breaks at its hyphens
        title_html = _HYPHENATED.sub(lambda m: f'<span class="tp-nowrap">{m.group(0)}</span>', esc(title))
        main = f'<div class="tp-main"><p class="tp-title">{title_html}</p>{byline}</div>'

        jury = ""
        if opts.jury:
            items = "".join(
                f'<li><p class="tp-name">{esc(m.name)}</p><p class="tp-role">'
                f'<span class="tp-role-name">{esc(m.role)}</span>'
                + (f'<span class="tp-affil">{esc(m.affiliation)}</span>' if m.affiliation else "")
                + "</p></li>" for m in opts.jury)
            jury = f'<section class="tp-jury" aria-label="Jury"><p class="tp-label">Jury</p><ol>{items}</ol></section>'

        motif = _lattice_motif() if opts.motif else ""
        return RenderResult(f'<div class="lt-title-page">{motif}{top}{main}{jury}</div>')
