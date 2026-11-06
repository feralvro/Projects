# Web pública del Inventory Watch (archivada)

La web está apagada desde 2026-11-06. Nada de esta carpeta se ejecuta: GitHub Actions
solo lee workflows de `.github/workflows/`, y la tarea nocturna ya no publica.
El contador diario (`contador.yml`) y el artefacto personal siguen funcionando igual.

El estado exacto antes de archivarla es el commit `a982ec4` (`git checkout a982ec4` para verlo).

## Qué hay aquí
- `web/`: la página (`index.html`) y sus datos (`web/data/*.json`).
- `web.yml`: el workflow que la publicaba en GitHub Pages.
- `scripts/exportar_web.py`: genera `web/data/panel.json` y `dias.json` desde `data/`.
- `scripts/snapshot_senales.py`: genera `web/data/senales.json` y `modelo.json` desde la base del artefacto.

## Cómo retomarla
1. Devolver los ficheros a su sitio:
   ```bash
   git mv archivo-web/web web
   git mv archivo-web/web.yml .github/workflows/web.yml
   git mv archivo-web/scripts/exportar_web.py archivo-web/scripts/snapshot_senales.py scripts/
   git commit -m "Retomar la web pública" && git push origin main
   ```
2. En GitHub: Settings → Pages → Source: **GitHub Actions** (si se despublicó).
3. Lanzar "Publicar web (Inventory Watch)" desde la pestaña Actions, o esperar al siguiente contador.
4. Si quieres los snapshots de señales automáticos otra vez, volver a añadir a la tarea nocturna
   el paso C: leer `senales` y `modelo/actual` del artefacto con ArtifactData y ejecutar
   `python3 -I scripts/snapshot_senales.py <carpeta senales> <modelo/actual.json> web/data`,
   con commit de `web/data/senales.json` y `web/data/modelo.json`.
