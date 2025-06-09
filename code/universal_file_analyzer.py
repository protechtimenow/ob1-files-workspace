#!/usr/bin/env python3
"""
Universal File Analyzer for OB-1 AI Agent
Handles analysis of ANY file type uploaded to the repository
"""

import os
import json
import csv
import mimetypes
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib
from datetime import datetime

class UniversalFileAnalyzer:
    """
    Universal file analyzer that can handle any file type and provide
    intelligent analysis based on content, structure, and context.
    """
    
    def __init__(self):
        self.supported_analysis_types = {
            'data_analysis': ['.csv', '.json', '.xml', '.xlsx', '.parquet'],
            'code_analysis': ['.py', '.js', '.sol', '.go', '.java', '.cpp', '.c'],
            'document_analysis': ['.txt', '.md', '.pdf', '.doc', '.docx'],
            'config_analysis': ['.json', '.yaml', '.yml', '.toml', '.ini'],
            'media_analysis': ['.jpg', '.png', '.gif', '.mp4', '.mp3'],
            'security_analysis': ['.log', '.cert', '.key', '.pem']
        }
        
        self.analysis_frameworks = {
            'structure': self._analyze_structure,
            'content': self._analyze_content,
            'quality': self._analyze_quality,
            'security': self._analyze_security,
            'optimization': self._analyze_optimization
        }
    
    def analyze_file(self, file_path: str, analysis_type: str = 'comprehensive') -> Dict[str, Any]:
        """
        Main entry point for file analysis
        
        Args:
            file_path: Path to the file to analyze
            analysis_type: Type of analysis ('quick', 'comprehensive', 'specific')
            
        Returns:
            Dictionary containing analysis results
        """
        if not os.path.exists(file_path):
            return {"error": "File not found", "status": "failed"}
        
        # Get file metadata
        file_info = self._get_file_metadata(file_path)
        
        # Determine analysis strategy
        analysis_strategy = self._determine_analysis_strategy(file_info)
        
        # Execute analysis based on strategy
        results = {
            "metadata": file_info,
            "analysis_strategy": analysis_strategy,
            "timestamp": datetime.now().isoformat(),
            "analysis_results": {}
        }
        
        # Run appropriate analysis frameworks
        for framework_name, framework_func in self.analysis_frameworks.items():
            if framework_name in analysis_strategy['frameworks']:
                try:
                    results["analysis_results"][framework_name] = framework_func(file_path, file_info)
                except Exception as e:
                    results["analysis_results"][framework_name] = {
                        "error": str(e),
                        "status": "failed"
                    }
        
        # Generate insights and recommendations
        results["insights"] = self._generate_insights(results)
        results["recommendations"] = self._generate_recommendations(results)
        
        return results
    
    def batch_analyze(self, directory_path: str) -> Dict[str, Any]:
        """
        Analyze multiple files in a directory
        
        Args:
            directory_path: Path to directory containing files
            
        Returns:
            Dictionary containing batch analysis results
        """
        if not os.path.exists(directory_path):
            return {"error": "Directory not found", "status": "failed"}
        
        batch_results = {
            "directory": directory_path,
            "timestamp": datetime.now().isoformat(),
            "files_analyzed": 0,
            "total_files": 0,
            "results": {},
            "summary": {}
        }
        
        # Get all files in directory
        files = []
        for root, dirs, filenames in os.walk(directory_path):
            for filename in filenames:
                if not filename.startswith('.'):  # Skip hidden files
                    files.append(os.path.join(root, filename))
        
        batch_results["total_files"] = len(files)
        
        # Analyze each file
        for file_path in files:
            try:
                relative_path = os.path.relpath(file_path, directory_path)
                analysis_result = self.analyze_file(file_path, 'quick')
                batch_results["results"][relative_path] = analysis_result
                batch_results["files_analyzed"] += 1
            except Exception as e:
                batch_results["results"][relative_path] = {
                    "error": str(e),
                    "status": "failed"
                }
        
        # Generate batch insights
        batch_results["summary"] = self._generate_batch_summary(batch_results)
        
        return batch_results
    
    def _get_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract comprehensive file metadata"""
        file_stats = os.stat(file_path)
        file_path_obj = Path(file_path)
        
        # Get MIME type
        mime_type, encoding = mimetypes.guess_type(file_path)
        
        # Calculate file hash
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        return {
            "name": file_path_obj.name,
            "extension": file_path_obj.suffix.lower(),
            "size_bytes": file_stats.st_size,
            "size_human": self._format_file_size(file_stats.st_size),
            "created": datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
            "mime_type": mime_type,
            "encoding": encoding,
            "hash_sha256": file_hash,
            "path": file_path
        }
    
    def _determine_analysis_strategy(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the best analysis strategy for the file"""
        extension = file_info["extension"]
        mime_type = file_info["mime_type"]
        
        strategy = {
            "primary_type": "unknown",
            "frameworks": ["structure", "content"],
            "specific_analyzers": [],
            "confidence": 0.5
        }
        
        # Determine primary file type
        for analysis_type, extensions in self.supported_analysis_types.items():
            if extension in extensions:
                strategy["primary_type"] = analysis_type
                strategy["confidence"] = 0.9
                break
        
        # Add appropriate frameworks based on type
        if strategy["primary_type"] == "data_analysis":
            strategy["frameworks"].extend(["quality", "optimization"])
            strategy["specific_analyzers"].extend(["statistical", "trend"])
            
        elif strategy["primary_type"] == "code_analysis":
            strategy["frameworks"].extend(["quality", "security", "optimization"])
            strategy["specific_analyzers"].extend(["complexity", "performance"])
            
        elif strategy["primary_type"] == "document_analysis":
            strategy["frameworks"].extend(["quality"])
            strategy["specific_analyzers"].extend(["readability", "sentiment"])
            
        elif strategy["primary_type"] == "config_analysis":
            strategy["frameworks"].extend(["security", "quality"])
            strategy["specific_analyzers"].extend(["validation", "best_practices"])
            
        elif strategy["primary_type"] == "security_analysis":
            strategy["frameworks"].extend(["security"])
            strategy["specific_analyzers"].extend(["vulnerability", "compliance"])
        
        return strategy
    
    def _analyze_structure(self, file_path: str, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze file structure and format"""
        extension = file_info["extension"]
        
        result = {
            "format_valid": True,
            "structure_type": "unknown",
            "complexity_score": 0,
            "details": {}
        }
        
        try:
            if extension == ".json":
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    result.update({
                        "structure_type": "json",
                        "complexity_score": self._calculate_json_complexity(data),
                        "details": {
                            "keys_count": len(data) if isinstance(data, dict) else 0,
                            "max_depth": self._get_json_depth(data),
                            "data_types": list(set(type(v).__name__ for v in data.values())) if isinstance(data, dict) else []
                        }
                    })
                    
            elif extension == ".csv":
                with open(file_path, 'r') as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                    result.update({
                        "structure_type": "tabular",
                        "complexity_score": len(rows[0]) if rows else 0,
                        "details": {
                            "columns": len(rows[0]) if rows else 0,
                            "rows": len(rows),
                            "headers": rows[0] if rows else []
                        }
                    })
                    
            elif extension in [".py", ".js", ".sol"]:
                with open(file_path, 'r') as f:
                    code = f.read()
                    lines = code.split('\n')
                    result.update({
                        "structure_type": "code",
                        "complexity_score": len(lines),
                        "details": {
                            "lines_of_code": len([line for line in lines if line.strip()]),
                            "total_lines": len(lines),
                            "comment_lines": len([line for line in lines if line.strip().startswith('#')])
                        }
                    })
        
        except Exception as e:
            result["format_valid"] = False
            result["error"] = str(e)
        
        return result
    
    def _analyze_content(self, file_path: str, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze file content for patterns and insights"""
        result = {
            "content_type": "unknown",
            "key_insights": [],
            "patterns_found": [],
            "anomalies": [],
            "summary": {}
        }
        
        # Implementation would vary based on file type
        # This is a simplified version
        
        return result
    
    def _analyze_quality(self, file_path: str, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze file quality and best practices compliance"""
        result = {
            "quality_score": 0.0,
            "issues_found": [],
            "best_practices": [],
            "recommendations": []
        }
        
        # Implementation would include specific quality checks
        # based on file type
        
        return result
    
    def _analyze_security(self, file_path: str, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze file for security issues and vulnerabilities"""
        result = {
            "security_score": 0.0,
            "vulnerabilities": [],
            "compliance_issues": [],
            "recommendations": []
        }
        
        # Implementation would include security-specific analysis
        
        return result
    
    def _analyze_optimization(self, file_path: str, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze file for optimization opportunities"""
        result = {
            "optimization_score": 0.0,
            "opportunities": [],
            "performance_issues": [],
            "recommendations": []
        }
        
        # Implementation would include optimization analysis
        
        return result
    
    def _generate_insights(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate actionable insights from analysis results"""
        insights = []
        
        # Extract insights based on analysis results
        # This would be a sophisticated AI-driven process
        
        return insights
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate specific recommendations for improvement"""
        recommendations = []
        
        # Generate recommendations based on analysis
        
        return recommendations
    
    def _generate_batch_summary(self, batch_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary for batch analysis"""
        summary = {
            "file_types": {},
            "total_size": 0,
            "average_quality": 0.0,
            "common_issues": [],
            "recommendations": []
        }
        
        # Calculate summary statistics
        
        return summary
    
    def _calculate_json_complexity(self, data: Any, depth: int = 0) -> int:
        """Calculate complexity score for JSON data"""
        if isinstance(data, dict):
            return sum(1 + self._calculate_json_complexity(v, depth + 1) for v in data.values())
        elif isinstance(data, list):
            return sum(self._calculate_json_complexity(item, depth + 1) for item in data)
        else:
            return 1
    
    def _get_json_depth(self, data: Any, depth: int = 0) -> int:
        """Calculate maximum depth of JSON structure"""
        if isinstance(data, dict):
            return max((self._get_json_depth(v, depth + 1) for v in data.values()), default=depth)
        elif isinstance(data, list):
            return max((self._get_json_depth(item, depth + 1) for item in data), default=depth)
        else:
            return depth
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['bytes', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

# Example usage
if __name__ == "__main__":
    analyzer = UniversalFileAnalyzer()
    
    # Example: Analyze a single file
    # result = analyzer.analyze_file("path/to/your/file.json")
    # print(json.dumps(result, indent=2))
    
    # Example: Batch analyze a directory
    # batch_result = analyzer.batch_analyze("path/to/directory")
    # print(json.dumps(batch_result, indent=2))
    
    print("Universal File Analyzer initialized and ready!")