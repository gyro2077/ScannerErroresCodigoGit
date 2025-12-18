"""
Basic tests for the vulnerability scanner project
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_project_structure():
    """Test that essential project files exist"""
    base_dir = Path(__file__).parent.parent
    
    # Check essential directories
    assert (base_dir / "models").exists(), "models/ directory should exist"
    assert (base_dir / "scripts").exists(), "scripts/ directory should exist"
    assert (base_dir / "public").exists(), "public/ directory should exist"
    
    # Check essential files
    assert (base_dir / "requirements.txt").exists(), "requirements.txt should exist"
    assert (base_dir / "README.md").exists(), "README.md should exist"
    assert (base_dir / "vercel.json").exists(), "vercel.json should exist"


def test_model_files_exist():
    """Test that ML model files exist"""
    base_dir = Path(__file__).parent.parent
    models_dir = base_dir / "models"
    
    required_models = [
        "vulnerability_detector.pkl",
        "vectorizer_detector.pkl",
        "cwe_classifier.pkl",
        "vectorizer_cwe_classifier.pkl",
        "language_encoder.pkl",
        "cwe_encoder.pkl"
    ]
    
    for model_file in required_models:
        model_path = models_dir / model_file
        assert model_path.exists(), f"Model file {model_file} should exist"
        assert model_path.stat().st_size > 0, f"Model file {model_file} should not be empty"


def test_scripts_exist():
    """Test that essential scripts exist"""
    base_dir = Path(__file__).parent.parent
    scripts_dir = base_dir / "scripts"
    
    required_scripts = [
        "ai_scan.py",
        "ia_scan.py"
    ]
    
    for script_file in required_scripts:
        script_path = scripts_dir / script_file
        assert script_path.exists(), f"Script {script_file} should exist"


def test_workflows_exist():
    """Test that GitHub workflow files exist"""
    base_dir = Path(__file__).parent.parent
    workflows_dir = base_dir / ".github" / "workflows"
    
    required_workflows = [
        "dev_scan.yml",
        "test_validation.yml",
        "main_deploy.yml"
    ]
    
    for workflow_file in required_workflows:
        workflow_path = workflows_dir / workflow_file
        assert workflow_path.exists(), f"Workflow {workflow_file} should exist"


def test_public_html_exists():
    """Test that public HTML file exists"""
    base_dir = Path(__file__).parent.parent
    html_file = base_dir / "public" / "index.html"
    
    assert html_file.exists(), "public/index.html should exist"
    
    # Check that HTML contains expected content
    content = html_file.read_text()
    assert "Scanner de Vulnerabilidades" in content, "HTML should contain title"
    assert "DEV" in content, "HTML should mention DEV stage"
    assert "TEST" in content, "HTML should mention TEST stage"
    assert "MAIN" in content, "HTML should mention MAIN stage"


def test_ai_scan_imports():
    """Test that ai_scan.py can be imported without errors"""
    try:
        # This will test if the script has valid Python syntax
        import scripts.ai_scan as ai_scan
        assert hasattr(ai_scan, 'cargar_modelo'), "ai_scan should have cargar_modelo function"
        assert hasattr(ai_scan, 'analizar_codigo'), "ai_scan should have analizar_codigo function"
    except ImportError as e:
        # If joblib/sklearn not installed, that's ok for structure test
        if "joblib" not in str(e) and "sklearn" not in str(e):
            raise


def test_requirements_file():
    """Test that requirements.txt has necessary dependencies"""
    base_dir = Path(__file__).parent.parent
    req_file = base_dir / "requirements.txt"
    
    content = req_file.read_text()
    
    # Check for essential dependencies
    assert "scikit-learn" in content, "requirements.txt should include scikit-learn"
    assert "joblib" in content, "requirements.txt should include joblib"
    assert "pytest" in content, "requirements.txt should include pytest"


if __name__ == "__main__":
    # Run tests manually
    import pytest
    pytest.main([__file__, "-v"])
