#!/usr/bin/env python3
import json

def update_final_descriptions():
    """Update the JSON with descriptions for remaining images 36-42"""
    
    # Load the current accurate descriptions
    with open('image_descriptions_accurate.json', 'r') as f:
        data = json.load(f)
    
    # Add descriptions for remaining images (all without Iron Man)
    additional_descriptions = {
        'futuristic_city_36.png': {
            'content': 'A blonde woman in an elegant black dress standing on the steps of the ancient Greek Parthenon in Athens with classical columns. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'ancient Greek Parthenon in Athens',
            'has_iron_man': False
        },
        'futuristic_city_37.png': {
            'content': 'A blonde woman in an elegant black dress standing in front of a modern government building or parliament with contemporary architecture. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'modern government building or parliament',
            'has_iron_man': False
        },
        'futuristic_city_38.png': {
            'content': 'A blonde woman in an elegant black dress standing on a frozen outdoor ice rink in winter with people ice skating and city skyline in the background. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'frozen outdoor ice rink in winter with city skyline',
            'has_iron_man': False
        },
        'futuristic_city_39.png': {
            'content': 'A blonde woman in an elegant black dress sitting on grass in front of a large white government building or palace with classical columns and green hills. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'white government building or palace with classical columns',
            'has_iron_man': False
        },
        'futuristic_city_40.png': {
            'content': 'A blonde woman in an elegant black dress standing in a traditional Nepalese or Tibetan temple courtyard with multi-tiered pagoda architecture and people around. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'traditional Nepalese or Tibetan temple courtyard with pagoda architecture',
            'has_iron_man': False
        },
        'futuristic_city_41.png': {
            'content': 'A blonde woman in an elegant black dress standing in front of a grand government building or presidential palace with modern architecture, columns, and flags. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'grand government building or presidential palace with flags',
            'has_iron_man': False
        },
        'futuristic_city_42.png': {
            'content': 'A blonde woman in an elegant black dress sitting on a bench in formal palace gardens with manicured landscaping and a grand palace building in the background. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'formal palace gardens with grand palace building',
            'has_iron_man': False
        }
    }
    
    # Add the new descriptions to the data structure
    for filename, desc in additional_descriptions.items():
        image_data = {
            'filename': filename,
            'content': desc['content'],
            'characters': desc['characters'],
            'setting': desc['setting'],
            'has_iron_man': desc['has_iron_man'],
            'style': 'cinematic, professional photography'
        }
        
        data['all_images'].append(image_data)
        data['categories']['without_iron_man'].append(image_data)
    
    # Update summary counts
    data['summary']['total_images'] = len(data['all_images'])
    data['summary']['images_without_iron_man'] = len(data['categories']['without_iron_man'])
    
    # Save the updated file
    with open('image_descriptions_accurate.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Updated final descriptions. Total images: {data['summary']['total_images']}")
    print(f"- Images with Iron Man: {data['summary']['images_with_iron_man']}")
    print(f"- Images without Iron Man: {data['summary']['images_without_iron_man']}")

if __name__ == "__main__":
    update_final_descriptions()