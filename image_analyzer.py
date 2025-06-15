import os
import argparse
import base64
import json
from pathlib import Path
from openai import OpenAI
from typing import List, Dict, Set, Tuple
import concurrent.futures
import random
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.tree import Tree
from collections import defaultdict

# Initialize Rich console for better output formatting
console = Console()

def encode_image_to_base64(image_path: str) -> str:
    """Encode an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

class ImageAnalyzer:
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """Initialize the ImageAnalyzer with OpenAI API key."""
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def discover_categories(self, image_paths: List[str], sample_size: int = 20) -> List[str]:
        """
        Discover appropriate categories by analyzing a sample of images.
        
        Args:
            image_paths: List of paths to all images
            sample_size: Number of images to sample for category discovery
            
        Returns:
            List of discovered categories
        """
        # Sample random images for analysis, or use all if fewer than sample_size
        if len(image_paths) <= sample_size:
            sampled_paths = image_paths
        else:
            sampled_paths = random.sample(image_paths, sample_size)
        
        console.print(f"[yellow]Analyzing [bold]{len(sampled_paths)}[/bold] sample images to discover appropriate categories...[/yellow]")
        
        sample_images_base64 = []
        for path in sampled_paths:
            try:
                sample_images_base64.append(encode_image_to_base64(path))
            except Exception as e:
                console.print(f"[red]Error encoding {path}: {str(e)}[/red]")
        
        # Create batches of 5 images to avoid token limits
        batches = [sample_images_base64[i:i+5] for i in range(0, len(sample_images_base64), 5)]
        all_suggested_categories = []
        
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
        ) as progress:
            task = progress.add_task("[cyan]Analyzing image batches for category discovery...", total=len(batches))
            
            for batch_idx, batch in enumerate(batches):
                # Create content with multiple images for the API request
                content = [
                    {"type": "text", "text": """Look at these images and suggest a comprehensive category system that would best organize them and similar images.

Please create:
1. A set of 5-15 main categories that make sense based on these images and would typically be found in a personal photo collection
2. For each main category, 3-6 subcategories that provide more specific organization

Respond in this exact JSON format:
{
    "categories": [
        {
            "main": "category_name",
            "subcategories": ["subcategory1", "subcategory2", ...]
        },
        ...
    ]
}

