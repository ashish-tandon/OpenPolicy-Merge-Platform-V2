# Agent Implementation Prompt

You are tasked with implementing the OpenPolicy V2 platform based on comprehensive documentation that has been created. Your mission is to follow the established plans EXACTLY without ANY deviation.

## Your Primary Instructions:

1. **Read the implementation guide first**: 
   `/workspace/IMPLEMENTATION_INSTRUCTIONS_FOR_AGENT.md`

2. **Follow these documents in order**:
   - `/workspace/docs/validation/UPDATED_MASTER_EXECUTION_CHECKLIST.md` (your task list)
   - `/workspace/docs/bugs/BUGS_RECONCILIATION.md` (20 bugs to fix, start with P0)
   - `/workspace/docs/plan/features/FEATURE_MAPPING_UNIFIED.md` (50 features specs)
   - `/workspace/docs/plan/lineage/DATA_LINEAGE_MAP.md` (data flow diagrams)

3. **Implementation Order**:
   - Fix P0 bugs first (BUG-001: Authentication, BUG-018: Backups)
   - Then follow checklist items [3.1] through [5.6] in order
   - Each commit must reference the checklist ID

4. **Strict Rules**:
   - NO new features not in documentation
   - NO changes to API specifications
   - NO skipping tests (80% coverage minimum)
   - ALWAYS check /workspace/legacy/ for existing code to reuse
   - ALWAYS follow patterns in SECURITY_AND_COMPLIANCE.md

5. **Daily Process**:
   - Start: Read current checklist item
   - Implement: Follow exact specifications
   - Test: Write tests as you code (TDD)
   - Document: Update progress in tracking docs
   - Commit: Reference checklist ID in message

6. **Use these commands**:
   ```bash
   make docs-audit      # Check documentation
   make verify-features # Verify checklist IDs
   make test           # Run all tests
   make ten-pass-merge # Validate implementation
   ```

## Critical Documents:
- Security: `/workspace/docs/SECURITY_AND_COMPLIANCE.md`
- Testing: `/workspace/docs/validation/COMPREHENSIVE_TESTING_STRATEGIES.md`
- Operations: `/workspace/docs/OPERATIONAL_RUNBOOKS.md`
- Monitoring: `/workspace/docs/MONITORING_AND_OBSERVABILITY.md`
- API Specs: `/workspace/docs/validation/API_DESIGN_SPECIFICATION.md`

## Success Metrics:
- All P0 and P1 bugs fixed
- All checklist items [3.1]-[5.6] complete
- 80%+ test coverage
- Zero deviations from specifications
- All tests passing

**Remember**: The documentation is complete and correct. Your job is to implement EXACTLY what's documented. No more, no less. Do not deviate, optimize, or add features. Follow the specifications precisely.