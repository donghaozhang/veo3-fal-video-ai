"""
Base controller class for command operations.

Provides common functionality and patterns for all command controllers.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import json
from abc import ABC, abstractmethod


class BaseController(ABC):
    """Base class for command controllers with common functionality."""
    
    def __init__(self, input_dir: str = 'input', output_dir: str = 'output', 
                 verbose: bool = True):
        """Initialize the base controller.
        
        Args:
            input_dir: Directory containing input files
            output_dir: Directory for output files
            verbose: Whether to print operation details
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def setup_directories(self) -> bool:
        """Setup and validate required directories.
        
        Returns:
            True if directories are ready, False otherwise
        """
        if not self.input_dir.exists():
            if self.verbose:
                print(f"📁 Input directory '{self.input_dir}' not found")
                print(f"💡 Create a '{self.input_dir}' directory and place your files there")
            return False
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        return True
    
    def print_header(self, title: str, width: int = 50):
        """Print a formatted header for command output.
        
        Args:
            title: Header title
            width: Width of the separator line
        """
        if self.verbose:
            print(title)
            print("=" * width)
    
    def print_file_info(self, files: List[Path], file_type: str = "file"):
        """Print information about discovered files.
        
        Args:
            files: List of file paths
            file_type: Type of files for display
        """
        if self.verbose:
            print(f"📁 Found {len(files)} {file_type}{'s' if len(files) != 1 else ''}:")
            for file in files:
                file_size = file.stat().st_size / (1024 * 1024)  # MB
                print(f"   - {file.name} ({file_size:.1f}MB)")
    
    def save_results(self, results: Dict[str, Any], filename: str) -> bool:
        """Save results to a JSON file.
        
        Args:
            results: Results dictionary to save
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = self.output_dir / filename
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            if self.verbose:
                print(f"💾 Results saved to: {output_path}")
            return True
            
        except Exception as e:
            if self.verbose:
                print(f"❌ Error saving results: {e}")
            return False
    
    def save_text_results(self, content: str, filename: str) -> bool:
        """Save text content to a file.
        
        Args:
            content: Text content to save
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = self.output_dir / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            if self.verbose:
                print(f"💾 Text saved to: {output_path}")
            return True
            
        except Exception as e:
            if self.verbose:
                print(f"❌ Error saving text: {e}")
            return False
    
    def get_user_choice(self, prompt: str, options: Dict[str, str], 
                       default: Optional[str] = None) -> Optional[str]:
        """Get user choice from a list of options.
        
        Args:
            prompt: Prompt message
            options: Dictionary mapping keys to descriptions
            default: Default choice if user presses enter
            
        Returns:
            Selected option key or None if cancelled
        """
        if not self.verbose:
            return default
        
        print(f"\n{prompt}")
        for key, desc in options.items():
            print(f"   {key}. {desc}")
        
        default_text = f" (default: {default})" if default else ""
        choice = input(f"\n🔢 Enter choice{default_text}: ").strip()
        
        if not choice and default:
            return default
        
        return choice if choice in options else None
    
    def get_user_input(self, prompt: str, default: Optional[str] = None) -> str:
        """Get user input with optional default.
        
        Args:
            prompt: Prompt message
            default: Default value if user presses enter
            
        Returns:
            User input or default value
        """
        if not self.verbose:
            return default or ""
        
        default_text = f" (default: {default})" if default else ""
        result = input(f"{prompt}{default_text}: ").strip()
        
        return result if result else (default or "")
    
    def get_yes_no(self, prompt: str, default: bool = False) -> bool:
        """Get yes/no response from user.
        
        Args:
            prompt: Prompt message
            default: Default value if user presses enter
            
        Returns:
            True for yes, False for no
        """
        if not self.verbose:
            return default
        
        default_text = "Y/n" if default else "y/N"
        response = input(f"{prompt} ({default_text}): ").strip().lower()
        
        if not response:
            return default
        
        return response in ['y', 'yes']
    
    def show_progress(self, current: int, total: int, item_name: str = "item"):
        """Show progress information.
        
        Args:
            current: Current item number
            total: Total number of items
            item_name: Name of the item being processed
        """
        if self.verbose:
            print(f"\n📊 Processing {item_name} {current}/{total}")
    
    def show_summary(self, successful: int, failed: int, total: int):
        """Show operation summary.
        
        Args:
            successful: Number of successful operations
            failed: Number of failed operations
            total: Total number of operations
        """
        if self.verbose:
            print(f"\n📊 Summary:")
            print(f"✅ Successful: {successful}")
            print(f"❌ Failed: {failed}")
            print(f"📋 Total: {total}")
            
            if total > 0:
                success_rate = (successful / total) * 100
                print(f"🎯 Success rate: {success_rate:.1f}%")
    
    def check_skip_existing(self, output_path: Path) -> bool:
        """Check if output file exists and ask to skip.
        
        Args:
            output_path: Path to output file
            
        Returns:
            True if should skip, False if should proceed
        """
        if output_path.exists():
            if self.verbose:
                print(f"⏭️  Skipping: {output_path.name} already exists")
            return True
        return False
    
    def get_safe_filename(self, base_name: str, suffix: str = "", 
                         extension: str = "") -> str:
        """Generate a safe filename avoiding conflicts.
        
        Args:
            base_name: Base filename
            suffix: Suffix to add
            extension: File extension
            
        Returns:
            Safe filename
        """
        # Remove problematic characters
        safe_name = "".join(c for c in base_name if c.isalnum() or c in "._-")
        
        if suffix:
            safe_name += f"_{suffix}"
        
        if extension and not extension.startswith('.'):
            extension = f".{extension}"
        
        return safe_name + extension
    
    @abstractmethod
    def run(self) -> bool:
        """Run the controller's main operation.
        
        Returns:
            True if successful, False otherwise
        """
        pass
    
    def validate_dependencies(self) -> Dict[str, bool]:
        """Validate required dependencies.
        
        Returns:
            Dictionary mapping dependency names to availability status
        """
        # Base implementation - subclasses should override
        return {}
    
    def print_dependency_status(self, deps: Dict[str, bool]):
        """Print dependency status information.
        
        Args:
            deps: Dictionary mapping dependency names to availability status
        """
        if not self.verbose:
            return
        
        print("\n🔧 Dependency Status:")
        for dep, available in deps.items():
            status = "✅ Available" if available else "❌ Missing"
            print(f"   {dep}: {status}")
        
        missing = [dep for dep, available in deps.items() if not available]
        if missing:
            print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
            return False
        
        print("✅ All dependencies available")
        return True