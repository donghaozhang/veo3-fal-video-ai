# ElevenLabs Controls Guide - Mastering Delivery, Pronunciation & Emotion

## Overview

This guide covers the technical control methods available in ElevenLabs text-to-speech models for precise control over delivery, pronunciation, and emotional expression. These techniques work across multiple ElevenLabs models and provide practical solutions while advanced features like "Director's Mode" are in development.

## 1. Pause Control

### Break Tags - Precise Timing Control

Use `<break time="x.xs" />` for natural pauses up to 3 seconds:

```xml
"Hold on, let me think." <break time="1.5s" /> "Alright, I've got it."
```

### Break Tag Best Practices

- **Maximum Duration**: Up to 3 seconds per break
- **Consistency**: Use break tags consistently to maintain natural speech flow
- **Limitation**: Excessive use can cause instability (AI might speed up or introduce artifacts)
- **Voice-Specific Behavior**: Different voices handle pauses differently, especially those trained with filler sounds

### Alternative Pause Methods

When break tags aren't suitable, try these alternatives (less consistent but sometimes effective):

```
"It… well, it might work."           # Ellipses for hesitant tones
"Wait — what's that noise?"          # Dashes for short pauses
```

## 2. Pronunciation Control

### Phoneme Tags - Precise Pronunciation

Specify exact pronunciation using SSML phoneme tags with two supported alphabets:

- **CMU Arpabet** (Recommended for consistency)
- **International Phonetic Alphabet (IPA)**

**Model Compatibility**: Only works with:
- Eleven Flash v2
- Eleven Turbo v2  
- Eleven English v1

#### CMU Arpabet Example:
```xml
<phoneme alphabet="cmu-arpabet" ph="M AE1 D IH0 S AH0 N">
Madison
</phoneme>
```

#### IPA Example:
```xml
<phoneme alphabet="ipa" ph="ˈmædɪsən">
Madison
</phoneme>
```

### Phoneme Tag Rules

1. **Single Words Only**: Each phoneme tag works for individual words only
2. **Multiple Words**: Create separate tags for first and last names
3. **Stress Marking**: Essential for multi-syllable words

#### Correct Multi-Syllable Example:
```xml
<phoneme alphabet="cmu-arpabet" ph="P R AH0 N AH0 N S IY EY1 SH AH0 N">
pronunciation
</phoneme>
```

### Alias Tags - Alternative Spelling Method

For models that don't support phoneme tags, use creative spelling approaches:

- **Capital Letters**: "trapezIi" instead of "trapezii" 
- **Dashes, Apostrophes**: Creative punctuation for emphasis
- **Single Quotes**: Around specific letters

#### Alias Tag Structure:
```xml
<lexeme>
<grapheme>Claughton</grapheme>
<alias>Cloffton</alias>
</lexeme>
```

#### Acronym Control:
```xml
<lexeme>
<grapheme>UN</grapheme>
<alias>United Nations</alias>
</lexeme>
```

## 3. Pronunciation Dictionaries

### Overview
Pronunciation dictionaries allow you to create consistent pronunciation rules across entire projects. Available in:
- Studio
- Dubbing Studio  
- Speech Synthesis API

### Dictionary Implementation

1. **Upload**: TXT or .PLS format files
2. **Auto-Application**: Automatically recalculates and marks content for re-conversion
3. **Search Order**: Dictionary is checked start-to-end, first match wins
4. **Case Sensitivity**: All searches are case sensitive

### Dictionary File Examples

