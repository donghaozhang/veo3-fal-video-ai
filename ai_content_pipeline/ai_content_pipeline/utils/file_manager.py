"""
File management utilities for AI Content Pipeline
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse
import hashlib


class FileManager:
    """
    Manages files and directories for the AI content pipeline.
    
    Handles temporary files, output organization, and file format conversions.
    """
    
    def __init__(self, base_dir: str = None):
        """
        Initialize file manager.
        
        Args:
            base_dir: Base directory for operations
        """
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.output_dir = self.base_dir / "output"
        self.temp_dir = self.base_dir / "temp"
        self.input_dir = self.base_dir / "input"
        
        # Create directories
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
        self.input_dir.mkdir(exist_ok=True)
        
        # Track temporary files for cleanup
        self.temp_files = []
    
    def create_temp_file(self, suffix: str = "", prefix: str = "pipeline_") -> str:
        """
        Create a temporary file.
        
        Args:
            suffix: File suffix (e.g., ".jpg", ".mp4")
            prefix: File prefix
            
        Returns:
            Path to temporary file
        """
        temp_file = tempfile.NamedTemporaryFile(
            suffix=suffix,
            prefix=prefix,
            dir=self.temp_dir,
            delete=False
        )
        temp_path = temp_file.name
        temp_file.close()
        
        self.temp_files.append(temp_path)
        return temp_path
    
    def create_output_path(
        self,
        filename: str,
        step_name: str = None,
        create_dirs: bool = True
    ) -> str:
        """
        Create an output file path.
        
        Args:
            filename: Desired filename
            step_name: Optional step name for organization
            create_dirs: Whether to create directories
            
        Returns:
            Full output file path
        """
        if step_name:
            output_path = self.output_dir / step_name
            if create_dirs:
                output_path.mkdir(exist_ok=True)
        else:
            output_path = self.output_dir
        
        return str(output_path / filename)
    
    def generate_unique_filename(
        self,
        base_name: str,
        extension: str,
        content_hash: str = None
    ) -> str:
        """
        Generate a unique filename.
        
        Args:
            base_name: Base name for the file
            extension: File extension (with or without dot)
            content_hash: Optional content hash for uniqueness
            
        Returns:
            Unique filename
        """
        if not extension.startswith('.'):
            extension = '.' + extension
        
        if content_hash:
            unique_part = content_hash[:8]
        else:
            import time
            unique_part = str(int(time.time()))
        
        return f"{base_name}_{unique_part}{extension}"
    
    def hash_content(self, content: str) -> str:
        """
        Generate hash for content (useful for caching).
        
        Args:
            content: Content to hash
            
        Returns:
            SHA256 hash
        """
        return hashlib.sha256(content.encode()).hexdigest()
    
    def copy_file(self, src: str, dst: str) -> str:
        """
        Copy file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            Destination file path
        """
        dst_path = Path(dst)
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(src, dst)
        return str(dst_path)
    
    def move_file(self, src: str, dst: str) -> str:
        """
        Move file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            Destination file path
        """
        dst_path = Path(dst)
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.move(src, dst)
        return str(dst_path)
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get information about a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary with file information
        """
        path = Path(file_path)
        
        if not path.exists():
            return {"exists": False}
        
        stat = path.stat()
        
        return {
            "exists": True,
            "size": stat.st_size,
            "size_mb": stat.st_size / (1024 * 1024),
            "modified": stat.st_mtime,
            "extension": path.suffix,
            "name": path.name,
            "stem": path.stem
        }
    
    def validate_file_format(self, file_path: str, allowed_formats: List[str]) -> bool:
        """
        Validate file format against allowed formats.
        
        Args:
            file_path: Path to file
            allowed_formats: List of allowed extensions (e.g., [".jpg", ".png"])
            
        Returns:
            True if format is allowed
        """
        extension = Path(file_path).suffix.lower()
        return extension in [fmt.lower() for fmt in allowed_formats]
    
    def organize_outputs(self, results: Dict[str, Any], chain_name: str = None):
        """
        Organize output files into a structured directory.
        
        Args:
            results: Chain execution results
            chain_name: Optional chain name for organization
        """
        if not chain_name:
            chain_name = "pipeline_output"
        
        # Create chain output directory
        chain_dir = self.output_dir / chain_name
        chain_dir.mkdir(exist_ok=True)
        
        # Move output files to organized structure
        for step_name, step_result in results.get("outputs", {}).items():
            output_path = step_result.get("path")
            if output_path and Path(output_path).exists():
                # Create step subdirectory
                step_dir = chain_dir / step_name
                step_dir.mkdir(exist_ok=True)
                
                # Move file to organized location
                new_path = step_dir / Path(output_path).name
                self.move_file(output_path, str(new_path))
                
                # Update result path
                step_result["path"] = str(new_path)
    
    def cleanup_temp_files(self):
        """Clean up all tracked temporary files."""
        cleaned = 0
        
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    cleaned += 1
            except Exception as e:
                print(f"⚠️  Failed to remove temp file {temp_file}: {e}")
        
        self.temp_files.clear()
        
        if cleaned > 0:
            print(f"🗑️  Cleaned up {cleaned} temporary files")
    
    def get_storage_usage(self) -> Dict[str, Any]:
        """
        Get storage usage information.
        
        Returns:
            Dictionary with storage usage stats
        """
        def get_dir_size(path: Path) -> int:
            total = 0
            if path.exists():
                for item in path.rglob('*'):
                    if item.is_file():
                        total += item.stat().st_size
            return total
        
        output_size = get_dir_size(self.output_dir)
        temp_size = get_dir_size(self.temp_dir)
        input_size = get_dir_size(self.input_dir)
        
        return {
            "output_dir": {
                "path": str(self.output_dir),
                "size_bytes": output_size,
                "size_mb": output_size / (1024 * 1024)
            },
            "temp_dir": {
                "path": str(self.temp_dir),
                "size_bytes": temp_size,
                "size_mb": temp_size / (1024 * 1024)
            },
            "input_dir": {
                "path": str(self.input_dir),
                "size_bytes": input_size,
                "size_mb": input_size / (1024 * 1024)
            },
            "total_mb": (output_size + temp_size + input_size) / (1024 * 1024)
        }
    
    def __del__(self):
        """Cleanup temporary files on destruction."""
        try:
            self.cleanup_temp_files()
        except:
            pass