from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

PROJECT = Path(__file__).resolve().parents[1]
DESTINATION = PROJECT.parent / 'SDN_QoS_Robotic_Communication_Windows.zip'
EXCLUDED_DIRS = {'.venv', '__pycache__', '.pytest_cache', '.git'}
EXCLUDED_FILES = {'.DS_Store'}
REQUIRED = ['README.md', 'requirements.txt', 'backend/main.py', 'controller/controller.py',
            'simulation/network_simulator.py', 'dashboard/app.py', 'experiments/run_all_experiments.py',
            'results/experiment_results.csv', 'docs/architecture.md', 'scripts/start_project.ps1']

def main():
    if DESTINATION.exists(): DESTINATION.unlink()
    with ZipFile(DESTINATION, 'w', ZIP_DEFLATED, compresslevel=7) as archive:
        for path in PROJECT.rglob('*'):
            if any(part in EXCLUDED_DIRS for part in path.relative_to(PROJECT).parts): continue
            if not path.is_file() or path.name in EXCLUDED_FILES: continue
            if 'smoke' in path.name.lower() or path.suffix == '.pyc': continue
            archive.write(path,Path(PROJECT.name)/path.relative_to(PROJECT))
    with ZipFile(DESTINATION) as archive:
        names=set(archive.namelist())
        missing=[(Path(PROJECT.name)/item).as_posix() for item in REQUIRED if (Path(PROJECT.name)/item).as_posix() not in names]
        if missing: raise RuntimeError(f'ZIP missing required files: {missing}')
        print(f'Created and verified {DESTINATION} ({len(names)} files, {DESTINATION.stat().st_size:,} bytes).')

if __name__=='__main__': main()
