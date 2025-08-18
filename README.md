# 🎛️ Slideme to Gutenberg Block Converter

A powerful Streamlit web application that converts WordPress `[slideme]` shortcodes into modern Gutenberg blocks with support for lists, paragraphs, and rich content formatting.

## ✨ Features

- **🔄 Dual Input Methods**: Upload files or paste content directly
- **📝 Smart List Conversion**: Automatically converts markdown and HTML lists to Gutenberg list blocks
- **🎯 Rich Content Support**: Handles mixed content with paragraphs and lists
- **👀 Preview Options**: View converted output or download as HTML file
- **⚡ Real-time Processing**: Convert with a single click
- **📱 Responsive Design**: Clean, modern interface with tabbed navigation
- **🐳 Docker Support**: Easy deployment with Docker and Docker Compose
- **🛠️ Development Tools**: Helper scripts for common Docker operations

## 🚀 Quick Start

### Prerequisites

Choose one of the following options:

**Option 1: Docker (Recommended)**

- Docker
- Docker Compose

**Option 2: Python Virtual Environment**

- Python 3.7+
- Streamlit

### Installation

#### 🐳 Option 1: Using Docker (Recommended)

1. Clone the repository:

```bash
git clone https://github.com/Singh-Ish/slideme-converter.git
cd slideme-converter
```

2. Run with Docker Compose:

```bash
# For development (with volume mount for live changes)
docker-compose up -d

# For production (without volume mount)
docker-compose --profile production up -d slideme-converter-prod
```

3. Open your browser and navigate to `http://localhost:8501`

#### 🛠️ Docker Helper Script

For convenience, you can use the included helper script:

```bash
# Make the script executable (first time only)
chmod +x docker-helper.sh

# Build the image
./docker-helper.sh build

# Run in development mode
./docker-helper.sh dev

# Run in production mode
./docker-helper.sh prod

# View logs
./docker-helper.sh logs

# Stop the application
./docker-helper.sh stop

# Clean up containers and images
./docker-helper.sh clean

# Check application health
./docker-helper.sh health

# Access container shell
./docker-helper.sh shell
```

#### Alternative Docker Commands

```bash
# Build the Docker image
docker build -t slideme-converter .

# Run the container
docker run -p 8501:8501 slideme-converter
```

#### 🐍 Option 2: Python Virtual Environment

#### 🐍 Option 2: Python Virtual Environment

1. Clone the repository:

```bash
git clone https://github.com/Singh-Ish/slideme-converter.git
cd slideme-converter
```

2. Create and activate a Python virtual environment:

**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
streamlit run app.py
```

5. Open your browser and navigate to `http://localhost:8501`

### 🛑 Stopping the Application

#### Docker

```bash
# Stop Docker Compose services
docker-compose down

# Stop and remove containers, networks, and volumes
docker-compose down -v
```

#### Python Virtual Environment

When you're done using the application, you can deactivate the virtual environment:

```bash
deactivate
```

## 🔧 Development

### Local Development with Docker

For development with live code changes:

```bash
# Run with volume mounting for live changes
docker-compose up

# View logs
docker-compose logs -f

# Access container shell
docker exec -it slideme-converter_slideme-converter_1 /bin/bash
```

### Building for Production

```bash
# Build production image
docker build -t slideme-converter:prod .

# Run production container
docker run -d -p 8501:8501 --name slideme-converter-prod slideme-converter:prod
```

### CI/CD with GitHub Actions

The project includes a GitHub Actions workflow that:

- **Builds** Docker images on every push and pull request
- **Tests** the built image with health checks
- **Publishes** images to Docker Hub (requires repository secrets)
- **Supports** multi-platform builds (AMD64 and ARM64)

To set up automated publishing:

1. Create Docker Hub repository secrets:

   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub access token

2. Push to the `main` branch to trigger the workflow

## 📖 How to Use

### Step 1: Input Your Content

Choose one of two methods:

- **📁 Upload File**: Upload `.txt`, `.html`, or `.md` files containing slideme shortcodes
- **📝 Paste Text**: Directly paste your content into the text area

