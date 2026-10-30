# fnv-port-pipeline

Pipeline **pública** do projeto de portar Fallout: New Vegas ao Android via
[DesertDroid](https://github.com/Kapro777/DesertDroid) (recompilação estática
x86-32 → C → HLE).

**BYOG — Bring Your Own Game.** O `FalloutNV.exe` **não** está aqui: vem de uma
release **privada** em outro repositório usando um secret de token. Logs do
jogo levantados no CI (`boot.log`, C liftado, símbolos) também são
**privados** (uploadados para a release privada), para permanecerem em
conformidade legal — o que fica público neste repositório é apenas
estatística do pipeline e engine.

## Estrutura

- `.github/workflows/compile-public.yml` — pipeline M0..M3 completa:
  seeds → catálogo → lift → Build M2 → smoke boot M3 (GDB)
- [DesertDroid](https://github.com/Kapro777/DesertDroid) — engine + HLE + overrides
- [pcrecomp (pinned 35548b8)](https://github.com/sp00nznet/pcrecomp) — runtime recomp

## Quem já roda quem

1. `gh workflow run -R Kapro777/fnv-port-pipeline 'compile M2'`
2. Logs do boot: release privada `logs-<run_id>` em `fnv-build-inputs`
3. Estatísticas: artifact público `m2-report-public`
