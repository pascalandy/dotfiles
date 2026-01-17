#!/usr/bin/env bun
import * as path from "path";
import { pathToFileURL } from "url";

type PluginInitInput = {
  client: unknown;
  project: unknown;
  worktree: unknown;
  directory: string;
  $: unknown;
};

const cwd = process.cwd();
const pluginGlob = new Bun.Glob(".opencode/plugin/*.{ts,js}");

const pluginFiles: string[] = [];
for await (const filePath of pluginGlob.scan({
  absolute: true,
  cwd,
  dot: true,
  followSymlinks: true,
})) {
  pluginFiles.push(filePath);
}
pluginFiles.sort();

const errors: string[] = [];

const pluginInitInput: PluginInitInput = {
  client: {},
  project: {},
  worktree: {},
  directory: cwd,
  $: () => {},
};

for (const absoluteFilePath of pluginFiles) {
  const relativeFilePath = path.relative(cwd, absoluteFilePath);
  const mod = await import(pathToFileURL(absoluteFilePath).href);

  for (const [exportName, exportedValue] of Object.entries(mod)) {
    if (typeof exportedValue !== "function") {
      const typeLabel = Array.isArray(exportedValue) ? "array" : typeof exportedValue;
      errors.push(`${relativeFilePath} export ${exportName} is ${typeLabel}, expected function`);
      continue;
    }

    try {
      const initResult = await exportedValue(pluginInitInput);
      if (!initResult || typeof initResult !== "object") {
        const typeLabel = initResult === null ? "null" : typeof initResult;
        errors.push(
          `${relativeFilePath} export ${exportName} returned ${typeLabel}, expected hook object`,
        );
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      errors.push(`${relativeFilePath} export ${exportName} threw: ${message}`);
    }
  }
}

if (errors.length > 0) {
  console.error("Invalid OpenCode plugins detected:");
  for (const err of errors) console.error(`- ${err}`);
  process.exit(1);
}

console.log(`OK: ${pluginFiles.length} plugin file(s)`);
