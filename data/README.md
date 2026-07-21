# PlayerPulse data workspace

The public project works without external football data. Its deterministic
fictional match is the only source enabled by default for tests, CI,
screenshots, and the demo.

- `raw/`: ignored developer-supplied source files.
- `interim/`: ignored normalized working files.
- `processed/`: ignored analytics-ready Parquet and reports.
- `sources.yml`: versioned rights and provenance registry; never a grant of
  rights beyond an official provider's current terms.

Do not place secrets, real athlete health records, unlicensed datasets, badges,
photographs, or provider logos here. `.gitkeep` files reproduce empty ignored
directories without redistributing their contents.

## Generate local demo outputs

From the repository root in Windows PowerShell:

```powershell
$env:UV_CACHE_DIR="$PWD\.uv-cache"
uv run --project backend python -m app.cli generate-demo `
  --output data/processed/demo
```

The command prints JSON containing `is_synthetic: true`, the quality report,
and six generated Parquet paths. The output directory is ignored by Git. Delete
and regenerate it at any time; the fixed seed produces repeatable content.

## External adapters

- The Metrica adapters accept only developer-supplied local long-form CSVs with
  normalized coordinates. PlayerPulse does not download or redistribute the
  provider's sample files.
- The StatsBomb adapter accepts only developer-supplied local event JSON and
  fails closed unless the caller explicitly acknowledges a current rights
  check. It does not provide tracking metrics from event-only input.
- Every local import can produce a SHA-256 manifest containing file roles,
  original names, sizes, MIME types, source identity, and a snapshot of the
  registry's rights evidence without copying raw source content.

Review `sources.yml` and `docs/DATASET_ATTRIBUTION.md` before every external
import or release. A registry entry records a check; it does not grant rights.
