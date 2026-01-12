# GitHub Identicon Lookup

Because apparently MD5 hashing your user ID and turning it into a 5x5 pixel art masterpiece is what passes for "unique visual identity" in 2026.

Nothing screams "cutting-edge technology" quite like reducing your entire digital persona to the computational equivalent of a Rorschach test designed by a colorblind algorithm.

Watch as your GitHub identity gets reduced to a glorified Rubik's cube that nobody asked for but everyone gets anyway. It's like a participation trophy, but uglier and more deterministic.

Powered by the same cryptographic technology your grandma uses to "secure" her email password.

---

## The "Logic" (It's simple math, try to keep up)

You think these things are arbitrary? **Adorably naive.** Your face is the result of a cold, unfeeling, deterministic calculation. I reverse-engineered this digital astrology chart just to prove it.

### The Formula

It all starts with your User ID. That number you didn't even know you had.

$$
H = \text{MD5}(U)
$$

I take your ID, $U$, and smash it through MD5 to get $H$, a 32-character hexadecimal string. Yes, MD5 is broken for security, but for generating ugly pixel art, it's just fine.

### 1. The Color Extraction (The "Vibe Check")

I don't "choose" a color for you. The algorithm literally judges you based on the **last 7 nibbles** of your hash. It decides if you're a "Depressing Grey" or "Aggressive Salmon."

$$
C_{hsl} = f(H_{-7:})
$$

*   **Hue:** Taken from the last 3 nibbles. Pure chaos.
*   **Saturation ($S$):** Calculated from nibbles $H_{-5:-3}$. I force it into $[45\%, 65\%]$ so you don't look *too* washed out.
*   **Lightness ($L$):** Calculated from nibbles $H_{-7:-5}$. Constrained to $[55\%, 75\%]$ so you're visible against a white background. You're welcome.

### 2. The Shape Construction

The pattern isn't random. It's strictly dictated by the **first 15 nibbles**.

$$
G_{grid} = H_{0:15}
$$

I populate a $5 \times 3$ matrix. For each cell $(x, y)$, I check its corresponding nibble $n$.

$$
\text{Cell}(x, y) = \begin{cases} \text{Color} & \text{if } n \text{ is even} \\ \text{White} & \text{if } n \text{ is odd} \end{cases}
$$

**"But wait,"** you whine, **"that's only half a face!"**

Correct. The final $5 \times 5$ grid is created by **mirroring** the first two columns. Why? Because humans are biologically hardwired to trust symmetrical things, and without this trick, your avatar would just look like QR code static.
