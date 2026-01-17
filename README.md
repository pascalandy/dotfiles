# Pascal Andy's Dotfiles

My personal dotfiles managed with [chezmoi](https://www.chezmoi.io/).

## Quick Start

1. Install chezmoi and apply:
```bash
chezmoi init https://github.com/pascalandy/dotfiles.git
chezmoi apply
```

2. Create `~/.config/chezmoi/chezmoi.toml` with your secrets (see below).

3. Re-apply to inject secrets:
```bash
chezmoi apply
```

## Required Template Variables

Create `~/.config/chezmoi/chezmoi.toml` with these variables:

```toml
[data]
# API Keys (required for opencode.json)
exa_api_key = "your-exa-api-key"
openrouter_api_key = "sk-or-v1-your-key"
context7_api_key = "your-context7-key"

# SSH Config (required for ~/.ssh/config)
ssh_host_1 = "your-server-1.example.com"
ssh_host_2 = "your-server-2.example.com"
ssh_user_2 = "your-username"
```

Get your API keys:
- Exa: https://exa.ai/
- OpenRouter: https://openrouter.ai/keys
- Context7: https://context7.com/

## What's Included

- Shell config (`.zshrc`, `.p10k.zsh`)
- Git config (`.gitconfig`)
- SSH config (templated)
- VS Code settings
- CLI tool configs (opencode, amp, zed)
- Custom scripts in `~/.local/bin/`
- AI agent skills and prompts

---

## Notes

For context:

Chez Moi manages dotfiles by storing desired state in `~/.local/share/chezmoi` and syncing (it copies, not symlink them to home on `chezmoi apply`.

## Add Files

- Add files: `chezmoi add ~/.file` (e.g., `~/.bashrc`, `~/.zshrc`).
- Edit: `vs ~/./file.txt`
	- [[alias]] `cfgoc`, `cfgzsh`
- Apply: `chezmoi apply`
- Commit: `chezmoi cd && git add . && git commit -m "msg" && git push`
	- via [[opencode]]
	- my repo: https://github.com/pascalandy/dotfiles
	- I have `gh` installed as well

## Templates for Secrets

- For files with keys (e.g., opencode.json): Replace key with `{{ .secret_name }}`.
- Add: `chezmoi add ~/.file`.
- Create `~/.config/chezmoi/chezmoi.toml` with `[data] secret_name = "value"`.
- Apply: `chezmoi apply` renders template

ERREUR : La variable template est littéralement dans le fichier final au lieu de la vraie clé API. C'est pour ça que l'authentification échoue.

````md
# Diagnostic et résolution : Erreur "No cookie auth credentials found" dans opencode

  ## Contexte
  L'utilisateur rencontrait une erreur avec l'agent Flash-3 (Google Gemini) dans opencode :
  No cookie auth credentials found

  ## Investigation

  ### Étape 1 : Analyse de config.json
  - Problème mineur trouvé : virgule superflue ligne 111 (JSON invalide)
  - Corrigé immédiatement

  ### Étape 2 : Analyse de opencode.json
  Configuration du provider OpenRouter :
  
  ```json
  "apiKey": "{{ .openrouter_api_key }}"
  → Variable template chezmoi présente
  ```
  
  Étape 3 : Vérification du fichier déployé (~/.config/opencode/opencode.json)

  Découverte clé : La variable template était présente LITTÉRALEMENT dans le fichier final :
  "apiKey": "{{ .openrouter_api_key }}"
  au lieu de la vraie clé API.

  Cause racine

  Le fichier source chezmoi était nommé opencode.json au lieu de opencode.json.tmpl.

  Conséquence : Chezmoi copie le fichier tel quel sans traiter les templates.

  Solution appliquée

  1. Renommer le fichier source

  mv opencode.json opencode.json.tmpl

  2. Définir la variable manquante

  Ajout dans ~/.config/chezmoi/chezmoi.toml :
  [data]
  openrouter_api_key = "sk-or-v1-..."

  3. Réappliquer la configuration

  chezmoi apply

  Résultat

  La clé API OpenRouter est maintenant correctement injectée dans le fichier final.
  L'agent Flash-3 fonctionne.

  Leçon retenue

  Tout fichier chezmoi contenant des variables {{ }} doit avoir l'extension .tmpl
  pour que le moteur de template les traite.
````

- [ ] Gérer les secrets chiffré avec [[Bitwarden]] #tsk/perso ➕ 2025-12-18

## 5a Scripts

- Types: `run_once_` (first apply), `run_after` (every apply).
- Create in `~/.local/share/chezmoi/`: `run_after_name.sh` with bash commands.
- Make executable: `chmod +x file.sh`.
- Commit like files.
- Use: Automate tasks (e.g., brew dump, backups).
- Wrong assumption: Scripts modify managed files cause errors; use carefully.

### 5b Brewfile Backup

- Dump: `brew bundle dump --file ~/.Brewfile --force`.
- Add: `chezmoi add ~/.Brewfile`.
- Auto-update: `run_after` script with dump (but may cause conflicts).
- Manual: Dump after installs, add, apply, commit.

> Donc ici, j'ai effectivement utilisé un script pour faire un backup automatique de mes BlueFiles.

### 5c Custom Backup (e.g., tree_my_docs.txt)

Backup via script: `run_after`
- `~/.local/share/chezmoi/run_after_backup-tree.sh`

To add a directory to chezmoi management, use chezmoi add `path`. For paths outside ~/, manual copying like this may be necessary.

[[2025-12-18]] dans ce script, je backup ce fichier qui n'est pas encore important. Je voulais vraiment tester le workflow auparavant.

````shell
#!/bin/bash
# Backup tree file to repo
cp ~/Documents/_my_docs/42_tree_of_my_dir_files/z_archive/tree_my_docs.txt ~/.local/share/chezmoi/backup_tree_my_docs.txt
````

### 5d External Files

- Manage outside ~: `chezmoi add /path/to/file` (stored as encoded flat file).
- Edit: `chezmoi edit /path/to/file`.
- If changes often: Use script to copy to repo (e.g., `run_after` cp to backup).
- Wrong assumption: Paths stay as tree; they're encoded for flat repo.

## 🚨 CRASH RECOVERY

> **Emergency procedures**: See [[crash_procedure.md]] for crash recovery guide

## Official Docs

These above are MY notes. But the truth is here: https://www.chezmoi.io/user-guide/command-overview/

END
