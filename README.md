# ObsidianRefactorizer

ObsidianRefactorizer is a repo where I collect my scripts to interact with Obsidian.

**Feel free to add yours by opening a PR!**


## Table of contents    
- [Tags](#tags)
  - [add_tag_to_random_notes](#add_tag_to_random_notes)
  - [remove_tag_from_random_notes](#remove_tag)

- [General](#general)
  - [quick_replace](#quick_replace)

## Configuration
Create a `config.yaml` file in the root of the repo. It should contain the following:
```yaml
vault_path: /path/to/your/vault
```

## General

### quick_replace
Replaces a regex in all notes in a specified folder.

**Args**:
- `--path`: Path to the folder where the notes are located (relative to the vault path).
- `--regex`: Regex to replace.
- `--new`: New string to replace the regex with.

**Example**:
```bash
python quick_replace.py --path "my_notes" --regex "myregex" --new "mynewstring"
```

## Tags

### add_tag_to_random_notes
Adds a tag to n random notes in a specified folder.

**Args**:
- `--path`: Path to the folder where the notes are located (relative to the vault path).
- `--n`: Number of notes to add the tag to.
- `--tag`: Tag to add to the notes.

**Example**:
```bash
python add_tag_to_random_notes.py --path "my_notes" --n 10 --tag "mytag"
```

### remove_tag
Removes a tag from all notes in a specified folder.

**Args**:
- `--path`: Path to the folder where the notes are located (relative to the vault path).
- `--tag`: Tag to remove from the notes.

**Example**:
```bash
python remove_tag.py --path "my_notes" --tag "mytag"
```
