# GitHub Identicon Lookup

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A tool to generate and visualize GitHub-style identicons based on unique user IDs. This application helps users understand the deterministic process behind the default avatars assigned to GitHub users without a profile picture.

**[Live Demo](https://git5ub-identicon-lookup.streamlit.app/)**

---

## Algorithm Explanation

The identicon generation process is strictly deterministic, relying on the user's unique numeric ID.

### 0. The Input

The process begins with the GitHub User ID, a unique integer assigned to every account.

$$
ID = \text{GitHubAPI}(\text{"username"})
$$

The tool accepts either a valid GitHub username (which it resolves to an ID via the API) or a raw integer ID directly.

### 1. Hashing

The integer **$ID$** is converted to bytes and hashed using the **MD5** algorithm to produce **$H$**, a 32-character hexadecimal string. This hash serves as the entropy source for both color and shape.

$$
H = \text{MD5}(ID)
$$

### 2. Color Extraction

The color is determined by the **last 7 nibbles** of the hash string $H$.

$$
C_{hsl} = f(H_{-7:})
$$

The HSL (Hue, Saturation, Lightness) values are derived as follows:
*   **Hue:** Derived from the last 3 nibbles.
*   **Saturation ($S$):** Calculated from $H_{-5:-3}$ and mapped to the range $[45\%, 65\%]$ to ensure vibrant colors.
*   **Lightness ($L$):** Calculated from $H_{-7:-5}$ and mapped to the range $[55\%, 75\%]$ for optimal contrast against dark/light backgrounds.

### 3. Shape Construction

The geometric pattern is dictated by the **first 15 nibbles** of the hash.

$$
G_{grid} = H_{0:15}
$$

A **$5 \times 3$** matrix is populated first. For each cell $(x, y)$, the corresponding nibble $n$ determines the state:

$$
\text{Cell}(x, y) = \begin{cases} \text{Color} & \text{if } n \equiv 0 \pmod 2 \quad (\text{even}) \\ \text{Background} & \text{if } n \equiv 1 \pmod 2 \quad (\text{odd}) \end{cases}
$$

The final **$5 \times 5$** grid is created by **mirroring** the first two columns to the right side. This horizontal symmetry is a key characteristic of GitHub identicons, making them aesthetically pleasing and easier for the human brain to recognize.

---

## Technical Stack

This application is built with Python 3.10+ and the following libraries:

*   **`streamlit`**: For the web interface and application logic.
*   **`Pillow` (PIL)**: For image generation, manipulation, and saving.
*   **`requests`**: For fetching user data from the GitHub API.
*   **`numpy`**: For efficient matrix operations and grid management.

---

## Installation

To run this tool locally, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/siddharth-narigra/github-identicon-lookup
```

### 2. Install dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

Launch the Streamlit server:

```bash
streamlit run app.py
```

The application will be accessible at `http://localhost:8501`.

---

## Usage

1.  **Enter a Username:** Input a valid GitHub username (e.g., `torvalds`) to look up their specific identicon.
2.  **Enter an ID:** Alternatively, input a raw integer ID (e.g., `1`) to see the identicon for that specific number.
3.  **View Result:** The app renders the 5x5 identicon in real-time.
4.  **Download:** Use the "Download" button to save a high-resolution `.PNG` version of the generated identicon.


