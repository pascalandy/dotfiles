/**
 * find-browse — locate the gstack browse binary.
 *
 * Compiled to browse/dist/find-browse (standalone binary, no bun runtime needed).
 * Outputs the absolute path to the browse binary on stdout, or exits 1 if not found.
 */

import { existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

// ─── Binary Discovery ───────────────────────────────────────────

function getGitRoot(): string | null {
  try {
    const proc = Bun.spawnSync(['git', 'rev-parse', '--show-toplevel'], {
      stdout: 'pipe',
      stderr: 'pipe',
    });
    if (proc.exitCode !== 0) return null;
    return proc.stdout.toString().trim();
  } catch {
    return null;
  }
}

export function locateBinary(): string | null {
  const root = getGitRoot();
  const home = homedir();
  const candidates: string[] = [];

  // Workspace-local takes priority.
  if (root) {
    candidates.push(
      join(root, '.opencode', 'skill', 'gstack', 'browse', 'dist', 'browse'),
      join(root, '.opencode', 'skills', 'gstack', 'browse', 'dist', 'browse'),
      join(root, '.claude', 'skills', 'gstack', 'browse', 'dist', 'browse'),
    );
  }

  // Global fallback.
  candidates.push(
    join(home, '.config', 'opencode', 'skill', 'gstack', 'browse', 'dist', 'browse'),
    join(home, '.config', 'opencode', 'skills', 'gstack', 'browse', 'dist', 'browse'),
    join(home, '.opencode', 'skill', 'gstack', 'browse', 'dist', 'browse'),
    join(home, '.opencode', 'skills', 'gstack', 'browse', 'dist', 'browse'),
    join(home, '.claude', 'skills', 'gstack', 'browse', 'dist', 'browse'),
  );

  for (const candidate of candidates) {
    if (existsSync(candidate)) return candidate;
  }

  return null;
}

// ─── Main ───────────────────────────────────────────────────────

function main() {
  const bin = locateBinary();
  if (!bin) {
    process.stderr.write(
      'ERROR: browse binary not found. Set GSTACK_BROWSE_BIN or run ./setup in a full gstack checkout.\n'
    );
    process.exit(1);
  }

  console.log(bin);
}

main();
