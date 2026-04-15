#!/usr/bin/env python3
"""
Anime Vibes CSS Integration Script
Automatically adds anime-vibes.css to all HTML files in PDF_OUTPUT directory
"""

import os
import re
from pathlib import Path

def add_anime_vibes_to_html(html_file):
    """Add anime-vibes.css link and theme toggle to HTML file"""
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has anime-vibes.css
        if 'anime-vibes.css' in content:
            print(f"✓ Already has anime-vibes.css: {os.path.basename(html_file)}")
            return True
        
        # Find the closing </head> tag and insert anime-vibes.css before it
        head_insert = '''    <!-- Anime Vibes CSS Framework -->
    <link rel="stylesheet" href="anime-vibes.css">
    '''
        
        if '</head>' in content:
            content = content.replace('</head>', head_insert + '</head>')
        
        # Add theme toggle JavaScript before closing </body>
        script_insert = '''
    <script>
        // Theme toggle
        function toggleTheme() {
            document.body.classList.toggle('light-mode');
            const themeBtn = document.getElementById('themeToggleBtn');
            if (document.body.classList.contains('light-mode')) {
                if (themeBtn) themeBtn.textContent = '☀️ Light';
                localStorage.setItem('theme', 'light');
            } else {
                if (themeBtn) themeBtn.textContent = '🌙 Dark';
                localStorage.setItem('theme', 'dark');
            }
        }

        // Load saved theme
        window.addEventListener('DOMContentLoaded', function() {
            const saved = localStorage.getItem('theme') || 'dark';
            const themeBtn = document.getElementById('themeToggleBtn');
            if (saved === 'light') {
                document.body.classList.add('light-mode');
                if (themeBtn) themeBtn.textContent = '☀️ Light';
            }
        });
    </script>
'''
        
        if '</body>' in content:
            content = content.replace('</body>', script_insert + '</body>')
        
        # Write back
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Updated: {os.path.basename(html_file)}")
        return True
        
    except Exception as e:
        print(f"✗ Error updating {os.path.basename(html_file)}: {e}")
        return False

def main():
    """Main function - process all HTML files"""
    
    pdf_output_dir = r"C:\Users\Manikandan Rangarjan\Documents\EJPT\ai-notes\PDF_OUTPUT"
    
    # Check if directory exists
    if not os.path.isdir(pdf_output_dir):
        print(f"Error: Directory not found: {pdf_output_dir}")
        return
    
    # Check if anime-vibes.css exists
    css_file = os.path.join(pdf_output_dir, 'anime-vibes.css')
    if not os.path.isfile(css_file):
        print(f"Error: anime-vibes.css not found in {pdf_output_dir}")
        return
    
    print("\n" + "="*60)
    print("✨ Anime Vibes CSS Integration Script ✨")
    print("="*60 + "\n")
    
    # Find all HTML files
    html_files = list(Path(pdf_output_dir).glob('*.html'))
    
    if not html_files:
        print("No HTML files found in PDF_OUTPUT directory")
        return
    
    print(f"Found {len(html_files)} HTML files\n")
    
    # Process each file
    updated = 0
    for html_file in sorted(html_files):
        # Skip template and index if you want
        if html_file.name == 'template.html':
            continue
        
        if add_anime_vibes_to_html(str(html_file)):
            updated += 1
    
    print(f"\n{'='*60}")
    print(f"✓ Successfully updated {updated}/{len(html_files)} files")
    print(f"{'='*60}\n")
    
    print("Next steps:")
    print("1. Open any HTML file in a browser")
    print("2. You should see the anime-vibes.css styling applied")
    print("3. Click the theme button to toggle dark/light mode")
    print("4. The theme preference is saved to localStorage\n")

if __name__ == '__main__':
    main()
