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
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React',
            '.tsx': 'React/TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.cs': 'CSharp',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.vue': 'Vue',
            '.dart': 'Dart',
            '.kt': 'Kotlin',
            '.swift': 'Swift',
        }
        
        found_languages = set()
        for file_path in self.repo_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                found_languages.add(extensions[file_path.suffix])

        return sorted(list(found_languages))
    
    def _get_dependencies(self) -> Dict[str, List[str]]:
        deps = {}
        
        requirements_txt = self.repo_path / 'requirements.txt'
        if requirements_txt.exists():
            try:
                content = requirements_txt.read_text()
                deps['python'] = [line.strip().split('==')[0].split('>=')[0].split('=<')[0]
                                  for line in content.split('\n')
                                  if line.strip() and not line.startsqith('#')]
            except:
                pass
            
        package_json = self.repo_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    deps['nodejs'] = list(data.get('dependencies', {}).keys())
            except:
                pass
            
            return deps
        
        
    def _get_scripts(self) -> Dict[str, str]:
        scripts = {}
        
        package_json = self.repo_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json) as d:
                    data = json.load(f)
                    scripts.update(data.get('scripts', {}))
            except:
                pass
            
            
            makefile = self.repo_path / 'Makefile'
            if makefile.exists():
                try:
                    content = makefile.read_text()
                    targets = re.findall(r'^([a-zA-Z_][a-zA-Z0-9_-]*)\s*:', content, re.MULTILINE)
                    for target in targets:
                        scripts[f'make {target}'] = f'Run {target} target'
                        
                except:
                    pass
                
                return scripts
    def _get_directory_structure(self) -> List[str]:
        important_dirs = []
        important_files = []
        
        for item in slef.repo_path.iterdir():
            if item.is_dir() and not item.name.startswith('.') and item.name not in ['node_modules', '__pycache__', 'venv']:
                important_dirs.append(item.name + '/')
            elif item.is_file() and item.name in ['README.md', 'LICENSE','setup.py', 'package.json', 'Dockerfile', 'docker-compose.yml' ]:
                important_files.append(item.name)
                
        return sorted(important_dirs) + sorted(important_files)
    
    def _detect_features(self) -> List[str]:
        features = []
        
        if (self.repo_path / 'Dockerfile').exists():
            features.append('Docker support')
            
        if (self.repo_path / '.github' / 'workflows').exists():
            features.append('Github Actions')
            
        test_dirs = ['tests', 'test', '__tests__']
        if any((self.repo_path / d).exists() for d in test_dirs):
            features.append('Automated testing')
            
        docs_dirs = ['docs', 'documentation']
        if any((self.repo_path / d).exists() for d in docs_dirs):
            features.append('Documentation')
            
        return features
    
    def _get_installation_instructions(self) -> List[str]:
        instructions = []
        primary_lang = self._detect_primary_language()
        
        if primary_lang == 'Python':
            if (self.repo_path / 'requirements.txt').exists():
                instructions.extend([
                    'pip install -r requirements.txt'
                ])
            elif (self.repo_path / 'setup.py').exists():
                instructions.extend([
                    'pip install .'
                ])
                
        elif primary_lang in ['JavaScript', 'TypeScript']:
            if (self.repo_path / 'package.json').exists():
                instructions.extend([
                    'npm install',
                    '# or',
                    'yarn install'
                ])
                
        return instructions
    
    def _get_usage_example(self) -> List[str]:
        examples = []
        primary_lang = self._detect_primary_language()
        
        if primary_lang == 'Python':
            if 