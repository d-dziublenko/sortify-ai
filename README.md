# Sortify AI 🖼️✨

An intelligent image organization tool that uses OpenAI's Vision API to automatically analyze, categorize, and sort your image collections based on their visual content.

## Features

- **Smart Query Matching**: Find images that match specific descriptions or requests
- **Adaptive Auto-Categorization**: AI discovers appropriate categories from your image collection
- **Hierarchical Organization**: Creates main categories with subcategories for better organization
- **Batch Processing**: Efficiently processes multiple images in parallel
- **Flexible Search**: Supports both single folder and recursive subfolder scanning
- **Visual Progress Tracking**: Rich terminal interface with progress bars and formatted output
- **Automatic File Organization**: Copies matched/categorized images to organized folder structures

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Examples](#examples)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

### From Source

1. Clone the repository:

```bash
git clone https://github.com/d-dziublenko/sortify-ai.git
cd sortify-ai
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### As a Package

You can also install Sortify AI as a Python package:

```bash
pip install -e .
```

This allows you to use `sortify-ai` command from anywhere on your system.

### API Key Setup

Set up your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or on Windows:

```bash
set OPENAI_API_KEY=your-api-key-here
```

## Quick Start

For a detailed quick start guide, see [QUICKSTART.md](QUICKSTART.md).

### Find specific images:

```bash
python image_analyzer.py -f ./photos -q "sunset over water" -o ./sunset_photos
```

### Auto-organize your collection:

```bash
python image_analyzer.py -f ./photos -a -o ./organized_photos
```

## Usage

### Query Mode - Find Specific Images

Search for images matching a specific description:

```bash
python image_analyzer.py -f ./photos -q "sunset over water" -o ./sunset_photos
```

### Auto-Categorization Mode

Let AI discover categories and organize your images:

```bash
python image_analyzer.py -f ./photos -a -o ./organized_photos
```

### Command Line Options

- `-f, --folder`: Path to the folder containing images (required)
- `-q, --query`: Description to match against images (required unless using `-a`)
- `-a, --auto-categorize`: Enable adaptive auto-categorization mode
- `-o, --output`: Output folder for matched/categorized images
- `-r, --recursive`: Search recursively through subfolders
- `-p, --parallel`: Number of parallel workers (default: 4)
- `-s, --sample-size`: Images to sample for category discovery (default: 20)
- `-v, --verbose`: Show detailed results for each image
- `-k, --api-key`: OpenAI API key (alternative to environment variable)

## Examples

The `examples/` directory contains comprehensive usage examples. Run the interactive example script:

```bash
python examples/example_usage.py
```

This will guide you through various use cases including:

- Finding specific content (e.g., pets, landmarks)
- Auto-categorizing photo collections
- Searching vacation photos
- Organizing family photos
- Professional product photo organization

### Example: Find all images with dogs

```bash
python image_analyzer.py -f ~/Pictures -q "images containing dogs" -o ./dog_photos -r
```

### Example: Organize vacation photos

```bash
python image_analyzer.py -f ./vacation_2024 -a -o ./vacation_organized -s 30
```

### Example: Process with more workers for faster analysis

```bash
python image_analyzer.py -f ./large_collection -a -p 8 -o ./sorted
```

## How It Works

### Query Mode

1. Scans the specified folder for image files
2. Sends each image to OpenAI's Vision API with your query
3. AI determines if the image matches your description
4. Matching images are copied to the output folder

### Auto-Categorization Mode

1. Samples a subset of your images to understand the collection
2. AI analyzes the samples and suggests appropriate categories
3. Creates a hierarchical category structure (e.g., "travel/beaches", "food/desserts")
4. Processes all images and assigns them to categories
5. Organizes images into a folder structure matching the categories

## Project Structure

```
sortify-ai/
├── .github/
│   └── workflows/
│       └── tests.yml         # GitHub Actions for automated testing
├── examples/
│   └── example_usage.py      # Interactive examples demonstrating usage
├── tests/
│   └── test_image_analyzer.py # Unit tests for the analyzer
├── image_analyzer.py         # Main application logic
├── main.py                  # Simple usage example
├── setup.py                 # Package installation configuration
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Development dependencies
├── README.md               # This file
├── QUICKSTART.md          # Quick start guide
├── CONTRIBUTING.md        # Contribution guidelines
├── LICENSE               # AGPL-3.0 license
└── .gitignore           # Git ignore rules
```

## Category Structure

When using auto-categorization, Sortify AI creates a hierarchical structure:

```
organized_photos/
├── travel/
│   ├── beaches/
│   ├── cities/
│   └── landmarks/
├── food/
│   ├── desserts/
│   └── restaurants/
├── people/
│   ├── portraits/
│   └── groups/
└── discovered_categories.json
```

The `discovered_categories.json` file contains the full category structure for reference.

## Development

### Setting Up Development Environment

1. Clone the repository and install development dependencies:

```bash
git clone https://github.com/d-dziublenko/sortify-ai.git
cd sortify-ai
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

2. Install pre-commit hooks:

```bash
pre-commit install
```

### Code Style

We use Black for code formatting and Flake8 for linting. Run before committing:

```bash
black .
flake8 .
```

### Running in Development Mode

For debugging, you can enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Testing

Run the test suite:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest tests/ --cov=./ --cov-report=html
```

Tests are automatically run on push via GitHub Actions.

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- WebP (.webp)

## Requirements

- Python 3.7+
- OpenAI API key with access to GPT-4 Vision
- Internet connection for API calls

## Tips for Best Results

1. **For Auto-Categorization**: Use a larger sample size (`-s 50`) for diverse collections
2. **API Usage**: Each image requires one API call, so monitor your usage for large collections
3. **Parallel Processing**: Increase workers (`-p 8`) for faster processing on capable systems
4. **Category Discovery**: The AI adapts categories based on your specific image collection

## Troubleshooting

### "No images found"

- Check the folder path is correct
- Ensure images have supported extensions
- Use `-r` flag to search subfolders

### "Error: OpenAI API key not provided"

- Set the `OPENAI_API_KEY` environment variable
- Or use the `-k` flag to provide the key directly

### Rate Limiting

- Reduce parallel workers with `-p 2`
- Add delays between batches (modify code if needed)

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Code style and standards
- Testing requirements
- Pull request process
- Development setup

## License

This project is licensed under the AGPL-3.0 license - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [OpenAI's GPT-4 Vision API](https://platform.openai.com/docs/guides/vision)
- Terminal formatting powered by [Rich](https://github.com/Textualize/rich)

## Future Enhancements

- [ ] Support for more image formats (RAW, HEIC)
- [ ] Export categorization results to various formats
- [ ] Web interface for easier interaction
- [ ] Integration with cloud storage services
- [ ] Custom category templates
- [ ] Duplicate detection and handling

## Support

If you encounter any issues or have questions:

1. Check the [QUICKSTART.md](QUICKSTART.md) guide
2. Review existing [Issues](https://github.com/d-dziublenko/sortify-ai.git)
3. Create a new issue with detailed information about your problem

## Star History

If you find Sortify AI useful, please consider giving it a star! ⭐

---

Made with ❤️ by Dmytro Dziublenko
