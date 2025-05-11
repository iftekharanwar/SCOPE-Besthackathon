import sys
import subprocess
import importlib.util

def check_package_installed(package_name):
    """Check if a Python package is installed"""
    try:
        if package_name == "scikit-learn":
            import sklearn
            return True
        else:
            spec = importlib.util.find_spec(package_name)
            return spec is not None
    except ImportError:
        return False

def main():
    """Test installation of required packages"""
    required_packages = [
        "fastapi", 
        "uvicorn", 
        "pandas", 
        "numpy", 
        "scikit-learn", 
        "spacy"
    ]
    
    missing_packages = []
    
    print("Testing package installation...")
    for package in required_packages:
        if check_package_installed(package):
            print(f"✅ {package} is installed")
        else:
            print(f"❌ {package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print("\nMissing packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("\nTesting spaCy language model...")
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy language model 'en_core_web_sm' is installed")
    except OSError:
        print("❌ spaCy language model 'en_core_web_sm' is NOT installed")
        print("\nInstall the language model with:")
        print("python -m spacy download en_core_web_sm")
        return False
    
    print("\nAll required packages and language models are installed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
