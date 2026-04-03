from __future__ import annotations

import base64
import io
import json
import random
from typing import Dict, Tuple

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image, ImageDraw, ImageOps

from solver import GOAL_STATE, SearchResult, neighbors, solve

State = Tuple[int, ...]

st.set_page_config(page_title="8-Puzzle AI Lab", page_icon="🧩", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}
.stApp {
    background: radial-gradient(circle at top right, #111827, #0f172a, #020617);
    color: #e2e8f0;
}
h1, h2, h3 {
    color: #f8fafc !important;
}
</style>
""", unsafe_allow_html=True)

ALGORITHM_OPTIONS = {
    "Breadth First Search": "bfs",
    "Depth First Search": "dfs",
    "A* (Manhattan)": "astar_manhattan",
    "A* (Euclidean)": "astar_euclidean",
}

def pil_to_b64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

def split_image_into_tiles_b64(image: Image.Image, tile_size: int = 180) -> Dict[str, str]:
    image = ImageOps.fit(image.convert("RGB"), (tile_size * 3, tile_size * 3))
    tiles: Dict[str, str] = {}

    blank = Image.new("RGB", (tile_size, tile_size), color=(15, 23, 42))
    draw = ImageDraw.Draw(blank)
    draw.rounded_rectangle((4, 4, tile_size - 5, tile_size - 5), radius=18, outline=(60, 60, 80), width=3)
    tiles["0"] = pil_to_b64(blank)

    tile_id = 1
    for row in range(3):
        for col in range(3):
            position = row * 3 + col
            if position == 0:
                continue
            crop = image.crop((col * tile_size, row * tile_size, (col + 1) * tile_size, (row + 1) * tile_size))
            overlay = ImageDraw.Draw(crop)
            overlay.rounded_rectangle((3, 3, tile_size - 4, tile_size - 4), radius=18, outline="white", width=3)
            overlay.rounded_rectangle((10, 10, 50, 44), radius=10, fill=(0, 0, 0, 180))
            overlay.text((22, 16), str(tile_id), fill="white")
            tiles[str(tile_id)] = pil_to_b64(crop)
            tile_id += 1
    return tiles

def random_scramble_from_goal(moves_count: int, seed: int | None = None) -> State:
    rng = random.Random(seed)
    state = GOAL_STATE
    previous = None
    for _ in range(moves_count):
        next_candidates = neighbors(state)
        if previous is not None:
            next_candidates = [(m, s) for m, s in next_candidates if s != previous] or next_candidates
        if not next_candidates:
            break
        _, nxt = rng.choice(next_candidates)
        previous, state = state, nxt
    return state

def pretty_algorithm_name(code: str) -> str:
    mapping = {
        "bfs": "Breadth First Search",
        "dfs": "Depth First Search",
        "astar_manhattan": "A* with Manhattan",
        "astar_euclidean": "A* with Euclidean",
    }
    return mapping.get(code, code)

def show_metrics(result: SearchResult) -> None:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Cost of path", result.cost_of_path)
    c2.metric("Nodes expanded", result.nodes_expanded)
    c3.metric("Search depth", result.search_depth)
    c4.metric("Running time (s)", f"{result.running_time:.6f}")
    c5.metric("Max frontier", result.max_frontier_size)


GAME_COMPONENT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');
        body {
            background-color: transparent;
            font-family: 'Outfit', sans-serif;
            color: white;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow-y: hidden;
        }
        .game-container {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 28px;
            padding: 30px 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255,255,255,0.1);
            display: flex;
            flex-direction: column;
            gap: 24px;
            width: fit-content;
        }
        .board {
            position: relative;
            width: 320px;
            height: 320px;
            background: rgba(15, 23, 42, 0.8);
            border-radius: 20px;
            border: 2px solid rgba(255,255,255,0.05);
            box-shadow: inset 0 10px 30px rgba(0,0,0,0.5);
            overflow: hidden;
            margin: 0 auto;
        }
        .tile {
            position: absolute;
            width: 100px;
            height: 100px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 38px;
            font-weight: 800;
            transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4), inset 0 1px 2px rgba(255,255,255,0.2);
            background-size: cover;
            background-position: center;
            user-select: none;
        }
        .tile.empty {
            background: rgba(255, 255, 255, 0.02);
            border: 2px dashed rgba(255, 255, 255, 0.08);
            box-shadow: none;
            color: transparent;
            z-index: 0;
        }
        .tile.numeric {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: white;
            border: 1px solid rgba(255,255,255,0.1);
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            z-index: 10;
        }
        .controls {
            display: flex;
            gap: 8px;
            justify-content: center;
            flex-wrap: wrap;
        }
        button {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 12px;
            padding: 10px 16px;
            font-family: inherit;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        button:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2);
        }
        button:active {
            transform: translateY(0);
        }
        button.primary {
            background: linear-gradient(135deg, #10b981, #059669);
            border-color: transparent;
        }
        button.primary:hover {
            background: linear-gradient(135deg, #34d399, #10b981);
            box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.4);
        }
        .info {
            display: flex;
            justify-content: space-between;
            font-size: 16px;
            color: #94a3b8;
            font-weight: 600;
            padding: 0 5px;
        }
        .move-text {
            color: #38bdf8;
            background: rgba(56, 189, 248, 0.1);
            padding: 2px 8px;
            border-radius: 8px;
        }
    </style>
</head>
<body>

<div class="game-container">
    <div class="info">
        <span id="step-counter">Step 0 / 0</span>
        <span id="move-info" class="move-text">Start</span>
    </div>
    <div class="board" id="board"></div>
    <div class="controls">
        <button onclick="goTo(0)">⏮ Start</button>
        <button onclick="prev()">◀ Prev</button>
        <button onclick="next()">Next ▶</button>
        <button onclick="goTo(statesPath.length - 1)">End ⏭</button>
        <button onclick="togglePlay()" class="primary" id="play-btn">▶ Play</button>
    </div>
</div>

<script>
    // This receives the json data passed from python
    const statesPath = WINDOW_DATA_STATES;
    const moves = WINDOW_DATA_MOVES;
    const tilesB64 = WINDOW_DATA_TILES;
    
    let currentStep = 0;
    let playInterval = null;
    let speedMs = 350;

    const boardEl = document.getElementById('board');
    const stepCounterEl = document.getElementById('step-counter');
    const moveInfoEl = document.getElementById('move-info');
    const playBtnEl = document.getElementById('play-btn');

    const tileElements = [];
    for (let i = 0; i < 9; i++) {
        const el = document.createElement('div');
        el.className = 'tile';
        boardEl.appendChild(el);
        tileElements.push(el);
    }

    function renderState(stepIndex) {
        const state = statesPath[stepIndex];
        const moveText = stepIndex === 0 ? "Start state" : moves[stepIndex - 1];
        
        stepCounterEl.innerText = `Step ${stepIndex} / ${statesPath.length - 1}`;
        moveInfoEl.innerText = moveText;

        for (let position = 0; position < 9; position++) {
            const tileValue = state[position];
            const row = Math.floor(position / 3);
            const col = position % 3;
            
            const pxLeft = 5 + col * (100 + 5);
            const pxTop = 5 + row * (100 + 5);

            const el = tileElements[tileValue];
            el.style.transform = `translate(${pxLeft}px, ${pxTop}px)`;
            
            if (tileValue === 0) {
                el.className = 'tile empty';
                el.innerHTML = '';
                if (tilesB64 && tilesB64["0"]) {
                    el.style.backgroundImage = `url(${tilesB64["0"]})`;
                }
            } else {
                if (tilesB64) {
                    el.className = 'tile';
                    el.style.backgroundImage = `url(${tilesB64[String(tileValue)]})`;
                    el.innerHTML = '';
                    el.style.border = 'none';
                } else {
                    el.className = 'tile numeric';
                    el.innerText = tileValue;
                }
            }
        }
    }

    function goTo(step) {
        currentStep = Math.max(0, Math.min(statesPath.length - 1, step));
        renderState(currentStep);
    }

    function prev() {
        goTo(currentStep - 1);
    }

    function next() {
        goTo(currentStep + 1);
    }

    function togglePlay() {
        if (playInterval) {
            clearInterval(playInterval);
            playInterval = null;
            playBtnEl.innerText = "▶ Play";
            playBtnEl.classList.remove('primary');
        } else {
            if (currentStep === statesPath.length - 1) {
                currentStep = 0;
            }
            playBtnEl.innerText = "⏸ Pause";
            playBtnEl.classList.add('primary');
            playInterval = setInterval(() => {
                if (currentStep < statesPath.length - 1) {
                    goTo(currentStep + 1);
                } else {
                    togglePlay(); 
                }
            }, speedMs);
        }
    }

    setTimeout(() => {
        renderState(0);
    }, 10);

</script>
</body>
</html>
"""

def render_interactive_game(result: SearchResult, tiles_b64: Dict[str, str] | None = None) -> None:
    states_json = json.dumps(result.states_path)
    moves_json = json.dumps(result.path_to_goal)
    tiles_json = json.dumps(tiles_b64) if tiles_b64 else "null"

    html_code = GAME_COMPONENT_HTML.replace("WINDOW_DATA_STATES", states_json)
    html_code = html_code.replace("WINDOW_DATA_MOVES", moves_json)
    html_code = html_code.replace("WINDOW_DATA_TILES", tiles_json)

    components.html(html_code, height=540)


def store_result(key: str, result: SearchResult) -> None:
    st.session_state[key] = result


def main() -> None:
    st.title("🧩 8-Puzzle AI Lab")
    st.markdown(
        "<p style='color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem;'>"
        "Choose an algorithm, generate a puzzle, and watch the agent solve it seamlessly!"
        "</p>", unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["🔢 Numeric Puzzle", "🖼️ Image Puzzle"])

    with tab1:
        st.subheader("Numeric 8-puzzle")
        default_state = "1,2,5,3,4,0,6,7,8"
        user_state = st.text_input("Initial state", value=default_state)
        algo_label = st.selectbox("Algorithm", list(ALGORITHM_OPTIONS.keys()), key="numeric_algo")

        if st.button("Solve numeric puzzle", type="primary"):
            try:
                result = solve(user_state, ALGORITHM_OPTIONS[algo_label])
                store_result("numeric_result", result)
            except Exception as exc:
                st.error(str(exc))

        numeric_result: SearchResult | None = st.session_state.get("numeric_result")
        if numeric_result is not None:
            if not numeric_result.found:
                st.error(numeric_result.message)
            else:
                st.success(f"Solved using {pretty_algorithm_name(ALGORITHM_OPTIONS[algo_label])}!")
                show_metrics(numeric_result)
                render_interactive_game(numeric_result)
                with st.expander("Show detailed path trace"):
                    st.write(", ".join(numeric_result.path_to_goal))

    with tab2:
        st.subheader("Image-based puzzle game")
        uploaded = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
        c1, c2 = st.columns(2)
        with c1:
            scramble_moves = st.slider("Scramble moves", min_value=5, max_value=80, value=25)
        with c2:
            image_algo_label = st.selectbox("Algorithm", list(ALGORITHM_OPTIONS.keys()), key="image_algo")

        if uploaded is not None:
            image = Image.open(uploaded)
            tiles_b64 = split_image_into_tiles_b64(image)
            
            if "image_start_state" not in st.session_state:
                st.session_state["image_start_state"] = random_scramble_from_goal(scramble_moves)

            col1, col2 = st.columns([1, 1])
            with col2:
                st.write("**Controls**")
                if st.button("🔀 Shuffle Board"):
                    st.session_state["image_start_state"] = random_scramble_from_goal(scramble_moves)
                    st.session_state.pop("image_result", None)

                st.info(f"Target scrambled moves: {scramble_moves}")
                st.info(f"Using algorithm: {image_algo_label}")

                if st.button("▶ Solve image puzzle", type="primary"):
                    current_start_state = st.session_state["image_start_state"]
                    result = solve(current_start_state, ALGORITHM_OPTIONS[image_algo_label])
                    store_result("image_result", result)
                    store_result("image_tiles_b64", tiles_b64)

            with col1:
                st.write("**Start board preview**")
                start_state = st.session_state["image_start_state"]
                dummy_res = SearchResult("dummy", start_state, start_state, False, [], [start_state], 0, 0, 0, 0, 0)
                render_interactive_game(dummy_res, tiles_b64)


        image_result: SearchResult | None = st.session_state.get("image_result")
        image_tiles: Dict[str, str] | None = st.session_state.get("image_tiles_b64")
        if image_result is not None and image_tiles is not None:
            if not image_result.found:
                st.error(image_result.message)
            else:
                st.success(f"Solved using {pretty_algorithm_name(ALGORITHM_OPTIONS[image_algo_label])}!")
                show_metrics(image_result)
                st.write("### Solution Playback")
                render_interactive_game(image_result, image_tiles)


if __name__ == "__main__":
    main()
