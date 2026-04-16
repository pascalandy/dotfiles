import type { Plugin } from "@opencode-ai/plugin";

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function getString(record: Record<string, unknown>, key: string): string | null {
  const value = record[key];
  return typeof value === "string" ? value : null;
}

function getBashCommand(output: unknown): string | null {
  if (!isRecord(output)) return null;
  const args = output["args"];
  if (!isRecord(args)) return null;
  return getString(args, "command");
}

function makeBlockedError(command: string, reason: string): Error {
  return new Error(
    [
      "BLOCKED by git-safety-guard",
      "",
      `Reason: ${reason}`,
      "",
      `Command: ${command}`,
      "",
      "Suggested: run `git status`, `git diff`, then `git stash push -u` before destructive ops.",
    ].join("\n"),
  );
}

type TokenizeResult = { words: string[] };

function tokenizeShellWords(command: string): TokenizeResult {
  const words: string[] = [];
  let current = "";

  let inSingle = false;
  let inDouble = false;

  const pushCurrent = () => {
    if (current.length > 0) {
      words.push(current);
      current = "";
    }
  };

  const isWhitespace = (ch: string) => ch === " " || ch === "\t";

  for (let i = 0; i < command.length; i += 1) {
    const ch = command[i] ?? "";

    if (inSingle) {
      if (ch === "'") {
        inSingle = false;
      } else {
        current += ch;
      }
      continue;
    }

    if (inDouble) {
      if (ch === '"') {
        inDouble = false;
        continue;
      }
      if (ch === "\\") {
        const next = command[i + 1];
        if (typeof next === "string") {
          current += next;
          i += 1;
          continue;
        }
        current += "\\";
        continue;
      }
      current += ch;
      continue;
    }

    if (ch === "'") {
      inSingle = true;
      continue;
    }

    if (ch === '"') {
      inDouble = true;
      continue;
    }

    if (ch === "\\") {
      const next = command[i + 1];
      if (typeof next === "string") {
        current += next;
        i += 1;
        continue;
      }
      current += "\\";
      continue;
    }

    if (ch === "#") {
      const prev = i > 0 ? (command[i - 1] ?? "") : "";
      if (i === 0 || isWhitespace(prev)) {
        pushCurrent();
        break;
      }
      current += "#";
      continue;
    }

    if (isWhitespace(ch)) {
      pushCurrent();
      continue;
    }

    current += ch;
  }

  pushCurrent();
  return { words };
}

function basename(executable: string): string {
  const parts = executable.split("/");
  const last = parts[parts.length - 1];
  return last && last.length > 0 ? last : executable;
}

function unwrapLeadingWrappers(words: string[]): number {
  let i = 0;

  while (i < words.length) {
    const w = words[i] ?? "";

    if (w === "sudo") {
      i += 1;
      while (i < words.length) {
        const opt = words[i] ?? "";
        if (!opt.startsWith("-")) break;
        if (opt === "-u" || opt === "-g" || opt === "-h") {
          i += words[i + 1] ? 2 : 1;
          continue;
        }
        i += 1;
      }
      continue;
    }

    if (w === "command" || w === "builtin") {
      i += 1;
      while (i < words.length) {
        const opt = words[i] ?? "";
        if (opt === "-p" || opt === "-v" || opt === "-V") {
          i += 1;
          continue;
        }
        break;
      }
      continue;
    }

    if (w === "env") {
      i += 1;
      while (i < words.length) {
        const opt = words[i] ?? "";
        if (opt === "-i" || opt === "-0") {
          i += 1;
          continue;
        }
        if (opt === "-u") {
          i += words[i + 1] ? 2 : 1;
          continue;
        }
        break;
      }

      while (i < words.length) {
        const maybeAssign = words[i] ?? "";
        const eq = maybeAssign.indexOf("=");
        if (eq > 0) {
          i += 1;
          continue;
        }
        break;
      }

      continue;
    }

    if (w === "nice") {
      i += 1;
      if (words[i] === "-n") i += words[i + 1] ? 2 : 1;
      else if ((words[i] ?? "").startsWith("-")) i += 1;
      continue;
    }

    if (w === "time") {
      i += 1;
      while (i < words.length && (words[i] ?? "").startsWith("-")) i += 1;
      continue;
    }

    break;
  }

  return i;
}