#### CMU Arpabet Dictionary (.pls):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<lexicon version="1.0"
xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon
http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"
alphabet="cmu-arpabet" xml:lang="en-GB">
<lexeme>
<grapheme>apple</grapheme>
<phoneme>AE P AH L</phoneme>
</lexeme>
<lexeme>
<grapheme>UN</grapheme>
<alias>United Nations</alias>
</lexeme>
</lexicon>
```

### Dictionary Generation Tools

Open-source tools for creating pronunciation dictionaries:

- **Sequitur G2P**: Learns pronunciation rules from data
- **Phonetisaurus**: G2P system trained on existing dictionaries
- **eSpeak**: Speech synthesizer with phoneme transcription
- **CMU Pronouncing Dictionary**: Pre-built English dictionary

## 4. Emotion Control

### Narrative Context Method

Use descriptive narrative to convey emotions:

```
"You're leaving?" she asked, her voice trembling with sadness.
"That's it!" he exclaimed triumphantly.
```

### Explicit Dialogue Tags

More predictable than context alone, but requires post-production editing:

```
"I can't believe this," he said angrily.
"Thank you so much," she whispered gratefully.
```

**Note**: The model will speak the emotional guidance text, which needs to be removed in post-production.

## 5. Pace Control

### Speed Setting (Primary Method)

Available in Text to Speech, Studio, and Conversational AI:

- **Default**: 1.0 (no adjustment)
- **Slow Down**: 0.7 minimum
- **Speed Up**: 1.2 maximum
- **Quality Impact**: Extreme values may affect audio quality

### Voice Training Impact

Pacing is heavily influenced by the training audio:
- Use longer, continuous samples when creating voices
- Avoid unnaturally fast speech by providing quality training data

### Narrative Pacing Control

Write in natural, narrative style to influence pacing:

```
"I… I thought you'd understand," he said, his voice slowing with disappointment.
```

## 6. Creative Control Techniques

### 1. Narrative Styling
Write prompts like screenplays to guide tone and pacing:

```
[Character takes a deep breath, speaking slowly and deliberately]
"This is the most important decision of my life."
```

### 2. Layered Outputs
- Generate speech and sound effects separately
- Combine using audio editing software
- Allows for complex compositions with precise timing

### 3. Phonetic Experimentation
- Try alternate spellings for difficult pronunciations
- Use phonetic approximations
- Test different approaches for challenging words

### 4. Manual Adjustments
- Combine individual elements in post-production
- Layer sound effects manually for precise timing
- Use audio editing for complex sequences

### 5. Feedback Iteration
- Tweak descriptions, tags, and emotional cues
- Test different approaches systematically
- Document what works for future reference

## 7. Troubleshooting Common Issues

### Inconsistent Pauses
- **Problem**: Irregular pause timing
- **Solution**: Use proper `<break time="x.xs" />` syntax
- **Alternative**: Try dashes or ellipses for simpler pauses

### Pronunciation Errors
- **Problem**: Incorrect word pronunciation
- **Solution**: Use CMU Arpabet phoneme tags for precision
- **Fallback**: Try IPA or creative spelling approaches

### Emotion Mismatch
- **Problem**: Wrong emotional tone
- **Solution**: Add narrative context or explicit dialogue tags
- **Post-Production**: Remove guidance text in audio editing

### Pacing Issues
- **Problem**: Too fast or too slow speech
- **Solution**: Adjust speed setting (0.7-1.2 range)
- **Prevention**: Use quality training audio for voice creation

## 8. Best Practices Summary

### Planning Phase
1. **Choose the right method**: Phoneme tags for precision, aliases for compatibility
2. **Consider model limitations**: Check which features work with your chosen model
3. **Plan for post-production**: Budget time for removing guidance text

### Implementation Phase
1. **Start simple**: Test basic controls before complex combinations
2. **Use consistent syntax**: Follow exact formatting for tags
3. **Test incrementally**: Verify each control works before adding more

### Quality Assurance
1. **Listen carefully**: Check for artifacts from excessive break tags
2. **Verify pronunciation**: Confirm phoneme tags produce expected results
3. **Remove guidance text**: Clean up emotional direction in post-production

### Optimization
1. **Document successful approaches**: Keep track of what works
2. **Iterate systematically**: Make one change at a time
3. **Consider workflow**: Balance control precision with production efficiency

## 9. Future Developments

ElevenLabs is actively developing "Director's Mode" for even greater control. Until then, these techniques provide comprehensive control over:

- **Timing**: Precise pause control
- **Pronunciation**: Exact phonetic specification
- **Emotion**: Contextual and explicit emotional direction
- **Pacing**: Speed and rhythm control
- **Quality**: Post-production refinement techniques

---

*This guide is based on ElevenLabs' official controls documentation. As features evolve, some techniques may be superseded by more advanced controls like Director's Mode.* 