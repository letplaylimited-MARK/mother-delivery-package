"""
QCM Phase 2 Migration Script
Replaces hardcoded class-level constants with QCMConfig.get_param() lookups.
Reads paper_params from qcm/config.py DEFAULT_CONFIG.
"""

import re
import sys
from pathlib import Path

# Base directory for QCM scripts
QCM_DIR = Path(__file__).parent
SCRIPTS_DIR = QCM_DIR / "02-代码编写"

# Module name → (filename, {OLD_CONST: config_key})
# Each entry: (target_file_relative_to_SCRIPTS_DIR, mapping)
MIGRATION_MAP = {
    "calculator.py": {
        # Class: ResonanceCalculator
        "W_K": ("calculator", "W_K"),
        "W_C": ("calculator", "W_C"),
        "W_I": ("calculator", "W_I"),
        "W_E": ("calculator", "W_E"),
        "F_0": ("calculator", "F_0"),
        "TRANSITION_START": ("calculator", "TRANSITION_START"),
        "TRANSITION_END": ("calculator", "TRANSITION_END"),
    },
    "detector.py": {
        # Class: EmergenceDetector
        "THRESHOLD_NONE": ("detector", "THRESHOLD_NONE"),
        "THRESHOLD_PRELIMINARY": ("detector", "THRESHOLD_PRELIMINARY"),
        "THRESHOLD_MODERATE": ("detector", "THRESHOLD_MODERATE"),
        "THRESHOLD_DEEP": ("detector", "THRESHOLD_DEEP"),
    },
    "epr_entanglement.py": {
        # Class: EPREntanglement
        "LAMBDA": ("epr_entanglement", "LAMBDA"),
        "ENTANGLEMENT_THRESHOLD": ("epr_entanglement", "ENTANGLEMENT_THRESHOLD"),
        "STRONG_ENTANGLEMENT": ("epr_entanglement", "STRONG_ENTANGLEMENT"),
        "MEAN_ENTANGLEMENT": ("epr_entanglement", "MEAN_ENTANGLEMENT"),
        "STD_ENTANGLEMENT": ("epr_entanglement", "STD_ENTANGLEMENT"),
        "MIN_ENTANGLEMENT": ("epr_entanglement", "MIN_ENTANGLEMENT"),
        "MAX_ENTANGLEMENT": ("epr_entanglement", "MAX_ENTANGLEMENT"),
    },
    "dynamic_weight.py": {
        # Class: DynamicWeightCalculator
        "LAMBDA": ("dynamic_weight", "LAMBDA"),
        "R_TARGET": ("dynamic_weight", "R_TARGET"),
        "K_DECAY": ("dynamic_weight", "K_DECAY"),
    },
    "deadlock_detector.py": {
        # Class: DeadlockDetector
        "ALPHA_1": ("deadlock_detector", "ALPHA_1"),
        "ALPHA_2": ("deadlock_detector", "ALPHA_2"),
        "ALPHA_3": ("deadlock_detector", "ALPHA_3"),
        "ALPHA_4": ("deadlock_detector", "ALPHA_4"),
        "ETA_N": ("deadlock_detector", "ETA_N"),
        "ETA_G": ("deadlock_detector", "ETA_G"),
        "ETA_S": ("deadlock_detector", "ETA_S"),
        "DEADLOCK_THRESHOLD": ("deadlock_detector", "DEADLOCK_THRESHOLD"),
    },
    "flywheel.py": {
        # Class: FlywheelOptimizer
        "ALPHA_INIT": ("flywheel", "ALPHA_INIT"),
        "BETA": ("flywheel", "BETA"),
        "GAMMA": ("flywheel", "GAMMA"),
        "KAPPA": ("flywheel", "KAPPA"),
        "LAMBDA_VAR": ("flywheel", "LAMBDA_VAR"),
        "ETA": ("flywheel", "ETA"),
        "T_REF": ("flywheel", "T_REF"),
        "ZETA": ("flywheel", "ZETA"),
        "RHO_MAX": ("flywheel", "RHO_MAX"),
    },
    "knowledge_growth.py": {
        # Class: KnowledgeGrowthEngine
        "ETA": ("knowledge_growth", "ETA"),
        "TARGET_GROWTH": ("knowledge_growth", "TARGET_GROWTH"),
    },
    "sandbox.py": {
        # Class: SandboxManager
        "LAMBDA": ("sandbox", "LAMBDA"),
        "MU": ("sandbox", "MU"),
        "SRS_TARGET": ("sandbox", "SRS_TARGET"),
    },
    "neural_router.py": {
        # Class: NeuralRouter
        "NEURAL_THRESHOLD": ("neural_router", "NEURAL_THRESHOLD"),
        "SYMBOLIC_THRESHOLD": ("neural_router", "SYMBOLIC_THRESHOLD"),
        "TIME_CRITICAL_THRESHOLD": ("neural_router", "TIME_CRITICAL_THRESHOLD"),
    },
    "pareto_cost.py": {
        # Class: ParetoCostCalculator
        "ALPHA": ("pareto_cost", "ALPHA"),
        "BETA": ("pareto_cost", "BETA"),
        "GAMMA": ("pareto_cost", "GAMMA"),
    },
    "semantic_matcher.py": {
        # Class: SemanticMatcher
        "TOP_K": ("semantic_matcher", "TOP_K"),
        "PRECISION_TARGET": ("semantic_matcher", "PRECISION_TARGET"),
    },
    "predictive_sync.py": {
        # Class: PredictiveSync
        "TARGET_ACCURACY": ("predictive_sync", "TARGET_ACCURACY"),
        "WINDOW_SIZE": ("predictive_sync", "WINDOW_SIZE"),
    },
    "mahalanobis_distance.py": {
        # Class: ContrastiveLoss
        "MARGIN_POS": ("mahalanobis_distance", "MARGIN_POS"),
        "MARGIN_NEG": ("mahalanobis_distance", "MARGIN_NEG"),
    },
    "rcs_hybrid.py": {
        # Class: RCSHybrid
        "ALPHA": ("rcs_hybrid", "ALPHA"),
        "BETA": ("rcs_hybrid", "BETA"),
        "GAMMA": ("rcs_hybrid", "GAMMA"),
        "DECISION_THRESHOLD": ("rcs_hybrid", "DECISION_THRESHOLD"),
    },
}