function tokenHasShortFlag(token: string, flag: string): boolean {
  if (!token.startsWith("-") || token.startsWith("--") || token === "-") return false;
  return token.slice(1).includes(flag);
}

function hasAnyForceFlag(tokens: string[]): boolean {
  return tokens.includes("--force") || tokens.includes("-f") || tokens.some((t) => tokenHasShortFlag(t, "f"));
}

function normalizeAbsolutePosixPathOrNull(raw: string): string | null {
  if (!raw.startsWith("/")) return null;

  const parts = raw.split("/");
  const out: string[] = [];

  for (const part of parts) {
    if (part === "" || part === ".") continue;
    if (part === "..") {
      if (out.length === 0) return null;
      out.pop();
      continue;
    }
    out.push(part);
  }

  return "/" + out.join("/");
}

function hasDotDotSegment(posixPath: string): boolean {
  return posixPath.split("/").some((p) => p === "..");
}

function isAllowedTmpdirTarget(rawTarget: string): boolean {
  if (rawTarget === "$TMPDIR" || rawTarget === "$TMPDIR/") return false;
  if (rawTarget === "${TMPDIR}" || rawTarget === "${TMPDIR}/") return false;

  if (rawTarget.startsWith("$TMPDIR/")) {
    const suffix = rawTarget.slice("$TMPDIR".length);
    if (!suffix.startsWith("/")) return false;
    if (hasDotDotSegment(suffix)) return false;
    return true;
  }

  if (rawTarget.startsWith("${TMPDIR}/")) {
    const suffix = rawTarget.slice("${TMPDIR}".length);
    if (!suffix.startsWith("/")) return false;
    if (hasDotDotSegment(suffix)) return false;
    return true;
  }

  return false;
}

function analyzeRm(wordsFromRm: string[]): string | null {
  const optsAndArgs = wordsFromRm.slice(1);
  let recursive = false;
  let force = false;

  const targets: string[] = [];
  let endOfOptions = false;

  for (let i = 0; i < optsAndArgs.length; i += 1) {
    const tok = optsAndArgs[i] ?? "";

    if (!endOfOptions && tok === "--") {
      endOfOptions = true;
      continue;
    }

    if (!endOfOptions && tok.startsWith("--")) {
      if (tok === "--recursive") recursive = true;
      if (tok === "--force") force = true;
      if (tok === "--no-preserve-root") {
        recursive = true;
        force = true;
      }
      continue;
    }

    if (!endOfOptions && tok.startsWith("-") && tok !== "-") {
      const flags = tok.slice(1);
      if (flags.includes("r") || flags.includes("R")) recursive = true;
      if (flags.includes("f")) force = true;
      continue;
    }

    targets.push(tok);
  }

  if (!(recursive && force)) return null;

  if (targets.length === 0) {
    return "`rm -rf` without explicit targets is not allowed.";
  }

  for (const t of targets) {
    if (t === "/") return "`rm -rf /` is not allowed.";
    if (t === "~" || t.startsWith("~/")) return "`rm -rf ~` is not allowed.";
  }

  for (const rawTarget of targets) {
    if (isAllowedTmpdirTarget(rawTarget)) continue;

    const normalized = normalizeAbsolutePosixPathOrNull(rawTarget);
    if (!normalized) {
      return "`rm -rf` is only allowed within `/tmp/`, `/var/tmp/`, or `$TMPDIR/`.";
    }

    if (normalized === "/tmp" || normalized === "/tmp/") {
      return "`rm -rf /tmp` is too broad; target a subpath like `/tmp/<name>` or `/tmp/*`.";
    }

    if (normalized === "/var/tmp" || normalized === "/var/tmp/") {
      return "`rm -rf /var/tmp` is too broad; target a subpath like `/var/tmp/<name>` or `/var/tmp/*`.";
    }

    if (normalized.startsWith("/tmp/")) continue;
    if (normalized.startsWith("/var/tmp/")) continue;

    return "`rm -rf` is only allowed within `/tmp/`, `/var/tmp/`, or `$TMPDIR/`.";
  }

  return null;
}

