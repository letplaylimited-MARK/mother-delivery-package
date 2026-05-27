# Ghost Hub SDK Customer Success Guide

## Onboarding Journey

### Week 1: Getting Started
| Day | Activity | Deliverable |
|-----|----------|------------|
| 1 | Environment Setup | SDK installed, first workflow |
| 2 | Core Concepts | Intent Bank understanding |
| 3 | Integration | First device connected |
| 4 | Templates | 3 templates customized |
| 5 | Testing | First workflow in production |

### Week 2-4: Expansion
| Week | Focus | Success Metric |
|------|-------|----------------|
| 2 | IoT Integration | 10 devices connected |
| 3 | Agent Setup | Multi-agent workflow running |
| 4 | Production | First customer-facing workflow |

### Month 2-3: Optimization
- Template customization
- Performance tuning
- Advanced features exploration
- ROI measurement

---

## Success Metrics

### Technical KPIs
| Metric | Target | Measurement |
|--------|--------|-------------|
| Workflow Success Rate | >99% | Success/total workflows |
| Intent Match Accuracy | >85% | Correct matches/total |
| Device Command Latency | <100ms | P95 latency |
| System Uptime | 99.9% | Uptime SLA |

### Business KPIs
| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to First Workflow | <2 days | Onboarding tracker |
| Workflows in Production | >10 | Month 1 |
| Development Time Saved | >50% | Developer survey |
| Cost Reduction | >30% | Monthly comparison |

---

## Common Onboarding Issues

### Issue: SDK Import Error
**Symptom**: `ModuleNotFoundError: No module named 'ghost_hub_sdk'`
**Solution**: 
```bash
pip install ghost-hub-sdk
pip install --upgrade ghost-hub-sdk
```

### Issue: Intent Not Matching
**Symptom**: Low confidence scores
**Solution**:
- Add custom patterns
- Use domain filter
- Provide more context

### Issue: Device Connection Failed
**Symptom**: Connection timeout
**Solution**:
- Verify network connectivity
- Check MQTT broker settings
- Verify device credentials

---

## Best Practices

### Workflow Design
1. Start simple, then iterate
2. Use templates as starting points
3. Log all workflow executions
4. Monitor intent matching accuracy
5. Test with production data early

### Performance
1. Batch device commands when possible
2. Use caching for frequent lookups
3. Configure appropriate timeouts
4. Monitor queue depths

### Security
1. Rotate API keys regularly
2. Enable audit logging
3. Use HTTPS for all connections
4. Implement rate limiting

---

## Customer Health Score

| Score | Status | Actions |
|-------|--------|---------|
| 90-100 | Thriving | Expand usage, identify advocates |
| 70-89 | Healthy | Monitor, provide tips |
| 50-69 | At Risk | Schedule check-in |
| <50 | Critical | Immediate intervention |

### Health Factors
- Login frequency
- Workflow execution count
- Feature adoption breadth
- Support ticket sentiment
- NPS score

---

## Expansion Opportunities

### Seat Expansion
When to expand:
- Team grows
- New use cases identified
- Usage near limits

### Feature Adoption
Cross-sell opportunities:
- No-UI Adapter → Agent Federation
- Community → Professional
- Professional → Enterprise

---

## Escalation Paths

### Tier 1: Self-Service
- Documentation: docs.ghosthub.dev
- Community: community.ghosthub.dev
- FAQ: ghosthub.dev/faq

### Tier 2: Email Support
- Professional: <4 hour response
- Enterprise: <1 hour response

### Tier 3: Dedicated CSM
- Weekly check-ins
- Monthly reviews
- Quarterly business reviews

---

## Resources

- **Documentation**: docs.ghosthub.dev
- **API Reference**: docs.ghosthub.dev/api
- **Templates**: docs.ghosthub.dev/templates
- **Support Portal**: support.ghosthub.dev
- **Community**: community.ghosthub.dev
