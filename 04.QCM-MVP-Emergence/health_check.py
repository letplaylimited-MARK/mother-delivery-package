#!/usr/bin/env python
"""
QCM-MVP System Health Check
Version: 4.0 (2026-04-27)
Run this every time before starting work
Config: Semantic + Paper weights
"""
import os
import sys
sys.path.insert(0, '02-代码编写')

from simple_role import SimpleRole, ROLE_CONFIG, create_demo_roles, RoleFactory
from calculator import ResonanceCalculator


def test_semantic():
    """Test semantic embedding and R calculation"""
    print("\n" + "=" * 60)
    print("QCM Health Check v4.0 - Semantic Model")
    print("=" * 60)
    
    results = []
    
    print(f"\n[1] Config Check")
    print(f"  USE_SEMANTIC: {ROLE_CONFIG.USE_SEMANTIC}")
    print(f"  F_0: {ROLE_CONFIG.BASE_INTERACTION}")
    results.append(ROLE_CONFIG.USE_SEMANTIC == True)
    
    role1, role2 = create_demo_roles()
    calc = ResonanceCalculator()
    
    print(f"\n[2] R Calculation")
    R = calc.calculate_R(role1, role2)
    print(f"  Initial R: {R:.4f}")
    results.append(0.30 <= R <= 0.60)
    
    comps = calc.get_components(role1, role2)
    print(f"  K_sim: {comps['K_sim']:.4f} (expected 0.3-0.6)")
    print(f"  C_comp: {comps['C_comp']:.4f}")
    print(f"  I_freq: {comps['I_freq']:.4f}")
    print(f"  E_div: {comps['E_div']:.4f}")
    
    results.append(0.3 <= comps['K_sim'] <= 0.6)
    
    print(f"\n[3] Weights")
    print(f"  Emergence weights: {calc.W_K}/{calc.W_C}/{calc.W_I}/{calc.W_E}")
    results.append(calc.W_K == 0.35)
    
    print(f"\n[4] 8-Role System")
    factory = RoleFactory()
    available_roles = factory.get_available_roles()
    roles = [factory.create_role(rt) for rt in available_roles]
    print(f"  Created {len(roles)} roles")
    results.append(len(roles) == 8)
    
    r_sec = next((r for r in roles if r.name == "Secretary"), None)
    r_res = next((r for r in roles if r.name == "Researcher"), None)
    
    if r_sec and r_res:
        R_sr = calc.calculate_R(r_sec, r_res)
        print(f"  Secretary-Researcher: R={R_sr:.4f}")
        results.append(0.30 <= R_sr <= 0.60)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Result: {passed}/{total} checks passed")
    
    if passed == total:
        print("Status: READY")
        return 0
    else:
        print("Status: NEEDS ATTENTION")
        return 1


if __name__ == "__main__":
    sys.exit(test_semantic())