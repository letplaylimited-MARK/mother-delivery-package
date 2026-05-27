# Ghost Hub SDK Template Index

> Complete list of pre-built workflow templates

---

## HR Templates (Human Resources)

| Template ID | Name | Description | Tasks |
|-------------|------|-------------|-------|
| `hr_recruitment` | Recruitment | End-to-end hiring workflow | 5 |
| `hr_interview_optimize` | Interview Optimization | Streamline interview process | 4 |
| `hr_onboarding` | Employee Onboarding | New hire onboarding steps | 6 |
| `hr_performance_review` | Performance Review | Annual review process | 3 |

### hr_recruitment
**Input Example:** "帮我招聘一个Python工程师"

**Tasks:**
1. Create job posting
2. Screen resumes
3. Schedule interviews
4. Conduct interviews
5. Make offer

### hr_onboarding
**Input Example:** "新员工入职流程"

**Tasks:**
1. Create accounts
2. Assign mentor
3. Schedule training
4. Equipment setup
5. Document signing
6. Team introduction

---

## IoT Templates (Smart Home & Industrial)

| Template ID | Name | Description | Devices |
|-------------|------|-------------|---------|
| `iot_smart_home` | Smart Home | Home automation | 10+ |
| `iot_industrial` | Industrial Control | Factory automation | 5+ |

### iot_smart_home
**Input Examples:**
- "开灯"
- "把温度调到24度"
- "离家模式"

**Supported Devices:**
- Lights (on/off, dim, color)
- Thermostats (temperature, mode)
- Locks (lock/unlock)
- Cameras (view, record)
- Sensors (motion, temperature, humidity)

---

## Operations Templates

| Template ID | Name | Description |
|-------------|------|-------------|
| `ops_ticket_resolution` | Ticket Resolution | IT support workflow |
| `ops_monitoring` | System Monitoring | Infrastructure monitoring |
| `ops_security_monitor` | Security Monitoring | Security event handling |

### ops_ticket_resolution
**Input Example:** "处理网络故障工单"

**Tasks:**
1. Triage ticket
2. Assign priority
3. Investigate issue
4. Implement fix
5. Verify resolution
6. Close ticket

---

## Finance Templates

| Template ID | Name | Description |
|-------------|------|-------------|
| `finance_invoicing` | Invoicing | Invoice generation |
| `finance_cost_optimization` | Cost Optimization | Expense analysis |
| `finance_report` | Financial Report | Report generation |

---

## Marketing Templates

| Template ID | Name | Description |
|-------------|------|-------------|
| `marketing_automation` | Campaign Automation | Marketing campaigns |

---

## Other Templates

| Template ID | Domain | Description |
|-------------|--------|-------------|
| `code_review` | DevOps | Code review workflow |
| `data_analytics` | Data | Data analysis pipeline |
| `meeting_assistant` | Productivity | Meeting management |
| `document_processing` | Productivity | Document workflow |
| `customer_service` | CRM | Support automation |
| `ecommerce_order` | E-commerce | Order processing |
| `inventory_management` | Logistics | Stock management |
| `it_asset_management` | IT | Asset tracking |
| `knowledge_management` | KM | Knowledge base |
| `supply_chain` | Logistics | Supply chain |
| `customer_relationship` | CRM | CRM workflows |
| `ai_project_management` | PM | AI project tracking |
| `software_development` | DevOps | SDLC workflow |

---

## Using Templates

### Direct Matching

```python
sdk = GhostHubSDK()
match = sdk.intention_bank.match_intent("帮我招聘工程师")
```

### Domain Filtering

```python
# Only search HR templates
hr_match = sdk.intention_bank.match_intent(
    "面试安排", 
    domain="hr"
)
```

### Template Structure

```json
{
  "id": "hr_recruitment",
  "name": "Recruitment",
  "domain": "hr",
  "patterns": [
    "招聘*",
    "招人*",
    " hiring*"
  ],
  "tasks": [
    {
      "id": "task_1",
      "name": "Create job posting",
      "type": "automated"
    }
  ],
  "priority": 10
}
```

---

## Custom Templates

### Adding Custom Templates

```python
custom_template = {
    "id": "custom_001",
    "name": "Custom Workflow",
    "domain": "custom",
    "patterns": ["custom pattern*"],
    "tasks": [
        {"id": "t1", "name": "Step 1"},
        {"id": "t2", "name": "Step 2"}
    ],
    "priority": 5
}

sdk.intention_bank.add_template(custom_template)
```

### Loading External Templates

```python
import json

with open("my_templates.json") as f:
    templates = json.load(f)

for template in templates:
    sdk.intention_bank.add_template(template)
```

---

## Template Matching Priority

Templates are matched by:
1. **Exact pattern match** (highest priority)
2. **Partial pattern match**
3. **Semantic similarity** (>0.7 threshold)
4. **Domain relevance**

**Minimum confidence threshold:** 0.5

---

## Statistics

| Metric | Value |
|--------|-------|
| Total templates | 22 |
| HR templates | 4 |
| IoT templates | 2 |
| Operations templates | 3 |
| Finance templates | 3 |
| Other templates | 10 |