Don't use placeholder text like "category_name". Use actual descriptive category names. Be specific but flexible to cover various types of images. Categories should be in lowercase with spaces between words."""}
                ]
                
                # Add each image in the batch
                for img_base64 in batch:
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_base64}"
                        }
                    })
                
                # Call OpenAI API
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {
                                "role": "user",
                                "content": content
                            }
                        ],
                        response_format={"type": "json_object"},
                        max_tokens=800
                    )
                    
                    result = response.choices[0].message.content
                    
                    # Parse the JSON response
                    try:
                        categories_data = json.loads(result)
                        batch_categories = categories_data.get("categories", [])
                        all_suggested_categories.extend(batch_categories)
                    except json.JSONDecodeError as e:
                        console.print(f"[red]Error parsing category suggestions (batch {batch_idx+1}): {str(e)}[/red]")
                        console.print(f"[red]Response: {result}[/red]")
                
                except Exception as e:
                    console.print(f"[red]Error getting category suggestions (batch {batch_idx+1}): {str(e)}[/red]")
                
                progress.update(task, advance=1)
        
        # Merge and deduplicate categories
        merged_categories = self._merge_categories(all_suggested_categories)
        
        console.print(f"[green]Successfully discovered [bold]{len(merged_categories)}[/bold] category groups.[/green]")
        
        # Display discovered categories
        self._display_discovered_categories(merged_categories)
        
        return merged_categories
    
    def _merge_categories(self, category_groups: List[Dict]) -> List[Dict]:
        """
        Merge and deduplicate categories from multiple batch analyses.
        
        Args:
            category_groups: List of category groups suggested by the model
            
        Returns:
            Deduplicated and merged list of category groups
        """
        # Create a dictionary to track main categories and their subcategories
        merged = {}
        
        for group in category_groups:
            main = group.get("main", "").lower().strip()
            if not main:
                continue
                
            subcategories = [s.lower().strip() for s in group.get("subcategories", []) if s.strip()]
            
            if main in merged:
                # Add new unique subcategories
                merged[main].update(subcategories)
            else:
                merged[main] = set(subcategories)
        
        # Convert back to the original format
        result = []
        for main, subcats in merged.items():
            result.append({
                "main": main,
                "subcategories": sorted(list(subcats))
            })
        
        return sorted(result, key=lambda x: x["main"])
    
    def _display_discovered_categories(self, categories: List[Dict]):
        """Display the discovered categories in a nice tree format."""
        tree = Tree("[bold]Discovered Categories[/bold]")
        
        for cat in categories:
            main = cat.get("main", "")
            subcats = cat.get("subcategories", [])
            
            branch = tree.add(f"[bold blue]{main}[/bold blue]")
            for subcat in subcats:
                branch.add(f"[cyan]{subcat}[/cyan]")
        
        console.print(Panel(tree, expand=False))
    
    def categorize_image(self, image_path: str, categories: List[Dict]) -> Dict:
        """
        Categorize a single image using the discovered category system.
        
        Args:
            image_path: Path to the image file
            categories: List of discovered category groups
            
        Returns:
            Dict containing categorization results
        """
        try:
            # Encode image to base64
            base64_image = encode_image_to_base64(image_path)
            
            # Prepare a flat list of all categories for the prompt
            category_options = []
            for cat in categories:
                main = cat.get("main", "")
                subcats = cat.get("subcategories", [])
                
                for subcat in subcats:
                    category_options.append(f"{main}/{subcat}")
            
            # Limit to 40 options maximum if there are too many
            if len(category_options) > 40:
                category_options = random.sample(category_options, 40)
            
            # Create the prompt
            prompt = f"""Analyze this image and classify it into the most appropriate category from this list:

{', '.join(category_options)}

If none of these categories fit well, create a new appropriate category in the same format (main/sub).

Return your answer in this exact format: "CATEGORY: brief explanation"
where CATEGORY is in the format "main/subcategory"."""
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            result = response.choices[0].message.content
            
            # Parse the category from the response
            # Expecting format: "main/subcategory: explanation"
            parts = result.strip().split(':', 1)
            category = parts[0].strip().lower()
            explanation = parts[1].strip() if len(parts) > 1 else ""
            
            # Handle malformed responses
            if '/' not in category:
                # Try to add a generic subcategory
                category = f"{category}/general"
            
            return {
                "path": image_path,
                "category": category,
                "explanation": explanation,
                "filename": os.path.basename(image_path)
            }
            
        except Exception as e:
            console.print(f"[red]Error analyzing {image_path}: {str(e)}[/red]")
            return {
                "path": image_path,
                "category": "error/processing",
                "explanation": f"Error: {str(e)}",
                "filename": os.path.basename(image_path)
            }
    
    def analyze_image(self, image_path: str, query: str) -> Dict:
        """
        Analyze a single image with the given query for matching.
        
        Args:
            image_path: Path to the image file
            query: Request/query to match against the image
            
        Returns:
            Dict containing analysis results
        """
        try:
            # Encode image to base64
            base64_image = encode_image_to_base64(image_path)
            
            # Prepare the prompt
            prompt = f"Does this image match the following description or request: '{query}'? Answer with YES or NO, followed by a brief explanation."
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            result = response.choices[0].message.content
            matches = result.strip().upper().startswith("YES")
            
            return {
                "path": image_path,
                "matches": matches,
                "explanation": result,
                "filename": os.path.basename(image_path)
            }
            
        except Exception as e:
            console.print(f"[red]Error analyzing {image_path}: {str(e)}[/red]")
            return {
                "path": image_path,
                "matches": False,
                "explanation": f"Error: {str(e)}",
                "filename": os.path.basename(image_path)
            }

