# Brooke InDesign Automation

Original TypeScript-authored editorial automation commands compiled into
standalone ExtendScript-safe JSX files.

## Build

```powershell
npm install
npm test
```

Generated commands appear in `dist/`. Copy the required JSX files into:

```text
C:\Users\toddl\AppData\Roaming\Adobe\InDesign\Version 21.0\en_US\Scripts\Scripts Panel
```

Each mutating command asks whether to apply changes. Choosing **No** runs a
diagnostic dry run. Reports are written to:

```text
C:\Users\toddl\Documents\Brooke Adobe Automation Reports
```

## Safety

- Active-document guard
- Dry-run-first option
- One-step undo grouping
- Explicit warnings and skipped-item counts
- No proprietary InDesign-Automation-Suite code
