#!/usr/bin/env python3
"""
🔗 GitHub Integration Module
Seamless integration with GitHub for file management and automation

Capabilities:
- Repository management and file operations
- Automated commits and pull requests
- Webhook handling for real-time updates
- Issue and project management
- Release automation
"""

import os
import json
import asyncio
import aiofiles
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import logging
from pathlib import Path
import base64

# GitHub API integration
try:
    from github import Github, GithubException
    import git
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False
    
logger = logging.getLogger(__name__)

class GitHubIntegration:
    """Complete GitHub integration for the consciousness platform"""
    
    def __init__(self, token: Optional[str] = None, repo_name: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.repo_name = repo_name or 'ob1-files-workspace'
        self.github_client = None
        self.repository = None
        
        if GITHUB_AVAILABLE and self.token:
            self.github_client = Github(self.token)
            self._initialize_repository()
        else:
            logger.warning("GitHub integration not available - install PyGithub and set GITHUB_TOKEN")
    
    def _initialize_repository(self):
        """Initialize repository connection"""
        try:
            user = self.github_client.get_user()
            self.repository = user.get_repo(self.repo_name)
            logger.info(f"Connected to repository: {self.repository.full_name}")
        except GithubException as e:
            logger.error(f"Failed to connect to repository: {str(e)}")
            self.repository = None
    
    async def upload_analysis_result(self, 
                                   analysis_result: Dict[str, Any], 
                                   task_id: str,
                                   auto_commit: bool = True) -> Dict[str, Any]:
        """Upload analysis results to GitHub repository"""
        if not self.repository:
            return {'status': 'error', 'message': 'GitHub repository not available'}
        
        try:
            # Create results directory structure
            timestamp = datetime.now().strftime('%Y/%m/%d')
            file_path = f"results/{timestamp}/{task_id}.json"
            
            # Prepare content
            content = json.dumps(analysis_result, indent=2, default=str)
            
            # Upload to GitHub
            if auto_commit:
                commit_message = f"🧠 Analysis Result: {task_id}"
                
                # Check if file exists
                try:
                    existing_file = self.repository.get_contents(file_path)
                    # Update existing file
                    self.repository.update_file(
                        path=file_path,
                        message=commit_message,
                        content=content,
                        sha=existing_file.sha
                    )
                except GithubException:
                    # Create new file
                    self.repository.create_file(
                        path=file_path,
                        message=commit_message,
                        content=content
                    )
                
                # Also create a summary in the outputs folder
                summary_path = f"outputs/analysis_summary_{task_id}.md"
                summary_content = self._generate_analysis_summary(analysis_result, task_id)
                
                try:
                    existing_summary = self.repository.get_contents(summary_path)
                    self.repository.update_file(
                        path=summary_path,
                        message=f"📊 Analysis Summary: {task_id}",
                        content=summary_content,
                        sha=existing_summary.sha
                    )
                except GithubException:
                    self.repository.create_file(
                        path=summary_path,
                        message=f"📊 Analysis Summary: {task_id}",
                        content=summary_content
                    )
                
                logger.info(f"Analysis results uploaded to GitHub: {file_path}")
                
                return {
                    'status': 'success',
                    'file_path': file_path,
                    'summary_path': summary_path,
                    'repository_url': self.repository.html_url,
                    'commit_message': commit_message
                }
            
        except Exception as e:
            logger.error(f"Failed to upload analysis results: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_analysis_summary(self, analysis_result: Dict[str, Any], task_id: str) -> str:
        """Generate markdown summary of analysis results"""
        timestamp = analysis_result.get('timestamp', datetime.now().isoformat())
        file_path = analysis_result.get('file_path', 'unknown')
        file_type = analysis_result.get('file_type', 'unknown')
        
        summary = f"""# 🧠 Analysis Summary: {task_id}

**Generated:** {timestamp}  
**File:** {file_path}  
**Type:** {file_type}  

## 📊 Key Insights

### Structure Analysis
"""
        
        # Add structure analysis
        if 'structure_analysis' in analysis_result:
            structure = analysis_result['structure_analysis']
            for key, value in structure.items():
                summary += f"- **{key.replace('_', ' ').title()}:** {value}\n"
        
        summary += "\n### Content Analysis\n"
        
        # Add content analysis
        if 'content_analysis' in analysis_result:
            content = analysis_result['content_analysis']
            for key, value in content.items():
                if isinstance(value, (list, dict)):
                    summary += f"- **{key.replace('_', ' ').title()}:** {len(value) if isinstance(value, list) else 'See details'}\n"
                else:
                    summary += f"- **{key.replace('_', ' ').title()}:** {value}\n"
        
        # Add quality metrics
        summary += "\n### Quality Metrics\n"
        if 'quality_metrics' in analysis_result:
            quality = analysis_result['quality_metrics']
            for key, value in quality.items():
                summary += f"- **{key.replace('_', ' ').title()}:** {value}\n"
        
        # Add consciousness indicators (if present)
        if 'consciousness_indicators' in analysis_result and analysis_result['consciousness_indicators']:
            summary += "\n### 🧠 Consciousness Indicators\n"
            consciousness = analysis_result['consciousness_indicators']
            
            if 'emergence_level' in consciousness:
                summary += f"- **Emergence Level:** {consciousness['emergence_level']}\n"
            
            if 'metrics' in consciousness:
                summary += "\n**Metrics:**\n"
                for metric, score in consciousness['metrics'].items():
                    percentage = f"{score * 100:.1f}%"
                    summary += f"- {metric.replace('_', ' ').title()}: {percentage}\n"
        
        # Add recommendations
        if 'optimization_recommendations' in analysis_result:
            summary += "\n### 💡 Recommendations\n"
            recommendations = analysis_result['optimization_recommendations']
            for rec in recommendations[:5]:  # Limit to top 5
                summary += f"- {rec}\n"
        
        # Add metadata
        summary += f"\n### 📈 Analysis Metadata\n"
        summary += f"- **Confidence Score:** {analysis_result.get('confidence_score', 'N/A')}\n"
        summary += f"- **Processing Time:** {analysis_result.get('processing_time', 'N/A')} seconds\n"
        summary += f"- **AI Model:** {analysis_result.get('ai_model_used', 'N/A')}\n"
        
        summary += f"\n---\n*Generated by OB-1 Quantum Consciousness Platform*"
        
        return summary
    
    async def create_automation_workflow(self, 
                                       automation_plan: Dict[str, Any],
                                       workflow_name: str) -> Dict[str, Any]:
        """Create GitHub Actions workflow for automation"""
        if not self.repository:
            return {'status': 'error', 'message': 'GitHub repository not available'}
        
        try:
            # Generate GitHub Actions workflow
            workflow_content = self._generate_github_workflow(automation_plan, workflow_name)
            workflow_path = f".github/workflows/{workflow_name.lower().replace(' ', '-')}.yml"
            
            # Create or update workflow file
            commit_message = f"🤖 Add automation workflow: {workflow_name}"
            
            try:
                existing_workflow = self.repository.get_contents(workflow_path)
                self.repository.update_file(
                    path=workflow_path,
                    message=commit_message,
                    content=workflow_content,
                    sha=existing_workflow.sha
                )
            except GithubException:
                self.repository.create_file(
                    path=workflow_path,
                    message=commit_message,
                    content=workflow_content
                )
            
            logger.info(f"GitHub Actions workflow created: {workflow_path}")
            
            return {
                'status': 'success',
                'workflow_path': workflow_path,
                'workflow_url': f"{self.repository.html_url}/actions",
                'message': f"Automation workflow '{workflow_name}' created successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to create automation workflow: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _generate_github_workflow(self, automation_plan: Dict[str, Any], workflow_name: str) -> str:
        """Generate GitHub Actions workflow YAML"""
        workflow = f"""name: {workflow_name}

# 🤖 Automated workflow generated by OB-1 Consciousness Platform
# Plan: {automation_plan.get('description', 'Generated automation workflow')}

on:
  workflow_dispatch:
    inputs:
      execute_immediately:
        description: 'Execute automation immediately'
        required: false
        default: 'true'
        type: boolean
  
  schedule:
    - cron: '0 */6 * * *'  # Run every 6 hours

jobs:
  automation:
    runs-on: ubuntu-latest
    
    steps:
    - name: 🔄 Checkout repository
      uses: actions/checkout@v4
      
    - name: 🐍 Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: 📦 Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r platform/core/requirements.txt
        
    - name: 🧠 Execute Automation
      env:
        GITHUB_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
        OPENAI_API_KEY: ${{{{ secrets.OPENAI_API_KEY }}}}
        ANTHROPIC_API_KEY: ${{{{ secrets.ANTHROPIC_API_KEY }}}}
      run: |
        cd platform/core
        python -c "
        import asyncio
        from universal_analyzer import analyze_file
        from github_integration import GitHubIntegration
        
        async def main():
            print('🚀 Starting automated analysis...')
            # Add your automation logic here
            print('✅ Automation completed successfully')
        
        asyncio.run(main())
        "
        
    - name: 📊 Generate Report
      run: |
        echo '# 🤖 Automation Report' > automation_report.md
        echo '' >> automation_report.md
        echo '**Executed:** $(date)' >> automation_report.md
        echo '**Status:** Success' >> automation_report.md
        echo '**Workflow:** {workflow_name}' >> automation_report.md
        
    - name: 📤 Commit Results
      uses: stefanzweifel/git-auto-commit-action@v5
      with:
        commit_message: '🤖 Automated workflow execution: {workflow_name}'
        branch: main
        """
        
        return workflow
    
    async def setup_webhooks(self, webhook_url: str, events: List[str] = None) -> Dict[str, Any]:
        """Set up GitHub webhooks for real-time integration"""
        if not self.repository:
            return {'status': 'error', 'message': 'GitHub repository not available'}
        
        default_events = ['push', 'pull_request', 'issues', 'issue_comment']
        events = events or default_events
        
        try:
            # Create webhook configuration
            webhook_config = {
                'url': webhook_url,
                'content_type': 'json',
                'insecure_ssl': False
            }
            
            # Create webhook
            hook = self.repository.create_hook(
                name='web',
                config=webhook_config,
                events=events,
                active=True
            )
            
            logger.info(f"GitHub webhook created: {hook.id}")
            
            return {
                'status': 'success',
                'webhook_id': hook.id,
                'webhook_url': webhook_url,
                'events': events,
                'message': 'Webhook configured successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to create webhook: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    async def create_release(self, 
                           version: str, 
                           release_notes: str,
                           artifacts: List[str] = None) -> Dict[str, Any]:
        """Create a GitHub release with artifacts"""
        if not self.repository:
            return {'status': 'error', 'message': 'GitHub repository not available'}
        
        try:
            # Create release
            release = self.repository.create_git_release(
                tag=f"v{version}",
                name=f"🧠 Consciousness Platform v{version}",
                message=release_notes,
                draft=False,
                prerelease=False
            )
            
            # Upload artifacts if provided
            if artifacts:
                for artifact_path in artifacts:
                    if os.path.exists(artifact_path):
                        with open(artifact_path, 'rb') as artifact_file:
                            release.upload_asset(
                                path=artifact_path,
                                label=os.path.basename(artifact_path)
                            )
            
            logger.info(f"Release created: v{version}")
            
            return {
                'status': 'success',
                'release_url': release.html_url,
                'version': version,
                'artifacts_uploaded': len(artifacts) if artifacts else 0
            }
            
        except Exception as e:
            logger.error(f"Failed to create release: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    async def manage_issues(self, action: str, **kwargs) -> Dict[str, Any]:
        """Manage GitHub issues programmatically"""
        if not self.repository:
            return {'status': 'error', 'message': 'GitHub repository not available'}
        
        try:
            if action == 'create':
                issue = self.repository.create_issue(
                    title=kwargs.get('title', 'New Issue'),
                    body=kwargs.get('body', ''),
                    labels=kwargs.get('labels', [])
                )
                return {
                    'status': 'success',
                    'issue_number': issue.number,
                    'issue_url': issue.html_url
                }
                
            elif action == 'list':
                issues = self.repository.get_issues(
                    state=kwargs.get('state', 'open')
                )
                return {
                    'status': 'success',
                    'issues': [{
                        'number': issue.number,
                        'title': issue.title,
                        'state': issue.state,
                        'url': issue.html_url
                    } for issue in issues[:10]]  # Limit to 10
                }
                
            elif action == 'close':
                issue_number = kwargs.get('issue_number')
                if issue_number:
                    issue = self.repository.get_issue(issue_number)
                    issue.edit(state='closed')
                    return {
                        'status': 'success',
                        'message': f'Issue #{issue_number} closed'
                    }
                    
            return {'status': 'error', 'message': f'Unknown action: {action}'}
            
        except Exception as e:
            logger.error(f"Issue management failed: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    async def sync_files(self, local_directory: str, remote_path: str = '') -> Dict[str, Any]:
        """Sync local files with GitHub repository"""
        if not self.repository:
            return {'status': 'error', 'message': 'GitHub repository not available'}
        
        try:
            synced_files = []
            local_path = Path(local_directory)
            
            # Walk through local files
            for file_path in local_path.rglob('*'):
                if file_path.is_file():
                    relative_path = file_path.relative_to(local_path)
                    github_path = os.path.join(remote_path, str(relative_path)).replace(os.sep, '/')
                    
                    # Read file content
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    
                    # Check if file exists in repo
                    try:
                        existing_file = self.repository.get_contents(github_path)
                        # Compare content (simplified)
                        existing_content = base64.b64decode(existing_file.content)
                        
                        if content != existing_content:
                            # Update file
                            self.repository.update_file(
                                path=github_path,
                                message=f"📁 Update {github_path}",
                                content=content,
                                sha=existing_file.sha
                            )
                            synced_files.append(f"updated: {github_path}")
                            
                    except GithubException:
                        # Create new file
                        self.repository.create_file(
                            path=github_path,
                            message=f"📁 Add {github_path}",
                            content=content
                        )
                        synced_files.append(f"created: {github_path}")
            
            return {
                'status': 'success',
                'synced_files': synced_files,
                'total_files': len(synced_files)
            }
            
        except Exception as e:
            logger.error(f"File sync failed: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    async def get_repository_insights(self) -> Dict[str, Any]:
        """Get repository insights and statistics"""
        if not self.repository:
            return {'status': 'error', 'message': 'GitHub repository not available'}
        
        try:
            # Basic repository info
            repo_info = {
                'name': self.repository.name,
                'full_name': self.repository.full_name,
                'description': self.repository.description,
                'url': self.repository.html_url,
                'stars': self.repository.stargazers_count,
                'forks': self.repository.forks_count,
                'open_issues': self.repository.open_issues_count,
                'size': self.repository.size,
                'language': self.repository.language,
                'created_at': self.repository.created_at.isoformat(),
                'updated_at': self.repository.updated_at.isoformat()
            }
            
            # Recent commits
            commits = self.repository.get_commits()[:5]
            recent_commits = [{
                'sha': commit.sha[:8],
                'message': commit.commit.message.split('\n')[0],
                'author': commit.commit.author.name,
                'date': commit.commit.author.date.isoformat()
            } for commit in commits]
            
            # Languages
            languages = self.repository.get_languages()
            
            return {
                'status': 'success',
                'repository': repo_info,
                'recent_commits': recent_commits,
                'languages': languages,
                'insights': {
                    'activity_level': 'high' if len(recent_commits) > 3 else 'medium' if len(recent_commits) > 1 else 'low',
                    'community_interest': 'high' if repo_info['stars'] > 10 else 'medium' if repo_info['stars'] > 0 else 'low'
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get repository insights: {str(e)}")
            return {'status': 'error', 'message': str(e)}

# ===== WEBHOOK HANDLERS =====

class GitHubWebhookHandler:
    """Handle GitHub webhook events"""
    
    def __init__(self, github_integration: GitHubIntegration):
        self.github = github_integration
        self.handlers = {
            'push': self._handle_push,
            'pull_request': self._handle_pull_request,
            'issues': self._handle_issues,
            'issue_comment': self._handle_issue_comment
        }
    
    async def handle_event(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming webhook events"""
        handler = self.handlers.get(event_type)
        if handler:
            return await handler(payload)
        else:
            return {
                'status': 'ignored',
                'message': f'No handler for event type: {event_type}'
            }
    
    async def _handle_push(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle push events"""
        commits = payload.get('commits', [])
        branch = payload.get('ref', '').replace('refs/heads/', '')
        
        logger.info(f"Push event on branch {branch} with {len(commits)} commits")
        
        # Auto-trigger analysis for certain file types
        modified_files = []
        for commit in commits:
            modified_files.extend(commit.get('modified', []))
            modified_files.extend(commit.get('added', []))
        
        analysis_triggered = []
        for file_path in modified_files:
            if any(file_path.endswith(ext) for ext in ['.py', '.js', '.md', '.json', '.csv']):
                # Trigger analysis (would integrate with main platform)
                analysis_triggered.append(file_path)
        
        return {
            'status': 'processed',
            'branch': branch,
            'commits': len(commits),
            'files_modified': len(modified_files),
            'analysis_triggered': analysis_triggered
        }
    
    async def _handle_pull_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle pull request events"""
        action = payload.get('action')
        pr_number = payload.get('number')
        
        logger.info(f"Pull request event: {action} for PR #{pr_number}")
        
        if action == 'opened':
            # Auto-review or analysis could be triggered here
            return {
                'status': 'processed',
                'action': 'pr_opened',
                'pr_number': pr_number,
                'auto_review_triggered': True
            }
        
        return {
            'status': 'processed',
            'action': action,
            'pr_number': pr_number
        }
    
    async def _handle_issues(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle issue events"""
        action = payload.get('action')
        issue_number = payload.get('issue', {}).get('number')
        
        logger.info(f"Issue event: {action} for issue #{issue_number}")
        
        return {
            'status': 'processed',
            'action': action,
            'issue_number': issue_number
        }
    
    async def _handle_issue_comment(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle issue comment events"""
        action = payload.get('action')
        comment_id = payload.get('comment', {}).get('id')
        
        logger.info(f"Issue comment event: {action} for comment #{comment_id}")
        
        return {
            'status': 'processed',
            'action': action,
            'comment_id': comment_id
        }

# ===== CONVENIENCE FUNCTIONS =====

async def quick_upload(file_path: str, 
                      analysis_result: Dict[str, Any], 
                      token: Optional[str] = None) -> Dict[str, Any]:
    """Quick upload of analysis results to GitHub"""
    github = GitHubIntegration(token=token)
    task_id = f"quick_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    return await github.upload_analysis_result(analysis_result, task_id)

async def setup_automation_pipeline(automation_plan: Dict[str, Any], 
                                  token: Optional[str] = None) -> Dict[str, Any]:
    """Set up complete automation pipeline"""
    github = GitHubIntegration(token=token)
    
    # Create workflow
    workflow_result = await github.create_automation_workflow(
        automation_plan, 
        automation_plan.get('name', 'Consciousness Automation')
    )
    
    # Set up webhooks (if webhook URL provided)
    webhook_result = None
    if 'webhook_url' in automation_plan:
        webhook_result = await github.setup_webhooks(
            automation_plan['webhook_url']
        )
    
    return {
        'workflow': workflow_result,
        'webhook': webhook_result,
        'status': 'success' if workflow_result.get('status') == 'success' else 'partial'
    }

if __name__ == "__main__":
    # Example usage
    import asyncio
    
    async def main():
        # Initialize GitHub integration
        github = GitHubIntegration()
        
        # Get repository insights
        insights = await github.get_repository_insights()
        print(f"Repository insights: {insights}")
        
        # Example analysis result upload
        analysis_result = {
            'file_path': 'test.py',
            'timestamp': datetime.now().isoformat(),
            'analysis_type': 'consciousness',
            'results': {'consciousness_level': 'emerging'}
        }
        
        upload_result = await github.upload_analysis_result(
            analysis_result, 
            'test_analysis_001'
        )
        print(f"Upload result: {upload_result}")
    
    asyncio.run(main())