### Step 2: Convert

Click the **"🔄 Convert to Gutenberg Blocks"** button to process your content.

### Step 3: Get Results

View your converted content in two ways:

- **👀 View Output**: Preview the converted Gutenberg blocks
- **📥 Download**: Copy the content or download as an HTML file

## 🔧 Supported Formats

### Input Format (Slideme Shortcodes)

```
[slideme title="Your Title Here"]
Your content with lists and paragraphs.

- First list item
- Second list item

1. Numbered item
2. Another numbered item

More paragraph content.
[/slideme]
```

### Output Format (Gutenberg Blocks)

```html
<!-- wp:cu-block/description-custom {"title":"Your Title Here","layout":"accordion"} -->
<!-- wp:paragraph -->
<p>Your content with lists and paragraphs.</p>
<!-- /wp:paragraph -->
<!-- wp:list -->
<ul>
  <li>First list item</li>
  <li>Second list item</li>
</ul>
<!-- /wp:list -->
<!-- wp:list {"ordered":true} -->
<ol>
  <li>Numbered item</li>
  <li>Another numbered item</li>
</ol>
<!-- /wp:list -->
<!-- wp:paragraph -->
<p>More paragraph content.</p>
<!-- /wp:paragraph -->
<!-- /wp:cu-block/description-custom -->
```

## 📋 Supported List Formats

### Markdown Lists

- **Unordered**: `- item`, `* item`, `+ item`
- **Ordered**: `1. item`, `2. item`, `3. item`

### HTML Lists

- **Unordered**: `<ul><li>item</li></ul>`
- **Ordered**: `<ol><li>item</li></ol>`

## 🛠️ Technical Details

### Core Functions

- `convert_slideme_to_gutenberg()`: Main conversion function
- `process_inner_content()`: Handles mixed content processing
- `convert_markdown_lists_to_html()`: Converts markdown lists to HTML
- `convert_lists_to_gutenberg()`: Converts HTML lists to Gutenberg blocks

### Dependencies

#### Docker

- `python:3.11-slim`: Base Python image
- `streamlit`: Web application framework
- `curl`: For health checks

#### Python Package Dependencies

- `streamlit`: Web application framework
- `re`: Regular expression operations (built-in)
- `base64`: File encoding for downloads (built-in)

## 🎯 Use Cases

- **WordPress Migration**: Convert legacy slideme shortcodes to modern Gutenberg blocks
- **Content Management**: Batch process multiple accordion-style content blocks
- **Developer Tools**: Streamline WordPress theme development workflow
- **Content Formatting**: Ensure consistent Gutenberg block structure

## 🔧 Troubleshooting

### Common Issues

**Problem**: "This site can't be reached" error
**Solution**:

1. Check if Docker container is running:
   ```bash
   docker ps
   ```
2. Check application health:
   ```bash
   ./docker-helper.sh health
   ```
3. View container logs:
   ```bash
   ./docker-helper.sh logs
   ```

**Problem**: Port already in use
**Solution**:

1. Stop any existing containers:
   ```bash
   ./docker-helper.sh stop
   ```
2. Check for other applications using port 8501:
   ```bash
   lsof -i :8501
   ```

### Docker Issues

**Problem**: Permission denied when running Docker
**Solution**: Ensure Docker Desktop is running and your user has Docker permissions

**Problem**: Container won't start
**Solution**:

1. Rebuild the image:
   ```bash
   ./docker-helper.sh build
   ```
2. Check Docker logs for specific errors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Issues & Support

If you encounter any issues or have questions:

1. Check existing [Issues](https://github.com/Singh-Ish/slideme-converter/issues)
2. Create a new issue with detailed description
3. Include sample input/output for debugging

## 🔄 Version History

- **v2.0.0**: Added Docker support with Docker Compose for easy deployment
- **v1.2.0**: Enhanced UI with tabs and convert button
- **v1.1.0**: Added list support and improved content processing
- **v1.0.0**: Initial release with basic slideme conversion

---

Made with ❤️ for WordPress developers and content creators