def find_images(folder_path: str, recursive: bool = False) -> List[str]:
    """
    Find all image files in the specified folder.
    
    Args:
        folder_path: Path to the folder containing images
        recursive: Whether to search recursively through subfolders
        
    Returns:
        List of paths to image files
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    image_paths = []
    
    if recursive:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if os.path.splitext(file.lower())[1] in image_extensions:
                    image_paths.append(os.path.join(root, file))
    else:
        for file in os.listdir(folder_path):
            if os.path.splitext(file.lower())[1] in image_extensions:
                image_paths.append(os.path.join(folder_path, file))
    
    return image_paths

def analyze_folder(api_key: str, folder_path: str, query: str = None, output_folder: str = None, 
                   recursive: bool = False, parallel: int = 4, auto_categorize: bool = False,
                   sample_size: int = 20) -> List[Dict]:
    """
    Analyze all images in a folder based on the given query or auto-categorize them.
    
    Args:
        api_key: OpenAI API key
        folder_path: Path to the folder containing images
        query: Request/query to match against the images (optional if auto_categorize is True)
        output_folder: If provided, matching/categorized images will be copied to this folder
        recursive: Whether to search recursively through subfolders
        parallel: Number of parallel workers for processing images
        auto_categorize: Whether to automatically categorize the images
        sample_size: Number of images to sample for category discovery
        
    Returns:
        List of dictionaries containing analysis results
    """
    # Find all images in the folder
    console.print(f"[yellow]Searching for images in {folder_path}...[/yellow]")
    image_paths = find_images(folder_path, recursive)
    
    if not image_paths:
        console.print("[red]No images found in the specified folder.[/red]")
        return []
    
    console.print(f"[green]Found {len(image_paths)} images.[/green]")
    
    # Initialize the analyzer
    analyzer = ImageAnalyzer(api_key=api_key)
    results = []
    
    # Create a descriptor for the progress bar
    if auto_categorize:
        # First discover categories through sampling
        categories = analyzer.discover_categories(image_paths, sample_size)
        
        # Save the discovered categories to a JSON file in the output folder if specified
        if output_folder:
            output_path = Path(output_folder)
            output_path.mkdir(exist_ok=True, parents=True)
            
            categories_file = output_path / "discovered_categories.json"
            with open(categories_file, "w") as f:
                json.dump({"categories": categories}, f, indent=2)
            
            console.print(f"[green]Saved discovered categories to {categories_file}[/green]")
        
        # Now categorize all images using the discovered categories
        console.print("[yellow]Categorizing all images using the discovered categories...[/yellow]")
        
        # Process images with a progress bar
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
        ) as progress:
            task = progress.add_task("[cyan]Categorizing images...", total=len(image_paths))
            
            # Use ThreadPoolExecutor for parallel processing
            with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
                future_to_path = {
                    executor.submit(analyzer.categorize_image, image_path, categories): image_path
                    for image_path in image_paths
                }
                
                for future in concurrent.futures.as_completed(future_to_path):
                    result = future.result()
                    results.append(result)
                    progress.update(task, advance=1)
    else:
        # Normal query matching mode
        console.print(f"[yellow]Analyzing images for query: \"{query}\"[/yellow]")
        
        # Process images with a progress bar
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
        ) as progress:
            task = progress.add_task("[cyan]Analyzing images...", total=len(image_paths))
            
            # Use ThreadPoolExecutor for parallel processing
            with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
                future_to_path = {
                    executor.submit(analyzer.analyze_image, image_path, query): image_path
                    for image_path in image_paths
                }
                
                for future in concurrent.futures.as_completed(future_to_path):
                    result = future.result()
                    results.append(result)
                    progress.update(task, advance=1)
    
    if auto_categorize:
        # Group images by category
        categories = defaultdict(list)
        for result in results:
            category = result.get("category", "other/uncategorized")
            categories[category].append(result)
        
        # Print category statistics
        console.print("\n[bold]Category Statistics:[/bold]")
        
        # Create a tree view of categories
        tree = Tree("[bold]Categorized Images[/bold]")
        
        # Track main categories to organize the tree
        main_branches = {}
        
        # Sort categories for consistent display
        for category, items in sorted(categories.items()):
            # Handle hierarchical categories
            if '/' in category:
                main_cat, sub_cat = category.split('/', 1)
                
                # Create main category branch if it doesn't exist
                if main_cat not in main_branches:
                    main_branches[main_cat] = tree.add(f"[bold blue]{main_cat}[/bold blue] ({sum(len(categories[c]) for c in categories if c.startswith(main_cat + '/'))})") 
                
                # Add subcategory with count
                main_branches[main_cat].add(f"[cyan]{sub_cat}[/cyan] ({len(items)})")
            else:
                # Directly add to tree for non-hierarchical categories
                tree.add(f"[bold blue]{category}[/bold blue] ({len(items)})")
        
        console.print(Panel(tree, expand=False))
        
        # Create category folders and copy images if output folder specified
        if output_folder:
            output_path = Path(output_folder)
            output_path.mkdir(exist_ok=True, parents=True)
            
            console.print(f"[yellow]Creating category folders and copying images to {output_folder}...[/yellow]")
            
            for category, items in categories.items():
                # Handle hierarchical category structure
                if '/' in category:
                    # Split into main and sub category
                    main_cat, sub_cat = category.split('/', 1)
                    
                    # Create main category folder if it doesn't exist
                    main_cat_path = output_path / main_cat
                    main_cat_path.mkdir(exist_ok=True)
                    
                    # Create subcategory folder
                    category_path = main_cat_path / sub_cat
                    category_path.mkdir(exist_ok=True)
                else:
                    # Create standard category folder
                    category_path = output_path / category
                    category_path.mkdir(exist_ok=True)
                
                # Copy images to category folder
                for item in items:
                    source_path = Path(item["path"])
                    dest_path = category_path / source_path.name
                    
                    try:
                        # Read the source file and write to destination
                        with open(source_path, "rb") as src_file:
                            with open(dest_path, "wb") as dst_file:
                                dst_file.write(src_file.read())
                        if '/' in category:
                            # Format: main_category/sub_category
                            main_cat, sub_cat = category.split('/', 1)
                            console.print(f"[green]Copied to {main_cat}/{sub_cat}: {source_path.name}[/green]")
                        else:
                            console.print(f"[green]Copied to {category}: {source_path.name}[/green]")
                    except Exception as e:
                        console.print(f"[red]Error copying {source_path.name}: {str(e)}[/red]")
    else:
        # Filter matching images for normal query mode
        matching_images = [result for result in results if result.get("matches", False)]
        
        # Copy matching images to output folder if specified
        if output_folder and matching_images:
            output_path = Path(output_folder)
            output_path.mkdir(exist_ok=True, parents=True)
            
            console.print(f"[yellow]Copying {len(matching_images)} matching images to {output_folder}...[/yellow]")
            
            for result in matching_images:
                source_path = Path(result["path"])
                dest_path = output_path / source_path.name
                
                try:
                    # Read the source file and write to destination
                    with open(source_path, "rb") as src_file:
                        with open(dest_path, "wb") as dst_file:
                            dst_file.write(src_file.read())
                    console.print(f"[green]Copied: {source_path.name}[/green]")
                except Exception as e:
                    console.print(f"[red]Error copying {source_path.name}: {str(e)}[/red]")
        
        # Print summary for query mode
        console.print("\n[bold]Analysis Summary:[/bold]")
        console.print(f"Total images analyzed: {len(results)}")
        console.print(f"Images matching query: {len(matching_images)}")
    
    # Return results
    return results

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="PixelSense - Intelligent Image Analyzer using OpenAI Vision API")
    parser.add_argument("--folder", "-f", required=True, help="Path to the folder containing images")
    parser.add_argument("--query", "-q", help="Request/query to match against the images (not required if using categorization)")
    parser.add_argument("--api-key", "-k", help="OpenAI API key (can also be set via OPENAI_API_KEY environment variable)")
    parser.add_argument("--output", "-o", help="Output folder for matching/categorized images (optional)")
    parser.add_argument("--recursive", "-r", action="store_true", help="Search recursively through subfolders")
    parser.add_argument("--parallel", "-p", type=int, default=4, help="Number of parallel workers for processing (default: 4)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed results for each image")
    parser.add_argument("--auto-categorize", "-a", action="store_true", help="Automatically discover categories and organize images")
    parser.add_argument("--sample-size", "-s", type=int, default=20, help="Number of images to sample for category discovery (default: 20)")
    
    args = parser.parse_args()
    
    # Get API key from args or environment
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        console.print("[red]Error: OpenAI API key not provided. Use --api-key or set OPENAI_API_KEY environment variable.[/red]")
        return
    
    # Verify that query is provided if not categorizing
    if not args.auto_categorize and not args.query:
        console.print("[red]Error: Either --query or --auto-categorize must be specified.[/red]")
        return
    
    # Welcome message with selected mode
    console.print(Panel("[bold blue]PixelSense - Intelligent Image Analyzer[/bold blue]", expand=False))
    if args.auto_categorize:
        console.print(Panel("[bold yellow]Mode: Adaptive Auto-Categorization[/bold yellow]\nAI will discover appropriate categories from your image collection", expand=False))
    else:
        console.print(Panel(f"[bold yellow]Mode: Query Matching[/bold yellow]\nFinding images matching: '{args.query}'", expand=False))
    
    # Run the analyzer
    results = analyze_folder(
        api_key=api_key,
        folder_path=args.folder,
        query=args.query,
        output_folder=args.output,
        recursive=args.recursive,
        parallel=args.parallel,
        auto_categorize=args.auto_categorize,
        sample_size=args.sample_size
    )
    
    # Print detailed results if verbose
    if args.verbose and results:
        console.print("\n[bold]Detailed Results:[/bold]")
        for result in results:
            if args.auto_categorize:
                category = result.get("category", "other/unknown")
                color = "green" if "error" not in category else "red"
                console.print(f"[{color}]{result['filename']} - Category: {category.upper()}[/{color}]")
                console.print(f"  {result['explanation']}\n")
            else:
                matches = result.get("matches", False)
                color = "green" if matches else "red"
                console.print(f"[{color}]{result['filename']}[/{color}]")
                console.print(f"  {result['explanation']}\n")
    
    console.print("[bold green]Analysis complete![/bold green]")

if __name__ == "__main__":
    main()