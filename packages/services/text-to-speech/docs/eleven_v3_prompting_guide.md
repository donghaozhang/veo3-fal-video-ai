# ElevenLabs Eleven v3 (Alpha) - Prompting Best Practices Guide

## Overview

ElevenLabs Eleven v3 is their most advanced text-to-speech model currently in alpha stage. This guide covers the essential techniques and best practices for getting optimal results from this model.

**Key Requirement**: Use prompts longer than 250 characters - very short prompts can cause inconsistent outputs.

## 1. Voice Selection - The Most Critical Factor

Voice selection is the **most important parameter** for Eleven v3. The chosen voice must be similar enough to your desired delivery style.

### Voice Strategy Guidelines

#### Emotionally Diverse Voices
- **Best for**: Expressive Instant Voice Clones (IVCs)
- **Approach**: Include both neutral and dynamic emotional samples
- **Result**: More variable and expressive outputs

#### Targeted Niche Voices  
- **Best for**: Specific use cases (e.g., sports commentary)
- **Approach**: Maintain consistent emotion throughout training data
- **Result**: Specialized performance for particular contexts

#### Neutral Voices
- **Best for**: Stability and reliability
- **Approach**: Consistent, balanced tone
- **Result**: More stable across languages and styles

### Voice Type Considerations

- **Instant Voice Clones (IVCs)**: Currently optimized for v3
- **Professional Voice Clones (PVCs)**: Not fully optimized yet - use IVCs or designed voices instead
- **Voice Library**: Contains 22+ excellent voices specifically curated for v3

## 2. Settings Configuration

### Stability Slider - Primary Control

The stability setting controls how closely the generated voice adheres to the original reference audio:

- **Creative**: Maximum expressiveness and emotion, but prone to hallucinations
- **Natural**: Balanced approach, closest to original voice recording
- **Robust**: Highly stable and consistent (similar to v2), but less responsive to directional prompts

**Recommendation**: Use Creative or Natural for maximum expressiveness with audio tags.

## 3. Audio Tags - Emotional Control System

Audio tags are Eleven v3's breakthrough feature for emotional and vocal control. Tags work by directing the AI to modify delivery style, emotion, and even add sound effects.

### Voice-Related Tags

Control vocal delivery and emotional expression:

```
[laughs], [laughs harder], [starts laughing], [wheezing]
[whispers]
[sighs], [exhales]
[sarcastic], [curious], [excited], [crying], [snorts], [mischievously]
```

**Example:**
```
[whispers] I never knew it could be this way, but I'm glad we're here.
```

### Sound Effects Tags

Add environmental sounds and effects:

```
[gunshot], [applause], [clapping], [explosion]
[swallows], [gulps]
```

**Example:**
```
[applause] Thank you all for coming tonight! [gunshot] What was that?
```

### Experimental/Special Tags

Creative applications (less consistent across voices):

```
[strong X accent] (replace X with desired accent)
[sings], [woo], [fart]
```

**Example:**
```
[strong French accent] "Zat's life, my friend — you can't control everysing."
```

### Tag Effectiveness Rules

1. **Voice Compatibility**: Tags must match the voice's character - don't expect a whispering voice to suddenly shout with `[shout]`
2. **Training Data Dependency**: Some tags work well with certain voices while others may not
3. **Creative Settings**: Tags work best with Creative or Natural stability settings

## 4. Punctuation Impact

Punctuation significantly affects delivery in v3:

- **Ellipses (…)**: Add pauses and dramatic weight
- **Capitalization**: Increases emphasis and volume
- **Standard punctuation**: Provides natural speech rhythm

**Example:**
```
"It was a VERY long day [sigh] … nobody listens anymore."
```

## 5. Single Speaker Applications

### Best Practices

1. **Match tags to voice character**: A meditative voice shouldn't shout; a hyped voice won't whisper convincingly
2. **Use natural speech patterns**: Structure text like real conversation
3. **Combine tags strategically**: Multiple audio tags can create complex emotional delivery

### Example Use Cases

- **Expressive Monologue**: Dynamic emotional range with varied tags
- **Customer Service**: Professional tone with appropriate emotional responses
- **Storytelling**: Dramatic pauses, emphasis, and emotional shifts

## 6. Multi-Speaker Dialogue

v3 excels at handling multi-voice prompts for realistic conversations.

### Implementation Strategy

1. **Assign distinct voices**: Use different voices from Voice Library for each speaker
2. **Clear speaker identification**: Use "Speaker 1:", "Speaker 2:" format
3. **Natural conversation flow**: Include interruptions, overlaps, and realistic timing

### Example Structure:
```
Speaker 1: [excitedly] Sam! Have you tried the new Eleven V3?
Speaker 2: [curiously] Just got it! The clarity is amazing. I can actually do whispers now—
[whispers] like this!
Speaker 1: [impressed] Ooh, fancy! Check this out—
[dramatically] I can do full Shakespeare now!
```

## 7. Advanced Tips and Techniques

### Tag Combinations
- Combine multiple audio tags for complex emotional delivery
- Experiment with different combinations to find optimal results
- Test thoroughly before production use

### Voice Matching Strategy
- Match tags to voice's character and training data
- Serious, professional voices may not respond well to playful tags like `[giggles]`
- Consider the emotional range present in the voice's training samples

### Text Structure Optimization
- Use natural speech patterns and proper punctuation
- Provide clear emotional context
- Structure text to guide the AI's interpretation

### Experimentation Approach
- There are likely many more effective tags beyond the documented list
- Test descriptive emotional states and actions
- Document what works for your specific use cases
- Iterate and refine based on results

## 8. Production Considerations

### Quality Assurance
- Test tags thoroughly with your chosen voice before production
- Verify consistency across different text lengths
- Monitor for hallucinations, especially with Creative settings

### Performance Optimization
- Longer prompts (250+ characters) generally produce more consistent results
- Balance expressiveness with stability based on your use case
- Consider voice selection as your primary quality lever

### Limitations and Workarounds
- PVCs not fully optimized - use IVCs or designed voices
- Some experimental tags may be inconsistent across voices
- Alpha status means ongoing improvements and potential changes

## 9. Key Takeaways

1. **Voice Selection First**: This is your most important decision - choose wisely
2. **Prompt Length Matters**: Use 250+ character prompts for consistency
3. **Stability Settings**: Creative/Natural for expressiveness, Robust for consistency
4. **Tags Are Powerful**: But must match voice character and training data
5. **Punctuation Counts**: Use strategically for pacing and emphasis
6. **Test Everything**: v3 is in alpha - experimentation is key to optimal results

## 10. Future Considerations

As Eleven v3 evolves from alpha to production:
- PVC optimization will improve
- New tags and features may be added
- Performance and consistency will continue to improve
- Best practices may evolve based on user feedback and model updates

---

*This guide is based on ElevenLabs' official documentation for Eleven v3 (alpha). As the model is in active development, practices and capabilities may change.* 