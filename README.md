# Sofia's 24 November News Front Page

[![Competition](https://make.fun/badge/competition/news-image-20261124)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/rank/bilowoabill-spec/news-image-20261124)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/reward/bilowoabill-spec/news-image-20261124)](https://make.fun/bounty/news-image-20261124)

A one-image front page summing up the world news of **Tuesday, 24 November 2026**,
drawn entirely in code: `render.py` (pure Python 3 stdlib, with its own bitmap
font and PNG encoder) paints the 1024x1024 newspaper page `entry.png`, and
`main.ts` (Node 22, stdlib only) copies it to the make.fun output directory.

## The six stories

1. **Russian jets enter S. Korea air zone** — Seoul scrambles fighters after
   Russian military aircraft enter its air defence zone near Ulleung Island;
   no airspace violation, alert lifted within minutes. *(AP / Yonhap)*
2. **Zelensky seeks four-way peace talks** — Kyiv is ready to meet Moscow,
   Washington and Europe as soon as possible, saying it could sit down as
   early as Tuesday. *(France 24)*
3. **UN chief: agree AI safety rules in a year** — Antonio Guterres urges
   nations to build a global framework for AI risk, with independent
   oversight, within twelve months. *(United Nations)*
4. **Asian markets soar as Nvidia chief returns** — Nikkei jumps 5%, Seoul
   7.4% and Taiwan 9% after Nvidia reinstates Jensen Huang as chief
   executive. *(Reuters)*
5. **US blacklists Megaspeed in chip scandal** — Washington bars the
   Singapore firm at the centre of the Nvidia spy row from buying US AI
   chips without a licence. *(Al Jazeera)*
6. **24 dead in Indonesia factory fire** — Officials confirm 24 workers
   killed and about 30 missing after a blaze guts a candy factory in
   Banten. *(Reuters)*

## Run it

```sh
python3 render.py            # rebuild entry.png (1024x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
