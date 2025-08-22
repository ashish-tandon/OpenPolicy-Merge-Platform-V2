#!/usr/bin/env python3
"""
Database Backup Script for OpenPolicy V2

This script implements automated database backups as required by BUG-018.
It creates both database dumps and file backups with timestamping and rotation.

Implements checklist item: Database backup automation
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Optional, List
import argparse

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabaseBackup:
    """Handles database and file backups for OpenPolicy V2."""
    
    def __init__(self, backup_dir: str = "/backups", max_backups: int = 7):
        """
        Initialize backup system.
        
        Args:
            backup_dir: Directory to store backups
            max_backups: Maximum number of backups to keep
        """
        self.backup_dir = Path(backup_dir)
        self.max_backups = max_backups
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Parse database URL to extract connection details
        self.db_config = self._parse_database_url(settings.DATABASE_URL)
        
    def _parse_database_url(self, database_url: str) -> dict:
        """Parse PostgreSQL connection string."""
        try:
            # Expected format: postgresql://user:password@host:port/database
            if database_url.startswith('postgresql://'):
                parts = database_url.replace('postgresql://', '').split('@')
                if len(parts) == 2:
                    auth_part, host_part = parts
                    username, password = auth_part.split(':')
                    host_port, database = host_part.split('/')
                    host, port = host_port.split(':') if ':' in host_port else (host_port, '5432')
                    
                    return {
                        'host': host,
                        'port': port,
                        'database': database,
                        'username': username,
                        'password': password
                    }
        except Exception as e:
            logger.error(f"Failed to parse database URL: {e}")
            
        # Fallback to environment variables
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'merge_v2_dev'),
            'username': os.getenv('DB_USER', 'merge_v2_user'),
            'password': os.getenv('DB_PASSWORD', 'merge_v2_password')
        }
    
    def create_database_backup(self) -> Optional[str]:
        """
        Create a PostgreSQL database backup.
        
        Returns:
            Path to the backup file if successful, None otherwise
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"database_backup_{timestamp}.sql"
            backup_path = self.backup_dir / backup_filename
            
            # Set environment variable for password
            env = os.environ.copy()
            env['PGPASSWORD'] = self.db_config['password']
            
            # Create database backup using pg_dump
            cmd = [
                'pg_dump',
                '-h', self.db_config['host'],
                '-p', self.db_config['port'],
                '-U', self.db_config['username'],
                '-d', self.db_config['database'],
                '--clean',  # Include DROP statements
                '--create',  # Include CREATE DATABASE statement
                '--if-exists',  # Use IF EXISTS with DROP
                '--no-password',  # Don't prompt for password
                '-f', str(backup_path)
            ]
            
            logger.info(f"Creating database backup: {backup_path}")
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Database backup created successfully: {backup_path}")
                return str(backup_path)
            else:
                logger.error(f"Database backup failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating database backup: {e}")
            return None
    
    def create_file_backup(self) -> Optional[str]:
        """
        Create a file backup of important data directories.
        
        Returns:
            Path to the backup file if successful, None otherwise
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"files_backup_{timestamp}.tar.gz"
            backup_path = self.backup_dir / backup_filename
            
            # Define directories to backup
            data_dirs = [
                'data',  # Data files
                'logs',  # Log files
                'uploads',  # User uploads
                'exports',  # Data exports
                'test_backup_data'  # Test data for development
            ]
            
            # Filter to only include existing directories
            existing_dirs = [d for d in data_dirs if os.path.exists(d)]
            
            if not existing_dirs:
                logger.warning("No data directories found to backup")
                return None
            
            # Create tar.gz backup
            cmd = ['tar', '-czf', str(backup_path)] + existing_dirs
            
            logger.info(f"Creating file backup: {backup_path}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"File backup created successfully: {backup_path}")
                return str(backup_path)
            else:
                logger.error(f"File backup failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating file backup: {e}")
            return None
    
    def create_full_backup(self) -> dict:
        """
        Create a complete backup (database + files).
        
        Returns:
            Dictionary with backup results
        """
        logger.info("Starting full backup process")
        
        backup_results = {
            'timestamp': datetime.now().isoformat(),
            'database_backup': None,
            'file_backup': None,
            'success': False
        }
        
        # Create database backup
        db_backup = self.create_database_backup()
        backup_results['database_backup'] = db_backup
        
        # Create file backup
        file_backup = self.create_file_backup()
        backup_results['file_backup'] = file_backup
        
        # Check if both backups were successful
        if db_backup and file_backup:
            backup_results['success'] = True
            logger.info("Full backup completed successfully")
        else:
            logger.error("Full backup failed - some components failed")
        
        return backup_results
    
    def cleanup_old_backups(self):
        """Remove old backups to maintain disk space."""
        try:
            # Get all backup files
            backup_files = list(self.backup_dir.glob("*_backup_*"))
            
            if len(backup_files) <= self.max_backups:
                logger.info(f"Only {len(backup_files)} backups exist, no cleanup needed")
                return
            
            # Sort by modification time (oldest first)
            backup_files.sort(key=lambda x: x.stat().st_mtime)
            
            # Remove oldest backups
            files_to_remove = backup_files[:-self.max_backups]
            
            for file_path in files_to_remove:
                try:
                    file_path.unlink()
                    logger.info(f"Removed old backup: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to remove old backup {file_path}: {e}")
                    
        except Exception as e:
            logger.error(f"Error during backup cleanup: {e}")
    
    def verify_backup(self, backup_path: str) -> bool:
        """
        Verify that a backup file is valid.
        
        Args:
            backup_path: Path to the backup file
            
        Returns:
            True if backup is valid, False otherwise
        """
        try:
            file_path = Path(backup_path)
            
            if not file_path.exists():
                logger.error(f"Backup file does not exist: {backup_path}")
                return False
            
            # Check file size
            file_size = file_path.stat().st_size
            if file_size == 0:
                logger.error(f"Backup file is empty: {backup_path}")
                return False
            
            logger.info(f"Backup verification passed: {backup_path} ({file_size} bytes)")
            return True
            
        except Exception as e:
            logger.error(f"Error verifying backup {backup_path}: {e}")
            return False


def main():
    """Main backup execution function."""
    parser = argparse.ArgumentParser(description='OpenPolicy V2 Database Backup Tool')
    parser.add_argument('--backup-dir', default='/backups', help='Backup directory')
    parser.add_argument('--max-backups', type=int, default=7, help='Maximum backups to keep')
    parser.add_argument('--database-only', action='store_true', help='Only backup database')
    parser.add_argument('--files-only', action='store_true', help='Only backup files')
    parser.add_argument('--cleanup', action='store_true', help='Clean up old backups')
    parser.add_argument('--verify', action='store_true', help='Verify existing backups')
    
    args = parser.parse_args()
    
    # Initialize backup system
    backup_system = DatabaseBackup(
        backup_dir=args.backup_dir,
        max_backups=args.max_backups
    )
    
    try:
        if args.cleanup:
            logger.info("Cleaning up old backups")
            backup_system.cleanup_old_backups()
            return
        
        if args.verify:
            logger.info("Verifying existing backups")
            backup_files = list(Path(args.backup_dir).glob("*_backup_*"))
            for backup_file in backup_files:
                backup_system.verify_backup(str(backup_file))
            return
        
        if args.database_only:
            logger.info("Creating database backup only")
            backup_path = backup_system.create_database_backup()
            if backup_path:
                backup_system.verify_backup(backup_path)
            return
        
        if args.files_only:
            logger.info("Creating file backup only")
            backup_path = backup_system.create_file_backup()
            if backup_path:
                backup_system.verify_backup(backup_path)
            return
        
        # Default: create full backup
        logger.info("Creating full backup")
        backup_results = backup_system.create_full_backup()
        
        # Verify backups
        if backup_results['database_backup']:
            backup_system.verify_backup(backup_results['database_backup'])
        if backup_results['file_backup']:
            backup_system.verify_backup(backup_results['file_backup'])
        
        # Cleanup old backups
        backup_system.cleanup_old_backups()
        
        # Log results
        if backup_results['success']:
            logger.info("Backup process completed successfully")
            sys.exit(0)
        else:
            logger.error("Backup process failed")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Backup process failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
