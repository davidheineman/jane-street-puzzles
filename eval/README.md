Based on https://github.com/centerforaisafety/hle

## Simple Evaluation
We provide a simple evaluation, using the `openai-python` interface. Set `num_workers` and `max_completion_tokens`. Our evaluation uses the maximum number of tokens available, but we observed some model collapse. We do not recommend setting max completion tokens below `32768` for reasoning models.

`temperature` is defaulted to `0` for our evaluation.

```sh
pip install -r requirements.txt
```

```sh
cd eval

MODEL="o4-mini-2025-04-16"
DATASET="davidheineman/jane-street-puzzles"
python run_model_predictions.py --dataset ${DATASET} --model ${MODEL} --max_completion_tokens 32768 --num_workers 100 # --max_samples 3 to test model
python run_judge_results.py --dataset ${DATASET} --predictions jane_street_${MODEL}.json --num_workers 100 # run judge
```

Sample output (on `o4-mini-2025-04-16`)
```sh
*** Metrics ***
Accuracy: 4.17% +/- 3.58% | n = 120
Calibration Error: 0.0
```
