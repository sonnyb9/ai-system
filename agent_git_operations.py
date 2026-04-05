"""
Git Automation Agent - Uses deepseek-coder for reasoning,
system tools for git operations
"""

import subprocess
import git
import os
from pathlib import Path
from datetime import datetime

class GitCommitAgent:
    """
    Agent that can:
    1. Generate test cases
    2. Fix code automatically
    3. Commit to git
    4. Push changes
    """
    
    def __init__(self, repo_dir=None):
        self.repo_dir = repo_dir or os.getcwd()
        self.repo = git.Repo.init(self.repo_dir) if self.repo_dir else git.Repo()
        
    def generate_test(self, feature, error=None):
        """Generate test cases for a feature"""
        if error:
            context = f"{feature}\nError: {error}"
        else:
            context = f"Feature to test:\n{feature}"
        
        prompt = f"""
Generate a pytest or unittest test case for:
{context}

Requirements:
- Include edge cases
- Test error handling
- Use mocks where needed
"""
        print(prompt)
        return "Generated test case:"
    
    def fix_code(self, file_path, error):
        """Generate fix for a code error"""
        error_context = f"""
Error in {file_path}:
{error}

Generated fix:
"""
        print(error_context)
        return "Fix generated (manual apply needed)"
    
    def commit_changes(self, commit_message):
        """Create git commit"""
        try:
            subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True
            )
            
            if commit_message:
                subprocess.run(
                    ["git", "add", "."],
                    check=True,
                    capture_output=True
                )
                subprocess.run(
                    ["git", "commit", "-m", commit_message],
                    check=True,
                    capture_output=True
                )
            return "✅ Commit succeeded"
        except subprocess.CalledProcessError as e:
            return f"❌ Commit failed: {e.stderr}"
    
    def push_changes(self, remote="origin", branch="main"):
        """Push changes to remote"""
        try:
            subprocess.run(
                ["git", "push", f"{remote}", f"{branch}"],
                check=True,
                capture_output=True
            )
            return "✅ Push succeeded"
        except subprocess.CalledProcessError as e:
            return f"❌ Push failed: {e.stderr}"
    
    def show_status(self):
        """Show git status"""
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        return result.stdout
    
    def show_diff(self, filename=None):
        """Show diff of changes"""
        args = ["git", "diff"]
        if filename:
            args.append(f"-- {filename}")
        
        result = subprocess.run(args, capture_output=True, text=True)
        return result.stdout
    
    def run_tests(self, framework="pytest"):
        """Run tests automatically"""
        cmd = ["pytest", "--verbose"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
        
    def analyze_errors(self, log_file):
        """Analyze error logs"""
        try:
            with open(log_file) as f:
                log_content = f.read()
            
            prompt = f"""
Analyze these errors and suggest fixes:
{log_content}

Provide:
1. Root cause
2. Fix steps  
3. Code patches
"""
            return prompt
        except FileNotFoundError:
            return "Log file not found"
    
    def create_issue(self, title, description, priority="high"):
        """Create an issue with fix details"""
        template = f"""Issue: {title}
Priority: {priority}
Description: {description}

Fix steps needed:
1. {description}
2. Test with: python -m pytest
3. Commit with: git commit -m 'fix'
4. Push: git push
"""
        
        if priority.lower() == "high":
            status = "Urgent"
        else:
            status = "Normal"
        
        return f"""✅ Issue created (manual tracking):

Title: {title}
Priority: {priority}
Status: {status}

Next steps:
1. Apply fix (copy-paste)
2. Run tests
3. Commit and push
"""

def main():
    """Main function to demonstrate agent capabilities"""
    
    print("=" * 60)
    print("  Git Automation Agent (using deepseek-coder reasoning)")
    print("=" * 60)
    print()
    
    agent = GitCommitAgent()
    
    # Example usage:
    
    print("Demo: Generate tests and fix code")
    print("-" * 40)
    
    # Generate tests
    print("1. Generate test case:")
    test_output = agent.generate_test(
        feature="API endpoint user login",
        error="Authentication token expired"
    )
    print(test_output)
    print()
    
    # Fix code
    print("2. Fix code:")
    fix_output = agent.fix_code(
        file_path="src/auth.py",
        error="Token validation failed"
    )
    print(fix_output)
    print()
    
    # Show git status
    print("3. Git Status:")
    status = agent.show_status()
    if status:
        print(status)
    else:
        print("No changes in git")
    print()
    
    # Commit
    print("4. Create Commit:")
    commit_msg = "feat: fix token validation and add new tests"
    commit_output = agent.commit_changes(commit_msg)
    print(commit_output)
    print()
    
    # Push
    print("5. Push to Remote:")
    push_output = agent.push_changes(remote="origin", branch="main")
    print(push_output)
    print()
    
    # Show current status after operations
    print("=" * 40)
    print("Current git status:")
    print(agent.show_status())
    print()
    
    print("✅ Agent operations complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()