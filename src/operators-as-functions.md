# Operators as Functions {#operators-as-functions layout=title}

# Operators as functions: the polynomial {#operators-example .small}

:::columns
:::column {#of-src width=1fr}
```code-morph {#of-morph lang=scheme room=fit}
versions:
  - file: programs/operators-as-functions.scm
    label: "p.scm"
  - file: programs/operators-as-functions-defs.scm
    label: "+ and * as functions"
    highlight: changed
```
:::/column
:::column {#of-notes width=1fr}
{.reveal}
- SBBV requires inlined operators
- ΛV can support operators as functions
:::/column
:::column {#of-col width=0}
```bbv-anim {#of-lv program="programs/operators-as-functions.bbv" algorithm=lv heuristic=arithmetic limit=3 entry=main direction=TB wrap=3 height=500}
show: [label, context, code]
paths:
  - reads: [fl]
```
:::/column
:::/columns

```arrow {#of-removed}
steps:
  - null
  - {to: of-lv.K1, to_anchor: right, angle: 330, length: 85, label: "removed type check in +"}
```

```timeline
reveal 1                                  # SBBV requires inlined operators
reveal 2                                  # ΛV can support operators as functions
of-morph 1                                # + and * as functions, above p
width of-src=0 of-notes=0 of-col=1fr      # the columns collapse; the ΛV run takes the whole width
of-lv 1..end-1                            # the run, one frame per step
of-lv end, of-removed 1                   # the fixnum version of +: its type check is gone
```


# Operators as functions: compile time {#operators-compile-time .small}

Operators as functions re-use specializations. Inlined operators had to re-specialize at every site.

```plot {backend=vega source="plots/thesis_plots.py:lv_operators_compile_time_all" legend=true width=10 height=4.2}
```
