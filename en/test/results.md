Command:
python macVoiceTurbo.py --autodiscover ../bible/en/test --format mp3 --parallel 1
171.17s user 37.86s system 151% cpu 2:17.67 total

python macVoiceTurbo.py --autodiscover ../bible/en --format wav --parallel 1 --max-chars 450 --device mps
164.88s user 30.29s system 133% cpu 2:26.20 total

python macVoiceTurbo.py --autodiscover ../bible/en/test --format wav --parallel 1 --max-chars 700  --device mps
160.57s user 30.45s system 126% cpu 2:30.57 total

python macVoiceTurbo.py --autodiscover ../bible/en/test --format mp3 --parallel 1
1220.00s user 292.47s system 1092% cpu 2:18.44 total (app says 124s)

