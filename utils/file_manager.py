import os
import json
import logging
from datetime import datetime

class FileManager:
    def __init__(self, projects_folder):
        self.projects_folder = projects_folder
        os.makedirs(projects_folder, exist_ok=True)

    def list_projects(self):
        """List all projects"""
        projects = []
        try:
            if not os.path.exists(self.projects_folder):
                return projects

            for project_dir in os.listdir(self.projects_folder):
                project_path = os.path.join(self.projects_folder, project_dir)
                if os.path.isdir(project_path):
                    metadata_file = os.path.join(project_path, 'metadata.json')
                    if os.path.exists(metadata_file):
                        try:
                            with open(metadata_file, 'r') as f:
                                metadata = json.load(f)
                                metadata['id'] = project_dir
                                projects.append(metadata)
                        except Exception as e:
                            logging.error(f"Error reading project metadata: {e}")
                            # Create basic metadata
                            projects.append({
                                'id': project_dir,
                                'name': project_dir,
                                'created_at': datetime.now().isoformat(),
                                'status': 'unknown'
                            })
        except Exception as e:
            logging.error(f"Error listing projects: {e}")

        return projects

    def get_project(self, project_id):
        """Get project by ID"""
        try:
            project_path = os.path.join(self.projects_folder, project_id)
            metadata_file = os.path.join(project_path, 'metadata.json')

            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    metadata['id'] = project_id
                    return metadata
            elif os.path.exists(project_path):
                # Create basic metadata if missing
                metadata = {
                    'id': project_id,
                    'name': project_id,
                    'created_at': datetime.now().isoformat(),
                    'status': 'unknown'
                }
                return metadata
        except Exception as e:
            logging.error(f"Error getting project {project_id}: {e}")

        return None

    def delete_project(self, project_id):
        """Delete project"""
        try:
            project_path = os.path.join(self.projects_folder, project_id)
            if os.path.exists(project_path):
                import shutil
                shutil.rmtree(project_path)
                return True
        except Exception as e:
            logging.error(f"Error deleting project {project_id}: {e}")

        return False

    def update_project_metadata(self, project_id, metadata_updates):
        """Update project metadata"""
        try:
            project_path = os.path.join(self.projects_folder, project_id)
            metadata_file = os.path.join(project_path, 'metadata.json')

            # Load existing metadata or create new
            metadata = {}
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)

            # Update metadata
            metadata.update(metadata_updates)
            metadata['updated_at'] = datetime.now().isoformat()

            # Save metadata
            os.makedirs(project_path, exist_ok=True)
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)

            return True
        except Exception as e:
            logging.error(f"Error updating project metadata {project_id}: {e}")

        return False
    
    def _get_directory_size(self, directory):
        """Calculate directory size"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
        except Exception as e:
            logging.error(f"Error calculating directory size: {str(e)}")
        
        return total_size
    
    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"