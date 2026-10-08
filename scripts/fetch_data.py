"""Download every input the paper uses into data/raw/ and check it against the hashes recorded
on 2026-10-08. The French library and FRED are revised over time; a hash mismatch means the
source has been updated, and results may differ slightly from the paper's."""
import hashlib
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
FRENCH = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
FILES = {
    "french/F-F_Research_Data_Factors.csv": (FRENCH + "F-F_Research_Data_Factors_CSV.zip", "d7d7fe37b150b5b15c9c069b3ba101dfe1af568c6d7b5db6e73cd0a6c0c9e5e5"),
    "french/F-F_Research_Data_Factors_daily.csv": (FRENCH + "F-F_Research_Data_Factors_daily_CSV.zip", "c2dc30c9e89eeea05a689c81fb426f4d76711270733b3731997615cbdff5b247"),
    "french/Europe_3_Factors_Daily.csv": (FRENCH + "Europe_3_Factors_Daily_CSV.zip", "5178bce67798f86c9e1741aac7d97bc77334bda4096d60944bbe4846dc99be72"),
    "french/Japan_3_Factors_Daily.csv": (FRENCH + "Japan_3_Factors_Daily_CSV.zip", "a5afa8f15d2a377eaa17eb131208a9e8c735063b1710d610a4e4c4d000c4ee79"),
    "french/Asia_Pacific_ex_Japan_3_Factors_Daily.csv": (FRENCH + "Asia_Pacific_ex_Japan_3_Factors_Daily_CSV.zip", "4d5d7c2dc4fef64824b6b59296f0610bf3e514778fd73ecd0412bb65966333cc"),
    "french/Developed_ex_US_3_Factors_Daily.csv": (FRENCH + "Developed_ex_US_3_Factors_Daily_CSV.zip", "6287bbbcba03be35c8dbe99d21364967f07eb087893079167f41ec8a9047f185"),
    "goyal/GW2008_PredictorData_updated_2025.xlsx": ("https://drive.google.com/uc?export=download&id=1qwpl2R_DNujpU5YUkk8lacP1tTeMb9iJ", "8d210b779442a5a9206702060aac67c1de4283186c0f167ebdb4488d149be872"),
    "fred/USREC.csv": ("https://fred.stlouisfed.org/graph/fredgraph.csv?id=USREC", "a42a3581fe9c260dd3627febc84a7d563e5ed162cc7085a7518ebde99dc3c3b4"),
    "fred/VIXCLS.csv": ("https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS", "2f5c1214537be30fbf01e26d0a0b4ec79624ba5858e0c8bc6c9da31eb8f5d5b4"),
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research data fetch)"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def main():
    bad = 0
    for rel, (url, sha) in FILES.items():
        dest = RAW / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            data = get(url)
            if url.endswith(".zip"):
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    name = next(n for n in z.namelist() if n.lower().endswith(".csv"))
                    data = z.read(name)
            dest.write_bytes(data)
        digest = hashlib.sha256(dest.read_bytes()).hexdigest()
        ok = digest == sha
        bad += not ok
        print(f"{'ok ' if ok else 'NEW'} {rel}" + ("" if ok else f"  (sha256 {digest[:12]}..., paper used {sha[:12]}...)"))
    if bad:
        print(f"{bad} file(s) differ from the versions used in the paper.", file=sys.stderr)


if __name__ == "__main__":
    main()
