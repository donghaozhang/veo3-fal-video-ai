# Parallel Pipeline Execution Design

## Current Limitations

The current pipeline executor (`ChainExecutor`) only supports sequential execution:
- Steps are processed one after another in a for loop
- Each step waits for the previous step to complete
- No support for parallel branches or fan-out patterns

## Proposed Solution

### 1. New Step Types for Parallel Execution

```yaml
# Example: Parallel TTS generation
name: "multi_voice_tts_parallel"
steps:
  - type: "parallel_group"
    name: "generate_voices"
    parallel_steps:
      - type: "text_to_speech"
        model: "elevenlabs"
        params:
          voice: "rachel"
          output_file: "voice_rachel.mp3"
      - type: "text_to_speech"
        model: "elevenlabs"
        params:
          voice: "drew"
          output_file: "voice_drew.mp3"
      - type: "text_to_speech"
        model: "elevenlabs"
        params:
          voice: "bella"
          output_file: "voice_bella.mp3"
```

### 2. Execution Strategies

#### Option A: Thread-based Parallel Execution
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def execute_parallel_group(self, parallel_steps, input_data):
    with ThreadPoolExecutor(max_workers=len(parallel_steps)) as executor:
        futures = {
            executor.submit(self._execute_step, step, input_data): step 
            for step in parallel_steps
        }
        
        results = []
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    
    return results
```

#### Option B: Async-based Parallel Execution
```python
import asyncio

async def execute_parallel_group_async(self, parallel_steps, input_data):
    tasks = [
        self._execute_step_async(step, input_data) 
        for step in parallel_steps
    ]
    results = await asyncio.gather(*tasks)
    return results
```

### 3. Data Flow Patterns

#### Fan-out Pattern
One input → Multiple parallel processes → Multiple outputs
```yaml
steps:
  - type: "text_to_image"
    model: "imagen4"
  - type: "parallel_group"
    parallel_steps:
      - type: "image_to_video"
        model: "hailuo"
        params: {duration: 6}
      - type: "image_to_video"  
        model: "kling"
        params: {duration: 10}
```

#### Fan-in Pattern
Multiple inputs → Single process
```yaml
steps:
  - type: "parallel_group"
    parallel_steps:
      - type: "text_to_image"
        model: "imagen4"
      - type: "text_to_image"
        model: "flux"
  - type: "merge_outputs"
    merge_strategy: "combine_images"
```

### 4. Implementation Plan

1. **Define new StepType enums**:
   - `PARALLEL_GROUP`
   - `MERGE_OUTPUTS`
   - `SPLIT_INPUT`

2. **Update ContentCreationChain**:
   - Add validation for parallel groups
   - Handle parallel step dependencies

3. **Enhance ChainExecutor**:
   - Add parallel execution methods
   - Implement result merging strategies
   - Handle parallel error aggregation

4. **Update YAML schema**:
   - Support `parallel_steps` field
   - Add merge/split configurations

### 5. Example Use Cases

#### Multi-Model Image Generation
```yaml
name: "multi_model_image_comparison"
steps:
  - type: "parallel_group"
    parallel_steps:
      - type: "text_to_image"
        model: "imagen4"
        params: {output_file: "imagen4_result.png"}
      - type: "text_to_image"
        model: "flux"
        params: {output_file: "flux_result.png"}
      - type: "text_to_image"
        model: "seedream"
        params: {output_file: "seedream_result.png"}
```

#### Batch Processing
```yaml
name: "batch_tts_processing"
inputs:
  - "text1.txt"
  - "text2.txt"
  - "text3.txt"
steps:
  - type: "batch_parallel"
    batch_size: 3
    step_template:
      type: "text_to_speech"
      model: "elevenlabs"
      params:
        voice: "rachel"
```

### 6. Benefits

- **Performance**: Process independent tasks simultaneously
- **Flexibility**: Support complex workflows with parallel branches
- **Comparison**: Easy A/B testing of different models/parameters
- **Scalability**: Better resource utilization for batch operations

### 7. Challenges to Address

- **Resource Management**: Limit concurrent operations to avoid overload
- **Error Handling**: Aggregate and report errors from parallel branches
- **Progress Tracking**: Show progress for parallel operations
- **Cost Calculation**: Accurate cost tracking for parallel operations