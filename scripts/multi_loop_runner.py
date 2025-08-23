#!/usr/bin/env python3
"""
Multi-Loop Audit Runner

Runs all loops (A-F) for multiple passes
"""

import subprocess
import json
import time
from pathlib import Path
from typing import Dict, Any

class MultiLoopRunner:
    def __init__(self):
        self.scripts = {
            'A': 'scripts/var_func_map.py',
            'B': ['scripts/env_audit.py', 'scripts/bug_audit.py', 'scripts/data_journey.py'],
            'C': 'scripts/flow_design.py',
            'D': 'scripts/arch_synthesis.py',
            'E': ['scripts/routing_realignment.py', 'scripts/exec_plan.py'],
            'F': 'scripts/source_of_truth.py'
        }
        self.pass_results = []
        
    def run_script(self, script_path: str) -> bool:
        """Run a single script and return success status"""
        try:
            print(f"  Running {script_path}...")
            result = subprocess.run(['python3', script_path], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"    ⚠️  Script failed with error:")
                print(f"    {result.stderr}")
                return False
            else:
                # Extract summary info from output
                output_lines = result.stdout.strip().split('\n')
                for line in output_lines[-10:]:  # Check last 10 lines for summary
                    if '✓' in line or 'Score:' in line or 'Total' in line:
                        print(f"    {line}")
                return True
        except Exception as e:
            print(f"    ❌ Error running script: {e}")
            return False
            
    def run_loop(self, loop_letter: str, pass_num: int) -> Dict[str, Any]:
        """Run all scripts for a specific loop"""
        print(f"\n### Pass {pass_num} - Loop {loop_letter}")
        
        loop_results = {
            'loop': loop_letter,
            'pass': pass_num,
            'success': True,
            'scripts_run': []
        }
        
        scripts = self.scripts.get(loop_letter)
        if isinstance(scripts, list):
            for script in scripts:
                success = self.run_script(script)
                loop_results['scripts_run'].append({
                    'script': script,
                    'success': success
                })
                if not success:
                    loop_results['success'] = False
        else:
            success = self.run_script(scripts)
            loop_results['scripts_run'].append({
                'script': scripts,
                'success': success
            })
            if not success:
                loop_results['success'] = False
                
        return loop_results
        
    def run_pass(self, pass_num: int) -> Dict[str, Any]:
        """Run all loops for a single pass"""
        print(f"\n## Starting Pass {pass_num}")
        
        pass_result = {
            'pass_number': pass_num,
            'start_time': time.time(),
            'loops': []
        }
        
        for loop in ['A', 'B', 'C', 'D', 'E', 'F']:
            loop_result = self.run_loop(loop, pass_num)
            pass_result['loops'].append(loop_result)
            
        pass_result['end_time'] = time.time()
        pass_result['duration'] = pass_result['end_time'] - pass_result['start_time']
        
        # Load alignment scores from source of truth
        try:
            with open('reports/organizer_manifest.json', 'r') as f:
                manifest = json.load(f)
                pass_result['alignment_scores'] = manifest.get('alignment_summary', {})
        except:
            pass_result['alignment_scores'] = {}
            
        return pass_result
        
    def run_multiple_passes(self, start_pass: int, end_pass: int):
        """Run multiple passes"""
        print(f"Running passes {start_pass} through {end_pass}")
        
        for pass_num in range(start_pass, end_pass + 1):
            pass_result = self.run_pass(pass_num)
            self.pass_results.append(pass_result)
            
            # Update manifest with pass number
            try:
                with open('reports/organizer_manifest.json', 'r') as f:
                    manifest = json.load(f)
                manifest['pass_number'] = pass_num
                with open('reports/organizer_manifest.json', 'w') as f:
                    json.dump(manifest, f, indent=2)
            except:
                pass
                
            # Print pass summary
            print(f"\n### Pass {pass_num} Complete!")
            print(f"Duration: {pass_result['duration']:.1f} seconds")
            if pass_result['alignment_scores']:
                print("Alignment Scores:")
                for category, score_data in pass_result['alignment_scores'].items():
                    if isinstance(score_data, dict) and 'score' in score_data:
                        print(f"  - {category}: {score_data['score']:.1f}%")
                        
        # Save overall results
        self.save_results()
        
    def save_results(self):
        """Save results from all passes"""
        results = {
            'total_passes': len(self.pass_results),
            'passes': self.pass_results,
            'final_alignment': self.pass_results[-1].get('alignment_scores', {}) if self.pass_results else {}
        }
        
        with open('reports/multi_loop_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        # Generate summary report
        with open('reports/MULTI_LOOP_SUMMARY.md', 'w') as f:
            f.write("# Multi-Loop Audit Summary\n\n")
            f.write(f"## Total Passes Completed: {len(self.pass_results)}\n\n")
            
            if self.pass_results:
                # Show alignment trend
                f.write("## Alignment Score Trends\n\n")
                f.write("| Pass | Architecture | Features | Data Flow | Routing | Quality | Operations |\n")
                f.write("|------|-------------|----------|-----------|---------|---------|------------|\n")
                
                for result in self.pass_results:
                    scores = result.get('alignment_scores', {})
                    f.write(f"| {result['pass_number']} ")
                    for category in ['architecture', 'features', 'data_flow', 'routing', 'quality', 'operations']:
                        score_data = scores.get(category, {})
                        score = score_data.get('score', 0) if isinstance(score_data, dict) else 0
                        f.write(f"| {score:.1f}% ")
                    f.write("|\n")
                    
                # Final scores
                final_scores = self.pass_results[-1].get('alignment_scores', {})
                f.write(f"\n## Final Alignment Scores (Pass {self.pass_results[-1]['pass_number']})\n\n")
                overall_total = 0
                overall_count = 0
                for category, score_data in final_scores.items():
                    if isinstance(score_data, dict) and 'score' in score_data:
                        f.write(f"- **{category.replace('_', ' ').title()}**: {score_data['score']:.1f}%\n")
                        overall_total += score_data['score']
                        overall_count += 1
                        
                if overall_count > 0:
                    f.write(f"\n**Overall Average**: {overall_total / overall_count:.1f}%\n")


def main():
    runner = MultiLoopRunner()
    
    # Run passes 4 through 10
    runner.run_multiple_passes(4, 10)
    
    print("\n✅ All passes complete!")
    print("Reports saved to:")
    print("  - reports/multi_loop_results.json")
    print("  - reports/MULTI_LOOP_SUMMARY.md")


if __name__ == "__main__":
    main()