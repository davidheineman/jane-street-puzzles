import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def replace_puzzle_images(puzzle):
    """ Replace image names with 0.png, 1.png, ... """
    image_map = {}
    next_num = 0
    
    # Process puzzle content
    content = puzzle['puzzle_content']
    i = 0
    while i < len(content):
        if '/puzzles/' in content[i:] and '.png' in content[i:]:
            start = content.find('/puzzles/', i)
            end = content.find('.png', start) + 4
            original = content[start:end]
            
            if original not in image_map:
                image_map[original] = f'/puzzles/{next_num}.png'
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
        if '/puzzles/' in content[i:] and '.png' in content[i:]:
            start = content.find('/puzzles/', i)
            end = content.find('.png', start) + 4
            original = content[start:end]
            
            if original not in image_map:
                image_map[original] = f'/puzzles/{next_num}.png'
                next_num += 1
                
            replacement = image_map[original]
            content = content[:start] + replacement + content[end:]
            i = start + len(replacement) # Move i past the replacement
        else:
            i += 1
            
    puzzle['solution_content'] = content
    return puzzle
