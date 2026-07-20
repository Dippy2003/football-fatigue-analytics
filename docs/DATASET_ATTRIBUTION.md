# Dataset rights and attribution

Dataset rights are a release-blocking engineering control. Public availability
does not imply unrestricted copying, redistribution, hosting, modification, or
commercial use. This record is not legal advice and does not replace the
providers' current official terms.

## Verification record

- Verification timestamp: 2026-07-20T04:57:02Z
- Verification method: official repository pages opened; official branch heads
  resolved; small official terms files fetched temporarily for SHA-256 only.
- Raw football data downloaded: none
- Provider logos downloaded or bundled: none

## PlayerPulse deterministic synthetic data

PlayerPulse will generate its own fictional match with a fixed seed. It is the
only default for automated tests, CI, public screenshots, containers, and the
hosted demo. Every synthetic record must carry `is_synthetic=true`; fictional
teams and players must never be described as real.

Status: `project_owned_synthetic`.

## Metrica Sports sample data

- Official repository: https://github.com/metrica-sports/sample-data
- Official usage statement: https://github.com/metrica-sports/sample-data#legal-stuff
- Checked branch: `master`
- Checked commit: `e706dd506b360d69d9d123d5b8026e7294b13996`
- README/terms SHA-256: `fa4b178e62c4d3559e13b6d3a4fdd42e45293461c2ab656e05a13360a6adcbcf`
- Required acknowledgement: Metrica Sports
- PlayerPulse status: `local_import_only`

The official README asks users to act responsibly and acknowledge the source
for public use, but no separate standard root data licence was visible. The
project therefore does not download, commit, mirror, package, deploy, or
redistribute Metrica raw files. A future adapter reads files supplied locally by
the developer. Broader use requires explicit permission or independent rights
verification.

## StatsBomb Open Data

- Official repository: https://github.com/hudl/open-data
- Official licence: https://github.com/hudl/open-data/blob/master/LICENSE.pdf
- Checked branch: `master`
- Checked commit: `b0bc9f22dd77c206ddedc1d742893b3bbe64baec`
- Licence SHA-256: `a5462e69aeb71a39268b760b110c5c2190a2e0cee3015ba976f66bd71f6c2bb4`
- Required attribution: identify StatsBomb as the data source and follow the
  current official publication logo/branding requirement.
- PlayerPulse status: `verification_required`

The official repository describes selected data as available for public
research and genuine football-analytics interest. PlayerPulse does not mirror
the complete dataset or bundle a provider logo. Day 2's optional adapter must
re-check the licence, retain attribution, and clearly report analyses that are
unsupported without tracking data.

## Release rules

1. Re-open each official source and terms page immediately before release.
2. Compare checked commit and terms digest with this record.
3. Stop release when relevant rights are unclear or have changed.
4. Never imply the PlayerPulse MIT licence covers third-party data or marks.
5. Keep public demo, CI, screenshots, and portfolio walkthroughs synthetic.
