import streamlit as st
import re
import base64

def detect_tables_in_content(content):
    """Detect if there are tables in the content and return their count"""
    table_pattern = r'<table[^>]*>(.*?)</table>'
    matches = re.findall(table_pattern, content, re.DOTALL)
    return len(matches)

def convert_tables_to_wordpress_table(content):
    """Convert HTML tables to WordPress table blocks"""
    table_pattern = r'<table[^>]*>(.*?)</table>'
    
    def generate_alt_text(src, existing_alt=""):
        """Generate intuitive alt text for images"""
        if existing_alt and existing_alt.strip() and existing_alt.lower() not in ['', 'image', 'img', 'picture', 'photo']:
            return existing_alt.strip()
        
        # Extract filename from src and make it more readable
        filename = src.split('/')[-1]
        # Remove file extension
        name_without_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
        
        # Clean up common patterns in filenames
        name_without_ext = re.sub(r'[-_]', ' ', name_without_ext)
        name_without_ext = re.sub(r'\d+x\d+', '', name_without_ext)  # Remove dimensions like 160x235
        name_without_ext = re.sub(r'\s+', ' ', name_without_ext).strip()
        
        # If we have a meaningful name, use it
        if name_without_ext and len(name_without_ext) > 2:
            return name_without_ext.title()
        
        # Fallback to generic description
        return "Book cover image"
    
    def extract_table_as_wordpress_table(match):
        table_content = match.group(1)
        
        # Find all rows
        row_pattern = r'<tr[^>]*>(.*?)</tr>'
        rows = re.findall(row_pattern, table_content, re.DOTALL)
        
        if not rows:
            return ""
        
        # Process each row
        table_body = []
        header_row = None
        
        for i, row in enumerate(rows):
            # Extract cells (both th and td)
            cell_pattern = r'<t[hd][^>]*>(.*?)</t[hd]>'
            cells = re.findall(cell_pattern, row, re.DOTALL)
            
            if not cells:
                continue
            
            processed_cells = []
            for cell in cells:
                # Convert images in cells to proper image blocks first
                img_pattern = r'<img[^>]*src=["\']([^"\']+)["\'][^>]*(?:alt=["\']([^"\']*)["\'][^>]*)?[^>]*/?>'
                images_in_cell = re.findall(img_pattern, cell)
                
                # Replace images with placeholders and collect image blocks
                cell_content = cell
                image_blocks = []
                
                for src, alt in images_in_cell:
                    intuitive_alt = generate_alt_text(src, alt)
                    image_block = f'<!-- wp:image {{"sizeSlug":"full","linkDestination":"none","isDecorative":true}} -->\n<figure class="wp-block-image size-full"><img src="{src}" alt="{intuitive_alt}"/></figure>\n<!-- /wp:image -->'
                    image_blocks.append(image_block)
                
                # Remove image tags from cell content
                cell_content = re.sub(r'<a[^>]*>[\s]*<img[^>]*>[\s]*</a>', '', cell_content)
                cell_content = re.sub(r'<img[^>]*/?>', '', cell_content)
                
                # Clean up cell content but preserve formatting
                cell_content = re.sub(r'</?(?:h[1-6]|p|div)[^>]*>', ' ', cell_content)
                cell_content = re.sub(r'<br\s*/?>', ' ', cell_content)
                cell_content = re.sub(r'\s+', ' ', cell_content).strip()
                
                # If cell had images, add them after the table
                if image_blocks:
                    cell_content += " [IMAGES_AFTER_TABLE]"
                    # Store image blocks for later (we'll add them after the table)
                
                processed_cells.append(cell_content)
            
            # Determine if this should be a header row (first row or contains th tags)
            if i == 0 or '<th' in row:
                header_row = processed_cells
            else:
                table_body.append(processed_cells)
        
        # Determine the maximum number of columns in the table
        max_columns = 0
        if header_row:
            max_columns = max(max_columns, len(header_row))
        for row in table_body:
            max_columns = max(max_columns, len(row))
        
        # Create WordPress table block with proper format
        # Note: WordPress table blocks have specific requirements for JSON attributes
        if max_columns >= 3:
            # For scrollable tables, use simpler approach that WordPress recognizes
            table_block = f'<!-- wp:table {{"hasFixedLayout":true}} -->\n'
            table_block += f'<figure class="wp-block-table"><table class="has-fixed-layout">'
        else:
            table_block = f'<!-- wp:table {{"hasFixedLayout":true}} -->\n'
            table_block += f'<figure class="wp-block-table"><table class="has-fixed-layout">'
        
        # Add header if exists
        if header_row:
            table_block += '<thead><tr>'
            for cell in header_row:
                # Fix double-escaped quotes while preserving HTML formatting
                import html
                # First decode any existing entities to get back to normal HTML
                decoded_cell = html.unescape(cell)
                # Fix double quotes in attributes that occur after unescaping
                fixed_cell = re.sub(r'""([^"]*?)""', r'"\1"', decoded_cell)
                table_block += f'<th>{fixed_cell}</th>'
            table_block += '</tr></thead>'
        
        # Add body
        if table_body:
            table_block += '<tbody>'
            for row in table_body:
                table_block += '<tr>'
                for cell in row:
                    # Fix double-escaped quotes while preserving HTML formatting
                    import html
                    # First decode any existing entities to get back to normal HTML
                    decoded_cell = html.unescape(cell)
                    # Fix double quotes in attributes that occur after unescaping
                    fixed_cell = re.sub(r'""([^"]*?)""', r'"\1"', decoded_cell)
                    table_block += f'<td>{fixed_cell}</td>'
                table_block += '</tr>'
            table_block += '</tbody>'
        
        table_block += '</table></figure>\n<!-- /wp:table -->'
        
        return table_block
    
    return re.sub(table_pattern, extract_table_as_wordpress_table, content, flags=re.DOTALL)

