# Manim Creative Studio

Independent creative animation projects, separate from AOI production.

## Video signature standard

Use the exact text **Soph Laugh** in small, legible letters in the lower-right safe area of every new video. Keep the signature unobtrusive, visible, inside the frame, and away from equations and diagrams. Adjust its position for individual compositions if needed.

## MATH-001 — The mathematics of love

A continuous luminous trace of the implicit equation, starting at the first frame and tracing for ten seconds. The final four seconds display the completed outline and caption. The red interior fills radially as the boundary is drawn. The renderer verifies the maximum absolute residual of the original implicit equation at 2,401 sampled boundary vertices before rendering. Portrait master: 1080 × 1920, 30 fps.

From the repository root, render with Manim Community Edition and a working LaTeX installation:

```sh
manim -qh --fps 30 -r 1080,1920 creative_studio/scenes/math_001_heart.py MathematicalHeart
```

## MATH-002 — The geometry of autumn

An original radial maple leaf polygon with positive fan-triangle orientation, continuously drawn and filled in autumn red and orange. Portrait 1080 × 1920, 30 fps, Soph Laugh signature.

```sh
python -m manim -pqh --fps 30 -r 1080,1920 -o MATH-002.mp4 creative_studio/scenes/math_002_thanksgiving.py ThanksgivingLeaf
```
