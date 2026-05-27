from qcm.roles.identity import ROLE_REGISTRY
from qcm.summoning.matching import calculate_skill_match, dynamic_penalty

class DynamicRoleRegistry:
    def __init__(self):
        self._roles = list(ROLE_REGISTRY)
        self._dynamic_roles = []

    @property
    def all_roles(self):
        return self._roles + self._dynamic_roles

    def register_dynamic_role(self, role):
        self._dynamic_roles.append(role)

    def summon(self, required_skills, max_roles=15):
        candidates = []
        for role in self.all_roles:
            match = calculate_skill_match(required_skills, {"skills": [role.role_id]})
            if match > 0.75:
                penalty = dynamic_penalty(len(self.all_roles))
                candidates.append((role, match - penalty))
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [c[0] for c in candidates[:max_roles]]
