import re
import difflib


class BacklinksApi:

    def __init__(self, fs_api):
        self._fs_api = fs_api

    def get_backlinks(self, dir, existing=None):
        dir = self._fs_api.format_path(dir)

        backlinks_regex = r'\[\[([\w\d\s-]*)\|?\w*\]\]'
        backlinks = []
        for file in self._fs_api.listdir(dir, recursive=True):
            if file.endswith('.md'):
                content = self._fs_api.read_file(file)
                backlinks += re.findall(backlinks_regex, content)

        backlinks = list(set(backlinks))

        if existing:
            created_backlinks = [file.split('/')[-1].split('.')[0] for file in self._fs_api.listdir(dir, recursive=True) if file.endswith('.md')]
            backlinks = [backlink for backlink in backlinks if backlink in created_backlinks]
        elif existing is False:
            created_backlinks = [file.split('/')[-1].split('.')[0] for file in self._fs_api.listdir(dir, recursive=True) if file.endswith('.md')]
            backlinks = [backlink for backlink in backlinks if backlink not in created_backlinks]

        return backlinks

    def match_backlinks(self, dir, cutoff=0.7):
        dir = self._fs_api.format_path(dir)

        existing_backlinks = self.get_backlinks(dir, existing=True)
        not_existing_backlinks = self.get_backlinks(dir, existing=False)

        matches = []

        for backlink in not_existing_backlinks:
            match = False

            for existing_backlink in existing_backlinks:
                if self.clean_backlink(existing_backlink) == backlink:
                    match = True
                    matches.append((backlink, existing_backlink))

            if not match:
                matches_ = difflib.get_close_matches(backlink, existing_backlinks, n=1, cutoff=cutoff)
                if len(matches_) > 0:
                    matches.append((backlink, matches_[0]))

        return matches

    def clean_backlink(self, backlink):
        return re.sub(r' - \d+$', '', backlink)