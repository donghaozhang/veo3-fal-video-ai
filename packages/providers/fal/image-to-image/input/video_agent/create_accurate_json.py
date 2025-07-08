#!/usr/bin/env python3
import json
import os

def create_accurate_descriptions():
    """Create accurate image descriptions based on verification findings"""
    
    # Load original list and remove duplicates
    with open('image_names.json', 'r') as f:
        original_names = json.load(f)
    
    # Remove duplicates (city_10=city_7, city_11=city_8, city_23=city_1)
    duplicates = ['futuristic_city_10.png', 'futuristic_city_11.png', 'futuristic_city_23.png']
    unique_names = [name for name in original_names if name not in duplicates]
    
    # Verified descriptions based on actual image content
    verified_descriptions = {
        'futuristic_city_1.png': {
            'content': 'A blonde woman in an elegant black dress reclining on a white beach chair alongside Iron Man in his iconic red and gold armor suit, set on a tropical beach with turquoise water and luxury resort buildings in the background.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'tropical beach with turquoise water and luxury resort',
            'has_iron_man': True
        },
        'futuristic_city_2.png': {
            'content': 'A blonde woman in an elegant black dress standing alongside Iron Man in his iconic red and gold armor suit, set in front of an ornate golden temple with traditional Southeast Asian architecture.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'ornate golden temple with traditional architecture',
            'has_iron_man': True
        },
        'futuristic_city_3.png': {
            'content': 'A blonde woman in an elegant black dress walking alongside Iron Man flying/hovering in his armor, set in an urban park with monument and green landscaping.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'urban park with monument and green landscaping',
            'has_iron_man': True
        },
        'futuristic_city_4.png': {
            'content': 'A blonde woman in an elegant black dress standing next to Iron Man in his armor suit, set in a government plaza with tall obelisk monument and official buildings.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'government plaza with tall obelisk monument',
            'has_iron_man': True
        },
        'futuristic_city_5.png': {
            'content': 'A blonde woman in an elegant black dress sitting on a modern balcony/terrace with Iron Man standing nearby, overlooking a modern city skyline with twin towers.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'modern city skyline with twin towers',
            'has_iron_man': True
        },
        'futuristic_city_6.png': {
            'content': 'A blonde woman in an elegant black dress standing with Iron Man flying nearby in palace grounds with golden traditional architecture.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'palace grounds with golden architecture',
            'has_iron_man': True
        },
        'futuristic_city_7.png': {
            'content': 'A blonde woman in an elegant black dress standing with Iron Man on a mountain viewpoint with pyramid/obelisk structure at sunset, overlooking a city.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'mountain viewpoint with pyramid/obelisk at sunset',
            'has_iron_man': True
        },
        'futuristic_city_8.png': {
            'content': 'A blonde woman in an elegant black dress sitting with Iron Man standing nearby in futuristic gardens with tree-like structures (similar to Singapore Gardens by the Bay).',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'futuristic gardens with tree-like structures',
            'has_iron_man': True
        },
        'futuristic_city_9.png': {
            'content': 'A blonde woman in an elegant black dress walking on golden temple steps with Iron Man flying overhead, surrounded by crowds of people.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'golden temple steps with crowds',
            'has_iron_man': True
        },
        'futuristic_city_12.png': {
            'content': 'A blonde woman in an elegant black dress standing with Iron Man flying overhead in a white mosque courtyard with minarets.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'white mosque with minarets and courtyard',
            'has_iron_man': True
        },
        'futuristic_city_13.png': {
            'content': 'A blonde woman in an elegant black dress walking through a classical columned corridor/hallway with Iron Man standing in the background.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'classical columned corridor/hallway',
            'has_iron_man': True
        },
        'futuristic_city_14.png': {
            'content': 'A blonde woman in an elegant black dress standing with Iron Man in a modern white mosque courtyard with multiple minarets.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'modern white mosque with multiple minarets',
            'has_iron_man': True
        },
        'futuristic_city_15.png': {
            'content': 'A blonde woman in an elegant black dress sitting on steps with Iron Man standing nearby in a university campus courtyard with people around.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'university campus courtyard with people',
            'has_iron_man': True
        },
        'futuristic_city_16.png': {
            'content': 'A blonde woman in an elegant black dress standing with Iron Man flying overhead in a modern city plaza with distinctive tower/spire architecture.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'modern city plaza with distinctive tower/spire architecture',
            'has_iron_man': True
        },
        'futuristic_city_17.png': {
            'content': 'A blonde woman in an elegant black dress walking with Iron Man through a traditional Middle Eastern/Arabic market street with arches.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'traditional Middle Eastern/Arabic market street with arches',
            'has_iron_man': True
        },
        'futuristic_city_18.png': {
            'content': 'A blonde woman in an elegant black dress standing with Iron Man on a modern skyscraper balcony/terrace with city skyline view.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'modern skyscraper balcony/terrace with city skyline view',
            'has_iron_man': True
        },
        'futuristic_city_19.png': {
            'content': 'A blonde woman in an elegant black dress sitting with Iron Man standing nearby in an Islamic mosque courtyard with traditional architecture.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'Islamic mosque courtyard with traditional architecture',
            'has_iron_man': True
        },
        'futuristic_city_20.png': {
            'content': 'A blonde woman in an elegant black dress standing with Iron Man flying overhead at a modern sports stadium at night with city lights.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'modern sports stadium at night with city lights',
            'has_iron_man': True
        },
        'futuristic_city_21.png': {
            'content': 'A blonde woman in an elegant black dress walking with Iron Man through an ancient Roman amphitheater with stone steps and crowds.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'ancient Roman amphitheater with stone steps and crowds',
            'has_iron_man': True
        },
        'futuristic_city_22.png': {
            'content': 'A blonde woman in an elegant black dress standing with Iron Man on a rocky coastal cliff with sea stacks and ocean waves.',
            'characters': ['blonde woman in black dress', 'Iron Man in red/gold armor'],
            'setting': 'rocky coastal cliff with sea stacks and ocean waves',
            'has_iron_man': True
        },
        'futuristic_city_24.png': {
            'content': 'A blonde woman in an elegant black dress standing in front of a Chinese traditional palace/temple with ornate architecture. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'Chinese traditional palace/temple with ornate architecture',
            'has_iron_man': False
        },
        'futuristic_city_25.png': {
            'content': 'A blonde woman in an elegant black dress walking on a London street with Big Ben and red double-decker bus in the background. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'London street with Big Ben and red double-decker bus',
            'has_iron_man': False
        },
        # Images 26-35 - Woman only, no Iron Man
        'futuristic_city_26.png': {
            'content': 'A blonde woman in an elegant black dress standing on a Paris rooftop terrace with the Eiffel Tower and city skyline in the background. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'Paris rooftop view with Eiffel Tower',
            'has_iron_man': False
        },
        'futuristic_city_27.png': {
            'content': 'A blonde woman in an elegant black dress sitting on a bench in a cherry blossom park with pink flowering trees. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'cherry blossom park with bench',
            'has_iron_man': False
        },
        'futuristic_city_28.png': {
            'content': 'A blonde woman in an elegant black dress standing in Moscow Red Square with the Kremlin walls and architecture in the background. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'Moscow Red Square with Kremlin',
            'has_iron_man': False
        },
        'futuristic_city_29.png': {
            'content': 'A blonde woman in an elegant black dress walking on the White House lawn in Washington DC with the presidential residence in the background. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'White House lawn in Washington DC',
            'has_iron_man': False
        },
        'futuristic_city_30.png': {
            'content': 'A blonde woman in an elegant black dress standing in front of the Egyptian pyramids of Giza in the desert. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'Egyptian pyramids of Giza',
            'has_iron_man': False
        },
        'futuristic_city_31.png': {
            'content': 'A blonde woman in an elegant black dress sitting on steps at the Sydney Opera House waterfront with the iconic architecture in the background. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'Sydney Opera House waterfront',
            'has_iron_man': False
        },
        'futuristic_city_32.png': {
            'content': 'A blonde woman in an elegant black dress standing in front of a European castle/palace with formal gardens and crowds. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'European castle/palace with gardens',
            'has_iron_man': False
        },
        'futuristic_city_33.png': {
            'content': 'A blonde woman in an elegant black dress walking through a Korean traditional palace corridor with wooden architecture and people in traditional dress. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'Korean traditional palace corridor',
            'has_iron_man': False
        },
        'futuristic_city_34.png': {
            'content': 'A blonde woman in an elegant black dress sitting by a fountain in a European city square with classical architecture. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'European city square with fountain',
            'has_iron_man': False
        },
        'futuristic_city_35.png': {
            'content': 'A blonde woman in an elegant black dress standing in front of the Roman Colosseum ruins with ancient architecture. Iron Man is NOT visible in this image.',
            'characters': ['blonde woman in black dress'],
            'setting': 'Roman Colosseum ruins',
            'has_iron_man': False
        }
    }
    
    # Create organized JSON structure
    organized_data = {
        'summary': {
            'total_images': len(unique_names),
            'images_with_iron_man': len([desc for desc in verified_descriptions.values() if desc['has_iron_man']]),
            'images_without_iron_man': len([desc for desc in verified_descriptions.values() if not desc['has_iron_man']]),
            'duplicates_removed': len(duplicates),
            'original_total': len(original_names)
        },
        'categories': {
            'with_iron_man': [],
            'without_iron_man': []
        },
        'all_images': []
    }
    
    # Organize by category and add to all_images
    for filename in unique_names:
        if filename in verified_descriptions:
            desc = verified_descriptions[filename]
            image_data = {
                'filename': filename,
                'content': desc['content'],
                'characters': desc['characters'],
                'setting': desc['setting'],
                'has_iron_man': desc['has_iron_man'],
                'style': 'cinematic, professional photography'
            }
            
            organized_data['all_images'].append(image_data)
            
            if desc['has_iron_man']:
                organized_data['categories']['with_iron_man'].append(image_data)
            else:
                organized_data['categories']['without_iron_man'].append(image_data)
    
    # Update the image names list (remove duplicates)
    with open('image_names_unique.json', 'w') as f:
        json.dump(unique_names, f, indent=2)
    
    # Save the organized accurate descriptions
    with open('image_descriptions_accurate.json', 'w') as f:
        json.dump(organized_data, f, indent=2)
    
    print(f"Created accurate descriptions for {len(unique_names)} unique images")
    print(f"- Images with Iron Man: {organized_data['summary']['images_with_iron_man']}")
    print(f"- Images without Iron Man: {organized_data['summary']['images_without_iron_man']}")
    print(f"- Duplicates removed: {len(duplicates)}")

if __name__ == "__main__":
    create_accurate_descriptions()