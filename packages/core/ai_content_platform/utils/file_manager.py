"""Async file manager for handling uploads, downloads, and file operations."""

import asyncio
import hashlib
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List
import aiofiles
import aiohttp
from urllib.parse import urlparse

from ai_content_platform.core.exceptions import FileOperationError
from ai_content_platform.utils.logger import get_logger


class FileManager:
    """Async file manager for platform operations."""
    
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path.cwd()
        self.logger = get_logger(__name__)
        
        # Ensure base directory exists
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    async def download_file(
        self, 
        url: str, 
        destination: Optional[Path] = None,
        filename: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Path:
        """Download file from URL asynchronously.
        
        Args:
            url: URL to download from
            destination: Destination directory (defaults to base_dir)
            filename: Custom filename (extracted from URL if not provided)
            headers: Optional HTTP headers
            
        Returns:
            Path to downloaded file
            
        Raises:
            FileOperationError: If download fails
        """
        try:
            destination = destination or self.base_dir
            destination.mkdir(parents=True, exist_ok=True)
            
            if not filename:
                parsed_url = urlparse(url)
                filename = Path(parsed_url.path).name or "downloaded_file"
            
            file_path = destination / filename
            
            self.logger.info(f"Downloading {url} to {file_path}")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers or {}) as response:
                    response.raise_for_status()
                    
                    async with aiofiles.open(file_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            await f.write(chunk)
            
            self.logger.success(f"Downloaded {file_path}")
            return file_path
            
        except Exception as e:
            error_msg = f"Failed to download {url}: {str(e)}"
            self.logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    async def upload_file(
        self,
        file_path: Path,
        upload_url: str,
        headers: Optional[Dict[str, str]] = None,
        form_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Upload file to URL asynchronously.
        
        Args:
            file_path: Path to file to upload
            upload_url: URL to upload to
            headers: Optional HTTP headers
            form_data: Optional form data to include
            
        Returns:
            Response data from upload
            
        Raises:
            FileOperationError: If upload fails
        """
        try:
            if not file_path.exists():
                raise FileOperationError(f"File not found: {file_path}")
            
            self.logger.info(f"Uploading {file_path} to {upload_url}")
            
            async with aiohttp.ClientSession() as session:
                data = aiohttp.FormData()
                
                # Add form data if provided
                if form_data:
                    for key, value in form_data.items():
                        data.add_field(key, value)
                
                # Add file
                data.add_field(
                    'file',
                    open(file_path, 'rb'),
                    filename=file_path.name,
                    content_type='application/octet-stream'
                )
                
                async with session.post(
                    upload_url, 
                    data=data, 
                    headers=headers or {}
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
            
            self.logger.success(f"Uploaded {file_path}")
            return result
            
        except Exception as e:
            error_msg = f"Failed to upload {file_path}: {str(e)}"
            self.logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    async def copy_file(self, source: Path, destination: Path) -> Path:
        """Copy file asynchronously.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            Destination path
            
        Raises:
            FileOperationError: If copy fails
        """
        try:
            if not source.exists():
                raise FileOperationError(f"Source file not found: {source}")
            
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"Copying {source} to {destination}")
            
            # Use asyncio for non-blocking copy
            await asyncio.to_thread(shutil.copy2, source, destination)
            
            self.logger.success(f"Copied to {destination}")
            return destination
            
        except Exception as e:
            error_msg = f"Failed to copy {source} to {destination}: {str(e)}"
            self.logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    async def move_file(self, source: Path, destination: Path) -> Path:
        """Move file asynchronously.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            Destination path
            
        Raises:
            FileOperationError: If move fails
        """
        try:
            if not source.exists():
                raise FileOperationError(f"Source file not found: {source}")
            
            destination.parent.mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"Moving {source} to {destination}")
            
            # Use asyncio for non-blocking move
            await asyncio.to_thread(shutil.move, source, destination)
            
            self.logger.success(f"Moved to {destination}")
            return destination
            
        except Exception as e:
            error_msg = f"Failed to move {source} to {destination}: {str(e)}"
            self.logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    async def delete_file(self, file_path: Path) -> bool:
        """Delete file asynchronously.
        
        Args:
            file_path: Path to file to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            FileOperationError: If deletion fails
        """
        try:
            if not file_path.exists():
                self.logger.warning(f"File not found for deletion: {file_path}")
                return False
            
            self.logger.info(f"Deleting {file_path}")
            
            # Use asyncio for non-blocking deletion
            await asyncio.to_thread(file_path.unlink)
            
            self.logger.success(f"Deleted {file_path}")
            return True
            
        except Exception as e:
            error_msg = f"Failed to delete {file_path}: {str(e)}"
            self.logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    async def get_file_hash(self, file_path: Path, algorithm: str = "md5") -> str:
        """Calculate file hash asynchronously.
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm (md5, sha1, sha256)
            
        Returns:
            Hex digest of file hash
            
        Raises:
            FileOperationError: If hashing fails
        """
        try:
            if not file_path.exists():
                raise FileOperationError(f"File not found: {file_path}")
            
            hash_func = hashlib.new(algorithm)
            
            async with aiofiles.open(file_path, 'rb') as f:
                while chunk := await f.read(8192):
                    hash_func.update(chunk)
            
            return hash_func.hexdigest()
            
        except Exception as e:
            error_msg = f"Failed to hash {file_path}: {str(e)}"
            self.logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    async def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get file information asynchronously.
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary with file information
            
        Raises:
            FileOperationError: If file info retrieval fails
        """
        try:
            if not file_path.exists():
                raise FileOperationError(f"File not found: {file_path}")
            
            stat = await asyncio.to_thread(file_path.stat)
            
            return {
                "name": file_path.name,
                "path": str(file_path),
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "is_file": file_path.is_file(),
                "is_dir": file_path.is_dir(),
                "suffix": file_path.suffix,
                "parent": str(file_path.parent)
            }
            
        except Exception as e:
            error_msg = f"Failed to get info for {file_path}: {str(e)}"
            self.logger.error(error_msg)
            raise FileOperationError(error_msg) from e
    
    async def list_files(
        self, 
        directory: Path, 
        pattern: str = "*",
        recursive: bool = False
    ) -> List[Path]:
        """List files in directory asynchronously.
        
        Args:
            directory: Directory to search
            pattern: File pattern to match
            recursive: Search recursively
            
        Returns:
            List of matching file paths
            
        Raises:
            FileOperationError: If listing fails
        """
        try:
            if not directory.exists():
                raise FileOperationError(f"Directory not found: {directory}")
            
            if recursive:
                files = await asyncio.to_thread(
                    lambda: list(directory.rglob(pattern))
                )
            else:
                files = await asyncio.to_thread(
                    lambda: list(directory.glob(pattern))
                )
            
            # Filter to only files
            return [f for f in files if f.is_file()]
            
        except Exception as e:
            error_msg = f"Failed to list files in {directory}: {str(e)}"
            self.logger.error(error_msg)
            raise FileOperationError(error_msg) from e