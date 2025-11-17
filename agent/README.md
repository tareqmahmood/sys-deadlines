# Agent for `sys-deadline` extraction

## Steps

```bash
# install uv
# clone sys-deadlines
cd agent
uv sync
touch .env
# paste OPENAI_API_KEY inside .env
```

## Example

```bash
uv run main.py -u <url-of-cfp-page>
```


Sample input:

```bash
uv run main.py -u "https://icml.cc/Conferences/2026/CallForPapers"
```

Sample output:

```yml
- title: ICML
  year: 2026
  id: icml-2026
  link: https://icml.cc/Conferences/2026/CallForPapers
  deadline: 2026-01-29 12:00:00
  abstract_deadline: 2026-01-24 12:00:00
  timezone: UTC+0
  place: Seoul, South Korea
  date: July 7-12, 2026
  start: 2026-07-07
  end: 2026-07-12
  sub: ML
```

Paste this to `sys-deadlines/_data/conferences.yml`
