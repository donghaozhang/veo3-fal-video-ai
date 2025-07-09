#!/usr/bin/env python3
"""
Google Cloud Storage Permissions Fix Script

This script automatically fixes common permission issues for Google Veo video generation.
It grants the necessary permissions to service accounts for accessing GCS buckets.

Usage:
    python fix_permissions.py
    python fix_permissions.py --project-id your-project-id --bucket-name your-bucket
"""

import os
import subprocess
import sys
import argparse
import re

def run_command(command, description=""):
    """Run a shell command and return the result."""
    print(f"🔧 {description}")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(f"   ✅ Success")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {e.stderr}")
        return None

def get_project_info():
    """Get current project information."""
    print("📋 Getting project information...")
    
    # Get current project
    result = run_command("gcloud config get project", "Getting current project ID")
    if result:
        project_id = result.strip()
        print(f"   Current project: {project_id}")
    else:
        print("   ❌ Could not get project ID")
        return None, None
    
    # Get project number
    result = run_command(f'gcloud projects describe {project_id} --format="value(projectNumber)"', 
                        "Getting project number")
    if result:
        project_number = result.strip()
        print(f"   Project number: {project_number}")
    else:
        print("   ❌ Could not get project number")
        return project_id, None
    
    return project_id, project_number

def extract_bucket_from_uri(bucket_uri):
    """Extract bucket name from GCS URI."""
    if bucket_uri.startswith("gs://"):
        # Remove gs:// and everything after the first /
        bucket_name = bucket_uri[5:].split('/')[0]
        return bucket_name
    return bucket_uri

def fix_vertex_ai_permissions(bucket_name, project_number):
    """Fix Vertex AI service account permissions."""
    print(f"\n🔐 Fixing Vertex AI permissions for bucket: {bucket_name}")
    
    vertex_ai_sa = f"service-{project_number}@gcp-sa-aiplatform.iam.gserviceaccount.com"
    
    permissions = [
        ("roles/storage.objectAdmin", "Full object access"),
        ("roles/storage.legacyBucketReader", "Bucket read access"),
    ]
    
    for role, description in permissions:
        run_command(
            f'gcloud storage buckets add-iam-policy-binding gs://{bucket_name} '
            f'--member="serviceAccount:{vertex_ai_sa}" --role={role}',
            f"Adding {description}"
        )

def fix_veo_permissions(bucket_name):
    """Fix Veo-specific service account permissions."""
    print(f"\n🎬 Fixing Veo service account permissions for bucket: {bucket_name}")
    
    veo_sa = "cloud-lvm-video-server@prod.google.com"
    
    permissions = [
        ("roles/storage.objectAdmin", "Full object access"),
        ("roles/storage.objectCreator", "Object creation"),
        ("roles/storage.objectViewer", "Object viewing"),
    ]
    
    for role, description in permissions:
        run_command(
            f'gcloud storage buckets add-iam-policy-binding gs://{bucket_name} '
            f'--member="user:{veo_sa}" --role={role}',
            f"Adding {description}"
        )

def enable_required_apis(project_id):
    """Enable required Google Cloud APIs."""
    print(f"\n🔌 Enabling required APIs for project: {project_id}")
    
    apis = [
        "aiplatform.googleapis.com",
        "storage.googleapis.com",
        "compute.googleapis.com"
    ]
    
    for api in apis:
        run_command(
            f"gcloud services enable {api} --project={project_id}",
            f"Enabling {api}"
        )

def wait_for_service_agents():
    """Wait for service agents to be provisioned."""
    print("\n⏳ Waiting for service agents to be provisioned...")
    print("   This may take a few minutes. Service agents are automatically created")
    print("   when you first use Vertex AI services in your project.")
    print("   If you continue to see 'Service agents are being provisioned' errors,")
    print("   wait 5-10 minutes and try again.")

def verify_permissions(bucket_name, project_number):
    """Verify that permissions are set correctly."""
    print(f"\n✅ Verifying permissions for bucket: {bucket_name}")
    
    result = run_command(
        f"gcloud storage buckets get-iam-policy gs://{bucket_name}",
        "Getting current bucket permissions"
    )
    
    if result:
        print("   Current permissions:")
        # Check for key service accounts
        vertex_ai_sa = f"service-{project_number}@gcp-sa-aiplatform.iam.gserviceaccount.com"
        veo_sa = "cloud-lvm-video-server@prod.google.com"
        
        if vertex_ai_sa in result:
            print(f"   ✅ Vertex AI service account found: {vertex_ai_sa}")
        else:
            print(f"   ⚠️  Vertex AI service account not found: {vertex_ai_sa}")
        
        if veo_sa in result:
            print(f"   ✅ Veo service account found: {veo_sa}")
        else:
            print(f"   ⚠️  Veo service account not found: {veo_sa}")
    
    return result

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Fix Google Cloud Storage permissions for Veo")
    parser.add_argument("--project-id", help="Google Cloud project ID")
    parser.add_argument("--bucket-name", help="GCS bucket name (without gs:// prefix)")
    parser.add_argument("--bucket-uri", help="Full GCS bucket URI (e.g., gs://bucket/path/)")
    parser.add_argument("--skip-apis", action="store_true", help="Skip API enablement")
    
    args = parser.parse_args()
    
    print("🔧 Google Cloud Storage Permissions Fix Script")
    print("=" * 60)
    
    # Get project information
    if args.project_id:
        project_id = args.project_id
        # Get project number
        result = run_command(f'gcloud projects describe {project_id} --format="value(projectNumber)"')
        project_number = result.strip() if result else None
    else:
        project_id, project_number = get_project_info()
    
    if not project_id or not project_number:
        print("❌ Could not get project information. Make sure you're authenticated with gcloud.")
        sys.exit(1)
    
    # Determine bucket name
    if args.bucket_name:
        bucket_name = args.bucket_name
    elif args.bucket_uri:
        bucket_name = extract_bucket_from_uri(args.bucket_uri)
    else:
        # Try to get from environment or config
        bucket_uri = os.getenv("OUTPUT_BUCKET_PATH", "gs://test_dh/veo_output/")
        bucket_name = extract_bucket_from_uri(bucket_uri)
        print(f"📋 Using bucket from environment: {bucket_name}")
    
    print(f"\n📋 Configuration:")
    print(f"   Project ID: {project_id}")
    print(f"   Project Number: {project_number}")
    print(f"   Bucket Name: {bucket_name}")
    
    # Enable APIs
    if not args.skip_apis:
        enable_required_apis(project_id)
    
    # Fix permissions
    fix_vertex_ai_permissions(bucket_name, project_number)
    fix_veo_permissions(bucket_name)
    
    # Wait message
    wait_for_service_agents()
    
    # Verify permissions
    verify_permissions(bucket_name, project_number)
    
    print("\n" + "=" * 60)
    print("✅ PERMISSION FIX COMPLETE")
    print("=" * 60)
    print("Next steps:")
    print("1. Wait 5-10 minutes for service agents to be fully provisioned")
    print("2. Run your video generation tests again")
    print("3. If you still see permission errors, run this script again")
    print("\nTest with:")
    print("   python test_veo.py")
    print("   python demo.py")

if __name__ == "__main__":
    main() 