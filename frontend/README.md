# glmhmmt documentation frontend

Astro/Starlight documentation for the `glmhmmt` package.

## Common commands

```bash
npm install
npm run dev
npm run build
```

## Plot gallery

The static plot gallery is generated from synthetic data, not from fitted
results:

```bash
python scripts/generate_plot_gallery.py
```

Outputs are written to `public/plot-gallery/` and embedded from the API docs.
When a public plot API changes, update the script and regenerate the PNGs in
the same change.

## Documentation rules

- Common model plots are documented as `postprocess -> plot` examples.
- Task plots document only task semantics; they should not duplicate model plot
  examples.
- Keep snippets executable against the package API, not notebook-local helpers.
