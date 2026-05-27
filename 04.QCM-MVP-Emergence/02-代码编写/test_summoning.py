import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcm.summoning.features import extract_tfidf_keywords, ensemble_score
from qcm.summoning.matching import calculate_skill_match, dynamic_penalty, mahalanobis_distance


def test_tfidf_extraction():
    keywords = extract_tfidf_keywords("我們需要開發一個醫療合規審查系統")
    assert isinstance(keywords, dict)
    assert len(keywords) > 0

def test_ensemble_score():
    score = ensemble_score(f1=0.7, f2=0.8, f3=0.6, f4=0.5, f5=0.7, f6=0.9)
    expected = 0.25*0.7 + 0.30*0.8 + 0.20*0.6 + 0.10*0.5 + 0.10*0.7 + 0.05*0.9
    assert abs(score - expected) < 1e-6

def test_skill_match_scoring():
    score = calculate_skill_match(["python", "ml", "nlp"], {"skills": ["python", "java", "sql"]})
    assert 0 <= score <= 1

def test_skill_match_below_threshold():
    score = calculate_skill_match(["cobol"], {"skills": ["python", "rust", "go"]})
    assert score < 0.75

def test_dynamic_penalty():
    assert dynamic_penalty(8) == 0.0
    assert dynamic_penalty(10) > 0
    assert dynamic_penalty(15) > dynamic_penalty(10)

def test_mahalanobis_distance():
    dist = mahalanobis_distance([1, 2], [1.5, 2.5], cov_matrix=[[1, 0], [0, 1]])
    assert dist > 0
