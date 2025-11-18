## Sys Deadlines

Countdown timers to keep track of a bunch of systems conference deadlines, that aligns with a small group's interests.

## Agent for deadline

### Steps

```bash
# install uv
# clone sys-deadlines
cd agent
uv sync
touch .env
# paste OPENAI_API_KEY inside .env
```

### Example

```bash
uv run extract.py -u <url-of-cfp-page>
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

Paste this to `_data/conferences.yml`


## Contributing

Contributions are very welcome!

To keep things minimal, I am only looking at SOSP, OSDI, FAST, NSDI, EuroSys, ASPLOS and, MLSys.

To add or update a deadline:
- Fork the repository
- Update `_data/conferences.yml`
- Make sure it has the `title`, `year`, `id`, `link`, `deadline`, `timezone`, `date`, `place`, `sub` attributes
    + See available timezone strings [here](https://momentjs.com/timezone/).
- Optionally add a `note` and `abstract_deadline` in case the conference has a separate mandatory abstract deadline
- Optionally add `hindex` (refers to h5-index from [here](https://scholar.google.com/citations?view_op=top_venues&vq=eng))
- Example:
    ```yaml
    - title: BestConf
      year: 2022
      id: bestconf22  # title as lower case + last two digits of year
      full_name: Best Conference for Anything  # full conference name
      link: link-to-website.com
      deadline: YYYY-MM-DD HH:SS
      abstract_deadline: YYYY-MM-DD HH:SS
      timezone: Asia/Seoul
      place: Incheon, South Korea
      date: September, 18-22, 2022
      start: YYYY-MM-DD
      end: YYYY-MM-DD
      paperslink: link-to-full-paper-list.com
      pwclink: link-to-papers-with-code.com
      hindex: 100.0
      sub: SP
      note: Important
    ```
- Send a pull request

# Development

Run `podman.sh` and visit `http://localhost:4000/sys-deadlines/`
