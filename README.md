# GitHub Identicon Lookup

Because apparently MD5 hashing your user ID and turning it into a 5x5 pixel art masterpiece is what passes for "unique visual identity" in 2026.

Nothing screams "cutting-edge technology" quite like reducing your entire digital persona to the computational equivalent of a Rorschach test designed by a colorblind algorithm.

Watch as your GitHub identity gets reduced to a glorified Rubik's cube that nobody asked for but everyone gets anyway. It's like a participation trophy, but uglier and more deterministic.

Powered by the same cryptographic technology your grandma uses to "secure" her email password.

---

## The "Logic" (It's simple math, try to keep up)

You think these things are arbitrary? **Adorably naive.** Your face is the result of a cold, unfeeling, deterministic calculation. I reverse-engineered this digital astrology chart just to prove it.

### 0. The Input (Who are you, really?)

You might think you are `@cool_coder_69`. GitHub disagrees. To the database, you are just an integer.

$$
ID = \text{GitHub\_API}(\text{"username"})
$$

If you change your username, your identicon stays the same. **You cannot run from your past.** This tool accepts either your username (which I look up because I'm nice) or your raw ID (if you're a robot).

### 1. The Hashing (The Meat Grinder)

We take that integer **$ID$**, convert it to bytes, and smash it through MD5 to get **$H$**, a 32-character hexadecimal string. Yes, MD5 is cryptographically broken, but for generating ugly pixel art, it's just fine.

$$
H = \text{MD5}(ID)
$$

### 2. The Color Extraction (The "Vibe Check")

I don't "choose" a color for you. The algorithm literally judges you based on the **last 7 nibbles** of your hash. It decides if you're a "Depressing Grey" or "Aggressive Salmon."

$$
C_{hsl} = f(H_{-7:})
$$

* **Hue:** Taken from the last 3 nibbles. Pure chaos.
* **Saturation (**$S$**):** Calculated from nibbles **$H_{-5:-3}$**. I force it into **$[45\%, 65\%]$** using basic arithmetic so you don't look *too* washed out.
* **Lightness (**$L$**):** Calculated from nibbles **$H_{-7:-5}$**. Constrained to **$[55\%, 75\%]$** so you're visible against a white background. You're welcome.

### 3. The Shape Construction

The pattern isn't random. It's strictly dictated by the  **first 15 nibbles** .

$$
G_{grid} = H_{0:15}
$$

I populate a **$5 \times 3$** matrix. For each cell **$(x, y)$**, I check its corresponding nibble **$n$**.

$$
\text{Cell}(x, y) = \begin{cases} \text{Color} & \text{if } n \equiv 0 \pmod 2 \quad (\text{even}) \\ \text{Background} & \text{if } n \equiv 1 \pmod 2 \quad (\text{odd}) \end{cases}
$$

**"But wait,"** you whine, **"that's only half a face!"**

Correct. The final **$5 \times 5$** grid is created by **mirroring** the first two columns. Why? Because humans are biologically hardwired to trust symmetrical things. Without this trick, your avatar would just look like QR code static.

---

## The Stack (How I built this monster)

I built this using **Python 3.10+** because I enjoy sensible syntax, and **Streamlit** because life is too short to center a `<div>` in CSS.

* **`streamlit`** : The frontend. It creates the web server so you don't have to touch HTML.
* **`Pillow` (PIL)** : The artist. It draws the pixels, scales them up, and saves them as PNGs so you can frame them on your wall.
* **`requests`** : The courier. It bothers the GitHub API to fetch your User ID so you don't have to look it up yourself.
* **`numpy`** : Overkill? Maybe. But I needed it to manipulate grid arrays, and I like my dependencies heavy.

---

## Installation (If you must)

You want to run this locally? Fine. But don't blame me if you don't like what you see in the mirror.

### 1. Clone this repository

(You know how to do this. I'm not pasting the command.)

### 2. Install the requirements

Feed the snake.

**Bash**

```
pip install -r requirements.txt
```

### 3. Run the "App"

This fires up a local web server, usually at `http://localhost:8501`.

**Bash**

```
streamlit run app.py
```

---

## Usage

1. **Type in a Username:** e.g., `torvalds`.
2. **Or type in an ID:** e.g., `1` (if you are feeling historical).
3. **Witness the Horror:** The app will render your 5x5 identicon in real-time.
4. **Download:** Click the button to save a high-res `.PNG`. Put it on your resume. confuse HR.

---

## Disclaimer

*This project is not affiliated with GitHub. It just mocks their design choices with love and mathematical precision. If your identicon is ugly, blame the MD5 collision, not me.*