def convert_tables_to_paragraphs(content):
    """Convert HTML tables to paragraphs"""
    table_pattern = r'<table[^>]*>(.*?)</table>'
    
    def generate_alt_text(src, existing_alt=""):
        """Generate intuitive alt text for images"""
        if existing_alt and existing_alt.strip() and existing_alt.lower() not in ['', 'image', 'img', 'picture', 'photo']:
            return existing_alt.strip()
        
        # Extract filename from src and make it more readable
        filename = src.split('/')[-1]
        # Remove file extension
        name_without_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
        
        # Clean up common patterns in filenames
        name_without_ext = re.sub(r'[-_]', ' ', name_without_ext)
        name_without_ext = re.sub(r'\d+x\d+', '', name_without_ext)  # Remove dimensions like 160x235
        name_without_ext = re.sub(r'\s+', ' ', name_without_ext).strip()
        
        # If we have a meaningful name, use it
        if name_without_ext and len(name_without_ext) > 2:
            return name_without_ext.title()
        
        # Fallback to generic description
        return "Book cover image"
    
    def extract_table_content(match):
        table_content = match.group(1)
        
        # Extract text from table cells first
        cell_pattern = r'<t[dh][^>]*>(.*?)</t[dh]>'
        cells = re.findall(cell_pattern, table_content, re.DOTALL)
        
        result_blocks = []
        
        for cell in cells:
            if not cell or not cell.strip():
                continue
            
            cell_text = cell.strip()
            
            # First, extract images from this cell and process them separately
            img_pattern = r'<img[^>]*src=["\']([^"\']+)["\'][^>]*(?:alt=["\']([^"\']*)["\'][^>]*)?[^>]*/?>'
            
            # Find all images in this cell
            images_in_cell = re.findall(img_pattern, cell_text)
            
            # Remove all img tags and their surrounding link tags from the cell text
            # But preserve the link tags if they contain text content
            cell_text_no_images = re.sub(r'<a[^>]*>[\s]*<img[^>]*>[\s]*</a>', '', cell_text)
            cell_text_no_images = re.sub(r'<img[^>]*/?>', '', cell_text_no_images)
            
            # Add image blocks first for images found in this cell
            for src, alt in images_in_cell:
                intuitive_alt = generate_alt_text(src, alt)
                image_block = f'<!-- wp:image {{"sizeSlug":"full","linkDestination":"none","isDecorative":true}} -->\n<figure class="wp-block-image size-full"><img src="{src}" alt="{intuitive_alt}"/></figure>\n<!-- /wp:image -->'
                result_blocks.append(image_block)
            
            # Now process the remaining text content
            if cell_text_no_images.strip():
                # Convert block elements to line breaks but preserve inline formatting
                cell_text_no_images = re.sub(r'</?(?:h[1-6]|p|div)[^>]*>', '\n', cell_text_no_images)
                cell_text_no_images = re.sub(r'<br\s*/?>', '\n', cell_text_no_images)
                
                # Clean up multiple line breaks but preserve intentional spacing
                cell_text_no_images = re.sub(r'\n\s*\n', '\n\n', cell_text_no_images)
                cell_text_no_images = re.sub(r'^\n+|\n+$', '', cell_text_no_images)  # Remove leading/trailing newlines
                
                # Split into separate paragraphs if there are double line breaks
                para_parts = re.split(r'\n\n+', cell_text_no_images)
                
                for part in para_parts:
                    if not part or not part.strip():
                        continue
                        
                    part = re.sub(r'\n+', ' ', part)  # Replace single line breaks with spaces
                    part = re.sub(r'\s+', ' ', part).strip()  # Clean up whitespace
                    
                    if part:
                        result_blocks.append(f'<!-- wp:paragraph -->\n<p>{part}</p>\n<!-- /wp:paragraph -->')
        
        return '\n\n'.join(result_blocks) + '\n' if result_blocks else ''
    
    return re.sub(table_pattern, extract_table_content, content, flags=re.DOTALL)

