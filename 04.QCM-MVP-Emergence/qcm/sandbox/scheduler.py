def priority_score(urgency, value, resource_availability, knowledge_transfer):
    return (0.35 * urgency + 0.30 * value + 0.20 * resource_availability
            + 0.15 * knowledge_transfer)

def schedule_projects(projects):
    for p in projects:
        p["priority"] = priority_score(
            p.get("urgency", 0), p.get("value", 0),
            p.get("resource_availability", 0), p.get("knowledge_transfer", 0))
    return sorted(projects, key=lambda x: x["priority"], reverse=True)
