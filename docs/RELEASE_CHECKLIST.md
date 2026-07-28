# PlayerPulse 1.0.0 release checklist

The release owner records command output in `DAY_5_REPORT.md`. A checked box is
valid only when the corresponding command actually passed on the release
commit.

## Source and governance

- [ ] `main` starts at the verified `day-4-complete` checkpoint
- [ ] At least 30 substantive commits exist after that tag
- [ ] Progress, decisions, implementation plan, and generated commit log agree
- [ ] Synthetic data remains the only public-demo/test/screenshot source
- [ ] Official Metrica and StatsBomb terms were re-checked
- [ ] No raw provider data, model binaries, secrets, local databases, or reports
      are tracked

## Quality and behavior

- [ ] Ruff formatting and lint pass
- [ ] mypy passes
- [ ] Full backend tests and coverage pass
- [ ] Prettier, ESLint, and TypeScript checks pass
- [ ] Full frontend unit tests and production build pass
- [ ] Desktop and mobile Playwright journeys pass
- [ ] Automated serious/critical accessibility scan passes
- [ ] Clean SQLite migrations upgrade, downgrade, and upgrade
- [ ] Docker Compose configuration and runtime stack pass where Docker exists
- [ ] Health, readiness, version, API docs, and reviewer flow are checked

## Security and operations

- [ ] Upload/path/size/media-type tests pass with uploads disabled by default
- [ ] Production CORS rejects wildcard, HTTP, and loopback origins
- [ ] API and Nginx security headers are present
- [ ] Tracked-secret and dataset-distribution scans pass
- [ ] Python dependency audit has no known vulnerability
- [ ] npm audit has no critical vulnerability; any lower accepted issue is
      scoped and documented
- [ ] CI covers backend, frontend, browser, PostgreSQL, rights, secrets, and
      Compose configuration

## Tagging

- [ ] `scripts/verify_release.py` passes before tagging
- [ ] Working tree is clean
- [ ] Annotated `day-5-complete` points at the verified commit
- [ ] Annotated `v1.0.0` points at the same verified commit
- [ ] Post-tag verification checks both tags
- [ ] Push occurs only after explicit owner authorization
