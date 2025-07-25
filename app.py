import streamlit as st
import re
import base64

def convert_lists_to_gutenberg(content):
    """Convert HTML lists to Gutenberg list blocks"""
    # Convert unordered lists
    ul_pattern = r'<ul>(.*?)</ul>'
    ol_pattern = r'<ol>(.*?)</ol>'
    li_pattern = r'<li>(.*?)</li>'
    
    def replace_ul(match):
        list_content = match.group(1)
        list_items = re.findall(li_pattern, list_content, re.DOTALL)
        items_html = ''.join([f'<li>{item.strip()}</li>' for item in list_items])
        return f'<!-- wp:list -->\n<ul>{items_html}</ul>\n<!-- /wp:list -->'
    
    def replace_ol(match):
        list_content = match.group(1)
        list_items = re.findall(li_pattern, list_content, re.DOTALL)
        items_html = ''.join([f'<li>{item.strip()}</li>' for item in list_items])
        return f'<!-- wp:list {{"ordered":true}} -->\n<ol>{items_html}</ol>\n<!-- /wp:list -->'
    
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

def process_inner_content(inner_content):
    """Process the inner content to handle lists and paragraphs"""
    # First convert markdown lists to HTML
    content_with_html_lists = convert_markdown_lists_to_html(inner_content)
    
    # Then convert HTML lists to Gutenberg blocks
    content_with_gutenberg_lists = convert_lists_to_gutenberg(content_with_html_lists)
    
    # Split content by list blocks and paragraphs
    parts = re.split(r'(<!-- wp:list.*?<!-- /wp:list -->)', content_with_gutenberg_lists, flags=re.DOTALL)
    
    processed_parts = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        # If it's already a Gutenberg list block, keep it as is
        if part.startswith('<!-- wp:list'):
            processed_parts.append(part)
        else:
            # Split remaining content into paragraphs
            paragraphs = [p.strip() for p in part.split('\n\n') if p.strip()]
            for para in paragraphs:
                if para and not para.startswith('<!--'):
                    processed_parts.append(f'<!-- wp:paragraph -->\n<p>{para}</p>\n<!-- /wp:paragraph -->')
    
    return '\n'.join(processed_parts)

def convert_slideme_to_gutenberg(content):
    pattern = r'\[slideme title="(.+?)"\](.*?)\[/slideme\]'
    blocks = []

    for match in re.finditer(pattern, content, re.DOTALL):
        title = match.group(1).strip()
        inner_content = match.group(2).strip()

        # Process the inner content to handle lists and paragraphs
        processed_content = process_inner_content(inner_content)

        block = f'''<!-- wp:cu-block/description-custom {{"title":"{title}","layout":"accordion"}} -->
{processed_content}
<!-- /wp:cu-block/description-custom -->\n'''
        blocks.append(block)

    return "\n".join(blocks)

# Streamlit UI
st.set_page_config(page_title="Slideme to Gutenberg Converter", layout="centered")
st.title("🎛️ Slideme Shortcode to Gutenberg Block Converter")

# Create tabs for different input methods
tab1, tab2 = st.tabs(["📁 Upload File", "📝 Paste Text"])

content = None

with tab1:
    uploaded_file = st.file_uploader("Upload a file with [slideme] shortcodes", type=["txt", "html", "md"])
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        st.success(f"✅ File uploaded successfully! ({len(content)} characters)")

with tab2:
    text_input = st.text_area(
        "Paste your content with [slideme] shortcodes here:",
        height=200,
        placeholder="Paste your content containing [slideme title=\"Your Title\"]Your content here[/slideme] shortcodes..."
    )
    if text_input.strip():
        content = text_input
        st.success(f"✅ Text input detected! ({len(content)} characters)")

# Show convert button only if content is available
if content:
    st.divider()
    
    # Convert button
    if st.button("🔄 Convert to Gutenberg Blocks", type="primary", use_container_width=True):
        with st.spinner("Converting your content..."):
            converted = convert_slideme_to_gutenberg(content)
            
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