type GitParseResult = { subcommand: string | null; args: string[] };

function parseGitSubcommand(wordsFromGit: string[]): GitParseResult {
  const rest = wordsFromGit.slice(1);

  let i = 0;
  while (i < rest.length) {
    const tok = rest[i] ?? "";
    if (tok === "--") {
      i += 1;
      break;
    }
    if (!tok.startsWith("-")) break;

    if (tok === "-C" || tok === "-c" || tok === "--git-dir" || tok === "--work-tree" || tok === "--namespace") {
      i += rest[i + 1] ? 2 : 1;
      continue;
    }

    i += 1;
  }

  const subcommand = rest[i] ?? null;
  const args = subcommand ? rest.slice(i + 1) : [];
  return { subcommand, args };
}

function analyzeGit(wordsFromGit: string[]): string | null {
  const { subcommand, args } = parseGitSubcommand(wordsFromGit);
  if (!subcommand) return null;

  if (subcommand === "checkout") {
    if (args.includes("-b") || args.includes("--orphan")) return null;
    if (args.includes("--")) return "`git checkout [<ref>] -- <paths>` overwrites the working tree with uncommitted changes lost.";
    if (args.includes("-f") || args.includes("--force")) return "`git checkout --force` overwrites the working tree.";
    return null;
  }

  if (subcommand === "restore") {
    if (args.includes("--worktree") || args.includes("-W")) return "`git restore --worktree` discards uncommitted changes.";
    if (args.includes("--staged")) return null;
    return "`git restore` is only allowed with `--staged` (worktree changes are blocked).";
  }

  if (subcommand === "clean") {
    const hasDryRun = args.includes("--dry-run") || args.some((t) => tokenHasShortFlag(t, "n"));
    if (!hasDryRun) return "`git clean` is only allowed with `-n`/`--dry-run`.";
    if (hasAnyForceFlag(args)) return "`git clean` with force flags (`-f`/`--force`) is not allowed.";
    return null;
  }

  if (subcommand === "push") {
    const hasForceWithLease =
      args.includes("--force-with-lease") || args.some((t) => t.startsWith("--force-with-lease="));

    if (hasForceWithLease) {
      const hasOtherForce =
        args.includes("--force") ||
        args.includes("-f") ||
        args.some((t) => tokenHasShortFlag(t, "f"));

      if (hasOtherForce) return "Do not combine `--force-with-lease` with other force flags.";
      return null;
    }

    if (hasAnyForceFlag(args)) return "Force pushes are only allowed with `--force-with-lease`.";
    return null;
  }

  if (subcommand === "reset") {
    if (args.includes("--hard")) return "`git reset --hard` destroys uncommitted changes.";
    if (args.includes("--merge")) return "`git reset --merge` can lose uncommitted changes.";
    return null;
  }

  if (subcommand === "branch") {
    if (args.includes("-D")) return "`git branch -D` force-deletes a branch.";
    return null;
  }

  if (subcommand === "stash") {
    const op = args[0] ?? "";
    if (op === "drop") return "`git stash drop` permanently deletes stashed changes.";
    if (op === "clear") return "`git stash clear` permanently deletes ALL stashes.";
    return null;
  }

  return null;
}

function analyzeCommand(command: string): string | null {
  const { words } = tokenizeShellWords(command);
  if (words.length === 0) return null;

  const execIndex = unwrapLeadingWrappers(words);
  if (execIndex >= words.length) return null;

  const exec = words[execIndex] ?? "";
  const tail = words.slice(execIndex);
  const base = basename(exec);

  if (base === "rm") return analyzeRm(tail);
  if (base === "git") return analyzeGit(tail);

  return null;
}

export const GitSafetyGuard: Plugin = async () => {
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool !== "bash") return;

      const command = getBashCommand(output);
      if (!command) return;

      const reason = analyzeCommand(command);
      if (reason) throw makeBlockedError(command, reason);
    },
  };
};
