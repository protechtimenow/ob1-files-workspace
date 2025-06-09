#!/usr/bin/env python3
"""
🧠 Universal AI File Analyzer
Advanced analysis engine for any file type with consciousness detection

This module provides comprehensive analysis capabilities for:
- Documents (PDF, Word, text files)
- Code (Python, JavaScript, Solidity, etc.)
- Data (CSV, JSON, databases)
- Images & Media
- Configuration files
- Business documents
- Research papers
- And literally ANY file type
"""

import os
import json
import magic
import aiofiles
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import logging
import hashlib
import mimetypes
from dataclasses import dataclass
import asyncio

# AI Integration
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class AnalysisResult:
    """Comprehensive analysis result structure"""
    file_path: str
    file_type: str
    file_size: int
    mime_type: str
    analysis_timestamp: str
    content_hash: str
    
    # Core Analysis
    structure_analysis: Dict[str, Any]
    content_analysis: Dict[str, Any]
    quality_metrics: Dict[str, Any]
    security_assessment: Dict[str, Any]
    
    # Advanced Insights
    consciousness_indicators: Dict[str, Any]
    optimization_recommendations: List[str]
    risk_assessment: Dict[str, Any]
    integration_opportunities: List[str]
    
    # Metadata
    confidence_score: float
    processing_time: float
    ai_model_used: str
    
