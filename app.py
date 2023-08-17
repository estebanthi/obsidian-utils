import click
from termcolor import colored
import random

from src.api import Api
api = Api(config_path='config.yaml')


@click.group
def cli():
    pass


def validate_path(ctx, param, value):
    if value is None:
        return None
    if not api.fs_api.path_is_in_vault(value):
        raise click.BadParameter(f"Path {value} is not in vault")
    if param.name == 'directory':
        if not api.fs_api.isdir(value):
            raise click.BadParameter(f"{value} is not a directory")
    if param.name == 'file':
        if not api.fs_api.isfile(value):
            raise click.BadParameter(f"{value} is not a file")
    return value


@cli.command(help="Compare existing backlinks with backlinks not created")
@click.argument('directory', type=str, required=False, default='./', callback=validate_path)
@click.option('-c', '--cutoff', type=click.FloatRange(0, 1), default=0.7, help="Cutoff value, 0 matching everything, and 1 matching only exact backlinks", show_default=True)
@click.option('-r', '--replace', is_flag=True, default=False, help="Ask user to replace backlinks")
def match_backlinks(directory, cutoff, replace):
    matches = api.backlinks_api.match_backlinks(directory, cutoff)
    for not_existing_backlink, existing_backlink in matches:
        if not replace:
            print(colored(not_existing_backlink, 'red'), '->', colored(existing_backlink, 'green'))
        if replace:
            rep = input(f"{colored(not_existing_backlink, 'red')} -> {colored(existing_backlink, 'green')} [y/N]")
            if rep == 'y':
                backlink_regex = rf"\[\[{not_existing_backlink}\]\]"
                api.fs_api.replace_in_dir(directory, backlink_regex, existing_backlink, recursive=True)


@cli.command(help="Find backlinks in vault")
@click.argument('path', type=str, required=False, default='./', callback=validate_path)
@click.option('--existing/--no-existing', default=None, help="To find only existing/not existing backlinks")
def find_backlinks(path, existing):
    backlinks = api.backlinks_api.get_backlinks(path, existing)
    print('\n'.join(backlinks))
    print(colored(f"Found {len(backlinks)} backlinks", 'yellow'))


@cli.command(help="Replace a regex in files")
@click.argument('regex', type=str)
@click.argument('new', type=str)
@click.argument('path', type=str, required=False, default='./', callback=validate_path)
@click.option('-r', '--recursive', is_flag=True, default=False, help="Browse directories recursively", show_default=True)
@click.confirmation_option(prompt="Are you sure you want to replace files in your vault?")
def replace(path, regex, new, recursive):
    api.fs_api.replace_in_dir(path, regex, new, recursive=recursive)


@cli.command(help="Remove tags from files")
@click.argument('directory', type=str, required=False, default='./', callback=validate_path)
@click.option('-t', '--tag', 'tags', type=str, multiple=True)
@click.option('-r', '--recursive', is_flag=True, default=False, help="Browse directories recursively", show_default=True)
def remove_tags(directory, tags, recursive):
    files = api.fs_api.listdir(directory, recursive=recursive)
    for file in files:
        yaml_frontmatter = api.frontmatter_api.get_yaml_frontmatter(file)
        if 'tags' in yaml_frontmatter:
            tags_in_yaml = yaml_frontmatter['tags']
            for tag in tags:
                if tag in tags_in_yaml:
                    tags_in_yaml.remove(tag)
            api.frontmatter_api.update_yaml_frontmatter(file, 'tags', tags_in_yaml)


@cli.command(help="Add tags to files")
@click.argument('directory', type=str, required=False, default='./', callback=validate_path)
@click.option('-t', '--tag', 'tags', type=str, multiple=True)
@click.option('-r', '--recursive', is_flag=True, default=False, help="Browse directories recursively", show_default=True)
@click.option('-n', '--number', type=int, default=None, help="Add tags to n random files")
def add_tags(directory, tags, recursive, number):
    files = api.fs_api.listdir(directory, recursive=recursive)
    if number is not None:
        files = random.sample(files, number)
    for file in files:
        yaml_frontmatter = api.frontmatter_api.get_yaml_frontmatter(file)
        if 'tags' in yaml_frontmatter:
            tags_in_yaml = yaml_frontmatter['tags']
            for tag in tags:
                if tag not in tags_in_yaml:
                    tags_in_yaml.append(tag)
            api.frontmatter_api.update_yaml_frontmatter(file, 'tags', tags_in_yaml)
        else:
            api.frontmatter_api.update_yaml_frontmatter(file, 'tags', tags)


if __name__ == '__main__':
    cli()