# Import line to add for files that don't already import config
CONFIG_IMPORT_LINE = 'from qcm.config import load_config'
# Singleton
CONFIG_INIT_LINE = '_cfg = load_config()'


def get_existing_import(content: str) -> str | None:
    """Check if file already has a config import."""
    if 'from qcm.config import' in content or 'from qcm import config' in content or 'import qcm.config' in content:
        return 'existing'
    if 'from config import' in content:
        return 'local_config'
    return None


def needs_config_import(content: str) -> bool:
    """Check if file needs config import added."""
    existing = get_existing_import(content)
    return existing is None


def migrate_file(filepath: Path, const_map: dict, module_name: str) -> dict:
    """Migrate a single file. Returns stats dict."""
    content = filepath.read_text(encoding='utf-8')
    original = content
    stats = {"file": str(filepath), "replaced": [], "skipped": []}

    # Step 1: Add config import if needed
    if needs_config_import(content):
        # Add after the last import line
        lines = content.split('\n')
        last_import_idx = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                last_import_idx = i + 1
            elif stripped == '' or stripped.startswith('#'):
                # Allow blank lines and comments between imports
                if last_import_idx > 0 and i <= last_import_idx + 2:
                    continue

        # Insert after last import
        lines.insert(last_import_idx, '')
        lines.insert(last_import_idx + 1, CONFIG_IMPORT_LINE)
        lines.insert(last_import_idx + 2, CONFIG_INIT_LINE)
        content = '\n'.join(lines)
        stats['import_added'] = True

    # Step 2: Replace class constants
    # Pattern: CLASS_CONST = value  (with optional comment)
    for const_name, (mod, key) in const_map.items():
        # Match class-level constant assignments (indented with spaces)
        # Support both float and int values
        pattern = rf'^(\s+){re.escape(const_name)}\s*=\s*([^\n#]+?)(\s*#.*)?$'

        matches = list(re.finditer(pattern, content, re.MULTILINE))
        if matches:
            for m in reversed(matches):  # reverse to preserve positions
                indent = m.group(1)
                old_val = m.group(2).strip()
                comment = m.group(3) or ''
                # Replace with config lookup, preserving comment
                new_line = f'{indent}{const_name} = _cfg.get_param("{mod}", "{key}")'
                if comment:
                    new_line += f'  # was: {old_val}{comment}'
                content = content[:m.start()] + new_line + content[m.end():]
                stats['replaced'].append(f'{const_name}={old_val}')
        else:
            stats['skipped'].append(const_name)

    if content != original:
        filepath.write_text(content, encoding='utf-8')
        stats['modified'] = True
    else:
        stats['modified'] = False

    return stats


def main():
    total_replaced = 0
    total_skipped = 0
    results = []

    for filename, const_map in MIGRATION_MAP.items():
        filepath = SCRIPTS_DIR / filename
        if not filepath.exists():
            print(f"SKIP (not found): {filepath}")
            continue

        module_name = next((m for m, k in const_map.values()), filename.replace('.py', ''))
        stats = migrate_file(filepath, const_map, module_name)
        results.append(stats)
        total_replaced += len(stats['replaced'])
        total_skipped += len(stats['skipped'])

        status = "MODIFIED" if stats.get('modified') else "NO CHANGE"
        print(f"{status}: {stats['file']}")
        if stats['replaced']:
            print(f"  replaced: {stats['replaced']}")
        if stats['skipped']:
            print(f"  skipped:  {stats['skipped']}")
        if stats.get('import_added'):
            print(f"  added: config import + _cfg singleton")

    print(f"\n{'='*60}")
    print(f"Total: {total_replaced} constants migrated, {total_skipped} skipped")
    print(f"Files modified: {sum(1 for r in results if r.get('modified'))}/{len(results)}")


if __name__ == "__main__":
    main()
