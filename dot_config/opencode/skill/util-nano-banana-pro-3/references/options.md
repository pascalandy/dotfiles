# Options Reference

## All Flags

| Flag                | Short | Description                                            |
| ------------------- | ----- | ------------------------------------------------------ |
| `--prompt`          | `-p`  | Image description or editing instructions (required)   |
| `--filename`        | `-f`  | Output filename (default: timestamped)                 |
| `--input-image`     | `-i`  | Input image path(s) for editing/composition (up to 14) |
| `--size`            | `-s`  | Image size: 1K (default), 2K, or 4K                    |
| `--aspect-ratio`    | `-a`  | Aspect ratio (see below)                               |
| `--seed`            |       | Seed for reproducible results                          |
| `--dry-run`         | `-n`  | Show what would be done without API call               |
| `--verbose`         | `-v`  | Debug output with API request/response details         |
| `--nbr-img-output`  | `-c`  | Number of images to generate (1-4, default: 1)         |
| `--format`          | `-F`  | Output format: png, jpeg (default: png)                |
| `--thinking`        | `-t`  | Thinking mode: low, medium, high                       |
| `--negative-prompt` | `-N`  | What to avoid in generation                            |
| `--safety`          |       | Safety filter: off, low, medium, high                  |
| `--output-dir`      | `-o`  | Output directory (default: ./EXPORT)                   |
| `--open-after`      |       | Open image(s) after generation (cross-platform)        |
| `--quiet`           | `-q`  | Suppress non-essential output (only show file paths)   |
| `--timeout`         |       | API request timeout in seconds (default: 120)          |
| `--version`         | `-V`  | Show version and exit                                  |
| `--no-color`        |       | Disable colored output (respects NO_COLOR env var)     |

## Image Sizes

- **1K** - Standard resolution (~1024px) - default
- **2K** - Higher resolution (~2048px)
- **4K** - Highest resolution (~4096px)

## Aspect Ratios

| Ratio  | Dimensions          |
| ------ | ------------------- |
| `1:1`  | 1024x1024 (default) |
| `2:3`  | 832x1248            |
| `3:2`  | 1248x832            |
| `3:4`  | 864x1184            |
| `4:3`  | 1184x864            |
| `4:5`  | 896x1152            |
| `5:4`  | 1152x896            |
| `9:16` | 768x1344            |
| `16:9` | 1344x768            |
| `21:9` | 1536x672            |

## Output Streams

The script separates output streams for composability:

- **stdout**: File paths only (safe for piping)
- **stderr**: Progress, debug info, errors, warnings

Capture paths while seeing progress:

```bash
paths=$(gen_image.py --prompt "Test" 2>/dev/null)

# Or with quiet mode
paths=$(gen_image.py --prompt "Test" --quiet)
```

## Filename Generation

Default: `yyyy-mm-dd-hh-mm-ss-generated.png`

Recommended pattern: `{timestamp}-{descriptive-name}.png`

- `2025-12-23-14-23-05-japanese-garden.png`
- `2025-12-23-15-30-12-sunset-mountains.png`