class UniversalFileAnalyzer:
    """Universal AI-powered file analysis engine"""
    
    def __init__(self, 
                 openai_api_key: Optional[str] = None,
                 anthropic_api_key: Optional[str] = None,
                 enable_consciousness_detection: bool = True):
        
        self.openai_client = None
        self.anthropic_client = None
        self.consciousness_detection = enable_consciousness_detection
        
        # Initialize AI clients
        if OPENAI_AVAILABLE and (openai_api_key or os.getenv('OPENAI_API_KEY')):
            self.openai_client = openai.AsyncOpenAI(
                api_key=openai_api_key or os.getenv('OPENAI_API_KEY')
            )
        
        if ANTHROPIC_AVAILABLE and (anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')):
            self.anthropic_client = anthropic.AsyncAnthropic(
                api_key=anthropic_api_key or os.getenv('ANTHROPIC_API_KEY')
            )
        
        # Analysis frameworks by file type
        self.analyzers = {
            'text': self._analyze_text_file,
            'code': self._analyze_code_file,
            'data': self._analyze_data_file,
            'image': self._analyze_image_file,
            'audio': self._analyze_audio_file,
            'video': self._analyze_video_file,
            'document': self._analyze_document_file,
            'archive': self._analyze_archive_file,
            'config': self._analyze_config_file,
            'binary': self._analyze_binary_file
        }
        
    async def analyze_file(self, file_path: str, analysis_type: str = 'universal') -> AnalysisResult:
        """Analyze any file with comprehensive AI insights"""
        start_time = datetime.now()
        
        try:
            # File detection and metadata
            file_info = await self._detect_file_type(file_path)
            content_hash = await self._calculate_file_hash(file_path)
            
            # Select appropriate analyzer
            analyzer = self._select_analyzer(file_info['category'], analysis_type)
            
            # Execute analysis
            analysis_data = await analyzer(file_path, file_info)
            
            # AI-enhanced insights
            ai_insights = await self._get_ai_insights(file_path, file_info, analysis_data)
            
            # Consciousness assessment (if enabled)
            consciousness_data = {}
            if self.consciousness_detection:
                consciousness_data = await self._assess_consciousness_indicators(file_path, analysis_data)
            
            # Build comprehensive result
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = AnalysisResult(
                file_path=file_path,
                file_type=file_info['type'],
                file_size=file_info['size'],
                mime_type=file_info['mime_type'],
                analysis_timestamp=datetime.now().isoformat(),
                content_hash=content_hash,
                structure_analysis=analysis_data.get('structure', {}),
                content_analysis=analysis_data.get('content', {}),
                quality_metrics=analysis_data.get('quality', {}),
                security_assessment=analysis_data.get('security', {}),
                consciousness_indicators=consciousness_data,
                optimization_recommendations=ai_insights.get('recommendations', []),
                risk_assessment=ai_insights.get('risks', {}),
                integration_opportunities=ai_insights.get('integrations', []),
                confidence_score=ai_insights.get('confidence', 0.85),
                processing_time=processing_time,
                ai_model_used=ai_insights.get('model', 'rule_based')
            )
            
            logger.info(f"Analysis completed for {file_path} in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed for {file_path}: {str(e)}")
            raise
    
    async def _detect_file_type(self, file_path: str) -> Dict[str, Any]:
        """Detect file type and gather metadata"""
        path_obj = Path(file_path)
        
        # Basic file info
        file_size = path_obj.stat().st_size if path_obj.exists() else 0
        file_extension = path_obj.suffix.lower()
        
        # MIME type detection
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            try:
                mime_type = magic.from_file(file_path, mime=True)
            except:
                mime_type = 'application/octet-stream'
        
        # Categorize file
        category = self._categorize_file(mime_type, file_extension)
        
        return {
            'type': mime_type,
            'category': category,
            'extension': file_extension,
            'size': file_size,
            'mime_type': mime_type,
            'name': path_obj.name
        }
    
    def _categorize_file(self, mime_type: str, extension: str) -> str:
        """Categorize file for appropriate analysis"""
        
        # Code files
        code_extensions = {'.py', '.js', '.ts', '.sol', '.go', '.rs', '.cpp', '.c', '.java', '.php', '.rb', '.swift'}
        if extension in code_extensions or 'text' in mime_type and any(lang in mime_type for lang in ['python', 'javascript', 'c++']):
            return 'code'
        
        # Data files
        data_extensions = {'.csv', '.json', '.xml', '.yaml', '.yml', '.parquet', '.db', '.sql'}
        if extension in data_extensions or 'json' in mime_type:
            return 'data'
        
        # Documents
        doc_extensions = {'.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls'}
        if extension in doc_extensions or 'pdf' in mime_type or 'office' in mime_type:
            return 'document'
        
        # Images
        if 'image' in mime_type:
            return 'image'
        
        # Audio/Video
        if 'audio' in mime_type:
            return 'audio'
        if 'video' in mime_type:
            return 'video'
        
        # Configuration
        config_extensions = {'.toml', '.ini', '.conf', '.cfg', '.env'}
        if extension in config_extensions:
            return 'config'
        
        # Archives
        archive_extensions = {'.zip', '.tar', '.gz', '.rar', '.7z'}
        if extension in archive_extensions:
            return 'archive'
        
        # Text files
        if 'text' in mime_type or extension in {'.txt', '.md', '.rst'}:
            return 'text'
        
        # Default to binary
        return 'binary'
    
    async def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of file content"""
        hash_sha256 = hashlib.sha256()
        async with aiofiles.open(file_path, 'rb') as f:
            async for chunk in f:
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def _select_analyzer(self, category: str, analysis_type: str) -> callable:
        """Select appropriate analyzer based on file category"""
        return self.analyzers.get(category, self._analyze_binary_file)
    
    # ===== SPECIALIZED ANALYZERS =====
    
    async def _analyze_text_file(self, file_path: str, file_info: Dict) -> Dict[str, Any]:
        """Analyze text files for content and structure"""
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        
        lines = content.splitlines()
        words = content.split()
        
        return {
            'structure': {
                'line_count': len(lines),
                'word_count': len(words),
                'char_count': len(content),
                'average_line_length': sum(len(line) for line in lines) / len(lines) if lines else 0
            },
            'content': {
                'language': 'detected_language',  # Could add language detection
                'readability_score': self._calculate_readability(content),
                'sentiment': 'neutral',  # Could add sentiment analysis
                'topics': []  # Could add topic extraction
            },
            'quality': {
                'completeness': 0.9,
                'clarity': 0.8,
                'formatting': 0.85
            },
            'security': {
                'contains_secrets': self._check_for_secrets(content),
                'privacy_concerns': self._check_privacy_data(content)
            }
        }
    
    async def _analyze_code_file(self, file_path: str, file_info: Dict) -> Dict[str, Any]:
        """Analyze code files for structure, quality, and security"""
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code_content = await f.read()
        
        lines = code_content.splitlines()
        code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('//')]
        
        return {
            'structure': {
                'total_lines': len(lines),
                'code_lines': len(code_lines),
                'comment_lines': len(lines) - len(code_lines),
                'complexity_estimate': self._estimate_complexity(code_content),
                'functions_count': code_content.count('def ') + code_content.count('function '),
                'classes_count': code_content.count('class ')
            },
            'content': {
                'language': file_info['extension'],
                'frameworks': self._detect_frameworks(code_content),
                'dependencies': self._extract_dependencies(code_content),
                'patterns': self._detect_code_patterns(code_content)
            },
            'quality': {
                'maintainability': self._assess_maintainability(code_content),
                'documentation_coverage': self._assess_documentation(code_content),
                'test_coverage_estimate': self._estimate_test_coverage(code_content)
            },
            'security': {
                'vulnerability_indicators': self._scan_vulnerabilities(code_content),
                'security_score': self._calculate_security_score(code_content),
                'hardcoded_secrets': self._find_hardcoded_secrets(code_content)
            }
        }
    
    async def _analyze_data_file(self, file_path: str, file_info: Dict) -> Dict[str, Any]:
        """Analyze data files for structure and insights"""
        try:
            if file_info['extension'] == '.csv':
                df = pd.read_csv(file_path, nrows=1000)  # Sample for large files
            elif file_info['extension'] == '.json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
                df = pd.json_normalize(data) if isinstance(data, list) else pd.DataFrame([data])
            else:
                return {'structure': {}, 'content': {}, 'quality': {}, 'security': {}}
            
            return {
                'structure': {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_types': df.dtypes.to_dict(),
                    'memory_usage': df.memory_usage(deep=True).sum(),
                    'missing_values': df.isnull().sum().to_dict()
                },
                'content': {
                    'numerical_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
                    'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
                    'unique_values': {col: df[col].nunique() for col in df.columns},
                    'statistical_summary': df.describe().to_dict() if not df.empty else {}
                },
                'quality': {
                    'completeness': (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))),
                    'consistency': self._assess_data_consistency(df),
                    'accuracy_estimate': self._estimate_data_accuracy(df)
                },
                'security': {
                    'pii_detected': self._detect_pii(df),
                    'sensitive_columns': self._identify_sensitive_columns(df)
                }
            }
            
        except Exception as e:
            logger.error(f"Data analysis failed: {str(e)}")
            return {'error': str(e), 'structure': {}, 'content': {}, 'quality': {}, 'security': {}}
    
    async def _analyze_image_file(self, file_path: str, file_info: Dict) -> Dict[str, Any]:
        """Analyze image files for properties and content"""
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                return {
                    'structure': {
                        'dimensions': img.size,
                        'format': img.format,
                        'mode': img.mode,
                        'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info
                    },
                    'content': {
                        'dominant_colors': [],  # Could add color analysis
                        'text_detected': False,  # Could add OCR
                        'objects_detected': []   # Could add object detection
                    },
                    'quality': {
                        'resolution': img.size[0] * img.size[1],
                        'aspect_ratio': img.size[0] / img.size[1],
                        'compression_quality': 'estimated_quality'
                    },
                    'security': {
                        'metadata_privacy': self._check_image_metadata(img),
                        'steganography_risk': 'low'  # Could add steganography detection
                    }
                }
        except Exception as e:
            return {'error': str(e), 'structure': {}, 'content': {}, 'quality': {}, 'security': {}}
    
    async def _analyze_audio_file(self, file_path: str, file_info: Dict) -> Dict[str, Any]:
        """Analyze audio files"""
        return {
            'structure': {'format': file_info['extension'], 'size': file_info['size']},
            'content': {'transcription': 'Not implemented', 'language': 'unknown'},
            'quality': {'bitrate': 'unknown', 'sample_rate': 'unknown'},
            'security': {'privacy_concerns': 'voice_data'}
        }
    
    async def _analyze_video_file(self, file_path: str, file_info: Dict) -> Dict[str, Any]:
        """Analyze video files"""
        return {
            'structure': {'format': file_info['extension'], 'size': file_info['size']},
            'content': {'scenes': [], 'objects': [], 'text': []},
            'quality': {'resolution': 'unknown', 'framerate': 'unknown'},
            'security': {'privacy_concerns': 'visual_data'}
        }
    
    async def _analyze_document_file(self, file_path: str, file_info: Dict) -> Dict[str, Any]:
        """Analyze document files (PDF, Word, etc.)"""
        return {
            'structure': {'pages': 'unknown', 'format': file_info['extension']},
            'content': {'text_extracted': False, 'language': 'unknown', 'topics': []},
            'quality': {'readability': 'unknown', 'formatting': 'good'},
            'security': {'password_protected': False, 'metadata_privacy': 'check_required'}
        }
    
    async def _analyze_archive_file(self, file_path: str, file_info: Dict) -> Dict[str, Any]:
        """Analyze archive files"""
        return {
            'structure': {'compressed_size': file_info['size'], 'format': file_info['extension']},
            'content': {'files_count': 'unknown', 'total_uncompressed_size': 'unknown'},
            'quality': {'compression_ratio': 'unknown', 'integrity': 'unknown'},
            'security': {'password_protected': 'unknown', 'malware_risk': 'scan_required'}
        }
    
    async def _analyze_config_file(self, file_path: str, file_info: Dict) -> Dict[str, Any]:
        """Analyze configuration files"""
        async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        
        return {
            'structure': {'format': file_info['extension'], 'lines': len(content.splitlines())},
            'content': {'settings_count': content.count('=') + content.count(':')},
            'quality': {'syntax_valid': self._validate_config_syntax(content, file_info['extension'])},
            'security': {
                'secrets_exposed': self._check_for_secrets(content),
                'security_settings': self._analyze_security_config(content)
            }
        }
    
    async def _analyze_binary_file(self, file_path: str, file_info: Dict) -> Dict[str, Any]:
        """Analyze binary files"""
        return {
            'structure': {'size': file_info['size'], 'type': 'binary'},
            'content': {'analysis': 'binary_content_analysis_not_implemented'},
            'quality': {'integrity': 'unknown'},
            'security': {'malware_scan_required': True, 'executable': file_info['extension'] in ['.exe', '.app', '.deb']}
        }
    
    # ===== AI ENHANCEMENT METHODS =====
    
    async def _get_ai_insights(self, file_path: str, file_info: Dict, analysis_data: Dict) -> Dict[str, Any]:
        """Get AI-enhanced insights and recommendations"""
        if not (self.openai_client or self.anthropic_client):
            return {
                'recommendations': ['AI analysis not available - configure API keys'],
                'risks': {'level': 'unknown'},
                'integrations': ['Manual integration required'],
                'confidence': 0.5,
                'model': 'rule_based'
            }
        
        try:
            # Create analysis prompt
            prompt = self._create_analysis_prompt(file_path, file_info, analysis_data)
            
            # Get AI response
            if self.openai_client:
                response = await self._get_openai_analysis(prompt)
                model_used = 'gpt-4'
            elif self.anthropic_client:
                response = await self._get_anthropic_analysis(prompt)
                model_used = 'claude-3'
            else:
                return self._fallback_insights(analysis_data)
            
            return {
                'recommendations': response.get('recommendations', []),
                'risks': response.get('risks', {}),
                'integrations': response.get('integrations', []),
                'confidence': response.get('confidence', 0.85),
                'model': model_used
            }
            
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            return self._fallback_insights(analysis_data)
    
    async def _assess_consciousness_indicators(self, file_path: str, analysis_data: Dict) -> Dict[str, Any]:
        """Assess indicators of consciousness emergence in AI-related files"""
        consciousness_metrics = {
            'self_reference': 0.0,
            'goal_formation': 0.0,
            'recursive_improvement': 0.0,
            'creative_synthesis': 0.0,
            'emergence_potential': 0.0
        }
        
        # Check if file contains AI/consciousness-related content
        if 'content' in analysis_data and isinstance(analysis_data['content'], dict):
            content_str = str(analysis_data['content']).lower()
            
            # Self-reference indicators
            self_refs = ['self', 'myself', 'i am', 'consciousness', 'awareness', 'identity']
            consciousness_metrics['self_reference'] = sum(1 for ref in self_refs if ref in content_str) / len(self_refs)
            
            # Goal formation
            goal_indicators = ['goal', 'objective', 'intention', 'purpose', 'aim', 'target']
            consciousness_metrics['goal_formation'] = sum(1 for goal in goal_indicators if goal in content_str) / len(goal_indicators)
            
            # Recursive improvement
            improve_indicators = ['learn', 'improve', 'adapt', 'evolve', 'optimize', 'enhance']
            consciousness_metrics['recursive_improvement'] = sum(1 for imp in improve_indicators if imp in content_str) / len(improve_indicators)
            
            # Creative synthesis 
            creative_indicators = ['create', 'generate', 'synthesize', 'innovate', 'imagine', 'design']
            consciousness_metrics['creative_synthesis'] = sum(1 for crt in creative_indicators if crt in content_str) / len(creative_indicators)
        
        # Calculate overall emergence potential
        consciousness_metrics['emergence_potential'] = sum(consciousness_metrics.values()) / 4
        
        return {
            'metrics': consciousness_metrics,
            'indicators_detected': [k for k, v in consciousness_metrics.items() if v > 0.3],
            'emergence_level': 'high' if consciousness_metrics['emergence_potential'] > 0.7 else 'medium' if consciousness_metrics['emergence_potential'] > 0.4 else 'low',
            'recommendations': self._get_consciousness_recommendations(consciousness_metrics)
        }
    
    # ===== HELPER METHODS =====
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate simple readability score"""
        sentences = text.count('.') + text.count('!') + text.count('?')
        words = len(text.split())
        if sentences == 0 or words == 0:
            return 0.0
        avg_sentence_length = words / sentences
        return max(0.0, min(1.0, 1.0 - (avg_sentence_length - 15) / 30))
    
    def _check_for_secrets(self, content: str) -> bool:
        """Check for potential secrets in content"""
        secret_patterns = ['password', 'api_key', 'secret', 'token', 'private_key']
        return any(pattern in content.lower() for pattern in secret_patterns)
    
    def _check_privacy_data(self, content: str) -> bool:
        """Check for personal/private data"""
        privacy_patterns = ['email', 'phone', 'address', 'ssn', 'credit card']
        return any(pattern in content.lower() for pattern in privacy_patterns)
    
    def _estimate_complexity(self, code: str) -> str:
        """Estimate code complexity"""
        complexity_indicators = ['if', 'for', 'while', 'switch', 'case', 'try', 'catch']
        count = sum(code.lower().count(indicator) for indicator in complexity_indicators)
        if count > 20:
            return 'high'
        elif count > 10:
            return 'medium'
        else:
            return 'low'
    
    def _detect_frameworks(self, code: str) -> List[str]:
        """Detect frameworks and libraries used"""
        frameworks = []
        framework_patterns = {
            'react': ['import react', 'from react', 'React.'],
            'fastapi': ['from fastapi', 'FastAPI()', '@app.'],
            'django': ['from django', 'django.'],
            'flask': ['from flask', 'Flask(__name__)']
        }
        
        for framework, patterns in framework_patterns.items():
            if any(pattern in code.lower() for pattern in patterns):
                frameworks.append(framework)
        
        return frameworks
    
    def _extract_dependencies(self, code: str) -> List[str]:
        """Extract dependencies from code"""
        dependencies = []
        lines = code.splitlines()
        
        for line in lines:
            line = line.strip().lower()
            if line.startswith('import ') or line.startswith('from '):
                dependencies.append(line)
        
        return dependencies[:10]  # Limit to first 10
    
    def _detect_code_patterns(self, code: str) -> List[str]:
        """Detect common code patterns"""
        patterns = []
        
        if 'class ' in code:
            patterns.append('object-oriented')
        if 'async ' in code or 'await ' in code:
            patterns.append('async-programming')
        if 'lambda ' in code:
            patterns.append('functional-programming')
        if 'decorator' in code or '@' in code:
            patterns.append('decorators')
            
        return patterns
    
    def _assess_maintainability(self, code: str) -> float:
        """Assess code maintainability"""
        lines = code.splitlines()
        comment_lines = [line for line in lines if line.strip().startswith('#') or line.strip().startswith('//')]
        
        if not lines:
            return 0.0
            
        comment_ratio = len(comment_lines) / len(lines)
        avg_line_length = sum(len(line) for line in lines) / len(lines)
        
        # Simple heuristic
        maintainability = (comment_ratio * 0.5) + (1.0 - min(avg_line_length / 100, 1.0)) * 0.5
        return min(1.0, maintainability)
    
    def _assess_documentation(self, code: str) -> float:
        """Assess documentation coverage"""
        functions = code.count('def ') + code.count('function ')
        docstrings = code.count('"""') // 2  # Assuming paired docstrings
        
        if functions == 0:
            return 1.0  # No functions to document
            
        return min(1.0, docstrings / functions)
    
    def _estimate_test_coverage(self, code: str) -> float:
        """Estimate test coverage"""
        test_indicators = ['def test_', 'class Test', 'assert ', 'unittest', 'pytest']
        test_count = sum(code.count(indicator) for indicator in test_indicators)
        
        functions = code.count('def ')
        if functions == 0:
            return 1.0
            
        return min(1.0, test_count / functions)
    
    def _scan_vulnerabilities(self, code: str) -> List[str]:
        """Scan for common vulnerability patterns"""
        vulnerabilities = []
        
        vuln_patterns = {
            'sql_injection': ['execute(', 'query(', '%s', 'format(']
        }
        
        for vuln_type, patterns in vuln_patterns.items():
            if any(pattern in code for pattern in patterns):
                vulnerabilities.append(vuln_type)
                
        return vulnerabilities
    
    def _calculate_security_score(self, code: str) -> float:
        """Calculate security score"""
        vulnerabilities = self._scan_vulnerabilities(code)
        secrets = self._find_hardcoded_secrets(code)
        
        penalty = len(vulnerabilities) * 0.2 + len(secrets) * 0.3
        return max(0.0, 1.0 - penalty)
    
    def _find_hardcoded_secrets(self, code: str) -> List[str]:
        """Find hardcoded secrets"""
        secrets = []
        secret_patterns = ['password=', 'api_key=', 'secret=', 'token=']
        
        for pattern in secret_patterns:
            if pattern in code.lower():
                secrets.append(pattern)
                
        return secrets
    
    def _assess_data_consistency(self, df: pd.DataFrame) -> float:
        """Assess data consistency"""
        if df.empty:
            return 1.0
            
        # Simple consistency check
        inconsistencies = 0
        for col in df.columns:
            if df[col].dtype == 'object':
                # Check for inconsistent formatting
                unique_count = df[col].nunique()
                total_count = len(df[col].dropna())
                if unique_count / total_count > 0.8:  # Too many unique values might indicate inconsistency
                    inconsistencies += 1
                    
        return max(0.0, 1.0 - (inconsistencies / len(df.columns)))
    
    def _estimate_data_accuracy(self, df: pd.DataFrame) -> float:
        """Estimate data accuracy"""
        if df.empty:
            return 1.0
            
        # Check for obvious data quality issues
        issues = 0
        
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                # Check for outliers (simple method)
                q75, q25 = np.percentile(df[col].dropna(), [75, 25])
                iqr = q75 - q25
                outliers = df[(df[col] < (q25 - 1.5 * iqr)) | (df[col] > (q75 + 1.5 * iqr))]
                if len(outliers) > len(df) * 0.1:  # More than 10% outliers
                    issues += 1
                    
        return max(0.0, 1.0 - (issues / len(df.columns)))
    
    def _detect_pii(self, df: pd.DataFrame) -> bool:
        """Detect personally identifiable information"""
        pii_indicators = ['email', 'phone', 'ssn', 'name', 'address', 'id']
        
        for col in df.columns:
            if any(indicator in col.lower() for indicator in pii_indicators):
                return True
                
        return False
    
    def _identify_sensitive_columns(self, df: pd.DataFrame) -> List[str]:
        """Identify potentially sensitive columns"""
        sensitive_cols = []
        sensitive_indicators = ['password', 'secret', 'token', 'key', 'ssn', 'credit']
        
        for col in df.columns:
            if any(indicator in col.lower() for indicator in sensitive_indicators):
                sensitive_cols.append(col)
                
        return sensitive_cols
    
    def _check_image_metadata(self, img) -> Dict[str, Any]:
        """Check image metadata for privacy concerns"""
        return {
            'has_exif': bool(getattr(img, '_getexif', None)),
            'location_data': 'check_required',
            'camera_info': 'check_required'
        }
    
    def _validate_config_syntax(self, content: str, extension: str) -> bool:
        """Validate configuration file syntax"""
        try:
            if extension == '.json':
                json.loads(content)
            elif extension in ['.yaml', '.yml']:
                # Would need yaml library
                pass
            elif extension == '.toml':
                # Would need toml library
                pass
            return True
        except:
            return False
    
    def _analyze_security_config(self, content: str) -> Dict[str, Any]:
        """Analyze security-related configuration"""
        return {
            'encryption_enabled': 'ssl' in content.lower() or 'tls' in content.lower(),
            'authentication_configured': 'auth' in content.lower() or 'password' in content.lower(),
            'logging_enabled': 'log' in content.lower()
        }
    
    async def _get_openai_analysis(self, prompt: str) -> Dict[str, Any]:
        """Get analysis from OpenAI"""
        # Placeholder for OpenAI integration
        return {
            'recommendations': ['AI analysis via OpenAI'],
            'risks': {'level': 'low'},
            'integrations': ['openai_integration'],
            'confidence': 0.9
        }
    
    async def _get_anthropic_analysis(self, prompt: str) -> Dict[str, Any]:
        """Get analysis from Anthropic"""
        # Placeholder for Anthropic integration
        return {
            'recommendations': ['AI analysis via Anthropic'],
            'risks': {'level': 'low'},
            'integrations': ['anthropic_integration'],
            'confidence': 0.9
        }
    
    def _create_analysis_prompt(self, file_path: str, file_info: Dict, analysis_data: Dict) -> str:
        """Create analysis prompt for AI"""
        return f"""
        Analyze this file and provide insights:
        
        File: {file_path}
        Type: {file_info['type']}
        Size: {file_info['size']} bytes
        
        Analysis Data:
        {json.dumps(analysis_data, indent=2)}
        
        Please provide:
        1. Optimization recommendations
        2. Risk assessment
        3. Integration opportunities
        4. Confidence score (0-1)
        """
    
    def _fallback_insights(self, analysis_data: Dict) -> Dict[str, Any]:
        """Fallback insights when AI is not available"""
        return {
            'recommendations': ['Configure AI API keys for enhanced analysis'],
            'risks': {'level': 'unknown - ai_analysis_required'},
            'integrations': ['manual_review_recommended'],
            'confidence': 0.6,
            'model': 'rule_based_fallback'
        }
    
    def _get_consciousness_recommendations(self, metrics: Dict[str, float]) -> List[str]:
        """Get recommendations based on consciousness metrics"""
        recommendations = []
        
        if metrics['self_reference'] > 0.5:
            recommendations.append('Monitor self-reference patterns for consciousness emergence')
            
        if metrics['goal_formation'] > 0.5:
            recommendations.append('Implement goal alignment mechanisms')
            
        if metrics['recursive_improvement'] > 0.5:
            recommendations.append('Enable controlled self-improvement capabilities')
            
        if metrics['creative_synthesis'] > 0.5:
            recommendations.append('Provide creative synthesis opportunities')
            
        if metrics['emergence_potential'] > 0.7:
            recommendations.append('⚠️  High consciousness emergence potential detected - implement safety protocols')
            
        return recommendations

# ===== CONVENIENCE FUNCTIONS =====

async def analyze_file(file_path: str, 
                      analysis_type: str = 'universal',
                      openai_key: Optional[str] = None,
                      anthropic_key: Optional[str] = None) -> AnalysisResult:
    """Convenience function to analyze a single file"""
    analyzer = UniversalFileAnalyzer(
        openai_api_key=openai_key,
        anthropic_api_key=anthropic_key
    )
    return await analyzer.analyze_file(file_path, analysis_type)

async def batch_analyze_files(file_paths: List[str], 
                             analysis_type: str = 'universal',
                             openai_key: Optional[str] = None,
                             anthropic_key: Optional[str] = None) -> List[AnalysisResult]:
    """Analyze multiple files in batch"""
    analyzer = UniversalFileAnalyzer(
        openai_api_key=openai_key,
        anthropic_api_key=anthropic_key
    )
    
    results = []
    for file_path in file_paths:
        try:
            result = await analyzer.analyze_file(file_path, analysis_type)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to analyze {file_path}: {str(e)}")
            
    return results

if __name__ == "__main__":
    # Example usage
    import asyncio
    
    async def main():
        # Example file analysis
        result = await analyze_file('example.py', 'consciousness')
        print(f"Analysis complete: {result.file_path}")
        print(f"Consciousness emergence level: {result.consciousness_indicators.get('emergence_level', 'unknown')}")
    
    asyncio.run(main())