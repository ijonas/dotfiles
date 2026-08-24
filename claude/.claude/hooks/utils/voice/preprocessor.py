#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "re",
# ]
# ///

import re
import sys

class VoicePreprocessor:
    """Preprocessor for cleaning up voice commands before execution."""
    
    def __init__(self):
        # Common speech artifacts to remove
        self.artifacts = [
            r'\b(um|uh|hmm|er|ah)\b',
            r'\b(like|you know|basically|actually)\b',
            r'\s+',  # Multiple spaces
        ]
        
        # Voice command transformations
        self.transformations = [
            # Politeness removals
            (r'\b(please|could you|can you|would you)\s*', ''),
            (r'\b(thanks?|thank you)\b', ''),
            
            # Natural language to command transformations
            (r'\b(show me|display|let me see)\s+', ''),
            (r'\b(create|make|build)\s+(a|an)?\s*', ''),
            (r'\b(open|go to|navigate to)\s+', ''),
            (r'\b(run|execute|do)\s+', ''),
            (r'\b(find|search for|look for)\s+', 'search '),
            (r'\b(edit|modify|change)\s+', 'edit '),
            (r'\b(delete|remove)\s+', 'rm '),
            (r'\b(list|show)\s+(all\s+)?', 'ls '),
            
            # File/directory references
            (r'\b(the\s+)?file\s+called\s+', ''),
            (r'\b(the\s+)?directory\s+(called\s+)?', ''),
            (r'\b(in\s+the\s+)?current\s+directory\b', '.'),
            (r'\b(parent\s+)?directory\b', '..'),
            
            # Common programming terms
            (r'\b(source\s+)?code\b', 'src'),
            (r'\bdocumentation\b', 'docs'),
            (r'\bconfiguration\b', 'config'),
            (r'\breadme\s+file\b', 'README.md'),
            
            # Git commands
            (r'\b(git\s+)?commit\s+(the\s+)?changes?\b', 'git commit'),
            (r'\b(git\s+)?status\b', 'git status'),
            (r'\b(git\s+)?push\b', 'git push'),
            (r'\b(git\s+)?pull\b', 'git pull'),
            
            # Common misspellings/homophones
            (r'\bthere\b', 'their'),  # Context-dependent, might need smarter logic
            (r'\bto\b(?=\s+\w+\.md)', 'two'),  # Numbers in filenames
            (r'\bfor\b(?=\s+loop)', '4'),
            
            # Slash command triggers
            (r'^(run\s+)?(slash\s+)?', '/'),  # "slash read" -> "/read"
        ]
        
        # Command aliases for voice-friendly names
        self.aliases = {
            'read me': '/read',
            'commit': '/commit',
            'create pr': '/createpr',
            'create pull request': '/createpr',
            'dry code': '/dry_code',
            'issues': '/issues',
            'open issues': '/open-issues',
            'product brief': '/product-brief',
        }
    
    def preprocess(self, text):
        """
        Clean and transform voice input text.
        
        Args:
            text: Raw transcribed text from speech-to-text
            
        Returns:
            str: Cleaned and transformed command text
        """
        if not text:
            return text
            
        # Convert to lowercase for processing
        processed = text.lower().strip()
        
        # Remove common speech artifacts
        for pattern in self.artifacts:
            processed = re.sub(pattern, ' ', processed, flags=re.IGNORECASE)
        
        # Apply transformations
        for pattern, replacement in self.transformations:
            processed = re.sub(pattern, replacement, processed, flags=re.IGNORECASE)
        
        # Check for exact aliases
        if processed in self.aliases:
            processed = self.aliases[processed]
        
        # Clean up extra whitespace
        processed = re.sub(r'\s+', ' ', processed).strip()
        
        return processed
    
    def validate_command(self, command):
        """
        Validate that the processed command is safe to execute.
        
        Args:
            command: Processed command text
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not command:
            return False, "Empty command"
        
        # Check for potentially dangerous commands
        dangerous_patterns = [
            r'\brm\s+-rf\s+/',  # rm -rf /
            r'\bsudo\s+rm',    # sudo rm
            r'\bformat\b',     # format command
            r'\bdel\s+\*',     # del *
            r'\bmv\s+.*\s+/dev/null',  # move to /dev/null
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"Potentially dangerous command detected: {command}"
        
        return True, ""
    
    def suggest_corrections(self, original, processed):
        """
        Generate suggestions if the processed command differs significantly.
        
        Args:
            original: Original transcribed text
            processed: Processed command text
            
        Returns:
            list: List of suggestion strings
        """
        suggestions = []
        
        if original.lower() != processed.lower():
            suggestions.append(f"Converted '{original}' to '{processed}'")
        
        # Check if it looks like a slash command
        if processed.startswith('/'):
            suggestions.append("Detected slash command")
        elif not processed.startswith(('ls', 'cd', 'pwd', 'git', 'cargo', 'npm')):
            suggestions.append("Note: This may not be a recognized command")
        
        return suggestions

def main():
    """Command-line interface for voice preprocessor."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Voice command preprocessor')
    parser.add_argument('text', nargs='*', help='Text to preprocess')
    parser.add_argument('--validate', action='store_true',
                        help='Validate the processed command')
    parser.add_argument('--suggestions', action='store_true',
                        help='Show processing suggestions')
    parser.add_argument('--stdin', action='store_true',
                        help='Read text from stdin')
    
    args = parser.parse_args()
    
    # Get input text
    if args.stdin:
        text = sys.stdin.read().strip()
    elif args.text:
        text = ' '.join(args.text)
    else:
        print("Error: No input text provided", file=sys.stderr)
        sys.exit(1)
    
    # Process the text
    preprocessor = VoicePreprocessor()
    processed = preprocessor.preprocess(text)
    
    # Validate if requested
    if args.validate:
        is_valid, error_msg = preprocessor.validate_command(processed)
        if not is_valid:
            print(f"❌ Validation failed: {error_msg}", file=sys.stderr)
            sys.exit(1)
    
    # Show suggestions if requested
    if args.suggestions:
        suggestions = preprocessor.suggest_corrections(text, processed)
        for suggestion in suggestions:
            print(f"💡 {suggestion}", file=sys.stderr)
    
    # Output the processed command
    print(processed)

if __name__ == "__main__":
    main()