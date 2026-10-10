# Conclusion {#conclusion}

::: columns
::: column
```takeaway {#tk-checks}
key: SBBV eliminates run-time checks
figure: "54–62%"
caption: fewer dynamic checks in Bigloo and Gambit with only **2 versions** per block, about 10% faster.
```
::: /column
::: column
```takeaway {#tk-static}
key: ΛV removes nearly all type checks
figure: "1"
caption: type check per input, then **none**; ΛV specializes `fib`, `ack` and `tak` optimally.
```
::: /column
::: column
```takeaway {#tk-flex}
key: whole-program specialization
figure: "AOT"
caption: code duplication to anticipate multiple run-time behaviors.
```
::: /column
::: /columns

```timeline
tk-checks 1       # SBBV: over half of the dynamic checks gone, about 10% faster
tk-static 1       # ΛV: optimal specialization, one type check per input
tk-flex 1         # and nothing given up for it
```

# Remerciements {#thanks}

```thanks
lines:
  - Merci à **Marc Feeley** et **Manuel Serrano** pour vos conseils et soutiens indéfectibles.
  - Merci au **jury de thèse**. Un merci particulier à **Matthew Flatt**.
  - Merci à toute la **communauté du DIRO**.
  - Merci à tous mes **collègues et amis** du **LTP**. 🤽
  - Merci à mes **amis** pour ces années de support.
  - Merci à ma **famille**, pour votre soutien, votre amour et votre fierté.
image: figures/dream-of-islands.png
alt: Un voilier sous la pluie, une chaloupe dans les vagues
caption: "*A Dream of Islands*, Philip Teece, p.&nbsp;33"
```
