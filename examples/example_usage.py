#!/usr/bin/env python
"""
Example usage scripts for Sortify AI
Demonstrates various ways to use the image analyzer
"""

import os
import sys
from pathlib import Path

# Add parent directory to path so we can import image_analyzer
sys.path.append(str(Path(__file__).parent.parent))

from image_analyzer import analyze_folder

def example_find_specific_content():
    """Example: Find all images containing specific objects or scenes"""
    print("=== EXAMPLE 1: Finding Specific Content ===")
    print("Looking for images with cats...\n")
    
    results = analyze_folder(
        api_key=os.environ.get("OPENAI_API_KEY"),
        folder_path="./sample_images",  # Change to your image folder
        query="images containing cats or kittens",
        output_folder="./found_cats",
        recursive=True,
        parallel=4
    )
    
    # Count matches
    matches = [r for r in results if r.get("matches", False)]
    print(f"\nFound {len(matches)} images with cats out of {len(results)} total images")
    
    return results

def example_auto_categorize_photos():
    """Example: Automatically categorize a photo collection"""
    print("\n=== EXAMPLE 2: Auto-Categorization ===")
    print("Discovering categories and organizing photos...\n")
    
    results = analyze_folder(
        api_key=os.environ.get("OPENAI_API_KEY"),
        folder_path="./sample_images",  # Change to your image folder
        output_folder="./organized_photos",
        recursive=True,
        parallel=4,
        auto_categorize=True,
        sample_size=25  # Sample 25 images to discover categories
    )
    
    # Show category distribution
    from collections import defaultdict
    categories = defaultdict(int)
    
    for result in results:
        category = result.get("category", "unknown")
        categories[category] += 1
    
    print("\nCategory Distribution:")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count} images")
    
    return results

def example_vacation_photo_search():
    """Example: Find specific vacation moments"""
    print("\n=== EXAMPLE 3: Vacation Photo Search ===")
    print("Finding beach sunset photos from vacation...\n")
    
    # You can be very specific with your queries
    results = analyze_folder(
        api_key=os.environ.get("OPENAI_API_KEY"),
        folder_path="./vacation_2024",  # Change to your vacation folder
        query="sunset or sunrise at the beach with orange or pink sky",
        output_folder="./beach_sunsets",
        recursive=True,
        parallel=6  # Use more workers for faster processing
    )
    
    return results

def example_family_photo_organization():
    """Example: Organize family photos by detected content"""
    print("\n=== EXAMPLE 4: Family Photo Organization ===")
    print("Organizing family photos into meaningful categories...\n")
    
    # This will create categories like:
    # - people/portraits
    # - people/groups
    # - events/birthdays
    # - events/holidays
    # etc.
    
    results = analyze_folder(
        api_key=os.environ.get("OPENAI_API_KEY"),
        folder_path="./family_photos",  # Change to your family photos folder
        output_folder="./family_organized",
        recursive=True,
        parallel=4,
        auto_categorize=True,
        sample_size=40  # Larger sample for diverse family photos
    )
    
    return results

def example_professional_use():
    """Example: Organize product photos for e-commerce"""
    print("\n=== EXAMPLE 5: Professional Product Photo Organization ===")
    print("Categorizing product images for online store...\n")
    
    # Find all product photos on white backgrounds
    results = analyze_folder(
        api_key=os.environ.get("OPENAI_API_KEY"),
        folder_path="./product_images",
        query="product photo with white or light background suitable for e-commerce",
        output_folder="./ecommerce_ready",
        recursive=False,
        parallel=8  # More workers for professional use
    )
    
    return results

def main():
    """Run examples based on user selection"""
    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: Please set your OPENAI_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY='your-key-here'")
        return
    
    print("Sortify AI - Example Usage Scripts")
    print("==================================\n")
    print("Choose an example to run:")
    print("1. Find specific content (e.g., cats)")
    print("2. Auto-categorize photo collection")
    print("3. Search vacation photos")
    print("4. Organize family photos")
    print("5. Professional product photo organization")
    print("6. Run all examples")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    examples = {
        "1": example_find_specific_content,
        "2": example_auto_categorize_photos,
        "3": example_vacation_photo_search,
        "4": example_family_photo_organization,
        "5": example_professional_use
    }
    
    if choice in examples:
        examples[choice]()
    elif choice == "6":
        for func in examples.values():
            func()
            input("\nPress Enter to continue to next example...")
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()