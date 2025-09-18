import re
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

class ReadmeGenerator:
    def __init__(self, template_path: str = "templates/default.md"):
        self.template_path = Path(template_path)
        
    def generator(self, repo_data: Dict[str, Any]) -> str:
        if not self.template_path.exists():
            template_content = self._get_default_template()
        else:
            template_content = self.template_path.read_text(encoding='utf-8')
            
        content = self._process_template(template_content, repo_data)
        
        return content
    
    def _get_default_template(self) -> str:
        return """# {{repo_name}}

{{description}}

{{#badges}}
{{badges}}
{{/badges}}

## 🚀 Features

{{#features}}
{{features}}
{{/features}}

## 📋 Requirements

{{#languages}}
- **Languages**: {{languages}}
{{/languages}}
{{#dependencies.python}}
- **Python Dependencies**: See `requirements.txt`
{{/dependencies.python}}
{{#dependencies.nodejs}}
- **Node.js Dependencies**: See `package.json`
{{/dependencies.nodejs}}

## 🔧 Installation

{{#installation}}
```bash
{{installation}}
```
{{/installation}}

## 📖 Usage

{{#usage}}
```bash
{{usage}}
```
{{/usage}}

{{#scripts}}
## 📜 Available Scripts

{{scripts}}
{{/scripts}}

{{#structure}}
## 📁 Project Structure

```
{{structure}}
```
{{/structure}}

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

{{#license}}
## 📝 License

This project is licensed under the {{license}} License.
{{/license}}

{{#author}}
## 👤 Author

**{{author.name}}**{{#author.email}} ({{author.email}}){{/author.email}}
{{/author}}

---

*This README was generated automatically on {{current_date}}*
"""
    def _process_conditionals(self, content: str, data: Dict[str, Any]) -> str:
        pattern = r'\{\{#([^}]+)\}\}(.*?)\{\{/\1\}\}'
        
        def replace_conditional(match):
            key = match.group(1)
            block_content = match.group(2)
            
            value = self._get_nested_value(data, key)
            if self._is_truthy(value):
                return block_content
            else:
                return ''