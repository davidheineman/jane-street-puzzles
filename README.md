Code to pull the Jane Street Puzzles dataset:

https://huggingface.co/datasets/davidheineman/jane-street-puzzles

```sh
pip install -r requirements.txt
python scrape.py # will create data/ folder
python convert_to_hf.py # will create staged/ folder
```

### TODO

[ ] Answer extraction
[ ] Scrape all pages (and the index page)

[ ] Fix image names: `[![](/puzzles/1.png)](/puzzles/1.png)` to `[IMG_1]`
[ ] Create a dev split of 5 Qs
[ ] Create a text-only split
[ ] Some explanations have PII