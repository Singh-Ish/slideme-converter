# 🎛️ Slideme to Gutenberg Block Converter

A powerful Streamlit web application that converts WordPress `[slideme]` shortcodes into modern Gutenberg blocks with support for lists, paragraphs, and rich content formatting.

## ✨ Features

- **🔄 Dual Input Methods**: Upload files or paste content directly
- **📝 Smart List Conversion**: Automatically converts markdown and HTML lists to Gutenberg list blocks
- **🎯 Rich Content Support**: Handles mixed content with paragraphs and lists
- **👀 Preview Options**: View converted output or download as HTML file
- **⚡ Real-time Processing**: Convert with a single click
- **📱 Responsive Design**: Clean, modern interface with tabbed navigation

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Streamlit

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Singh-Ish/slideme-converter.git
cd slideme-converter
```

2. Install dependencies:

```bash
pip install streamlit
```

3. Run the application:

```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

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

- `streamlit`: Web application framework
- `re`: Regular expression operations
- `base64`: File encoding for downloads

## 🎯 Use Cases

- **WordPress Migration**: Convert legacy slideme shortcodes to modern Gutenberg blocks
- **Content Management**: Batch process multiple accordion-style content blocks
- **Developer Tools**: Streamline WordPress theme development workflow
- **Content Formatting**: Ensure consistent Gutenberg block structure

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

- **v1.0.0**: Initial release with basic slideme conversion
- **v1.1.0**: Added list support and improved content processing
- **v1.2.0**: Enhanced UI with tabs and convert button

---

Made with ❤️ for WordPress developers and content creators
