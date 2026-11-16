from datetime import datetime
from pathlib import Path


class MissionLogger:
    """발표용 mission log를 파일과 터미널에 남기기 위한 간단한 logger."""

    def __init__(self, log_dir: str = "mission_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"mission_{stamp}.log"

    def write(self, message: str):
        line = f"[MISSION] {message}"
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        return line
