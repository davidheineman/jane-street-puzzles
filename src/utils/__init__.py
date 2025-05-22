import os

DATA_DIR_JS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'jane_street')
DATA_DIR_IBM = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'ibm')

def save_puzzle_data(puzzle_data, data_dir):
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(os.path.join(data_dir, "problem"), exist_ok=True)
    os.makedirs(os.path.join(data_dir, "solution"), exist_ok=True)

    # Save each puzzle and solution to separate files
    for puzzle in puzzle_data:
        puzzle_name = puzzle['puzzle_name']
        
        # Save puzzle content
        puzzle_path = os.path.join(data_dir, "problem", f"{puzzle_name}.md")
        with open(puzzle_path, 'w', encoding='utf-8') as f:
            f.write(puzzle['puzzle_content'])
            
        # Save solution content
        solution_path = os.path.join(data_dir, "solution", f"{puzzle_name}.md")
        with open(solution_path, 'w', encoding='utf-8') as f:
            f.write(puzzle['solution_content'])

def replace_puzzle_images(puzzle):
    """ Replace image names with 0.png, 1.png, ... """
    image_map = {}
    next_num = 0
    
    # Process puzzle content
    content = puzzle['puzzle_content']
    i = 0
    while i < len(content):
        # Check for any image extension
        extensions = ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']
        has_image = any(ext in content[i:] for ext in extensions)
        
        if '/puzzles/' in content[i:] and has_image:
            start = content.find('/puzzles/', i)
            
            # Find the end by looking for any of the extensions
            end = -1
            for ext in extensions:
                pos = content.find(ext, start)
                if pos != -1 and (end == -1 or pos < end):
                    end = pos + len(ext)
                    
            original = content[start:end]
            
            if original not in image_map:
                image_map[original] = f'/puzzles/{next_num}.jpg'
                next_num += 1
                
            replacement = image_map[original]
            content = content[:start] + replacement + content[end:]
            i = start + len(replacement) # Move i past the replacement
        else:
            i += 1
            
    puzzle['puzzle_content'] = content
    
    # Process solution content 
    content = puzzle['solution_content']
    i = 0
    while i < len(content):
        # Check for any image extension
        extensions = ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']
        has_image = any(ext in content[i:] for ext in extensions)
        
        if '/puzzles/' in content[i:] and has_image:
            start = content.find('/puzzles/', i)
            
            # Find the end by looking for any of the extensions
            end = -1
            for ext in extensions:
                pos = content.find(ext, start)
                if pos != -1 and (end == -1 or pos < end):
                    end = pos + len(ext)
                    
            original = content[start:end]
            
            if original not in image_map:
                image_map[original] = f'/puzzles/{next_num}.jpg'
                next_num += 1
                
            replacement = image_map[original]
            content = content[:start] + replacement + content[end:]
            i = start + len(replacement) # Move i past the replacement
        else:
            i += 1
            
    puzzle['solution_content'] = content
    return puzzle
