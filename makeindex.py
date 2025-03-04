import os
import glob
import re
import sys
import urllib.parse

def generate_markdown_index(root_folder):
    """
    Generates a Markdown index table for files in a directory.

    Args:
        root_folder (str): The root directory to search within.

    Returns:
        str: A Markdown table as a string.
    """

    file_data = []
    md_files = glob.glob(os.path.join(root_folder, '**/*.md'), recursive=True)

    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

            # Extract Name
            name_match = re.search(r"# Name\s*\n(.*?)\n", content, re.DOTALL)
            name = name_match.group(1).strip() if name_match else "No Name"

            # Extract Description
            description_match = re.search(r"# Description\s*\n(.*?)\n", content, re.DOTALL)
            description = description_match.group(1).strip() if description_match else "No Description"

            # Create relative link
            relative_path = os.path.relpath(md_file, root_folder)
            encoded_path = urllib.parse.quote(relative_path)
            # Create GitHub-compatible link with badge
            badge_link = "[![View](https://img.shields.io/badge/View-blue)](" + encoded_path + ")"

            file_data.append((name, description, badge_link))

    # Sort alphabetically by name
    file_data.sort(key=lambda x: x[0].lower())

    # Create Markdown table
    table_header = "## Alphabetical Index\n\n| Name | Description | Link |\n|---|---|---|"
    table_rows = [f"| {name} | {description} | {badge_link} |" for name, description, badge_link in file_data]
    markdown_table = table_header + "\n" + "\n".join(table_rows)

    return markdown_table

def update_readme_with_index(readme_path, index_content):
    """
    Updates the README.md file with the generated index.
    
    Args:
        readme_path (str): Path to the README.md file
        index_content (str): The index content to insert
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the current README content
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        # Find existing index section or insert after the title
        index_pattern = r'## Alphabetical Index\n\n\|.*?\n(?:\|.*?\n)+'
        if re.search(index_pattern, readme_content, re.DOTALL):
            # Replace existing index
            updated_content = re.sub(index_pattern, index_content + '\n\n', readme_content, flags=re.DOTALL)
        else:
            # Insert after the title (assuming the first line is the title)
            title_end = readme_content.find('\n') + 1
            updated_content = readme_content[:title_end] + '\n' + index_content + '\n\n' + readme_content[title_end:]
        
        # Write the updated content back to the README
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return True
    except Exception as e:
        print(f"Error updating README: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    configs_path = "configs"  # Replace with the actual path to your 'configs' folder
    markdown_output = generate_markdown_index(configs_path)
    readme_path = "README.md"
    if update_readme_with_index(readme_path, markdown_output):
        print(f"Successfully updated {readme_path} with the alphabetical index.")
    else:
        print(f"Failed to update {readme_path}.")