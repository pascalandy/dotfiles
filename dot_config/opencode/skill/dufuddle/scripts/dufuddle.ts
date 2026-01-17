#!/usr/bin/env bun
import { JSDOM } from "jsdom";
import { Defuddle } from "./node_modules/defuddle/src/node";

const enableColors = process.stdout.isTTY;

const colors = {
  reset: enableColors ? "\x1b[0m" : "",
  bold: enableColors ? "\x1b[1m" : "",
  green: enableColors ? "\x1b[32m" : "",
  red: enableColors ? "\x1b[31m" : "",
  blue: enableColors ? "\x1b[34m" : "",
  yellow: enableColors ? "\x1b[33m" : "",
  dim: enableColors ? "\x1b[2m" : "",
};

/**
 * Displays the help message
 */
function showHelp() {
  console.log(`
${colors.bold}${colors.blue}Defuddle CLI Wrapper${colors.reset}
Extract clean content and metadata from any web page.

${colors.bold}Usage:${colors.reset}
  bun run dufuddle.ts [options] <URL>

${colors.bold}Options:${colors.reset}
  --help        Show this help message
  --dry-run     Verify the URL is reachable without parsing content
  --content     Output only the markdown content (clean export)
  --json        Output the full result as JSON
  --timeout <ms> Set request timeout (default: 10000ms)

${colors.bold}Examples:${colors.reset}
  bun run dufuddle.ts https://simonwillison.net/2025/Dec/22/claude-chrome-cloudflare/
  bun run dufuddle.ts --dry-run URL
  bun run dufuddle.ts --content URL
  bun run dufuddle.ts --json URL
`);
}

async function main() {
  const args = Bun.argv.slice(2);

  // Improved argument parsing
  const flags = args.filter((arg) => arg.startsWith("-"));
  const positional = args.filter((arg) => !arg.startsWith("-"));

  // Default to help if no arguments or help flag
  if (args.length === 0 || flags.includes("--help") || flags.includes("-h")) {
    showHelp();
    return;
  }

  const isDryRun = flags.includes("--dry-run");
  const isJson = flags.includes("--json");
  const isContent = flags.includes("--content") || !process.stdout.isTTY;
  const timeoutArgIndex = args.indexOf("--timeout");
  const timeout = timeoutArgIndex !== -1 ? parseInt(args[timeoutArgIndex + 1] || "10000") : 10000;

  // Take the first positional argument as the URL
  const url = positional[0];

  if (!url || !url.startsWith("http")) {
    console.error(`${colors.red}Error: No valid URL provided.${colors.reset}`);
    showHelp();
    process.exit(1);
  }

  // Custom User-Agent to avoid being blocked by some sites
  const headers = {
    "User-Agent":
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  };

  try {
    if (isDryRun) {
      console.log(`${colors.dim}[Dry Run] Checking accessibility for: ${url}${colors.reset}`);
      const controller = new AbortController();
      const id = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(url, {
        method: "HEAD",
        headers,
        signal: controller.signal,
      });
      clearTimeout(id);

      if (response.ok) {
        console.log(
          `${colors.green}✅ URL is reachable (Status: ${response.status})${colors.reset}`,
        );
      } else {
        console.error(
          `${colors.red}❌ URL returned an error (Status: ${response.status})${colors.reset}`,
        );
      }
      return;
    }

    if (!isJson && !isContent)
      console.log(`${colors.dim}Fetching and parsing: ${url}...${colors.reset}`);

    // Fetch HTML manually to apply headers and timeout
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);

    const response = await fetch(url, {
      headers,
      signal: controller.signal,
    });
    clearTimeout(id);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const html = await response.text();
    const dom = new JSDOM(html, { url });

    const result = await Defuddle(dom, url, { markdown: true });

    if (isJson) {
      console.log(JSON.stringify(result, null, 2));
    } else if (isContent) {
      console.log(result.content || "");
    } else {
      console.log(`\n${colors.bold}${colors.blue}--- TITLE ---${colors.reset}`);
      console.log(result.title || "No title found");

      console.log(`\n${colors.bold}${colors.blue}--- CONTENT (Markdown) ---${colors.reset}`);
      console.log(result.content || "No content extracted");

      console.log(`\n${colors.bold}${colors.blue}--- METADATA ---${colors.reset}`);
      console.log(
        JSON.stringify(
          {
            author: result.author,
            published: result.published,
            site: result.site,
            wordCount: result.wordCount,
            domain: result.domain,
          },
          null,
          2,
        ),
      );
    }
  } catch (error: any) {
    const message = error.name === "AbortError" ? "Request timed out" : error.message;
    console.error(`\n${colors.red}❌ Error: ${message}${colors.reset}`);
    process.exit(1);
  }
}

main();