def convert_images_to_gutenberg(content):
    """Convert img tags to Gutenberg image blocks"""
    img_pattern = r'<img[^>]*src=["\']([^"\']+)["\'][^>]*(?:alt=["\']([^"\']*)["\'][^>]*)?[^>]*/?>'
    
    def generate_alt_text(src, existing_alt=""):
        """Generate intuitive alt text for images"""
        if existing_alt and existing_alt.strip() and existing_alt.lower() not in ['', 'image', 'img', 'picture', 'photo']:
            return existing_alt.strip()
        
        # Extract filename from src and make it more readable
        filename = src.split('/')[-1]
        # Remove file extension
        name_without_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
        
        # Clean up common patterns in filenames
        name_without_ext = re.sub(r'[-_]', ' ', name_without_ext)
        name_without_ext = re.sub(r'\d+x\d+', '', name_without_ext)  # Remove dimensions like 160x235
        name_without_ext = re.sub(r'\s+', ' ', name_without_ext).strip()
        
        # If we have a meaningful name, use it
        if name_without_ext and len(name_without_ext) > 2:
            return name_without_ext.title()
        
        # Fallback to generic description
        return "Book cover image"
    
    def replace_img(match):
        src = match.group(1)
        alt = match.group(2) if match.group(2) else ""
        
        intuitive_alt = generate_alt_text(src, alt)
        
        # Format similar to the example provided
        return f'\n<!-- wp:image {{"sizeSlug":"full","linkDestination":"none","isDecorative":true}} -->\n<figure class="wp-block-image size-full"><img src="{src}" alt="{intuitive_alt}"/></figure>\n<!-- /wp:image -->\n'
    
    return re.sub(img_pattern, replace_img, content, flags=re.DOTALL)

def convert_lists_to_gutenberg(content):
    """Convert HTML lists to Gutenberg list blocks"""
    # Convert unordered lists
    ul_pattern = r'<ul>(.*?)</ul>'
    ol_pattern = r'<ol>(.*?)</ol>'
    li_pattern = r'<li>(.*?)</li>'
    
    def replace_ul(match):
        list_content = match.group(1)
        list_items = re.findall(li_pattern, list_content, re.DOTALL)
        formatted_items = '\n'.join([f'    <li>{item.strip()}</li>' for item in list_items])
        return f'<!-- wp:list -->\n<ul>\n{formatted_items}\n</ul>\n<!-- /wp:list -->'
    
    def replace_ol(match):
        list_content = match.group(1)
        list_items = re.findall(li_pattern, list_content, re.DOTALL)
        formatted_items = '\n'.join([f'    <li>{item.strip()}</li>' for item in list_items])
        return f'<!-- wp:list {{"ordered":true}} -->\n<ol>\n{formatted_items}\n</ol>\n<!-- /wp:list -->'
    
    # Replace unordered lists
    content = re.sub(ul_pattern, replace_ul, content, flags=re.DOTALL)
    # Replace ordered lists
    content = re.sub(ol_pattern, replace_ol, content, flags=re.DOTALL)
    
    return content

