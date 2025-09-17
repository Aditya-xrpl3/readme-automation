import os
import json
import ymal
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
import re


class RepoAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self_data = {}
        
    def analyze(self) -> Dict[str, Any]:
        self.data = {
            'repo_name': self._get_repo_name(),
            'description': self._get_description(),
            'language': self._get_detect_primary_language(),
            'languages': self._get_all_languages(),
            'dependencies': self._get_dependencies(),
            'scripts': self._get_scripts(),
            'structure': self._get_directory_structure(),
            'features': self._get_detect_features(),
            'installation': self._get_installation_instructions(),
            'usage': self._get_usage_example(),
            'license': self._get_license(),
            'author': self._get_author_info(),
            'git_info': self._get_git_info(),
        }
        return self.data
    def _get_repo_name(self) -> str:
        return self.repo_path.name
    def _get_description(self) -> 'str':
        package_json = self.repo_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    if 'description' in data:
                        return data['description']
            except:
                pass
            
        setup_py = self.repo_path / 'setup.py'
        if setup_py.exist():
            try:
                content = setup_py.read_text()
                desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
                if desc_match:
                    return desc_match.group(1)
            except:
                pass
            
        pyproject = self.repo_path / 'pyproject.toml'
        if pyproject.exist():
            try:
                content = pyproject.read_text()
                desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
                if desc_match:
                    return desc_match.group(1)
            except:
                pass
            
        return f"A {self._detect_primary_language()} project"
    
    def _detect_primary_language(self) -> str:
        language_files = {
            'Python' : ['*.py', 'requirements.txt', 'setup.py', 'pyproject.toml'],
            'JavaScript' : ['*.js', 'package.json', '*.jsx'],
            'TypeScript' : ['*.ts', '*tsx', 'tsconfig.json'],
            'Java' : ['*.java', 'pom.xml', 'build.gradle',],
            'C++' : ['*.cpp', '*.hpp', '*.cc', 'CMakeLists.txt'],
            'C' : ['*.c', '*.h', 'Makefile'],
            'Go' : ['*.go', 'go.mod'],
            'Rust' : ['*.rs', 'Cargo.toml'],
            'PHP' : ['*.php', 'composer.json'],
            'Ruby' : ['*.rb', 'Gemfile'],
            'C#' : ['*.cs', '*.csproj'],
        }
        
        scores = {}
        for lang, patterns in language_files.items():
            score = 0
            for pattern in patterns:
                files = list(self.repo_path.rglob(pattern))
                score += len(files)
            scores[lang] = score
            
        if scores:
            return max(scores.item(), key=lambda x: x[1]) [0]
        return 'Unknown'
    
    def _get_all_languages(self) -> List[str]:
        extensions = {
            '.py': 'Python',
        }