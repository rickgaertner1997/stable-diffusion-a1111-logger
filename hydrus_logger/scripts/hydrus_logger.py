import os
import re
import json
import gradio as gr

from modules import scripts, script_callbacks, shared
# =========================
# GLOBAL STORAGE FOR UI INPUT
# =========================
USER_EXTRA_TAGS = ""

# =========================
# DANBOORU CONFIG
# =========================

DANBOORU_TAGS_PATH = os.path.join(os.path.dirname(__file__), "danbooru_tags.json")

EXTRA_TAGS = {"meta:stable_diffusion", "meta:png", "meta:explicit"}

PREFIXED_CATEGORIES = {
    1: "artist",
    2: "series",
    3: "character",
    4: "meta",
    5: "copyright"
}

BLOCKED_CATEGORIES = {0}

# =========================
# LOAD TAG DATA
# =========================

try:
    with open(DANBOORU_TAGS_PATH, "r", encoding="utf-8") as f:
        tag_data = json.load(f)

    TAG_RAW = {
        entry["name"]: entry["category"]
        for entry in tag_data
    }

    print(f"[HydiusLogger] Loaded {len(TAG_RAW)} Danbooru tags.")

except Exception as e:
    TAG_RAW = {}
    print(f"[HydiusLogger ERROR] Could not load tag dump: {e}")

# =========================
# TAG PROCESSING
# =========================

def clean_tag(tag: str) -> str:
    tag = tag.strip()
    tag = re.sub(r"^\((.+?):[0-9.]+\)$", r"\1", tag)
    tag = tag.replace(r"\(", "(").replace(r"\)", ")")

    if tag.startswith("(") and tag.endswith(")"):
        tag = tag[1:-1]

    tag = tag.replace(" ", "_")
    return tag

def format_tag(tag: str) -> str | None:
    tag = tag.strip()

    prefix_match = re.match(r"^(character|artist|series|meta):(.+)$", tag)
    if prefix_match:
        user_prefix, raw_tag = prefix_match.groups()
        raw_tag = clean_tag(raw_tag)
        return f"{user_prefix}:{raw_tag}"

    raw_tag = clean_tag(tag)
    category_id = TAG_RAW.get(raw_tag)

    if category_id in BLOCKED_CATEGORIES:
        return raw_tag

    tag_type = PREFIXED_CATEGORIES.get(category_id)
    if tag_type:
        return f"{tag_type}:{raw_tag}"

    return raw_tag

# =========================
# IMAGE SAVE CALLBACK
# =========================

def log_manual_save(params):
    try:
        log_path = params.filename + ".txt"

        raw_prompt = getattr(params.p, "prompt", "")

        # ✅ Get textbox value safely from the generation
        extra_tags = params.p.extra_generation_params.get("Hydrus Extra Tags", "")

        if extra_tags:
            raw_prompt += "," + extra_tags

        # Continue your normal tag formatting...
        raw_tags = re.split(r',(?![^()]*\))', raw_prompt)
        formatted_tags = [format_tag(tag.strip()) for tag in raw_tags]
        formatted_tags = [tag for tag in formatted_tags if tag]

        checkpoint_raw = shared.sd_model.sd_checkpoint_info.name
        checkpoint_base = os.path.splitext(os.path.basename(checkpoint_raw))[0]
        formatted_tags.append(f"meta:{checkpoint_base}")

        final_tags = list(dict.fromkeys(formatted_tags + list(EXTRA_TAGS)))
        final_prompt = ",".join(final_tags)

        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        with open(log_path, "w", encoding="utf-8") as f:
            f.write(final_prompt + "\n")

        print(f"[HydiusLogger] Saved tag file: {log_path}")

    except Exception as e:
        print(f"[HydiusLogger ERROR] {e}")

script_callbacks.on_image_saved(log_manual_save)

# =========================
# UI SCRIPT
# =========================

class Script(scripts.Script):

    def title(self):
        return "Hydrus Logger"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        textbox = gr.Textbox(
            label="Hydrus Logger",
            value="copyright:, character:",
            elem_classes=["prompt", "autocomplete"]  
        )
        return [textbox]

    def process(self, p, textbox):
        if textbox and textbox.strip():

            p.extra_generation_params["Hydrus Extra Tags"] = textbox.strip()

