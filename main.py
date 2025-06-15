import os
from image_analyzer import analyze_folder

# Set your OpenAI API key here or use the OPENAI_API_KEY environment variable
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

def main():
    # Example usage of adaptive auto-categorization
    results = analyze_folder(
        api_key=os.environ.get("OPENAI_API_KEY"),
        folder_path="./images",
        output_folder="./adaptive_categories",
        recursive=True,
        parallel=4,
        auto_categorize=True,
        sample_size=20  # Adjust sample size based on your collection
    )
    
    # Group results by main category and subcategory
    categories = {}
    
    for result in results:
        category = result.get("category", "other/unknown")
        if category not in categories:
            categories[category] = []
        categories[category].append(result["filename"])
    
    # Print totals by category
    print("\n=== ADAPTIVE CATEGORIZATION RESULTS ===")
    
    for category, files in sorted(categories.items()):
        print(f"\n• {category.upper()} ({len(files)} images)")
        # Show up to 3 example filenames
        for filename in files[:3]:
            print(f"  - {filename}")
        if len(files) > 3:
            print(f"  - ... and {len(files) - 3} more")
    
    # Print the path to the saved category structure
    if os.path.exists("./adaptive_categories/discovered_categories.json"):
        print("\nThe full category structure has been saved to:")
        print("./adaptive_categories/discovered_categories.json")

if __name__ == "__main__":
    main()