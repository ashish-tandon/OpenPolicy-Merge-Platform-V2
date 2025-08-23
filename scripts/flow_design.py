#!/usr/bin/env python3
"""
Flow Design & Feature Inventory Script
Scans origin/legacy repositories for all features and builds comprehensive flow design
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

def scan_legacy_features():
    """Scan legacy repositories for feature definitions"""
    features = []
    
    # Legacy directories to scan
    legacy_dirs = [
        'legacy/openparliament',
        'legacy/open-policy',
        'legacy/open-policy-app',
        'legacy/open-policy-web',
        'legacy/admin-open-policy',
        'legacy/represent-canada',
        'legacy/scrapers-ca'
    ]
    
    for legacy_dir in legacy_dirs:
        if os.path.exists(legacy_dir):
            for root, dirs, files in os.walk(legacy_dir):
                for file in files:
                    if file.endswith(('.md', '.txt', '.rst', '.py', '.js', '.ts')):
                        file_path = os.path.join(root, file)
                        features.extend(extract_features_from_file(file_path, legacy_dir))
    
    return features

def extract_features_from_file(file_path, source_dir):
    """Extract features from a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        features = []
        
        # Look for feature patterns
        feature_patterns = [
            r'feature[:\s]+([^\n]+)',
            r'Feature[:\s]+([^\n]+)',
            r'functionality[:\s]+([^\n]+)',
            r'Functionality[:\s]+([^\n]+)',
            r'capability[:\s]+([^\n]+)',
            r'Capability[:\s]+([^\n]+)'
        ]
        
        for pattern in feature_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                features.append({
                    'name': match.strip(),
                    'source_file': file_path,
                    'source_dir': source_dir,
                    'extracted_at': datetime.now().isoformat()
                })
        
        return features
    except Exception as e:
        return []

def build_flow_design():
    """Build comprehensive flow design document"""
    print("Building flow design...")
    
    # Get legacy features
    legacy_features = scan_legacy_features()
    print(f"Found {len(legacy_features)} legacy features")
    
    # Get current features from feature mapping
    current_features = []
    feature_map_file = 'docs/plan/features/FEATURE_MAPPING_UNIFIED.md'
    if os.path.exists(feature_map_file):
        with open(feature_map_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract feature names from markdown
            feature_matches = re.findall(r'##\s+([^\n]+)', content)
            for match in feature_matches:
                current_features.append({
                    'name': match.strip(),
                    'source': 'current_feature_mapping',
                    'extracted_at': datetime.now().isoformat()
                })
    
    # Build flow design
    flow_design = {
        'timestamp': datetime.now().isoformat(),
        'legacy_features': legacy_features,
        'current_features': current_features,
        'feature_mapping': {
            'legacy_to_current': {},
            'unmatched_legacy': [],
            'new_features': []
        }
    }
    
    # Map legacy to current features
    for legacy_feature in legacy_features:
        legacy_name = legacy_feature['name'].lower()
        matched = False
        
        for current_feature in current_features:
            current_name = current_feature['name'].lower()
            if any(word in current_name for word in legacy_name.split()) or any(word in legacy_name for word in current_name.split()):
                flow_design['feature_mapping']['legacy_to_current'][legacy_feature['name']] = current_feature['name']
                matched = True
                break
        
        if not matched:
            flow_design['feature_mapping']['unmatched_legacy'].append(legacy_feature)
    
    # Identify new features
    for current_feature in current_features:
        if not any(current_feature['name'] in mapping.values() for mapping in [flow_design['feature_mapping']['legacy_to_current']]):
            flow_design['feature_mapping']['new_features'].append(current_feature)
    
    return flow_design

def main():
    """Main flow design function"""
    print("=== LOOP C: FLOW DESIGN & FEATURE INVENTORY ===")
    
    # Build flow design
    flow_design = build_flow_design()
    
    # Save results
    os.makedirs('reports', exist_ok=True)
    with open('reports/flow_design.json', 'w') as f:
        json.dump(flow_design, f, indent=2)
    
    print(f"Flow design completed")
    print(f"Results saved to reports/flow_design.json")
    
    # Print summary
    print(f"\n=== SUMMARY ===")
    print(f"Legacy features: {len(flow_design['legacy_features'])}")
    print(f"Current features: {len(flow_design['current_features'])}")
    print(f"Legacy to current mapping: {len(flow_design['feature_mapping']['legacy_to_current'])}")
    print(f"Unmatched legacy: {len(flow_design['feature_mapping']['unmatched_legacy'])}")
    print(f"New features: {len(flow_design['feature_mapping']['new_features'])}")

if __name__ == "__main__":
    main()
