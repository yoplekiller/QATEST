import os
import shutil

SRC_DIR = "allure-report"
DEST_DIR = "deploy_dir"

#기존 deploy_dir 삭제
if os.path.exists(DEST_DIR):
    shutil.rmtree(DEST_DIR)


shutil.copytree(SRC_DIR, DEST_DIR)

print(f"✅ {SRC_DIR} → {DEST_DIR} 복사 완료")