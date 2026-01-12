# GitHub Identicon Lookup

Because apparently taking your User ID, running it through a broken hashing algorithm from the 90s, and vomiting a 5x5 pixel grid onto the screen is what we call "design" now.

This tool exists because you people can't leave well enough alone. You just *had* to know what your default avatar looked like before you uploaded that heavily filtered photo of yourself hiking.

Well, here it is. It's ugly. It's mathematical. And it’s strictly deterministic, meaning you were destined to look this pixelated from the moment you created your account.

Powered by **MD5**, the cryptographic equivalent of a wet cardboard lock.

---

## The "Logic" (It's 3rd grade math, sit down)

You think random number generators made your avatar? **Cute.** Nothing in your life is unique, not even your pixel art. Your face is the calculated result of a cold, unfeeling database entry. I literally reverse-engineered this digital horoscope just to prove how un-special you are.

### 0. The Input (You are a number to me)

You think you're `@ShadowCoder69`? Wrong. To the database, you're just Integer `582910`.

$$
ID = \text{GitHubAPI}(\text{"your-dumb-username"})
$$

Change your username all you want. Run. Hide. **Your Identicon finds you.** This tool takes your username (because I assume you don't know your own ID) or your raw ID (if you're actually competent).

### 1. The Hashing (The Digital Butcher)

I take your integer **$ID$**, convert it to bytes, and bludgeon it with **MD5** until it spits out **$H$**, a 32-character hex string. Yes, MD5 is insecure. No, I don't care. It's handling pixel colors, not your banking details (though let's be honest, those are probably `password123`).

$$
H = \text{MD5}(ID)
$$

### 2. The Color Extraction (The "Judgment")

I don't "pick" a color. The algorithm literally judges your soul based on the **last 7 nibbles** of your hash. It decides if you deserve "Clinical Depression Blue" or "Radioactive Vomit Green."

$$
C_{hsl} = f(H_{-7:})
$$

* **Hue:** Last 3 nibbles. Pure entropy.
* **Saturation ($S$):** Calculated from $H_{-5:-3}$. I force it into $[45\%, 65\%]$ because washed-out colors are for weaklings.
* **Lightness ($L$):** Calculated from $H_{-7:-5}$. Constrained to $[55\%, 75\%]$ so you're actually visible against the white background of the internet's indifference.

### 3. The Shape Construction (The Rorschach Test)

The pattern isn't random. It is strictly dictated by the **first 15 nibbles** of your hash.

$$
G_{grid} = H_{0:15}
$$

I populate a **$5 \times 3$** matrix. For each cell $(x, y)$, I check its corresponding nibble $n$.

$$
\text{Cell}(x, y) = \begin{cases} \text{Color} & \text{if } n \equiv 0 \pmod 2 \quad (\text{even}) \\ \text{Background} & \text{if } n \equiv 1 \pmod 2 \quad (\text{odd}) \end{cases}
$$

**"But that's only half a face!"** you scream into the void.

**Yes.** The final **$5 \times 5$** grid is created by **mirroring** the first two columns. Why? Because human brains are barely evolved monkey-ware that only trusts symmetrical objects. Without this cheap trick, your avatar would look like static noise, and you'd cry.

---

## The Stack (How I wasted my weekend)

I built this using **Python 3.10+** because I have standards, and **Streamlit** because writing CSS manually is a form of self-harm I don't practice anymore.

* **`streamlit`**: The frontend. It spins up a web server so I don't have to deal with the DOM.
* **`Pillow` (PIL)**: The artist. It draws pixels, scales them up, and saves them as PNGs so you can print them out and show your mom.
* **`requests`**: The courier. It harasses the GitHub API so you don't have to `curl` it yourself like a caveman.
* **`numpy`**: Overkill? Absolutely. But using a C-optimized linear algebra library to color 25 squares makes me feel powerful.

---

## Installation (If you must)

You want to run this locally? Fine. But don't come crying to me when it works perfectly.

### 1. Clone this repository

(You know how `git clone` works. If you don't, close this tab.)

### 2. Feed the snake

```bash
pip install -r requirements.txt
```

### 3. Run the "App"

This fires up a server at `http://localhost:8501`. Go there. Click buttons. Be amazed.

```bash
streamlit run app.py
```

---

## Usage

1. **Type in a Username:** e.g., `torvalds` (someone who actually contributed to society).
2. **Or type in an ID:** e.g., `1` (if you're feeling archaic).
3. **Witness the Horror:** The app will render your 5x5 identicon in real-time.
4. **Download:** Click the button to save a high-res `.PNG`. Put it on your LinkedIn. Confuse recruiters.

---

## Disclaimer

*This project is completely unaffiliated with GitHub. It exists solely to mock their aesthetic choices with aggressive mathematical precision. If your identicon is ugly, blame the MD5 collision, or your parents, not me.*
