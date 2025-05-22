import json
import os
import re
from pathlib import Path
from utils import DATA_DIR
from utils.gpt import openai_init, generate_gpt


EXTRACTION_PROMPT = """Please analyze this puzzle solution text and:
1. First explain where the solution/answer is located in the text
2. Then output just the solution/answer inside [SOLUTION]...[/SOLUTION] tags
If there is no clear single solution/answer, output [SOLUTION]None[/SOLUTION]

Here is the text:
{solution_text}"""


def extract_answers(solution_contents):
    prompts = []
    for solution_content in solution_contents:
        prompts.append(EXTRACTION_PROMPT.format(solution_text=solution_content))

    responses = generate_gpt(prompts)
    
    answers = []
    for response_text in responses:
        # Find solution between tags using regex
        match = re.search(r'\[SOLUTION\](.*?)\[/SOLUTION\]', response_text, re.DOTALL)
        if match:
            answer = match.group(1).strip()
            if answer == "None":
                answer = None
        else:
            answer = None

        answers.append(answer)
        
    return answers


def read_md_file(file_path):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def process_solution_files(data_dir):
    solution_dir = data_dir / "solution"
    
    solution_contents = []
    puzzle_ids = []
    for solution_file in solution_dir.glob("*.md"):
        puzzle_id = solution_file.stem
        
        solution_content = read_md_file(solution_file)
        
        puzzle_ids.append(puzzle_id)
        solution_contents.append(solution_content)
        
    # Extract answer
    answers = extract_answers(solution_contents)
        
    solutions = {}
    for answer, puzzle_id in zip(answers, puzzle_ids):
        if answer:
            solutions[puzzle_id] = answer

    return solutions


if __name__ == '__main__':
    openai_init()
    
    answers = process_solution_files(Path(DATA_DIR))
    
    output_path = Path(DATA_DIR) / "answers.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(answers, f, indent=2)
        
    print(f"Saved {len(answers)} answers to {output_path}")