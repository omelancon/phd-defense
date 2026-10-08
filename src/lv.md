# Lambda Versioning {#lv-title layout=title}

*Whole-program* ahead-of-time basic block versioning

# Overview of Lambda Versioning {.small}

{.reveal}
**The missing puzzle piece of SBBV**

{.reveal}
- *Intraprocedural* technique: limited propagation across abstraction barriers (functions)

{.reveal}
**Why?**

{.reveal}
1. SBBV propagates information *forward only*.
    - Propagating from a function's exit site to the call site requires *backward propagation*.
2. Call sites have a single return point.
    - This acts as a join point for all exit sites, losing context precision.

{.reveal}
**Solution**

{.reveal}
1. Backward propagation from function's exit sites to call sites.
2. Duplicate functions' entry points and exit sites to preserve context precision.

```timeline
reveal +2
reveal +2
reveal +1
reveal +2
reveal ..end
```

# Framing the problem with an example