# Quick Start Guide for Sortify AI

This guide will help you get Sortify AI running in just a few minutes!

## Prerequisites

Before you begin, ensure you have Python 3.7 or later installed on your system. You can check your Python version by opening a terminal and running `python --version`. If you don't have Python installed, download it from the official Python website at python.org.

You'll also need an OpenAI API key to use the Vision API. If you don't have one yet, visit platform.openai.com to create an account and generate an API key.

## Step 1: Clone and Set Up

First, let's get the code and set up your environment. Open your terminal and run these commands:

```bash
# Clone the repository
git clone https://github.com/d-dziublenko/sortify-ai.git
cd sortify-ai

# Create a virtual environment (recommended)
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

## Step 2: Configure Your API Key

The easiest way to set your OpenAI API key is through an environment variable:

```bash
# On macOS/Linux:
export OPENAI_API_KEY="your-api-key-here"

# On Windows:
set OPENAI_API_KEY=your-api-key-here
```

## Step 3: Prepare Your Images

Create a folder with the images you want to analyze. For this example, let's say your images are in a folder called "my_photos" on your desktop.

## Step 4: Your First Image Search

Let's find all images containing dogs in your photo collection:

```bash
python image_analyzer.py -f ~/Desktop/my_photos -q "dogs or puppies" -o ./found_dogs
```

This command will:

- Search through all images in my_photos
- Find images containing dogs or puppies
- Copy matching images to a new folder called "found_dogs"

## Step 5: Auto-Organize Your Photos

Now let's try the auto-categorization feature to organize your entire photo collection:

```bash
python image_analyzer.py -f ~/Desktop/my_photos -a -o ./organized_photos
```

This will:

- Analyze a sample of your images to understand what categories make sense
- Create a category structure (like travel/beaches, people/portraits, etc.)
- Sort all your images into appropriate folders

## Common Use Cases

### Find vacation photos from a specific place

```bash
python image_analyzer.py -f ./photos -q "beach in Hawaii or tropical island" -o ./hawaii_photos -r
```

### Organize screenshots separately

```bash
python image_analyzer.py -f ./downloads -q "screenshot of computer screen or mobile app" -o ./screenshots
```

### Find all food photos

```bash
python image_analyzer.py -f ./photos -q "food, meals, or dishes" -o ./food_pics -r
```

### Let AI organize your entire photo library

```bash
python image_analyzer.py -f ~/Pictures -a -o ~/Pictures_Organized -r -p 8
```

## Understanding the Output

When Sortify AI runs, you'll see:

- A progress bar showing how many images have been processed
- Category statistics (in auto-categorization mode)
- Files being copied to the output folder
- A summary of results at the end

## Tips for Best Results

1. **Be specific in your queries**: Instead of "animals", try "cats and dogs playing together"
2. **Use more samples for diverse collections**: Add `-s 50` for better category discovery
3. **Process faster with more workers**: Add `-p 8` if you have a powerful computer
4. **Search subfolders**: Always add `-r` to search recursively

## Next Steps

Now that you've got Sortify AI running, explore more advanced features:

- Read the full README.md for all available options
- Check out the examples folder for more use cases
- Customize category names by editing the discovered_categories.json file
- Integrate Sortify AI into your photo workflow

## Need Help?

If you encounter any issues:

- Check that your API key is correctly set
- Ensure your image folder path is correct
- Verify you have supported image formats (JPG, PNG, etc.)
- See the troubleshooting section in README.md

Happy organizing! 🖼️✨