def convert_markdown_lists_to_html(content):
    """Convert markdown-style lists to HTML lists first"""
    lines = content.split('\n')
    result_lines = []
    in_ul = False
    in_ol = False
    
    for line in lines:
        stripped = line.strip()
        
        # Check for unordered list items (-, *, +)
        if re.match(r'^[-*+]\s+(.+)', stripped):
            if not in_ul and not in_ol:
                result_lines.append('<ul>')
                in_ul = True
            elif in_ol:
                result_lines.append('</ol>')
                result_lines.append('<ul>')
                in_ol = False
                in_ul = True
            
            item_text = re.sub(r'^[-*+]\s+', '', stripped)
            result_lines.append(f'<li>{item_text}</li>')
            
        # Check for ordered list items (1., 2., etc.)
        elif re.match(r'^\d+\.\s+(.+)', stripped):
            if not in_ol and not in_ul:
                result_lines.append('<ol>')
                in_ol = True
            elif in_ul:
                result_lines.append('</ul>')
                result_lines.append('<ol>')
                in_ul = False
                in_ol = True
            
            item_text = re.sub(r'^\d+\.\s+', '', stripped)
            result_lines.append(f'<li>{item_text}</li>')
            
        else:
            # Close any open lists
            if in_ul:
                result_lines.append('</ul>')
                in_ul = False
            elif in_ol:
                result_lines.append('</ol>')
                in_ol = False
            
            # Add the line as is (if not empty)
            if stripped:
                result_lines.append(line)
    
    # Close any remaining open lists
    if in_ul:
        result_lines.append('</ul>')
    elif in_ol:
        result_lines.append('</ol>')
    
    return '\n'.join(result_lines)

def process_inner_content(inner_content, preserve_tables_as_wp_tables=False):
    """Process the inner content to handle tables, images, lists and paragraphs"""
    
    if preserve_tables_as_wp_tables:
        # Convert tables to WordPress table blocks
        content_with_converted_tables = convert_tables_to_wordpress_table(inner_content)
    else:
        # Convert tables to paragraphs (this also handles images within tables)
        content_with_converted_tables = convert_tables_to_paragraphs(inner_content)
    
    # Only process standalone images if we don't already have image blocks from tables
    if '<!-- wp:image' not in content_with_converted_tables:
        content_with_gutenberg_images = convert_images_to_gutenberg(content_with_converted_tables)
    else:
        content_with_gutenberg_images = content_with_converted_tables
    
    # Convert markdown lists to HTML
    content_with_html_lists = convert_markdown_lists_to_html(content_with_gutenberg_images)
    
    # Then convert HTML lists to Gutenberg blocks
    content_with_gutenberg_lists = convert_lists_to_gutenberg(content_with_html_lists)
    
    # Split content by blocks (lists, images, tables and paragraphs)
    parts = re.split(r'(<!-- wp:(?:list|image|paragraph|table).*?<!-- /wp:(?:list|image|paragraph|table) -->)', content_with_gutenberg_lists, flags=re.DOTALL)
    
    processed_parts = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        # If it's already a Gutenberg block, keep it as is
        if part.startswith('<!-- wp:'):
            processed_parts.append(part)
        else:
            # Process remaining content preserving paragraph structure
            # Split by double line breaks for paragraphs
            paragraphs = re.split(r'\n\s*\n', part)
            
            for para in paragraphs:
                para = para.strip()
                if para and not para.startswith('<!--'):
                    # Preserve single line breaks within paragraphs as spaces
                    para = re.sub(r'\n+', ' ', para)
                    # Clean up extra spaces
                    para = re.sub(r'\s+', ' ', para).strip()
                    if para:
                        processed_parts.append(f'<!-- wp:paragraph -->\n<p>{para}</p>\n<!-- /wp:paragraph -->')
    
    return '\n\n'.join(processed_parts)
    
    processed_parts = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        # If it's already a Gutenberg block, keep it as is
        if part.startswith('<!-- wp:'):
            processed_parts.append(part)
        else:
            # Process remaining content preserving paragraph structure
            # Split by double line breaks for paragraphs
            paragraphs = re.split(r'\n\s*\n', part)
            
            for para in paragraphs:
                para = para.strip()
                if para and not para.startswith('<!--'):
                    # Preserve single line breaks within paragraphs as spaces
                    para = re.sub(r'\n+', ' ', para)
                    # Clean up extra spaces
                    para = re.sub(r'\s+', ' ', para).strip()
                    processed_parts.append(f'<!-- wp:paragraph -->\n<p>{para}</p>\n<!-- /wp:paragraph -->')
    
    return '\n\n'.join(processed_parts)

