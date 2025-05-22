Code to pull the Jane Street Puzzles dataset:

https://huggingface.co/datasets/davidheineman/jane-street-puzzles

```sh
pip install -r requirements.txt
python src/scrape_jane_street.py # will create data/ folder
python src/extract_answer.py # will create answers.json
python src/convert_to_hf.py # will create staged/ folder
```

### TODO

[ ] Improve answer extraction
[ ] Scrape the index page

[ ] Fix image names: `[![](/puzzles/1.png)](/puzzles/1.png)` to `[IMG_1]`
[ ] Create a dev split of 5 Qs
[ ] Create a text-only split
[ ] Some explanations have PII