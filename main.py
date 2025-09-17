""""
Auto generate README.md file
"""

import os
import sys
import argparse
from pathlib import Path

from src.repo_analyzer import RepoAnalyzer
from src.readme_generator import ReadmeGenerator
from src.github_api import GitHubAPI

def main():
    parser = argparse.ArgumentParser(description="Auto Generate README.md file for a GitHub repository.")
    parser.add_argument('--repo-path', '-r', default='.',help='Path to Repository (default: current directory)' )
    parser.add_argument('--output-path', '-o', default='README.md', help='Output filename (default: README.md)')
    parser.add_argument('--template', '-t', default='templates/default_template.md', help='Template file to use')
    parser.add_argument('--github-repo', '-g', help='Github repository (format: owner/repo)')
    parser.add_argument('--force', '-f', action='store_true', help='Force overwrite existing README.md')
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path).absolute()
    if not repo_path.exists():
        print(f"Error: Repository path '{repo_path}' does not exist.")
        sys.exit(1)
        
    output_path = repo_path / args.output_path
    if output.path.exists() and not args.force:
        overwrite = input(f"README.md already exists at '{output_path}'. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Operation cancelled,")
            sys.exit(0)
            
    print(f"Analyzing repository at '{repo_path}'...")
        
        
    analyzer = RepoAnalyzer(repo_path)
    repo_data = analyzer.analyze()
    
    if args.github_repo:
        print(f"Fetching Github data for '{args.github_repo}'...")
        github_api = GithubAPI()
        github_data = github_api.get_repo_info(args.github_repo)
        repo_data.update(github_data)
        
        
    print(f"Generating README.md using template '{args.template}'...") 
    generator = ReadmeGenerator(args.template)
    readme_content = generator.generate(repo_data)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)  
        
    print(f"README.md generated succesfully at '{output_path}'")
    
    print("\n" + "="*50)
    print("PREVIEW")
    print("="*50)
    print(readme_content[:500] + "...." if len(readme_content) > 500 else readme_content)
    
    
if __name__ == "__main__":
    main()