def convert_slideme_to_gutenberg(content, preserve_tables_as_wp_tables=False):
    pattern = r'\[slideme title="(.+?)"\](.*?)\[/slideme\]'
    blocks = []

    for match in re.finditer(pattern, content, re.DOTALL):
        title = match.group(1).strip()
        inner_content = match.group(2).strip()

        # Process the inner content to handle tables, images, lists and paragraphs
        processed_content = process_inner_content(inner_content, preserve_tables_as_wp_tables)

        block = f'''<!-- wp:cu-block/description-custom {{"title":"{title}","layout":"accordion"}} -->
{processed_content}
<!-- /wp:cu-block/description-custom -->'''
        blocks.append(block)

    return "\n\n".join(blocks)

# Streamlit UI
st.set_page_config(page_title="Slideme to Gutenberg Converter", layout="centered")
st.title("🎛️ Slideme Shortcode to Gutenberg Block Converter")

# Create tabs for different input methods
tab1, tab2 = st.tabs(["📁 Upload File", "📝 Paste Text"])

# Use session state to track content dynamically
if 'content' not in st.session_state:
    st.session_state.content = ""

def update_content_from_file():
    uploaded_file = st.session_state.uploaded_file
    if uploaded_file:
        st.session_state.content = uploaded_file.read().decode("utf-8")
        st.success(f"✅ File uploaded successfully! ({len(st.session_state.content)} characters)")

def update_content_from_text():
    st.session_state.content = st.session_state.text_input
    st.success(f"✅ Text input detected! ({len(st.session_state.content)} characters)")

with tab1:
    st.file_uploader(
        "Upload a file with [slideme] shortcodes", 
        type=["txt", "html", "md"], 
        key="uploaded_file", 
        on_change=update_content_from_file
    )

with tab2:
    st.text_area(
        "Paste your content with [slideme] shortcodes here:",
        height=200,
        placeholder="Paste your content containing [slideme title=\"Your Title\"]Your content here[/slideme] shortcodes...",
        key="text_input",
        on_change=update_content_from_text
    )

# Convert button always visible and dynamically enabled/disabled
st.divider()

# Check for tables in content before conversion
table_preference = False
if st.session_state.content:
    table_count = detect_tables_in_content(st.session_state.content)
    
    if table_count > 0:
        st.info(f"📊 Detected {table_count} table(s) in your content")
        
        table_preference = st.radio(
            "How would you like to handle tables?",
            options=[False, True],
            format_func=lambda x: "Convert tables to paragraphs" if not x else "Preserve tables as WordPress table blocks",
            index=0,
            help="Choose whether to convert tables to text paragraphs or keep them as proper table blocks"
        )
        
        if table_preference:
            st.success("✅ Tables will be preserved as WordPress table blocks")
            # Check if any tables have many columns
            content_lines = st.session_state.content.split('\n')
            has_wide_tables = any(line.count('<td') >= 3 or line.count('<th') >= 3 for line in content_lines)
            if has_wide_tables:
                st.info("💡 **Note for wide tables**: WordPress tables with 3+ columns may benefit from custom CSS for horizontal scrolling. Consider adding this to your theme: `.wp-block-table { overflow-x: auto; }`")
        else:
            st.info("ℹ️ Tables will be converted to paragraphs")

convert_button = st.button(
    "🔄 Convert to Gutenberg Blocks",
    type="primary",
    use_container_width=True,
    disabled=not bool(st.session_state.content)
)

if convert_button:
    with st.spinner("Converting your content..."):
        converted = convert_slideme_to_gutenberg(st.session_state.content, preserve_tables_as_wp_tables=table_preference)
        
        if converted.strip():
            # Store in session state to persist the result
            st.session_state.converted_content = converted
            st.session_state.show_results = True
        else:
            st.session_state.show_results = False
            st.warning("⚠️ No [slideme] shortcodes found in the provided content.")

# Display results if available
if hasattr(st.session_state, 'show_results') and st.session_state.show_results:
    st.subheader("✅ Converted Gutenberg Blocks")
    
    # Create tabs for output options
    output_tab1, output_tab2 = st.tabs(["👀 View Output", "📥 Download"])
    
    with output_tab1:
        st.code(st.session_state.converted_content, language="html")
        
    with output_tab2:
        st.text_area("Copy the converted content:", st.session_state.converted_content, height=300)
        
        # Download button
        st.download_button(
            label="📥 Download as HTML file",
            data=st.session_state.converted_content,
            file_name="converted-gutenberg-blocks.html",
            mime="text/html"
        )
