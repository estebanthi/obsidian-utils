# obsidian-utils

Obsidian-utils is a little app I use to automate some tasks in my Obsidian vault.


## Configuration
Create a `config.yaml` file in the root of the repo. It should contain the following:
```yaml
vault_path: /path/to/your/vault
```

To change the default logging configuration ('INFO'), just add a `logging_level` key to the config file:
```yaml
vault_path: /path/to/your/vault
logging_level: DEBUG
```

## Usage

```python
python app.py --help
```