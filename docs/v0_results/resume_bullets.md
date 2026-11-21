# Resume / LinkedIn bullets: F1TENTH autonomous racing (V0, 2026-11-20)

## Pick 3–4 for a resume

- Cut an autonomous race car's lap time by **40% (27.7 s → 16.6 s)** in one day by diagnosing planner and control
  bugs directly from ROS 2 bag data on a 1/10-scale F1TENTH car (ROS 2, LiDAR, VESC).
- Brought a reactive Follow-the-Gap planner to **within 4.5% of a practiced human driver's lap time**, and **16%
  faster** than the same driver's first session, with **6.5× lower lap-to-lap spread** (0.23 s vs. 1.49 s).
- Found and fixed a disparity-extension cascade bug that **blinded 8% of LiDAR scans**, cutting wrong-direction
  steering flips by **~70%** (validated by offline replay of recorded scans).
- Designed a speed law from measured vehicle dynamics. A brake test showed the motor controller braking at **0.85 vs.
  ~1.5 m/s²** depending on the command. This raised average speed **75% (1.26 → 2.20 m/s)** while keeping **50% more
  wall clearance** than the human driver (0.27 m vs. 0.18 m).
- Built a Python bag-analysis toolkit (LiDAR scan-matching lap timing, ICP SLAM track reconstruction, offline planner
  replay) to benchmark autonomy against human teleop.

## One-line version (LinkedIn headline / application summary)

Tuned a LiDAR-based autonomous racing planner from 27.7 s to 16.6 s laps (−40%) in a day of data-driven testing,
reaching within 4.5% of a practiced human driver with 6.5× better consistency.

## Research-application paragraph

On our F1TENTH platform I ran a systematic benchmark of autonomous planning against human teleoperation. Using only
recorded ROS 2 bags, I built tools to time laps by LiDAR scan matching, rebuild the track with ICP SLAM, and replay
the planner offline. That let me trace failures to specific causes: a disparity-extension cascade that blinded 8% of
scans, oscillation at track forks, and a motor-controller braking asymmetry (0.85 vs. ~1.5 m/s²). Fixing these cut
autonomous lap time by 40%, from 27.7 s to 16.6 s. The planner now runs within 4.5% of a practiced human's pace with
about 6.5× lower lap-to-lap spread. V0 covers one day and one driver; a larger frozen-parameter benchmark is planned.

## Notes so the claims hold up

- "Practiced human" means the same driver's second session (median 15.9 s over ~9 laps). Session 1 median was 19.9 s.
- Both the human and the autonomy were capped at about 2.45–2.5 m/s.
- The ~70% flip reduction is from offline (open-loop) replay of recorded scans, not a closed-loop test.
- Keep the "within 4.5%" wording. Don't claim gap follow beats the practiced human.
