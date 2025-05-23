Code to pull the Jane Street Puzzles dataset:

https://huggingface.co/datasets/davidheineman/jane-street-puzzles

*Also working on IBM's Ponder This!*

### Setup

```sh
pip install -r requirements.txt
python src/scrape_jane_street.py # will create data/jane_street folder
python src/scrape_ibm.py # will create data/ibm folder
python src/extract_answer.py # will create answers.json
python src/convert_to_hf.py # will create staged/ folder
```

### About

**What are these puzzles?** Puzzles are a great way to obfuscate math, code and stats. See the [current puzzle](https://www.janestreet.com/puzzles/current-puzzle/) for Jane Street.

**Why this capability?** The first post of [Ponder This](https://research.ibm.com/haifa/ponderthis/challenges/May1998.html) in May 1998 summarizes the goal of these puzzles quite well:

> Here's what happened... Business Week recently ran an item about a "little book of big ideas" we published for the people here at IBM Research. "Sort of like the Tao for people who think about computers all day," they wrote. Seemed harmless enough. The story highlighted some of the simple things our researchers do to get a new perspective on things, ending with this one:
> 
> If a belt were placed around the Earth's equator, and then had six meters of length added to it, and you grabbed it at a point and lifted it until all the slack was gone, how high above Earth's surface would you be?
> 
> In retrospect, the example should have carried a warning: For professional mathematicians only. Don't try this at home. Nonetheless, many readers were game. ("I lost the entire weekend," lamented Jan from the Bay Area.) Dozens of answers were submitted. All but one were wrong. (For what it's worth, Jan got it right.) Most interesting, though, were the different approaches people used to try and solve the problem.
> 
> One person imagined a triangle sitting tangent to the earth at its base (Hint: wrong triangle, wrong tangent point).
> 
> Another tried to establish an upper limit on the height based on assuming an earth-radius of zero, then working back from that, declaring that the height must be less than 3.1416--the truncated value of pi. (Hint: try that and you'll be off by several orders of magnitude.)
> 
> Overall, though, most attempts couldn't get past the barrier of "common sense"-- if only six meters of length were added to a taut belt, wouldn't the height attained by lifting "up" on the belt have to be less than six meters, or in some way related to that limiting number? (Hint: it's not.)
> 
> **Which is precisely why we posited the problem in the first place.** Sometimes our most fundamental assumptions are wrong. Often, in the process of solving a seemingly unrelated problem, preexisting biases and limits to creative thinking are exposed. When that happens, the mind can open up to new ideas -- and when you're a researcher that's a good thing.

The Jane Street puzzles resemble *Ponder This* quite closely, so this repo contains a scraper for both problem sets.

### TODO

- [ ] Extraction for IBM, split by '\n---\n'

- [ ] Improve answer extraction
- [ ] Scrape the index page for Jane Street
- [ ] Add image previews to dataset

- [ ] Fix image names: `[![](/puzzles/1.png)](/puzzles/1.png)` to `[IMG_1]`
- [ ] Create a dev split of 5 Qs
- [ ] Create a text-only split
- [ ] Some explanations have PII