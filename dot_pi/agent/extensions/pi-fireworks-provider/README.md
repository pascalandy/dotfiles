# pi-fireworks-provider

A [pi](https://github.com/marioechr/pi) extension that registers [Fireworks AI](https://fireworks.ai/) as a custom provider for **Kimi models only**.

## Features

- **Kimi K2.5 Turbo** - Fast, efficient with vision support
- **Kimi K2 Thinking** - Extended reasoning capabilities  
- **Kimi K2 Instruct** - Standard instruction following
- **Cost Tracking** with per-model pricing
- **Vision Support** for K2.5 (text + image input)

## Installation

This extension is located at `~/.pi/agent/extensions/pi-fireworks-provider/` and is automatically loaded by pi.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FIREWORKS_API_KEY` | Yes | Your Fireworks AI API key |

## Usage

1. Set your Fireworks API key:
   ```bash
   export FIREWORKS_API_KEY=your-api-key-here
   ```

2. Run pi and use the `/model` command:
   ```
   /model
   ```

3. Select "fireworks" as the provider and choose a Kimi model.

## Available Models

| Model | Type | Context | Max Tokens | Input Cost | Output Cost |
|-------|------|---------|------------|------------|-------------|
| Kimi K2.5 Turbo | Text + Image | 256K | 16K | $0.60 | $3.00 |
| Kimi K2 Thinking | Text | 256K | 256K | $0.60 | $2.50 |
| Kimi K2 Instruct | Text | 128K | 16K | $1.00 | $3.00 |

*Costs are per million tokens. Prices subject to change - check [fireworks.ai](https://fireworks.ai) for current pricing.*

## License

MIT
