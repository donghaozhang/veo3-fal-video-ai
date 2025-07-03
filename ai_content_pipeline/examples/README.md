# AI Content Pipeline Examples

This directory contains example scripts and proof-of-concept implementations that demonstrate various pipeline capabilities.

## 📁 Files

### `parallel_executor_poc.py`
**Purpose**: Proof-of-concept demonstration of parallel vs sequential execution

**What it does**:
- Demonstrates basic parallel execution concepts
- Compares performance between parallel and sequential TTS generation
- Shows thread-based concurrent execution

**Usage**:
```bash
cd ai_content_pipeline
python examples/parallel_executor_poc.py
```

**Note**: This is an educational example. For production use, use the built-in parallel pipeline features via YAML configuration.

## 🎯 When to use these examples

- **Learning**: Understand how parallel execution works under the hood
- **Benchmarking**: Compare performance characteristics
- **Development**: Reference implementations for new features
- **Debugging**: Isolated test cases for specific functionality

## 🚀 Production vs Examples

| Feature | Example (POC) | Production Pipeline |
|---------|---------------|-------------------|
| Purpose | Demonstration | Real workflows |
| Configuration | Hardcoded | YAML-based |
| Error handling | Basic | Comprehensive |
| Integration | Standalone | Full pipeline |
| Documentation | Inline comments | Complete docs |

## 📚 Related Documentation

- [GETTING_STARTED.md](../docs/GETTING_STARTED.md) - Production usage guide
- [YAML_CONFIGURATION.md](../docs/YAML_CONFIGURATION.md) - Configuration reference
- [parallel_pipeline_design.md](../docs/parallel_pipeline_design.md) - Design concepts

## 🔧 Development

These examples can serve as starting points for:
- New parallel execution patterns
- Performance optimization experiments
- Feature prototyping
- Educational demonstrations

Feel free to modify and experiment with these examples!