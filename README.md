# GSDSIC

## FAQ Database Template

A searchable FAQ database template using Python with full-text search, tag filtering, and CRUD operations.

### Quick Start

```bash
# Import sample data
python3 faq_cli.py import sample_faq_data.json

# Search the database
python3 faq_cli.py search "password"

# Run examples
python3 example_usage.py
```

### Documentation

See [FAQ_README.md](FAQ_README.md) for complete documentation including:
- Setup and installation
- Python API reference
- CLI usage guide
- Integration examples
- Advanced features

### Features

- ✅ SQLite-based storage (portable, no dependencies)
- ✅ Full-text search across questions and answers
- ✅ Tag/keyword filtering
- ✅ Category organization
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Export to JSON and CSV
- ✅ Command-line interface
- ✅ Well-documented Python API

### Files

- `faq_database.py` - Core FAQ database module
- `faq_cli.py` - Command-line interface
- `example_usage.py` - Example usage demonstrations
- `sample_faq_data.json` - Sample FAQ entries
- `FAQ_README.md` - Complete documentation